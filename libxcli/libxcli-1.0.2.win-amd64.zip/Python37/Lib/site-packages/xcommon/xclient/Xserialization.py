# coding:utf-8

import struct;
import datetime;
import re;
import json;

from xcommon.utils import *;
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
		
		



XC_TYPE_ARRAY = 0X80000000;
XC_TYPE_REFERENCE = 0X40000000;
XC_TYPE_INT8 = 1;
XC_TYPE_INT16 = 2;
XC_TYPE_INT32 = 3;
XC_TYPE_INT64 = 4;
XC_TYPE_STRING = 5;
XC_TYPE_FLOAT = 7;
XC_TYPE_DOUBLE = 8;
XC_TYPE_CHAR = 9;
XC_TYPE_DATE = 10;
XC_TYPE_BOOLEAN = 11;
XC_TYPE_ENUM = 12;
XC_TYPE_CLASS = 13;

XC_TYPE_BEAN = 20;
XC_TYPE_LIST = 21;
XC_TYPE_MAP = 22;
XC_TYPE_SET = 23;
XC_TYPE_NULL = 30;


XC_DATE_CLASS_NAME = 'java.util.Date';


TYPE_OBJECT = 'Object' ;
	
class SerializeBuff(XBuffer.Buffer):
	def __init__( self,buff =None, capacity=DEFAULT_SIZE ):
		XBuffer.Buffer.__init__(self, buff, capacity);
	
	def put_string( self , val ):
		if val == None:
			self.putInt32(XC_TYPE_NULL)
		else:
			self.putInt32(XC_TYPE_STRING)
			self.putString(val)

	def put_bool ( self , val ):
		if val == None:
			self.putInt32(XC_TYPE_NULL)
			return ;

		self.putInt32(XC_TYPE_BOOLEAN);
		if val:
			self.put(1);
		else:
			self.put(0);


	def put_int32( self , val ):
		if val == None:
			self.putInt32(XC_TYPE_NULL)
			return ;

		self.putInt32(XC_TYPE_INT32);
		self.putInt32(val);
	
	def put_int64( self , val ):
		if val == None:
			self.putInt32(XC_TYPE_NULL)
			return;


		self.putInt32(XC_TYPE_INT64);
		self.putInt64(val);
		
	def put_double( self , val ):
		if val == None:
			self.putInt32(XC_TYPE_NULL)
			return;


		self.putInt32(XC_TYPE_DOUBLE);
		self.putDouble(val);

	def put_float(self, val):
		if val == None:
			self.putInt32(XC_TYPE_NULL)
			return;

		self.putInt32(XC_TYPE_FLOAT);
		self.putFloat(val);

	def put_date(self , val):
		if val == None:
			self.putInt32(XC_TYPE_NULL)
			return;


		self.putInt32(XC_TYPE_DATE);
		self.putString(XC_DATE_CLASS_NAME);
		self.putDate(val);

	def get_date(self):
		if self.length() < 12:
			raise XBuffer.BufferException('Invaild buff size ,wanted >=12 , get ' + str(self.length()))
		ctype = self.getInt32()
		if ctype == XC_TYPE_NULL:
			return None;

		if ctype != XC_TYPE_DATE:
			raise XBuffer.BufferException('Invaild buff ,wanted type XC_TYPE_DATE , get ' + str(ctype))
		clazz = self.getString();
		val = self.getDate();
		return val

	def get_float(self):
		if self.length() < 8:
			raise XBuffer.BufferException('Invaild buff size ,wanted >=8 , get ' + str(self.length()))
		ctype = self.getInt32()
		if ctype == XC_TYPE_NULL:
			return None;

		if ctype != XC_TYPE_FLOAT:
			raise XBuffer.BufferException('Invaild buff ,wanted type	 XC_TYPE_FLOAT , get ' + str(ctype))

		val = self.getFloat();
		return val

	def get_double( self ):
		if self.length() < 12 :
			raise XBuffer.BufferException('Invaild buff size ,wanted >=12 , get ' + str(self.length()))
		ctype = self.getInt32()
		if ctype == XC_TYPE_NULL:
			return None;


		if ctype != XC_TYPE_DOUBLE :
			raise XBuffer.BufferException('Invaild buff ,wanted type	 XC_TYPE_DOUBLE , get ' + str(ctype))
		
		val = self.getDouble();
		return val

	def get_bool(self):
		if self.length() < 5:
			raise XBuffer.BufferException('Invaild buff size ,wanted >=5 , get ' + str(self.length()))
		ctype = self.getInt32();
		if ctype == XC_TYPE_NULL:
			return None;

		if ctype != XC_TYPE_BOOLEAN:
			raise XBuffer.BufferException('Invaild buff ,wanted type	 XC_TYPE_BOOLEAN , get ' + str(ctype))

		val = self.get();
		if val != 0:
			return True;
		else:
			return False;



	def get_int32( self ):
		if self.length() < 8 :
			raise XBuffer.BufferException('Invaild buff size ,wanted >=8 , get ' + str(self.length()))
		ctype = self.getInt32();
		if ctype == XC_TYPE_NULL:
			return None;


		if ctype != XC_TYPE_INT32 :
			raise XBuffer.BufferException('Invaild buff ,wanted type	 XC_TYPE_INT32 , get ' + str(ctype))
		
		val = self.getInt32()
		return val

	def get_int64(self):
		if self.length() < 12:
			raise XBuffer.BufferException('Invaild buff size ,wanted >=12 , get ' + str(self.length()))
		ctype = self.getInt32();
		if ctype == XC_TYPE_NULL:
			return None;

		if ctype != XC_TYPE_INT64:
			raise XBuffer.BufferException('Invaild buff ,wanted type	 XC_TYPE_INT64 , get ' + str(ctype))

		val = self.getInt64()
		return val


	def get_string( self ):
		if self.remaining() < 4 :
			raise XBuffer.BufferException('Invaild buff size ,wanted >=4 , get ' + str(self.length()))
		ctype = self.getInt32();
		
		if ctype == XC_TYPE_NULL:
			return None
			
		if ctype != XC_TYPE_STRING :
			raise XBuffer.BufferException('Invaild buff ,wanted XC_TYPE_STRING , get ' + str(ctype))
		
		val = self.getString()
		return val


