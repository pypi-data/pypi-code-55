import os,random,time
import numpy as np
import pandas as pd
import inspect as ins
from .fun import ispump

class pump:

    def demo():
        '''demo is used to demonstrate typical examples about this class.'''
        
        demostr = '''
import clubear as cb
#clubear.csv is generated by cb.manager.demo()
pm=cb.pump('clubear.csv') #start a new pump
pm.keep #check the head lists
ck=cb.check(pm) #create a checker
ck.stats() #check the for stats
pm.qlist=['age','height','weight','logsales']
ck.stats() #check stats again
ck.table() #check table
pm.subsize=10000 #check the subsize
pm.seq=True #sequential sampling method
df=pm.go() #start to pump data
'''
        print(demostr)
        
    def __init__(self,pathfile):
        '''Initialization: check whether pathfile is correct.'''
        
        '''Very careful initial checking.'''
        if not isinstance(pathfile,str): print('pump: The pathfile must be a str.'); return
        if not os.path.exists(pathfile): print('pump: This file dose not exists!'); return
        if not os.path.isfile(pathfile): print('pump: This is not a file!'); return
        self.reader=open(pathfile,encoding='iso8859-1')    
        self.keep=self.reader.readline().replace('\n','').split(',')
        self.keep=[each.strip() for each in self.keep]
        if len(self.keep)==0: print('pump: Nothing found in the file!'); return 
        head_min_str_len=min([len(each) for each in self.keep])
        if head_min_str_len==0: print('pump: Empty head found in heads.'); return
        if len(self.keep)!=len(set(self.keep)): print('pump: Identical heads exist.'); return
        random.seed(0);np.random.seed(0)
        
        self.subsize=100
        self.drop=[];
        self.qlist=self.keep
        self.seq=False
        self.intercept=True
        self.pathfile=pathfile
              
    def go(self):
        '''go is used to pump out data'''
        
        subsize=self.subsize
        '''Careful check all the inputs and pre-conditions'''                
        if not isinstance(subsize,int): print('pump.go: The subsize must be a int.'); return
        if not isinstance(self.keep,list): print('pump.go: The keep list must be a list.'); return
        if not isinstance(self.drop,list): print('pump.go: The drop list must be a list.'); return
        if not isinstance(self.qlist,list): print('pump.go: The qlist must be list.'); return
        if not isinstance(self.seq,bool): print('pump.go: The seq choice must be a bool.'); return
        if not isinstance(self.intercept,bool): print('pump.go: The intercept choice must be a bool.'); return
        
        self.drop=[each.strip() for each in self.drop]
        self.keep=[each.strip() for each in self.keep]
        self.qlist=[each.strip() for each in self.qlist]
        
        self.reader.seek(0,0)
        Heads=self.reader.readline().replace('\n','').split(',')
        Heads=[each.strip() for each in Heads]
        
        self.qlist=[each for each in self.qlist if each in Heads]
        self.drop=[each for each in self.drop if each in Heads]
        self.keep=[each for each in self.keep if each in Heads]
        self.keep=[each for each in self.keep if each not in self.drop]
        
        if len(self.keep)==0: print('pump.go: The heads list contains no valid heads.'); return
        select=[each for each in range(len(Heads)) if Heads[each] in self.keep]

        '''Find the file size'''
        self.reader.seek(0,2)
        file_size=self.reader.tell()
        
        '''start to generate the data'''
        oklines=0;data=[];self.reader.seek(0,0);ncolumns = len(Heads);
        if self.seq==False:
            while oklines<subsize:
                pos=int(random.random()*file_size)
                self.reader.seek(pos,0)
                skip_line=self.reader.readline()
                real_line=self.reader.readline()
                data.append(real_line)
                oklines=oklines+1
                
        if self.seq==True:
            pos=int(random.random()*file_size)
            self.reader.seek(pos,0)
            skip_line=self.reader.readline()
            trytime=0
            while oklines<subsize:
                if trytime>=100: print('pump.go: Try too many times and failed.'); return;
                real_line=self.reader.readline()
                if real_line=='':
                    trytime=trytime+1
                    pos=int(random.random()*file_size)
                    self.reader.seek(pos,0)
                    skip_line=self.reader.readline() 
                    continue
                data.append(real_line)
                oklines=oklines+1
                trytime=0
                
        data=[each.replace('\n','').split(',') for each in data]
        df=pd.DataFrame(data)
        if df.shape[1]!=len(Heads): print('pump: No. of columns not equal to No. of heads!'); return
        df.columns=Heads
        df=df[self.keep]
        
        '''create numerical values'''
        df=df.astype('object')
        self.qlist=[each for each in self.qlist if each in df.columns]
        if len(self.qlist)>0:
            for each in self.qlist: 
                df[each]=pd.to_numeric(df[each],errors='coerce')
                
        if self.intercept: df['_INTERCEPT_']=1.0 #include an intercept
        return df
    
