from xcommon.utils import *
from xcommon.xclient import *

import struct;
import binascii
import types;
import time;
import inspect;

def timeit(func):
	
	# 定义一个内嵌的包装函数，给传入的函数加上计时功能的包装
	def func_wrapper(*args, **kwargs):
	
		argspec = inspect.getargspec(func)
		namedargs = inspect.getcallargs(func, *args, **kwargs)

		# def foo(a, b=0, *c, **d): pass
		# foo(1, b=2, c=3, d=4) will convert c=3 to namedargs.
		unnamedargs = namedargs.pop(argspec.varargs, ())
		namedargs.update(namedargs.pop(argspec.keywords, {}))

		func_wrapper.__namedargs__ = namedargs
		func_wrapper.__unnamedargs__ = unnamedargs
		#func_wrapper.__annotations__ = annotations
		
		start = time.clock()
		result = func(*args, **kwargs)
			
		
		end =time.clock()
		print ('used:' + str(end - start));
		return result;
	 
	# 将包装后的函数返回
	return func_wrapper
	
# 
# 
class WrapMe(object):
	def __init__(self, obj): 
		self.data = obj; 
		
	def get(self):
		return self.data;
		
	def __repr__(self):
		return 'self.data';
		
		
	def __str__(self):
		return str(self.data);
		
	def __getattr__(self, attr):
		
		obj = getattr(self.data, attr);
		return timeit(obj);

	

class _Wrap(f):
	def __getattr__(self, attr):
		print( 'in getattr' + attr);
		print( 'in getattr' + attr);
		obj = getattr(self.data, attr);
		return timeit(obj);

		
class Factory:
	def __init__(self, name): 
		self.name  = name; 
		
	def createInterface():
		
		
		

class MyTest:
	def __init__(self, name ):
		self.name = name ;
		
	def sayHello( self , name ):
		print('Hello ' + name + ' , this is '+ self.name );
		return name;
	
t = WrapMe(MyTest('n'));	
r = t.sayHello('aaa',102,'acefg');

print('result is ' + r);