class SerializeException(Exception):
	def __init__(self, value):
		self.value = value

	def __str__(self):
		return repr(self.value)



class ConvertorException(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)
		
class ConvertContext:
	def __init__(self , meta ):
		self.no = 0 ;
		self.meta = meta;

	def getMeta(self):
		return self.meta;

	def getNO(self):
		self.no = self.no+1;
		return self.no ;

'''
	类型序列化&返序列化
'''
		
class Convertor:

	'''
		序列化 Obj 对象， 按照 valueType 类型，或者 Obj 自身类型

		context ： 序列化的上下文
		buff : 数据流
		valueType : 应该转换的类型
		obj : 要进行序列化的对象

	'''
	def write( self , context,  buff , valueType , obj ):
		pass;
		
	'''
		从 buff 中反序列化出对象， 通过 valueType 类型
	'''
	def read( self ,  context,  buff , valueType  ):
		pass;




class StringConvertor(Convertor):
	def write(self,context,  buff , valueType  , obj):
		if obj is str:
			buff.put_string(obj);
		else:
			buff.put_string(str(obj));

	def read(self, context,  buff  , valueType):
		return buff.get_string();


class BoolConvertor(Convertor):
	def write(self, context,  buff , valueType  ,  obj):
		buff.put_bool(obj);

	def read(self, context,  buff  , valueType):
		return buff.get_bool();


class Int64Convertor(Convertor):
	def write(self, context, buff, valueType, obj):
		if type(obj) is int:
			buff.put_int64(obj);
		else:
			buff.put_int64(int(obj));

	def read(self, context, buff, valueType):
		return buff.get_int64();

class Int32Convertor(Convertor):
	def write( self , context,  buff, valueType  , obj ):
		if type(obj) is int:
			buff.put_int32(obj);
		else:
			buff.put_int32(int(obj));
		
		
	def read(  self , context,  buff  , valueType):
		return buff.get_int32();

class DoubleConvertor(Convertor):
	def write( self , context,  buff , valueType , obj ):
		if obj is float:
			buff.put_double(obj);
		else:
			buff.put_double(float(obj));
		
		
	def read(  self ,context,  buff  , valueType ):
		return buff.get_double();


