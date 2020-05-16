#encoding:utf-8

'''
   $Id: XClient.py 705 2016-06-06 04:43:01Z liukang $
'''



import errno
import io
import socket 
import select
import time
import sys
import os
import array
import types;
import re;

import json;
import socket				# Import socket module
from xcommon.utils import *
from xcommon.xclient import Xserialization;



#define MAX_PACKET_LENGTH			0x00ffffff 
#define 
#define 
#define PROTOCOL_MAGIC				0x77775555

#define PROTOCOL_MAGIC				0x77775555
MAX_PACKET_LENGTH =	0x00ffffff 
PROTOCOL_VERSION  = 0x00100000
PROTOCOL_TAG	  = 0x57577575
PROTOCOL_MAGIC	  = 0x77775555

# service invoke command id
COMMAOND_SERVICES = 20000


MSG_LIVE = 9; 


RESULT_OK = 0;
RESULT_ERROR = -1;
RESULT_NEEDMORE = 2;

PACKET_HEADER_SIZE = 12 ;
PACKET_HEADER_TOTAL_SIZE = 32 ;	

MSG_SUCCESS = 1 ;
MSG_ERROR   = 2 ;
MSG_EXCEPTION   = 3;

class StackTraceElement:
	def __init__(self, clazz , method , file1, line ):
		self.clazz = clazz;
		self.method  = method;
		self.file = file1 ;
		self.line  = line ;
		
		
class StackTrace:
	def __init__(self, clazz , message , code , stacks):
		self.clazz = clazz;
		self.message = message;
		self.code  = code; 
		self.stacks = stacks ;

	def dump(self):
		print( "Class %s: %s" %(self.clazz ,  self.message ));
		for st in self.stacks:
			print(  "\tat %s.%s(%s:%d)" %( st.clazz, st.method, st.file, st.line )); 
	
		
class RemoteException(Exception):
	def __init__(self, stackTraces):
		self.message = None;
		self.stackTraces = stackTraces;
		if len(stackTraces) > 0:
			self.message = stackTraces[0].message ;
		
	# def __eq__(self, other):
		# return self.__dict__ == other.__dict__

	def dump(self):
		for st in self.stackTraces:
			st.dump();

	def __str__(self):
		return str( self.__class__.__qualname__ )+ ' : '+ self.message;
	



class EncodeException(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)
			
		
class RX:
	def __init__(self):
		self.length = 0;
		self.payload = None;
		self.result = 0 ;
		self.error  = 0 ;
		self.exception = None;
	

