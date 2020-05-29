from .functions import *
import glob
import os,errno
import shutil
import glob
from ..status import error,success,info
from ..operators import *

class subclass:
  def __init__(self):
      pass
  
  def write(self,fn_dict,data=None):
   crt_time = datetime.datetime.now().strftime("%Y%S%f");dc_id = f"{crt_time}{random.randint(10000, 99999)}"
   try:
    if data is None and isinstance(fn_dict,dict):fn_dict={'unid':dc_id,**fn_dict};writenodoc(self.coll_name,fn_dict,self.config) 
    else:
     fn_dict, data['cr_dc_path'] = {'unid':dc_id,**fn_dict},f"{self.coll_name}/{fn_dict}.{self.config['enc_type']}"
     if not os.path.exists(self.coll_name):os.mkdir(self.coll_name)
     writejson(data['cr_dc_path'],data,self.config['secret-key'])
    return success.s0(fn_dict, self.coll_name)
   except Exception as e:return error.e4
  
  def read(self,file_name=None,key_name=None,**kwargs):
   kwargs,r_data = extract_kwargs(kwargs),{"data":[],"status":1}
   if key_name is not None:return {"data":openjson(f"{self.coll_name}/{file_name}",self.config['secret-key'])[key_name],"status":1}
   elif file_name is not None:data_files=glob.glob(f"{self.coll_name}/{file_name}.{self.config['enc_type']}")
   else:data_files = extractfiles(self.coll_name,kwargs)
   for x_file in data_files[kwargs['f_a']:kwargs['l_a']]:
     o_data = openjson(x_file,self.config['secret-key'])
     if isinstance(o_data,list):r_data['data'].extend(o_data)
     else:r_data['data'].append(o_data)
   return r_data

  def trash(self,file_name=None,key_name=None,**kwargs):
   if len(kwargs):
    if 'dropkey' in kwargs:key_name=kwargs['dropkey']
    if 'where' in kwargs:
      trashbyfilter(self.filter(kwargs['where'])['data'],key_name,self.config)
      return True
   if key_name is not None:
     tr_data = openjson(f"{self.coll_name}/{file_name}",self.config['secret-key']);tr_data.pop(key_name)
     writejson(f"{self.coll_name}/{file_name}",tr_data,self.config['secret-key'])
     return success.s2(key_name,file_name)
   elif file_name is not None:os.remove(f"{self.coll_name}/{file_name}.{self.config['enc_type']}");return success.s3(file_name)
   else:shutil.rmtree(self.coll_name, ignore_errors=False, onerror=None);return success.s4(self.coll_name)
  
  def sort(self,command_tup,order=False,**kwargs):
   all_data,kwargs=self.read()['data'],extract_kwargs(kwargs);r_data = {"data":all_data,"status":1}
   if isinstance(command_tup,set):
    key_tup = "i"+str([[x] for x in command_tup])[1:-1].replace(', ',"")
    r_data['data'] = sorted(r_data['data'], key = lambda i:(exec('global s;s = %s' % key_tup),s),reverse=order)
   else: 
    if isinstance(command_tup,str):r_data['data'] = sorted(r_data['data'],key = lambda i: i[command_tup],reverse=order)
   r_data['data'] = r_data['data'][kwargs['f_a']:kwargs['l_a']]
   return r_data
  
  def filter(self,*command_tup,**kwargs):
   kwargs = extract_kwargs(kwargs)
   r_data,command_arr,all_data= {"data":[],'status':1},[],self.read()
   if OR in command_tup:
    for x_p in command_tup:
      if x_p != OR:command_arr.append(x_p)
    for command in command_arr:
     data_get = andfilter(command,self.config,all_data['data'])
     for x in data_get[kwargs['f_a']:kwargs['l_a']]:
      if x not in r_data['data']:r_data['data'].append(x)
    return r_data
   else:
    for x_r in andfilter(command_tup[0],self.config,all_data['data'])[kwargs['f_a']:kwargs['l_a']]:r_data['data'].append(x_r)
    return r_data

    
    