class FloatConvertor(Convertor):
	def write(self, context, buff, valueType, obj):
		if obj is float:
			buff.put_float(obj);
		else:
			buff.put_float(float(obj));

	def read(self, context, buff, valueType):
		return buff.get_float();


class DateConvertor(Convertor):
	def write(self, context, buff , valueType , obj):
		buff.put_date(obj);

	def read(self,context,  buff  , valueType):
		return buff.get_date();


class ClassConvertor(Convertor):
	def write(self,context,  buff , valueType  , obj):
		if type(obj) is not str:
			raise SerializeException('Invaild obj ' + obj+ ',' + str(obj));

		buff.putInt32(XC_TYPE_CLASS);
		buff.putString(obj);

	def read(self, context,  buff  , valueType):
		ctype = buff.getInt32()
		if ctype == XC_TYPE_NULL:
			return None;

		if ctype != XC_TYPE_CLASS:
			raise SerializeException('Invaild buff ,wanted XC_TYPE_CLASS , get ' + str(ctype));

		clazz = buff.getString();
		return clazz;



class CollectionConvertor(Convertor):

	def __init__(self, id , className):
		self.id = id;
		self.className = className;

	def write(  self , context,  buff , valueType  , objs ):

		if objs == None:
			buff.putInt32(XC_TYPE_NULL);
			return ;


		buff.putInt32(self.id);
		buff.putInt32(context.getNO());
		buff.putString(self.className); # 'java.util.ArrayList'

		length = len(objs);
		buff.putInt32(length);

		if length == 0 :
			return ;

		param =  TYPE_OBJECT;
		if valueType!=None:
			params = valueType.getParameter();
			if params!=None:
				param = params[0];

		manager = ConvertorManager();

		if param == TYPE_OBJECT:
			for element in objs:
				manager.packByPythonType(context, None, buff, element);
		else :
			for element in objs:
				manager.pack(context, param, buff, element);


	def read(  self , context,  buff  , valueType ):

		ctype = buff.getInt32()
		if ctype == XC_TYPE_NULL:
			return None;

		if ctype != self.id :
			raise SerializeException('Invaild buff ,wanted ' + self.id + '  , get ' + str(ctype));

		no = buff.getInt32();
		clazz = buff.getString();
		length = buff.getInt32();

		manager = ConvertorManager();

		list=[];

		for i in range(length):
			val = manager.unpack( context , buff);
			list.append(val);

		return list;




class MapConvertor(Convertor):
	def write(  self , context,  buff , valueType  , objs ):

		if objs == None:
			buff.putInt32(XC_TYPE_NULL);
			return ;


		if type(objs) is not dict:
			raise SerializeException('objs is not dict ' + str(objs));


		buff.putInt32(XC_TYPE_MAP);
		buff.putInt32(context.getNO());
		buff.putString('java.util.HashMap');

		length = len(objs);
		buff.putInt32(length);

		if length == 0 :
			return ;

		paramKey   =  TYPE_OBJECT;
		paramValue =  TYPE_OBJECT;

		if valueType!=None:
			params = valueType.getParameter();
			if params!=None:
				if len(params)>0:
					paramKey = params[0];
				if len(params) > 1:
					paramValue = params[1];

		manager = ConvertorManager();

		for key, value in objs.items():
			if paramKey == TYPE_OBJECT or paramKey.isAccept(TYPE_OBJECT):
				manager.packByPythonType(context, None, buff, key);
			else:
				manager.pack(context, paramKey, buff, key);

			if paramValue == TYPE_OBJECT  or paramValue.isAccept(TYPE_OBJECT):
				manager.packByPythonType(context, None, buff, value);
			else:
				manager.pack(context, paramValue, buff, value);


	def read(  self , context,  buff  , valueType ):

		ctype = buff.getInt32()
		if ctype == XC_TYPE_NULL:
			return None;

		if ctype != XC_TYPE_MAP :
			raise XBuffer.BufferException('Invaild buff ,wanted XC_TYPE_MAP , get ' + str(ctype));

		no = buff.getInt32();
		clazz = buff.getString();
		length = buff.getInt32();

		manager = ConvertorManager();

		results ={};

		for i in range(length):
			key = manager.unpack( context , buff);
			val  = manager.unpack(context, buff);
			results[key] = val;

		return results;


