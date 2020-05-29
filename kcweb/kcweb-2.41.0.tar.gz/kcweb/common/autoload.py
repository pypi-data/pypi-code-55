# -*- coding: utf-8 -*-
import time,hashlib,json,re,os,platform,sys,shutil,zipfile 
import datetime as core_datetime
from kcweb import config
from kcweb.utill.dateutil.relativedelta import relativedelta as core_relativedelta
from kcweb.utill.db import mysql as kcwmysql
from kcweb.utill.db import mongodb as kcwmongodb
from kcweb.utill.db import sqlite as kcwsqlite
from kcweb.utill.cache import cache as kcwcache
from kcweb.utill.redis import redis as kcwredis
from kcweb.utill.http import Http
from kcweb.utill.queues import Queues
from kcweb.utill.db import model
from mako.template import Template as kcwTemplate
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
from . import globals
redis=kcwredis()
def send_mail(user,text="邮件内容",theme="邮件主题",recNick="收件人昵称"):
    """发送邮件

    参数 user：接收邮件的邮箱地址

    参数 text：邮件内容

    参数 theme：邮件主题

    参数 recNick：收件人昵称

    return Boolean类型
    """
    ret=True
    if not theme:
        theme=config.email['theme']
    if not recNick:
        recNick=config.email['recNick']
    try:
        msg=MIMEText(text,'plain','utf-8')
        msg['From']=formataddr([config.email['sendNick'],config.email['sender']]) 
        msg['To']=formataddr([recNick,user]) 
        msg['Subject']=theme

        server=smtplib.SMTP_SSL("smtp.qq.com", 465) 
        server.login(config.email['sender'], config.email['pwd']) 
        server.sendmail(config.email['sender'],[user,],msg.as_string())
        server.quit()
    except Exception:
        ret=False
    return ret
get_sysinfodesffafew=None
def get_sysinfo():
    """获取系统信息

    return dict类型
    """
    global get_sysinfodesffafew
    if get_sysinfodesffafew:
        sysinfo=get_sysinfodesffafew
    else:
        sysinfo={}
        sysinfo['platform']=platform.platform()        #获取操作系统名称及版本号，'Linux-3.13.0-46-generic-i686-with-Deepin-2014.2-trusty'  
        sysinfo['version']=platform.version()         #获取操作系统版本号，'#76-Ubuntu SMP Thu Feb 26 18:52:49 UTC 2015'
        sysinfo['architecture']=platform.architecture()    #获取操作系统的位数，('32bit', 'ELF')
        sysinfo['machine']=platform.machine()         #计算机类型，'i686'
        sysinfo['node']=platform.node()            #计算机的网络名称，'XF654'
        sysinfo['processor']=platform.processor()       #计算机处理器信息，''i686'
        sysinfo['uname']=platform.uname()           #包含上面所有的信息汇总，('Linux', 'XF654', '3.13.0-46-generic', '#76-Ubuntu SMP Thu Feb 26 18:52:49 UTC 2015', 'i686', 'i686')
        sysinfo['start_time']=times()
        get_sysinfodesffafew=sysinfo
            # 还可以获得计算机中python的一些信息：
            # import platform
            # platform.python_build()
            # platform.python_compiler()
            # platform.python_branch()
            # platform.python_implementation()
            # platform.python_revision()
            # platform.python_version()
            # platform.python_version_tuple()
    return sysinfo
def Template(path,**context):
    "模板渲染引擎函数,使用配置的模板路径"
    return Templates(str(config.app['tpl_folder'])+str(path),**context)
def Templates(path,**context):
    "模板渲染引擎函数，需要完整的模板目录文件"
    body=''
    with open(path, 'r',encoding='utf-8') as f:
        content=f.read()
        t=kcwTemplate(content)
        body=t.render(**context)
    return body
def mysql(table=None,configss=None):
    """mysql数据库操作实例
    
    参数 table：表名

    参数 configss 数据库配置  可以传数据库名字符串
    """
    dbs=kcwmysql.mysql()
    if table is None:
        return dbs
    elif configss:
        return dbs.connect(configss).table(table)
    else:
        return dbs.connect(config.database).table(table)
def sqlite(table=None,configss=None):
    """sqlite数据库操作实例
    
    参数 table：表名

    参数 configss 数据库配置  可以传数据库名字符串
    """
    dbs=kcwsqlite.sqlite()
    if table is None:
        return dbs
    elif configss:
        return dbs.connect(configss).table(table)
    else:
        return dbs.connect(config.sqlite).table(table)