class tank:
    def demo():
        '''demo is used to demonstrate typical examples about this class.'''
        
        demostr = '''
import clubear as cb
import numpy as np
#clubear.csv is generated by cb.manager.demo()
pm=cb.pump('clubear.csv')  #read in the demodata for illustration
pm.drop=['brand','company','weight'] #drop some varialbe for illustration
pm.qlist=['age','height','logsales','price'] #define the quant variables
ck=cb.check(pm).table(tv=True); #levels of quali variables

tk=cb.tank(pm); #create a new tank to hold the pump work for prepressing
tk.app(np.log,'age','logage') #app np.log transformation to age
tk.app(lambda x: x**2,'height') #app a user defined func to height
tk.ady('gender',['Female']) #add dummy for gender
tk.ady('region',ck['region'][1]) #add dummy for region
ck=cb.check(tk).stats() #check the newly generated tank        
'''
        print(demostr)
    
    def __init__(self,pm):
        '''Initialization: check whether pm is a PUMP!.'''
        
        self.pm=pm;
        if not ispump(self.pm): print('tank.go: The input seems not a valid pump.'); return
        self.App=[];self.Ady=[];self.drop=[];self.keep=[]
        
    def app(self,func,head,newhead=''):
        '''app is used to app func to the head column'''
        
        '''check the initial condition very carefully'''
        df=self.pm.go();Heads=list(df.columns)
        if not callable(func): print('tank.app: the input func *'+str(func)+'* is not a function.'); return
        if not isinstance(head,str): print('tank.app: the head *'+str(head)+'* must be a str.'); return
        if not isinstance(newhead,str): print('tank.app: the newhead *'+str(newhead)+'* must be a str.'); return
        head=head.strip();newhead=newhead.strip()
        if len(head)==0: print('tank.app: the head *'+str(head)+'* cannot be empty.'); return
        if not head in Heads: print('tank.app: the head *'+str(head)+'* not found in df heads.'); return
        if len(newhead)==0: newhead=head
        
        self.App.append([func,head,newhead])
        
    def ady(self,head,levels,drop=True):
        '''ady is used to add dumy varialbes for head according to levels.'''
        
        '''this part check the current parameters of the tank'''
        df=self.pm.go();Heads=list(df.columns)
        if not isinstance(head,str): print('tank.ady: the head *'+str(head)+'* must be a str.'); return
        head=head.strip()
        if len(head)==0: print('tank.ady: the head *'+str(head)+'* cannot be empty.'); return
        if not head in Heads: print('tank.ady: the head *'+str(head)+'* not found in df heads.'); return
        if not isinstance(levels,list): print('tank.ady: the input levels must be a list.'); return
        if len(levels)==0: print('tank.ady: the input levels cannot be empty'); return
        if not isinstance(drop,bool): print('tank.ady: the drop input should be a bool.'); return
        
        self.Ady.append([head,levels])
        self.drop.append(head)   
        
    def go(self):
        '''go is used to pump out data'''

        '''get pump data'''
        df=self.pm.go();Heads=list(df.columns)
                
        '''this part is used to do app transformation'''
        if not isinstance(self.App,list): print('tank.go: The App list must be a list.'); return
        self.App=[each for each in self.App if isinstance(each,list)]
        self.App=[each for each in self.App if len(each)==3]
        self.App=[each for each in self.App if callable(each[0])]
        self.App=[each for each in self.App if each[1] in Heads]
        self.App=[each for each in self.App if isinstance(each[2],str)]
        for each in self.App: df[each[2]]=list(map(each[0],df[each[1]]))
            
        
        '''this part is used to add dummy variable'''
        if not isinstance(self.Ady,list): print('tank.go: The Ady list must be a list.'); return
        self.Ady=[each for each in self.Ady if isinstance(each,list)]
        self.Ady=[each for each in self.Ady if len(each)==2]
        self.Ady=[each for each in self.Ady if each[0] in Heads]
        for each in self.Ady:
            head=each[0];levels=each[1]
            nlevels=len(levels)
            newname=[head+'_'+str(each) for each in levels]
            for j in range(nlevels): 
                dummys=[1.0*(each==levels[j]) for each in df[head]]
                df[newname[j]]=dummys
        
        '''this part is used to handle drop and keep list'''
        if not isinstance(self.drop,list): print('tank.go: The drop list must be a list.'); return
        self.drop=[each for each in self.drop if each in df.columns]
        df=df.drop(self.drop,axis=1)
        
        if not isinstance(self.keep,list): print('tank.go: The keep list must be a list.'); return
        self.keep=[each for each in self.keep if each in df.columns]
        if len(self.keep)>0: df=df[self.keep]
            
        '''this part eliminate all np.nan observations'''
        ss=df.shape[0]
        flag=[True for each in range(ss)]
        for each in df.columns:
                if df.dtypes[each]!='object':
                    newflag=list(np.isnan(df[each]))
                    newflag=[not each for each in newflag]
                    flag=[flag[each]&newflag[each] for each in range(ss)]
        df=df.iloc[list(flag)]
        
        return df
    
