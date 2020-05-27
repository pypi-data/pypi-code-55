##Tests for pipeline
import sys,os,traceback
import numpy as np
import time
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..'))
import pyParz

indata=np.arange(0,100,1)
def par_func1(x):
	time.sleep(.1)
	return(x**2)
start = time.time()
res=[par_func1(x) for x in indata]
end = time.time()
print('without par',end - start)
start = time.time()
res=pyParz.foreach(indata,par_func1,args=None)
end = time.time()
print('with par',end - start)

indata2=1

def par_func2(args):
  x,y=args
  time.sleep(.1)
  return(x**2+y)
start = time.time()
res=[par_func2([x,indata2]) for x in indata]
end = time.time()
print('without par',end - start)
start = time.time()
res2=pyParz.foreach(indata,par_func2,args=[indata2])
end = time.time()
print('with par',end - start)