def M(table=None,confi=None):
    """数据库操作实例
    
    参数 table：表名

    参数 confi 数据库配置  可以传数据库名字符串
    """
    if confi:
        if confi['type']=='sqlite':
            return sqlite(table,confi)
        else:
            return mysql(table,confi)
    else:
        if config.database['type']=='sqlite':
            return sqlite(table)
        else:
            return mysql(table)
def mongo(table=None,configss=None):
    """mongodb数据库操作实例
    
    参数 table：表名(mongodb数据库集合名)

    参数 configss mongodb数据库配置  可以传数据库名字符串
    """
    mObj=kcwmongodb.mongo()
    if table is None:
        return mObj
    elif configss:
        return mObj.connect(configss).table(table)
    else:
        return mObj.connect(config.mongo).table(table)
def is_index(params,index):
    """判断列表或字典里的索引是否存在

    params  列表或字典

    index   索引值

    return Boolean类型
    """
    try:
        params[index]
    except KeyError:
        return False
    except IndexError:
        return False
    else:
        return True
def set_cache(name,values,expire="no"):
    """设置缓存

    参数 name：缓存名

    参数 values：缓存值

    参数 expire：缓存有效期 0表示永久  单位 秒
    
    return Boolean类型
    """
    return kcwcache.cache().set_cache(name,values,expire)
def get_cache(name):
    """获取缓存

    参数 name：缓存名

    return 或者的值
    """
    return kcwcache.cache().get_cache(name)
def del_cache(name):
    """删除缓存

    参数 name：缓存名

    return Boolean类型
    """
    return kcwcache.cache().del_cache(name)
def md5(strs):
    """md5加密
    
    参数 strs：要加密的字符串

    return String类型
    """
    m = hashlib.md5()
    b = strs.encode(encoding='utf-8')
    m.update(b)
    return m.hexdigest()
def times():
    """生成时间戳整数 精确到秒(10位数字)
    
    return int类型
    """
    return int(time.time())
def json_decode(strs):
    """json字符串转python类型"""
    try:
        return json.loads(strs)
    except Exception:
        return {}
def json_encode(strs):
    """python列表或字典转成字符串"""
    try:
        return json.dumps(strs,ensure_ascii=False)
    except Exception:
        return ""
def dateoperator(date,years=0,formats='%Y%m%d%H%M%S',months=0, days=0, hours=0, minutes=0,seconds=0,
                 leapdays=0, weeks=0, microseconds=0,
                 year=None, month=None, day=None, weekday=None,
                 yearday=None, nlyearday=None,
                 hour=None, minute=None, second=None, microsecond=None):
    """日期相加减计算
    date 2019-10-10
    formats 设置需要返回的时间格式 默认%Y%m%d%H%M%S
    
    years 大于0表示加年  反之减年
    months 大于0表示加月  反之减月
    days 大于0表示加日  反之减日

    return %Y%m%d%H%M%S
    """
    formatss='%Y%m%d%H%M%S'
    date=re.sub('[-年/月:：日 时分秒]','',date)
    if len(date) < 8:
        return None
    if len(date) < 14:
        s=14-len(date)
        i=0
        while i < s:
            date=date+"0"
            i=i+1
    d = core_datetime.datetime.strptime(date, formatss)
    strs=(d + core_relativedelta(years=years,months=months, days=days, hours=hours, minutes=minutes,seconds=seconds,
                 leapdays=leapdays, weeks=weeks, microseconds=microseconds,
                 year=year, month=month, day=day, weekday=weekday,
                 yearday=yearday, nlyearday=nlyearday,
                 hour=hour, minute=minute, second=second, microsecond=microsecond))
    strs=strs.strftime(formats)
    return strs
def get_folder():
    '获取当前框架目录'
    return os.path.split(os.path.realpath(__file__))[0][:-7] #当前框架目录
# aa=[]
def get_file(folder='./',is_folder=True,suffix="*",lists=[],append=False):
    """获取文件夹下所有文件夹和文件

    folder 要获取的文件夹路径

    is_folder  是否返回列表中包含文件夹

    suffix 获取指定后缀名的文件 默认全部
    """
    if not append:
        lists=[]
    lis=os.listdir(folder)
    for files in lis:
        if not os.path.isfile(folder+"/"+files):
            if is_folder:
                zd={"type":"folder","path":folder+"/"+files,'name':files}
                lists.append(zd)
            get_file(folder+"/"+files,is_folder,suffix,lists,append=True)
        else:
            if suffix=='*':
                zd={"type":"file","path":folder+"/"+files,'name':files}
                lists.append(zd)
            else:
                if files[-(len(suffix)+1):]=='.'+str(suffix):
                    zd={"type":"file","path":folder+"/"+files,'name':files}
                    lists.append(zd)
    return lists