class  Bean(dict):

	def __init__(self, name ):
		self.__className__ = name ;
	def getClass(self):
		return self.__className__ ;

	# def __str__(self):
	# 	return self.__className__ + '{' + str(dict.__dict__) +'}';


class EnumConvertor(Convertor):
	def write(self, context, buff, valueType, obj ):

		if obj == None:
			buff.putInt32(XC_TYPE_NULL);
			return;

		if type(obj) is not str:
			raise SerializeException('obj is not str ' + str(obj));

		buff.putInt32(XC_TYPE_ENUM);
		_type = valueType.getFirstParameter();
		buff.putString(_type.getName());
		buff.putString(obj);


	def read(self, context, buff, valueType):

		ctype = buff.getInt32()
		if ctype == XC_TYPE_NULL:
			return None;

		if ctype != XC_TYPE_ENUM:
			raise XBuffer.BufferException('Invaild buff ,wanted XC_TYPE_ENUM , get ' + str(ctype));

		clazz = buff.getString();
		value = buff.getString();

		return value;


class BeanConvertor(Convertor):
	def write(self, context, buff, valueType, objs):

		if objs == None:
			buff.putInt32(XC_TYPE_NULL);
			return;

		if type(objs) is not Bean:
			raise SerializeException('objs is not Bean ' + str(objs));

		buff.putInt32(XC_TYPE_BEAN);
		buff.putInt32(context.getNO());
		buff.putString( objs.getClass());

		className = objs.getClass();
		clazz = context.getMeta().getClass( className);

		length = 0 ;
		for key in objs :
			if not key.startswith('__'):
				length = length+1;



		buff.putInt32(length);

		if length == 0:
			return;

		manager = ConvertorManager();

		for key, value in objs.items():

			if not key.startswith('__'):
				buff.putString( key);
				valueType = clazz.getField( key);
				# manager.packByPythonType(context, valueType, buff, value);
				manager.pack(context, valueType, buff, value);


	def read(self, context, buff, valueType):

		ctype = buff.getInt32()
		if ctype == XC_TYPE_NULL:
			return None;

		if ctype != XC_TYPE_BEAN:
			raise XBuffer.BufferException('Invaild buff ,wanted XC_TYPE_BEAN , get ' + str(ctype));

		no = buff.getInt32();
		clazz = buff.getString();
		length = buff.getInt32();

		manager = ConvertorManager();

		results = Bean(clazz);

		for i in range(length):
			field = buff.getString();
			val = manager.unpack(context, buff);
			results[field] = val;

		return results;


# XC_TYPE_ARRAY = 0X80000000;
# XC_TYPE_REFERENCE = 0X40000000;
# XC_TYPE_INT8 = 1;
# XC_TYPE_INT16 = 2;
# XC_TYPE_INT32 = 3;
# XC_TYPE_INT64 = 4;
# XC_TYPE_STRING = 5;
# XC_TYPE_FLOAT = 7;
# XC_TYPE_DOUBLE = 8;
# XC_TYPE_CHAR = 9;
# XC_TYPE_DATE = 10;
# XC_TYPE_BOOLEAN = 11;
	
