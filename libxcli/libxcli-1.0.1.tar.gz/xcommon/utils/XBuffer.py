# coding:utf-8

import struct;
import datetime;
# import re;
# import json;

from xcommon.utils import XUtil;
SHORT_SIZE = 2;
INT_SIZE = 4;
FLOAT_SIZE = 4;
LONG_SIZE = 8;
DOUBLE_SIZE = 8;
DEFAULT_SIZE = 2048 ;

# 
class Singleton(object):  
	def __new__(cls, *args, **kw):	
		if not hasattr(cls, '_instance'):  
			orig = super(Singleton, cls)  
			cls._instance = orig.__new__(cls, *args, **kw)	
		return cls._instance ;
		
EMPTY_BYTES = b'';
		

class BufferException(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)
		

class Buffer:
	
	def __init__(self,buff =None, capacity=DEFAULT_SIZE):
		if buff == None :
			if( capacity == None ) :
				self.inputBytes = bytearray(DEFAULT_SIZE)
				self.limit = DEFAULT_SIZE;
			else:
				self.inputBytes = bytearray(capacity);
				self.limit = capacity;
			self.endPos = 0;
			self.beginPos = 0;
		else:
			self.inputBytes = buff;
			self.limit = len(buff);
			self.endPos = self.limit ;
			self.beginPos = 0;
		
	@staticmethod
	def allocate(capacity):
		return Buffer(None, capacity);

	@staticmethod
	def attach(buff):
		return Buffer(buff);

	def attach0(self, buff):
		self.inputBytes = buff;
		self.limit = len(buff);
		self.endPos = self.limit ;
		self.beginPos = 0;

		
	def position(self , newpos = 0):
		ret = self.beginPos;
		self.beginPos = newpos ;
		return ret ;
		
		
	def reset(self):
		self.endPos = 0;
		self.beginPos = 0;
		return ;
		
		
	def capacity(self , extends ):
		if self.endPos + extends >= self.limit :
			newsize = max( extends , DEFAULT_SIZE );
			bytes = bytearray(newsize);
			self.inputBytes.extend(bytes);
			self.limit = len(self.inputBytes)
		

	def _putBytes(self,value, length , begin = 0):
		
		self.capacity(length);			

		self.inputBytes[ self.endPos : self.endPos+length ] = value[begin:begin+length] ;

		# for i in range(length):
		# 	self.inputBytes[self.endPos+i] = value[i];
		self.endPos = self.endPos + length;
	
	def put(self,oneByte):
		self.capacity(1);	
		self.inputBytes[self.endPos] = oneByte & 0xff;
		self.endPos = self.endPos + 1;
	
	def putInt16(self,shortValue):
		shortBytes = struct.pack("!h",shortValue);
		self._putBytes( shortBytes, SHORT_SIZE ) ;

	def putInt32(self,intValue):
		intBytes = struct.pack("!I",intValue);
		self._putBytes( intBytes, INT_SIZE ) ;
		 

	def putInt64(self,longValue):
		longBytes = struct.pack("!q",longValue);
		self._putBytes( longBytes, LONG_SIZE ) ;

	'''
		Put Datestamp , Python 的 datatime 返回 float 类型的e
		时间（秒）， 但java接受的是 毫秒的 long 类型 ；
		因此会有些 微秒数据的丢失
	'''
	def putDate(self,datetime):

		if datetime == None:
			return;

		# 转换为 整形，并 * 1000
		ts = datetime.timestamp();
		# print('ts is ', ts);
		ts = int((ts)*1000);
		# print('ts is ', ts);

		longBytes = struct.pack("!q",ts);
		self._putBytes( longBytes, LONG_SIZE ) ;




	def putDouble(self,doubleValue):
		dbBytes = struct.pack("!d",doubleValue);
		self._putBytes( dbBytes, DOUBLE_SIZE ) ;

			
	def putFloat(self,floatValue):
		fBytes = struct.pack("!f",floatValue);
		self._putBytes( fBytes, FLOAT_SIZE ) ;

	def putString(self,string):
		utf8str	 = string.encode('utf-8');
		length = len(utf8str)
		self.putInt32(length)
		self._putBytes( utf8str, length );

	def putBytes(self,bytes , begin=0, length = -1):
		if bytes!=None:
			if length <0:
				length = len(bytes) - begin;

			self._putBytes( bytes, length , begin );

	

	def get(self):
		oneByte = self.inputBytes[self.beginPos];
		self.beginPos = self.beginPos + 1;
		return oneByte;
	
	def _getBytes(self , length ):
		if self.beginPos > self.endPos:
			raise RuntimeError("empty data");
	
		_bytes = bytearray(length);
		_bytes = self.inputBytes[ self.beginPos : self.beginPos+ length]
		# for i in range(length):
		# 	_bytes[i] = self.inputBytes[self.beginPos+i];
		self.beginPos = self.beginPos + length;
		
		return _bytes;

	def _peekBytes(self , length ):
		if self.beginPos > self.endPos:
			raise RuntimeError("empty data");
	
		_bytes = bytearray(length);
		for i in range(length):
			_bytes[i] = self.inputBytes[self.beginPos+i];
		return _bytes;
	
	def getInt16(self):
		shortBytes = self._getBytes(SHORT_SIZE );
		shortValue = struct.unpack("!h",shortBytes)[0];
		return shortValue;
		
	def getInt32(self):
		intBytes = self._getBytes(INT_SIZE );
		#change bytes to int
		intValue = struct.unpack("!I",(intBytes))[0];
		return intValue;
	
	def peekInt32(self):
		intBytes = self._peekBytes(INT_SIZE );
		#change bytes to int
		intValue = struct.unpack("!I",(intBytes))[0];
		return intValue;

	def getFloat(self):
		fBytes = self._getBytes(FLOAT_SIZE );
		#change bytes to int
		fValue = struct.unpack("!f",(fBytes))[0];
		return fValue;
		
	def getDouble(self):
		dBytes = self._getBytes( DOUBLE_SIZE );
		#change bytes to int
		dValue = struct.unpack("!d",(dBytes))[0];
		return dValue;
		
	def getInt64(self):
		longBytes= self._getBytes(LONG_SIZE ); 
		
		longValue = struct.unpack(">q",(longBytes))[0];
		return longValue;

	def getDate(self):
		dt = self.getInt64();

		return datetime.datetime.fromtimestamp(dt / 1000);
	
	def getBuff(self):
		
		strLen = self.getInt32();
		if strLen == 0:
			return None;
		
		if strLen == 0xFFFFFFFF:
			return None;
		
		if self.remaining() < strLen:
			raise BufferException('Invaild buff size , wanted' + str(strLen));
		
		if strLen == 0:
			return EMPTY_BYTES;
		
		bytes = self._getBytes(strLen);
		
		return bytes;
	
	def getString(self):
		
		strLen = self.getInt32();
		if strLen == 0 :
			return None;
			
		if strLen == 0xFFFFFFFF:
			return None;
			
		if self.remaining() < strLen :
			raise BufferException('Invaild buff size , wanted' + str(strLen)) ;

		if strLen == 0:
			return '';

		strBytes = self._getBytes( strLen );
		
		#change bytes to string
		#strValue = struct.unpack(str(strLen) + "s",strBytes)[0];
		return str((strBytes), encoding = "utf-8")	;

	def getBytes(self,byteSize):
		bytesArray = self._getBytes( byteSize );
		
		return (bytesArray);

	def remaining(self):
		return self.endPos - self.beginPos;
	
	def value(self):
		val = self.inputBytes[self.beginPos:self.endPos];
		return val;

	def length(self):
		return self.endPos - self.beginPos;

	def array(self):
		return self.inputBytes;
		
	def dump(self):
		XUtil.dump(self.inputBytes, self.beginPos, self.endPos);