class Xclient(object):

	def __init__(self, ip, port , debug=False):
		self.ip = ip;
		self.port = port;
		self.h = None;
		self.debug = debug;


	def __del__(self):
		self.close()



	def connect( self ):
		self.close()
		self.h = socket.socket()		 # Create a socket object
			# host = socket.gethostname() # Get local machine name
		self.h.connect((self.ip, self.port))

		
	def close( self ):
		if self.h != None:
			self.h.close()
			self.h = None

	def isConnected(self):
		return self.h != None;


	
	def executeBuff(self,  msgId , buff ):
		return self.execute( msgId , buff.value());
		

	def execute(self,  msgId , payload ):

		if not self.isConnected():
			self.connect();


		buff = XBuffer.Buffer()
		Xclient.packet( buff, msgId , payload );
		length = buff.length(); 
		val = buff.value();

		if self.debug:
			print('Send:');
			XUtil.dump(val, 0, len(val))
		
		send = self.h.send(val)
		if send == 0:
			raise RuntimeError("socket connection broken")

		rx = RX();
		# reset 
		buff.reset();
		recved = 0 ;
		while True :
			chunk = self.h.recv( 1024 );
			if chunk == b'':
				raise RuntimeError("socket connection broken")
			
			buff.putBytes(chunk);

			if self.debug:
				print('Recv:');
				buff.dump();

			result = Xclient.decode(buff, rx);
			if result == RESULT_NEEDMORE:
				continue;
			elif result == RESULT_OK:	
				bf= Xclient.decodeResult( rx.payload ,rx.result ); 
				return bf.value();
			else:
				pass;
		
		


	@staticmethod
	def packet(	 buff, msgid, payload ):
		payloadlength = 0 ;
		if payload !=None:
			payloadlength = len(payload);

		padding = 8 - ( (payloadlength + 16 )  % 8);
		total = 32 + padding + payloadlength ;

		buff.putInt32( PROTOCOL_VERSION )
		buff.putInt32( PROTOCOL_TAG )
		
		buff.putInt32( total )
		buff.putInt32( 0 ) # flag 
		buff.putInt32( PROTOCOL_MAGIC )
		buff.putInt32( padding )
		buff.putInt32( msgid )
		buff.putBytes( payload )
		
		for i in range(padding):
			buff.put( 0xff )
		
		c32 = XUtil.crc32(buff.array(), 16, total - 4);
		buff.putInt32( c32 );

		return buff;
		
	
	@staticmethod
	def decodeResult( payload, result ):
		
		buff = XBuffer.Buffer(payload);
		
		if  result == MSG_SUCCESS or  result==MSG_ERROR:
			srcId  = buff.getInt32();
			error  = buff.getInt32();
			
			return buff;
			
		elif  result == MSG_EXCEPTION : 
		
			#print('before decode exception ------------ ');
			#buff.dump();
			srcId  = buff.getInt32();
			error  = buff.getInt32();
			
			e = Xclient.decodeExceptions( buff);
			raise e;
			
		else :
			raise RuntimeError("ResultType error " + str(result));
			
	
	@staticmethod
	def decodeExceptions( buff ):
		
		# print('in decodeExceptions ' );
		# buff.dump();
		
		traces = [];
		size = buff.getInt32();
		for i in range(size):
			rt = Xclient.decodeException(buff);
			traces.append(rt);
			
		return RemoteException( traces );
		#return traceback.TracebackException(None,None, traces);
			

	@staticmethod
	def decodeException( buff ):
		
		error = -1 ;
		clazz = buff.getString();
		type  = buff.getInt32();
		if type == 1 :
			error = buff.getInt32();
		
		message = buff.getString();
		stacks = buff.getInt32();
		
		_stacks = [];
		if stacks>0:
			
			for i in range(stacks):
				name = buff.getString();
				method = buff.getString();
				file1 = buff.getString();
				line = buff.getInt32();
				#st = traceback.StackSummary(file1,  line , name+'#'+ method );
				st = StackTraceElement(name,method,file1,line);
				#_stacks.append((file1,  line , name+'#'+ method, None));
				_stacks.append(st);
				
		return StackTrace( clazz , message, error , _stacks );
		#return traceback.StackSummary.from_list(_stacks);
	
	@staticmethod
	def decode(buff , rx ):
		
		if rx.length == 0 :
			if buff.length() > PACKET_HEADER_SIZE:
				version = buff.getInt32();
				if PROTOCOL_VERSION != version:
					raise RuntimeError("version error " + str(version));
					
				tag = buff.getInt32();
				if PROTOCOL_TAG != tag:
					raise RuntimeError("tag error " + str(tag));
					
				rx.length = buff.getInt32();
			else:
				return RESULT_NEEDMORE;
				
			
		if buff.length() < rx.length - PACKET_HEADER_SIZE :
			return RESULT_NEEDMORE;
			
		flag = buff.getInt32();
		
		c32 = XUtil.crc32(buff.array(), 16, rx.length - 20 + 16);
		
		magic = buff.getInt32();
		padding = buff.getInt32();
		rx.result = buff.getInt32();
		paySize = rx.length - PACKET_HEADER_TOTAL_SIZE - padding;
		
		rx.payload = buff.getBytes( paySize );
		pads = buff.getBytes( padding );
		crc32 = buff.getInt32();
		
		if crc32 != c32:
			raise RuntimeError("crc32 error");
		

		return RESULT_OK;