def save(tk,filename=''):
    if not isinstance(filename,str): print('save: The filename should be a str.'); return
    pm=tk
    pmlist=[]
    while ispump(pm):
        pmlist.append(pm)
        try:
            pm=pm.pm
        except:
            break
    FileName=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    FileName='CluBear ('+FileName+').py'
    if len(filename)>0: FileName=filename+'.py'
    f=open(FileName,'w')
    f.write('import clubear as cb\n')
    f.write('import numpy as np\n')
    f.write('import pandas as pd\n')
    f.write('\n')

    pm=pmlist[-1];pmname='pm0'
    f.write("'''This is pump: 0'''\n")
    f.write('pm0=cb.pump("'+pm.pathfile+'")\n')
    f.write('pm0.subsize='+str(pm.subsize)+'\n')
    f.write('pm0.drop='+str(pm.drop)+'\n')
    f.write('pm0.qlist='+str(pm.qlist)+'\n')
    f.write('pm0.seq='+str(pm.seq)+'\n')
    f.write('pm0.intercept='+str(pm.intercept)+'\n')
    f.write('\n')

    length=len(pmlist)
    
    if length>0:
        f.write("'''User defiend functions here'''\n")
        myfunc=[]
        for k in range(length-1):
            app=pmlist[k].App
            [myfunc.append(each[0]) for each in app]
        myfunc=list(set(myfunc))
        myfunc=[each for each in myfunc if '<lambda>' not in str(each)]
        myfunc=[each for each in myfunc if 'ufunc' not in str(each)]
        for each in myfunc: f.write(ins.getsource(each)+'\n')

        for k in range(length-2,-1,-1):
            index=length-k-1
            pm=pmlist[k];
            pmname='pm'+str(index)

            pm.keep=sorted(list(set(pm.keep)))
            pm.drop=sorted(list(set(pm.drop)))
            
            f.write("'''This is pump: "+str(index)+"'''\n")
            f.write(pmname+'=cb.tank(pm'+str(index-1)+')\n')
            f.write(pmname+'.keep='+str(pm.keep)+'\n')
            f.write(pmname+'.drop='+str(pm.drop)+'\n')
            f.write('\n')

            '''write App codes'''
            out=pm.App
            for each in out:
                ftype=str(each[0])+str(type(each[0]))
                if "<lambda>" in ftype: 
                    codes=ins.getsource(each[0]).split('.')
                    codes[0]=pmname
                    codes='.'.join(codes)
                    f.write(codes); continue
                if "numpy.ufunc" in ftype:
                    func=str(each[0]).split("'")[-2]
                    codes=pmname+'.app('+'np.'+func+',"'+each[1]+'","'+each[2]+'")\n'
                    f.write(codes); continue

                myfunc=ftype.split('function')[1].strip().split(' ')[0]
                codes=pmname+'.app("'+each[1]+'",'+myfunc+',"'+each[2]+'")\n'
                f.write(codes)
            f.write('\n')

            for each in pm.Ady: f.write(pmname+'.ady("'+each[0]+'",'+str(each[1])+')\n')        
            f.write('\n')
        
    f.write('cpm=cb.tank('+pmname+')\n')
    f.close()
    