def list_to_tree(data, pk = 'id', pid = 'pid', child = 'lowerlist', root=0,childstatus=True):
    """列表转换tree
    
    data 要转换的列表

    pk 关联节点字段

    pid 父节点字段

    lowerlist 子节点列表

    root 主节点值

    childstatus 当子节点列表为空时是否需要显示子节点字段
    """
    arr = []
    for v in data:
        if v[pid] == root:
            kkkk=list_to_tree(data,pk,pid,child,v[pk],childstatus)
            if childstatus:
                # print(kkkk)
                v[child]=kkkk
            else:
                if kkkk:
                    v[child]=kkkk
            arr.append(v)
    return arr
class zip:
    def packzip(dirname,zipfilename):
        filelist = []
        if os.path.isfile(dirname):
            filelist.append(dirname)
        for root, dirs, files in os.walk(dirname):
            for name in files:
                filelist.append(os.path.join(root, name))
        zf = zipfile.ZipFile(zipfilename, "w", zipfile.zlib.DEFLATED)
        for tar in filelist:
            arcname = tar[len(dirname):]
            #print arcname
            zf.write(tar,arcname)
        zf.close()
    def unzip_file(zipfilename, unziptodir):
        zf = zipfile.ZipFile(zipfilename)
        zf.extractall(unziptodir)
        zf.close()
