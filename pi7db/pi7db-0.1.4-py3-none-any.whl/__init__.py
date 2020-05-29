import os,errno,hashlib,shutil,datetime,glob,random
from .status import error,success,info
from .functions.functions import *
from .functions.subclass import subclass
from .operators import *

class pi7db:
  def __init__(self,db_name,db_path=os.getcwd()):
   self.db_np,self.db_name = os.path.join(db_path,db_name),db_name
   self.config_file,self.coll_name = os.path.join(self.db_np,db_name),None
   if not os.path.exists(self.db_np):os.makedirs(self.db_np)
   if not os.path.exists(f"{self.config_file}.bin"):
    self.config = {'secret-key':None,'enc_type':'bin','doc_size':15000000}
    writejson(f"{self.config_file}.bin",self.config)
   else:self.config=openjson(f"{self.config_file}.bin")
     
  def __getattr__(self, attrname):
   path=self.coll_name=os.path.join(self.db_np,attrname)
   SubClass = type(attrname,(subclass,),{'coll_name':self.coll_name,'cr_collection':attrname,'config':self.config,'db_name':self.db_name})
   SubClass = SubClass()
   return SubClass
  
  def key(self,password):
   key = hashlib.md5(password.encode()).hexdigest()
   if self.config['secret-key'] is not None: 
    if key != self.config['secret-key']:raise ValueError(error.e0)
   else:
     self.config = {'secret-key':key,'enc_type':'pi7db'}
     writejson(self.config_file,self.config)

  def changekey(self,old_key,New_key):
   files,old_key,New_key = glob.glob(f"{self.db_np}/*/*."),hashlib.md5(old_key.encode()).hexdigest(),hashlib.md5(New_key.encode()).hexdigest()
   if old_key == openjson(self.config_file)['secret-key']:
    for x_js in files:
     writejson(x_js[:-len(self.config['enc_type'])-1],openjson(x_js[:-len(self.config['enc_type'])-1],old_key),New_key)
     if os.path.exists(x_js):os.remove(x_js)
    writejson(self.config_file,{'secret-key':New_key})
   else:raise ValueError(error.e1)

  def write(self,coll_name,fn_dict,data=None):
   path,crt_time = os.path.join(self.db_np,coll_name),datetime.datetime.now().strftime("%Y%S%f");dc_id = f"{crt_time}{random.randint(10000, 99999)}"
   if data is None and isinstance(fn_dict,dict):fn_dict={'unid':dc_id,**fn_dict};writenodoc(path,fn_dict,self.config)
   else:
    try: 
     data_dict={'unid':dc_id,**data}
     data_dict['cr_dc_path'] = f"{path}/{fn_dict}.{self.config['enc_type']}";create_coll(path)
     writejson(data_dict['cr_dc_path'],data_dict,self.config['secret-key'])
     return success.s0(fn_dict, self.coll_name)
    except Exception as e:return error.e4
  
  def update(self,coll_name,file_name=None,data_arg=None,**kwargs):
   if "where" in kwargs:
     if isinstance(coll_name,str) and isinstance(file_name,dict):
       if isinstance(kwargs['where'],list) or isinstance(kwargs['where'],tuple):updatebyfilter(self.filter(coll_name,*kwargs['where'])['data'],file_name,self.config)
       else:updatebyfilter(self.filter(coll_name,kwargs['where'])['data'],file_name,self.config)
       return True
     if isinstance(coll_name,dict) and file_name is None:
      if isinstance(kwargs['where'],list) or isinstance(kwargs['where'],tuple):updatebyfilter(self.filter(coll_name,*kwargs['where'])['data'],coll_name,self.config)
      else:updatebyfilter(self.filter(kwargs['where'])['data'],coll_name,self.config)
      return True 
   try:
    js_data=openjson(f"{self.db_np}/{coll_name}/{file_name}.{self.config['enc_type']}",self.config['secret-key'])
    if isinstance(data_arg,dict):
      for x in data_arg:
        if isinstance(data_arg[x],dict) and increment_v in data_arg[x]:js_data[x] = js_data[x]+data_arg[x][increment_v]
        elif isinstance(data_arg[x],dict) and decrement_v in data_arg[x]:js_data[x] = js_data[x]-data_arg[x][decrement_v]
        else:js_data.update({x:data_arg[x]})
    else:return error.e2
    writejson(f"{self.db_np}/{coll_name}/{file_name}.{self.config['enc_type']}",js_data,self.config['secret-key'])
    return success.s1(file_name)
   except OSError as e:
    if isinstance(file_name,dict):
     file_name = None
     if e.errno == errno.ENOENT:return error.e3(file_name)
    else:return e

  def read(self,coll_name=None,file_name=None,key_name=None,**kwargs):
   kwargs,data_files,r_data = extract_kwargs(kwargs,self.db_name),[],{"data":[],"status":1}
   if key_name is not None:return {"data":openjson(f"{self.db_np}/{coll_name}/{file_name}",self.config['secret-key'])[key_name],"status":1}
   elif file_name is not None:data_files=[f"{self.db_np}/{coll_name}/{file_name}.{self.config['enc_type']}"]
   elif coll_name is not None:data_files = extractfiles(f"{self.db_np}/{coll_name}",kwargs)
   else:data_files = extractfiles(f"{self.db_np}",kwargs)
   for x_file in data_files[kwargs['f_a']:kwargs['l_a']]:
     o_data = openjson(x_file,self.config['secret-key'])
     if isinstance(o_data,list):r_data['data'].extend(o_data)
     else:r_data['data'].append(o_data)
   return r_data
    
  def trash(self,coll_name=None,file_name=None,key_name=None,**kwargs):
   if len(kwargs):
    if 'dropkey' in kwargs:key_name=kwargs['dropkey']
    if isinstance(coll_name,str) and 'where' in kwargs:
      if isinstance(kwargs['where'],list) or isinstance(kwargs['where'],tuple):trashbyfilter(self.filter(coll_name,*kwargs['where'])['data'],key_name,self.config)
      else:trashbyfilter(self.filter(coll_name,kwargs['where'])['data'],key_name,self.config)
      return True
    if 'where' in kwargs and coll_name is None:
      if isinstance(kwargs['where'],list) or isinstance(kwargs['where'],tuple):trashbyfilter(self.filter(coll_name,*kwargs['where'])['data'],key_name,self.config)
      else:trashbyfilter(self.filter(kwargs['where'])['data'],key_name,self.config)
      return True
   if key_name is not None:
     tr_data = openjson(f"{self.db_np}/{coll_name}/{file_name}.{self.config['enc_type']}",self.config['secret-key']);tr_data.pop(key_name)
     writejson(f"{self.db_np}/{coll_name}/{file_name}.{self.config['enc_type']}",tr_data,self.config['secret-key'])
     return success.s2(key_name,file_name)
   elif file_name is not None:
     os.remove(f"{self.db_np}/{coll_name}/{file_name}.{self.config['enc_type']}")
     return success.s3(file_name)
   elif coll_name is not None:
     shutil.rmtree(f"{self.db_np}/{coll_name}", ignore_errors=False, onerror=None)
     return success.s4(coll_name)
 
  def sort(self,coll_name,command_tup=None,**kwargs):
   un_ex_kwargs,kwargs,order = kwargs,extract_kwargs(kwargs,self.db_name),False
   if "order" in kwargs:order = kwargs['order']
   if isinstance(coll_name,set):all_data,command_tup=self.read(**un_ex_kwargs),coll_name
   else:all_data=self.read(coll_name,**un_ex_kwargs)
   r_data = {"data":all_data['data'],"status":1}
   if isinstance(command_tup,set):
    key_tup = "i"+str([[x] for x in command_tup])[1:-1].replace(', ',"")
    r_data['data'] = sorted(r_data['data'], key = lambda i:(exec('global s;s = %s' % key_tup),s),reverse=order)
   else: 
    if isinstance(command_tup,str):r_data['data'] = sorted(r_data['data'],key = lambda i: i[command_tup],reverse=order)[kwargs['f_a']:kwargs['l_a']]
   return r_data

  def sortdict(self,dict_list,sort_key,**kwargs):
   kwargs,order,r_data = extract_kwargs(kwargs,self.db_name),False,{"data":dict_list['data'],"status":1}
   if "order" in kwargs:order = kwargs['order']
   if isinstance(sort_key,set):
    key_tup = "i"+str([[x] for x in sort_key])[1:-1].replace(', ',"")
    r_data['data'] = sorted(r_data['data'][kwargs['f_a']:kwargs['l_a']], key = lambda i:(exec('global s;s = %s' % key_tup),s),reverse=order)
   else: 
    if isinstance(sort_key,str):r_data['data'][kwargs['f_a']:kwargs['l_a']] = sorted(r_data['data'],key = lambda i: i[sort_key],reverse=order)
   return r_data
  
  def filter(self,*command_tup,**kwargs):
   un_ex_kwargs,kwargs = kwargs,extract_kwargs(kwargs,self.db_name)
   if isinstance(command_tup[0],str):command_tup,all_data = list(command_tup[1:]),self.read(command_tup[0],**un_ex_kwargs) 
   else:all_data = self.read(**un_ex_kwargs) 
   r_data,command_arr= {"data":[],'status':1},[]
   if OR in command_tup:
    for x_p in command_tup:
      if x_p != OR:command_arr.append(x_p)
    for command in command_arr:
     data_get = andfilter(command,all_data['data'])
     for x in data_get[kwargs['f_a']:kwargs['l_a']]:
      if x not in r_data['data']:r_data['data'].append(x)
    return r_data
   else:
    for x_r in andfilter(command_tup[0],all_data['data'])[kwargs['f_a']:kwargs['l_a']]:r_data['data'].append(x_r)
    return r_data