# XC_TYPE_BEAN = 20;
# XC_TYPE_LIST = 21;
# XC_TYPE_MAP = 22;
# XC_TYPE_NULL = 30;
class ConvertorManager (Singleton):
	def __init__(self):
		self.convertors = {} ;
		self.convertors['int'] = Int32Convertor();
		self.convertors['string'] = StringConvertor();
		self.convertors['double'] = DoubleConvertor();

		self.convertors['float'] = FloatConvertor();
		self.convertors['Date'] = DateConvertor();
		self.convertors['bool'] = BoolConvertor();
		self.convertors['List'] = CollectionConvertor(XC_TYPE_LIST, 'java.util.ArrayList');
		self.convertors['Set'] = CollectionConvertor(XC_TYPE_SET, 'java.util.HashSet');
		self.convertors['Map'] = MapConvertor();
		self.convertors['Bean'] = BeanConvertor();
		self.convertors['long'] = Int64Convertor();
		self.convertors['Enum'] = EnumConvertor();
		self.convertors['Class'] = ClassConvertor();


		
		self.types= {};
		self.types[XC_TYPE_INT32] = self.convertors['int'] ;
		self.types[XC_TYPE_INT64] = self.convertors['long'];
		self.types[XC_TYPE_STRING] = self.convertors['string'] ;
		self.types[XC_TYPE_DOUBLE] = self.convertors['double'] ;
		self.types[XC_TYPE_FLOAT] = self.convertors['float'];
		self.types[XC_TYPE_DATE] = self.convertors['Date'];
		self.types[XC_TYPE_BOOLEAN] = self.convertors['bool'];
		self.types[XC_TYPE_LIST] = self.convertors['List'];
		self.types[XC_TYPE_SET] = self.convertors['Set'];
		self.types[XC_TYPE_MAP] = self.convertors['Map'];
		self.types[XC_TYPE_BEAN] =self.convertors['Bean']  ;
		self.types[XC_TYPE_ENUM] = self.convertors['Enum'] ;
		self.types[XC_TYPE_CLASS] = self.convertors['Class'];

		self.ptypes = {};
		self.ptypes[int] = self.convertors['int'];
		self.ptypes[str] = self.convertors['string'];
		self.ptypes[float] = self.convertors['double'];
		self.ptypes[list] = self.convertors['List'];
		self.ptypes[dict] = self.convertors['Map'];


	def get( self , valueType  ):
		# 根据类型，找到转换器
		if valueType.isParameterized():
			name = valueType.getName();
			return self.convertors[name];
		else:
			# 简单类型， bean
			if type(valueType) is ClassType:
				return self.convertors['Bean'] ;

			name = valueType.getName();
			return self.convertors[name];

	def getByPythonType(self, val):
		return self.ptypes[type(val)];

	def getByType( self, valueType):
		return self.types[valueType];

	# def packByType(self, context, type, buff, val):
	# 	if val == None:
	# 		buff.putInt32(XC_TYPE_NULL);
	# 		return;
	#
	# 	ct = self.getByType(val);
	# 	if ct == None:
	# 		raise ConvertorException("Can't find type " + type + " " + str(type(val)));
	#
	# 	ct.write(context, buff, type, val);


	def packByPythonType(self, context, valueType, buff, val):
		if val == None:
			buff.putInt32(XC_TYPE_NULL);
			return;

		ct = self.getByPythonType(val);
		if ct == None:
			raise ConvertorException("Can't find type " + valueType + " " + str(type(val)));

		ct.write(context, buff, valueType, val);

	def pack( self, context,  valueType , buff , val ):
		if val == None :
			buff.putInt32( XC_TYPE_NULL );
			return ;
			
		ct = self.get(valueType);
		if ct == None:
			raise ConvertorException("Can't find type " + valueType + " "+ str(type(val)));
				
		ct.write( context , buff, valueType , val);


		
	def unpack( self, context,  buff ):
		
		valueType = buff.peekInt32();
		if valueType == XC_TYPE_NULL:
			# ignore 
			buff.getInt32(); 
			return None;
			
				
		ct = self.getByType(valueType);
		if ct == None:
			raise ConvertorException("Can't find type " + str(valueType));
				
		return ct.read( context, buff , None );


PrimitiveTypes = ['int', 'string', 'bool', 'byte', 'char', 'short', 'long', 'float', 'double', 'Date', 'void' , TYPE_OBJECT];


ParameterizedTypeREG = re.compile("^(?P<raw>\w+)(\<(?P<parameters>.*)\>)?$", re.I);

'''
 parse List<int> , List<Map<int,string>> ..
'''


def parseTypes(input):

	if input in PrimitiveTypes:
		return PrimitiveType(input);

	if input == '?':
		return TYPE_OBJECT;


	# match regex 'Name<P1,P2>'
	match = ParameterizedTypeREG.search(input)
	if match != None:
		#			print 'line' + line
		raw = match.group('raw');
		parameter = match.group('parameters');
		if parameter == None or len(parameter) == 0:
			return ParameterizedType(raw);
		else:
			_parameters = [];

			parameters = parameter.split(',');
			for param in parameters:
				p = parseTypes(param);
				_parameters.append(p);

			return ParameterizedType(raw, _parameters);
	else:
		# Bean ?

		return ClassType(input);


class Type:
	def getName(self):
		pass;