class create:
    appname=None
    modular=None
    path=get_folder() #当前框架目录
    def __init__(self,appname="app",modular="api"):
        self.appname=str(appname)
        self.modular=str(modular)
    def uninstallplug(self,plug):
        """卸载插件

        plug 插件名
        """
        f=open(self.appname+"/"+self.modular+"/controller/__init__.py","r",encoding='utf-8')
        text=f.read()
        f.close()
        f=open(self.appname+"/"+self.modular+"/controller/__init__.py","w",encoding='utf-8')
        text=re.sub("from . import "+plug,"",text)
        f.write(text)
        f.close()
        shutil.rmtree(self.appname+"/"+self.modular+"/controller/"+plug)
        return True
    def packplug(self,plug):
        """打包插件
        
        plug 插件名
        """
        """打包模块"""
        if os.path.exists(self.appname+"/"+self.modular+"/controller/"+plug):
            zip.packzip(self.appname+"/"+self.modular+"/controller/"+plug,self.appname+"/"+self.modular+"/controller/"+plug+".zip")
            return True
        else:
            return False
    def installplug(self,plug):
        """创建一个插件，如果您的模块目录下没有插件包，则创建默认插件文件
        
        plug 插件名
        """
        plug=str(plug)
        if os.path.exists(self.appname+"/"+self.modular+"/controller/"+plug):
            raise Exception("该插件已存在")
        else:
            if os.path.isfile(self.appname+"/"+self.modular+"/controller/"+plug+".zip"):#安装打包好的插件
                zip.unzip_file(self.appname+"/"+self.modular+"/controller/"+plug+".zip",self.appname+"/"+self.modular+"/controller/"+plug+"/")
                os.remove(self.appname+"/"+self.modular+"/controller/"+plug+".zip")
            else:#安装默认插件
                if not os.path.exists(self.appname+"/"+self.modular+"/controller/"+plug):
                    os.makedirs(self.appname+"/"+self.modular+"/controller/"+plug)
                content=Templates(self.path+"/application/api/controller/plug/__init__.py",appname=self.appname,modular=self.modular)
                f=open(self.appname+"/"+self.modular+"/controller/"+plug+"/__init__.py","a",encoding='utf-8')
                f.write(content)
                f.close()
                content=Templates(self.path+"/application/api/controller/plug/index.py",appname=self.appname,modular=self.modular)
                f=open(self.appname+"/"+self.modular+"/controller/"+plug+"/index.py","a",encoding='utf-8')
                f.write(content)
                f.close()
            content="\nfrom . import "+plug
            f=open(self.appname+"/"+self.modular+"/controller/__init__.py","a",encoding='utf-8')
            f.write(content)
            f.close()
            return True
    def uninstallmodular(self):
        "卸载模块"
        f=open(self.appname+"/__init__.py","r")
        text=f.read()
        f.close()
        f=open(self.appname+"/__init__.py","w")
        text=re.sub("from . import "+self.modular,"",text)
        f.write(text)
        f.close()
        shutil.rmtree(self.appname+"/"+self.modular)
        return True
    def packmodular(self):
        """打包模块"""
        if os.path.exists(self.appname+"/"+self.modular):
            zip.packzip(self.appname+"/"+self.modular,self.appname+"/"+self.modular+".zip")
            return True
        else:
            return False
    def installmodular(self):
        "创建模块，如果应用不存，则创建默认应用，如果在您的应用目录下没有模块包，则创建默认模块文件"
        if not os.path.exists(self.appname):
            os.makedirs(self.appname)
        else:
            if not os.path.isfile(self.appname+"/__init__.py") or not os.path.exists(self.appname+"/common"):
                raise Exception(self.appname+"不是kcweb应用")
        if not os.path.exists(self.appname+"/common"):
            os.makedirs(self.appname+"/common")
            f=open(self.appname+"/common/__init__.py","w+",encoding='utf-8')
            content=Templates(self.path+"/application/common/__init__.py",appname=self.appname,modular=self.modular)
            f.write(content)
            f.close()
            f=open(self.appname+"/common/autoload.py","w+",encoding='utf-8')
            content=Templates(self.path+"/application/common/autoload.py",appname=self.appname,modular=self.modular)
            f.write(content)
            f.close()
        if not os.path.exists(self.appname+"/config"):
            os.makedirs(self.appname+"/config")
            f=open(self.appname+"/config/__init__.py","w+",encoding='utf-8')
            content=Templates(self.path+"/application/config/__init__.py",appname=self.appname,modular=self.modular)
            f.write(content)
            f.close()
            f=open(self.appname+"/config/other.py","w+",encoding='utf-8')
            content=Templates(self.path+"/application/config/other.py",appname=self.appname,modular=self.modular)
            f.write(content)
            f.close()
        if os.path.exists(self.appname+"/"+self.modular):
            raise Exception(self.appname+"/"+self.modular+"已存在")
        else:
            if os.path.isfile(self.appname+"/"+self.modular+".zip"):#安装打包好的模块
                zip.unzip_file(self.appname+"/"+self.modular+".zip",self.appname+"/"+self.modular+"/")
                os.remove(self.appname+"/"+self.modular+".zip")
            else:
                os.makedirs(self.appname+"/"+self.modular)#创建模块
                self.__zxmodular("")
        
            if os.path.isfile(self.appname+"/__init__.py"):
                content="\nfrom . import "+self.modular
            else:
                #在应用目录下创建初始化文件
                lists=os.listdir(self.appname)
                modulars=[]
                filters=['__init__','__pycache__','common','config','runtime','log']
                for files in lists:
                    if not os.path.isfile(self.appname+"/"+files):
                        if files not in filters:
                            modulars.append(files)
                content=Templates(self.path+"/application/__init__.py",appname=self.appname,tuple_modular=modulars)
                if "Windows" in platform.platform():
                    pythonname="python"
                else:
                    pythonname="python3"
                sys.argv[0]=re.sub('.py','',sys.argv[0])
                content=('# #gunicorn -b 0.0.0.0:39010 '+self.appname+':app\n'+
                        'from kcweb import web\n'+
                        'import '+self.appname+' as application\n'+
                        'from '+self.appname+'.common import *\n'+
                        'app=web(__name__,application)\n'+
                        'if __name__ == "__main__":\n'+
                        '    #host监听ip port端口 name python解释器名字 (windows一般是python  linux一般是python3)\n'+
                        '    app.run(host="0.0.0.0",port="39001",name="'+pythonname+'")')
                f=open("./"+sys.argv[0]+".py","w+",encoding='utf-8')
                f.write(content)
                f.close()
            f=open(self.appname+"/__init__.py","a",encoding='utf-8')
            f.write(content)
            f.close()
            return True
    def __zxmodular(self,sourcep):
        "处理模块文件"
        path1=self.path+"/application/api"+sourcep
        path2=self.appname+"/"+self.modular+sourcep
        lists=os.listdir(path1)
        for files in lists:
            if os.path.isfile(path1+"/"+files):
                if ".py" in files:
                    content=Templates(path1+"/"+files,appname=self.appname,modular=self.modular)
                    f=open(path2+"/"+files,"w+",encoding='utf-8')
                    f.write(content)
                    f.close()
                else:
                    f=open(path1+"/"+files,"r",encoding='utf-8')
                    content=f.read()
                    f.close()
                    f=open(path2+"/"+files,"w+",encoding='utf-8')
                    f.write(content)
                    f.close()
            elif files != '__pycache__':
                if not os.path.exists(path2+"/"+files):
                    os.makedirs(path2+"/"+files)
                self.__zxmodular(sourcep+"/"+files)