class XclientV2(Xclient):		
	
	def __init__(self, *args, **kwargs):
		Xclient.__init__(self, *args , **kwargs);



	def remoteCall( self , service , method , params  ):
		buff = Xserialization.SerializeBuff();
		# buff.putInt32(len(service) + len(signature) + 1 );
		buff.putString(service + ':' + method.signature);
		nums = len(params);
		buff.putInt32(nums);
		
		XclientV2.pack( buff, method , params );
		if self.debug:
			buff.dump();
		
		result = self.executeBuff( COMMAOND_SERVICES , buff);
		
		buff.attach0(result);

		if self.debug:
			print('response:');
			buff.dump();
		
		
		rets = XclientV2.decodeResponse( method , buff );
		return rets;

	@staticmethod
	def decodeResponse( method, buff):
	
		length = buff.getInt32();
		if length != buff.remaining():
			raise EncodeException('length != remaining  ' + str(length));
			
		resp = buff.getInt32();
		if resp != 0 :
			type = buff.getInt32();
			if type == MSG_EXCEPTION :
				e = Xclient.decodeExceptions( buff);
				raise e;
				
		else:
			rets = XclientV2.unpack( buff , method);
			# print(len(rets) );
			if rets != None :
				if len(rets) == 1:
					# print(rets);
					return rets[0];

			return rets;	
		
	@staticmethod
	def pack( buff , method ,params ):

		context = Xserialization.ConvertContext(method.getMeta());
		
		manger = Xserialization.ConvertorManager();



		parameters = method.parameters ;

		params_len = len(params);

		if len(parameters)!= params_len:
			raise EncodeException('parameters len != params len' + str(params));
		
		for i in range(len(params)):
			define = parameters[i];
			param  = params[i];
			manger.pack( context, define.type , buff, param );
		
		
	@staticmethod
	def unpack( buff , method ):
		result = [];

		context = Xserialization.ConvertContext(method.getMeta());

		manger = Xserialization.ConvertorManager();
		
		while buff.remaining()>0:
			val = manger.unpack( context,  buff );
			result.append( val);
			
		return result;
		

def _Execute( client , service,
		method , func):

	# print('in _Execute ');
	# 定义一个内嵌的包装函数，给传入的函数加上计时功能的包装
	def _wrapper( *args, **kwargs):
		
		# print('args ' + str(*args));
		# print('kwargs ' + str( **kwargs ));
		
		# argspec = inspect.getargspec(func)
		# namedargs = inspect.getcallargs(func, *args, **kwargs)
	
		buff = client.remoteCall(  service  , method ,  args );
		# print(buff);
		# XUtil.dump(buff, 0, len(buff)); #.dump();
		return buff;
	 
	# 将包装后的函数返回
	return _wrapper
	
class DummayClass():
	pass;
# 
class Proxy(object):
	def __init__(self, h , metas, service =None  ):

		
		self.__data = DummayClass();
		if service == None:
			service = metas.getService();

		self.__data.__dict__['service'] = service;
		self.__data.__dict__['metas'] = metas;
		self.__data.__dict__['h'] = h;


	def get(self):
		return self.__data;
		
	def __repr__(self):
		return 'self.__data';
		
		
	def __str__(self):
		return str(self.__data);
		
	def __getattr__(self, attr):

		m = self.__data.__dict__['metas'] ;
		h = self.__data.__dict__['h'] ;
		s = self.__data.__dict__['service'] ;

		# print(' self is ' + str(self));
		# m = object.__getattribute__(self, 'meta');
		method = m.getMethod(attr ,s );
		# h = object.__getattribute__(self, 'h'); #.h ; #['h'];
		# s = object.__getattribute__(self, 'service'); # ['service'];
		return _Execute( h, s , method, None);


class Factory(object):
	def __init__(self, ip, port, metaFile=None , dumpJson=None):

		self.h = XclientV2(ip, port);

		f = None;
		if metaFile != None:
			f = Xserialization.MetaFactoryFile(metaFile);
		else:
			f = Xserialization.MetaFactoryRemote(self.h, dumpJson);

		self.metas = f.loadMeta();

	def create(self, service=None):
		return Proxy(self.h, self.metas , service);






		
		