class ClassType(Type):
	def __init__(self, name):
		self.name = name;

	def __str__(self):
		return self.name;

	def isParameterized(self):
		return False;

	def getName(self):
		return self.name;

	def isAccept(self, name):
		return self.name == name ;



class PrimitiveType(Type):
	def __init__(self, name):
		self.name = name;

	def __str__(self):
		return self.name;

	def isParameterized(self):
		return False;

	def getName(self):
		return self.name;

	def isAccept(self, name):
		return self.name == name ;


class ParameterizedType(Type):
	# RowType<Parameter,...>
	def __init__(self, name, params=None):
		self.name = name;
		self.params = params;

	def getName(self):
		return self.name;

	def getFirstParameter(self):
		return self.params[0];


	def getParameter(self):
		return self.params;


	def isParameterized(self):
		return True;

	def __str__(self):
		if self.params != None:
			pn = '';
			for param in self.params:
				if len(pn) > 0:
					pn = pn + "," + str(param);
				else:
					pn = str(param);

			return self.name + '[' + pn + ']';
		else:
			return self.name;


class Parameter:
	def __init__(self, valueType):
		self.type = parseTypes(valueType);


class Method:
	def __init__(self, meta, name, signature, parameters, returnType):
		self.meta = meta;
		self.name = name;
		self.signature = signature;
		self.parameters = parameters;
		self.returnType = returnType;


	def getMeta(self):
		return self.meta;


class BeanInf:
	def __init__(self, name, fields):
		self.name = name;
		self.fields = fields;

	def getField(self, name):
		if name in self.fields:
			return self.fields[name];
		raise SerializeException('Cant find field ' + name);


class Meta:
	def __init__(self, service ):
		self.service = service;


	def setMeta(self,   methods, classes):
		self.methods = methods;
		self.classes = classes;


	def getClass(self, name ):
		if name in self.classes:
			return self.classes[name];

		raise SerializeException('Cant find class ' + name);

	def getMethod(self, name):
		if name in self.methods:
			return self.methods[name];

		raise SerializeException('Cant find method ' + name );


class Metas:
	def __init__(self):
		self.metas = [];
		self.service = None;

	def addMeta(self, meta):
		self.metas.append(meta
		                  );

	def getService(self):
		if self.service == None:
			if len(self.metas) == 1:
				self.service = self.metas[0].service;

		return self.service;

	def getMethod(self, name, service=None):
		if service == None:
			service = self.getService();

		if service == None:
			raise RuntimeError('Service empty');

		for meta in self.metas:
			if meta.service == service:
				return meta.getMethod(name);


class MetaFactory:
	def loadJSON(self):
		pass

	def loadMeta(self):
		js = self.loadJSON();

		metas = Metas();

		for _meta in js:

			methods = {};
			classes = {};

			meta = Meta(_meta['service']);

			for method in _meta['methods']:
				parameters = [];
				for p in method['parameters']:
					parameters.append(Parameter(p['type']));

				m = Method( meta , method['name'], method['signature'], parameters, method['returnType']);
				methods[method['name']] = m;

			for bean in _meta['classes']:
				name = bean['name'];
				fields = {};
				for _name, _value in bean['fields'].items():

					fields[_name] =parseTypes(_value);

				b = BeanInf(name, fields);
				classes[name] = b;

			meta.setMeta( methods, classes);
			metas.addMeta(meta);

		return metas;


class MetaFactoryFile(MetaFactory):
	def __init__(self, file):
		self.file = file;

	def loadJSON(self):
		h = None;
		try:
			h = open(self.file, encoding='utf-8');
			if h != None:
				js = json.load(h);
				return js;
		finally:
			if h != None:
				h.close();

		pass;

COMMAOND_SERVICES_DESCRIBER = 20001

class MetaFactoryRemote(MetaFactory ):
	def __init__(self, h , dumpJson = None):
		self.h = h;
		self.debug = dumpJson;

	def loadJSON(self):
		buff = self.h.execute(COMMAOND_SERVICES_DESCRIBER, b'ALL');
		if buff != None:
			buff1 = XBuffer.Buffer.attach(buff);
			jsonstr = buff1.getString();

			if self.debug != None:
				f = open(self.debug , 'w');
				f.write(jsonstr);
				f.close();


			js = json.loads(jsonstr);
			return js;

