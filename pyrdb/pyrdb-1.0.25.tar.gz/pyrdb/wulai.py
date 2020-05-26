import pyrda.sqlserver as sqlserver
import pyrdo.tuple as rdtpl
import pyrdo.array as rdarr
import pyrdo.list as rdlist


# test for function notation
def helloworld(txt: dict(type=str, help='input text')):
    print(txt)
# 增加日志功能
def db_add_log(conn,app_id,obj_id,desc_txt):
    sql = "insert into t_km_log (Fapp_id,Fobj_id,FdescTxt)values('%s','%s','%s')" % (app_id,obj_id,desc_txt)
    sqlserver.sql_insert(conn,sql)
#判断是否为一个新的知识库
def db_is_new_aibot(conn,app_id):
    sql = "select * from t_km_kc where Fapp_id ='%s' and Fid = '0'" % (app_id)
    data = sqlserver.sql_select(conn,sql)
    ncount = len(data)
    if ncount > 0:
        res = False
    else:
        res = True
    return res



def db_is_new_user(conn,app_id,user_name):
    sql = "select Fuser_name from t_km_user where Fapp_id = '%s' and Fuser_name = '%s'" % (app_id,user_name)
    data = sqlserver.sql_select(conn,sql)
    ncount = len(data)
    if ncount > 0:
        res = False
    else:
        res = True
    return res

# 向数据库中插入数据
def db_insert_user(conn,app_id,user_name,user_id,avatar_url):
    # 执行插入新增
    sql = "insert into t_km_user (Fapp_id,Fuser_name,Fuser_id,Favatar_url) values('%s','%s','%s','%s')" % (app_id,user_name,user_id,avatar_url)
    sqlserver.sql_insert(conn,sql)
    info = '用户' + user_name +'已创建'
    # 写入日志
    db_add_log(conn= conn,app_id=app_id,obj_id='t_km_user',desc_txt=info)

# 查询用户
def db_select_user(conn,app_id,user_name):
    sql = "select Fuser_name,Fuser_id,Favatar_url  from t_km_user where Fapp_id = '%s' and Fuser_name = '%s'" % (app_id, user_name)
    data = sqlserver.sql_select(conn, sql)
    res = rdarr.array_tupleItem_as_list(data)
    return res
#获取用户id
def db_get_userId(conn,app_id,user_name):
    sql = "select Fuser_id from t_km_user where Fapp_id = '%s' and Fuser_name = '%s'" % (app_id, user_name)
    data = sqlserver.sql_select(conn, sql)
    ncount = len(data)
    if ncount >0 :
        user_id = data[0][0]
    else:
        user_id = False
    return user_id
#备份待删除用户
def db_bak_user(conn,app_id,user_name):
    sql = "insert into t_km_userDel select *from t_km_user where Fapp_id = '%s' and Fuser_name = '%s'" % (app_id,user_name)
    sqlserver.sql_insert(conn,sql)
# 删除用户
def db_delete_user(conn,app_id,user_name):
    #删除要删除的用户
    db_bak_user(conn,app_id,user_name)
    #执行删除
    sql = "delete  from t_km_user where Fapp_id = '%s' and Fuser_name = '%s'" % (app_id, user_name)
    sqlserver.sql_delete(conn,sql)
    #写入日志
    info = '删除用户' + user_name
    db_add_log(conn=conn,app_id=app_id,obj_id='t_km_user',desc_txt=info)
#################################################################################
# 知识分类更新
#
#
#
#
##################################################################################
# initial knowledge category in database
def initial_kc(conn, app_id: dict(type=str, help="the name of km app") = 'caas'):
    data = (app_id, '0', 'root', '-1', 0)
    sql = "insert into t_km_kc values('%s','%s','%s','%s',%s)" % data
    sqlserver.sql_insert(conn, sql)


def insert_kc(conn, data):
    sql = "insert into t_km_kc values('%s','%s','%s','%s',%s)" % data
    sqlserver.sql_insert(conn, sql)


# 批量插入数据，不做是否重复判定
def insert_kc_batch(conn, arrayData):
    for i in range(len(arrayData)):
        item = arrayData[i]
        data = rdtpl.list_as_tuple(item)
        insert_kc(conn, data)


def select_kc(conn, app_id):
    sql = "select * from t_km_kc where Fapp_id = '%s' " % app_id
    res = sqlserver.sql_select(conn, sql)
    # convert data from sql into array data
    res = rdarr.array_tupleItem_as_list(res)
    # print(sql)
    # print(res)
    return (res)


def upload_kc(conn, app_id, arrayData, id_index):
    old_data = select_kc(conn, app_id)
    new_data = arrayData
    diff_data = rdarr.array_diff(old_data, new_data, id_index)
    if len(diff_data) > 0:
        insert_kc_batch(conn, diff_data)
        res = True
    else:
        res = False
    return res
# 显示所有Fflag = 0 的列表
def kc_unSearched(conn,app_id):
    sql = "select Fid from t_km_kc where Fapp_id = '%s' and Fflag = 0" % app_id
    print(sql)
    res = sqlserver.sql_select(conn,sql)
    res = rdarr.array_tupleItem_as_list(res)
    data = []
    for i in range(len(res)):
        item = res[i][0]
        data.append(item)
    return(data)
# 设置知识分类已更新
def kc_updated(conn,app_id,fid):
    sql = "update a  set Fflag = 1 from t_km_kc a where Fapp_id = '%s' and Fid = '%s' and  Fflag = 0" % (app_id,fid)
    sqlserver.sql_update(conn,sql)
    # print(sql)
def kc_del(conn,app_id,fid):
    #备份数据
    sql1 = "insert into t_km_kcDel select * from t_km_kc where Fapp_id ='%s' and Fid='%s'" % (app_id,fid)
    sqlserver.sql_exec(conn,sql1)
    #执行删除
    sql2 = "delete  from t_km_kc where Fapp_id ='%s' and Fid='%s'" % (app_id,fid)
    sqlserver.sql_delete(conn,sql2)
    #记录日志
    info = '知识分类已删除' + fid
    db_add_log(conn=conn,app_id=app_id,obj_id='t_km_kc',desc_txt=info)
# 根据知识分类的名称进行删除
def kc_del_byName(conn,app_id,kc_name):
    #备份数据
    sql1 = "insert into t_km_kcDel select * from t_km_kc where Fapp_id ='%s' and Fname='%s'" % (app_id,kc_name)
    sqlserver.sql_exec(conn,sql1)
    #执行删除
    sql2 = "delete  from t_km_kc where Fapp_id ='%s' and Fname='%s'" % (app_id,kc_name)
    sqlserver.sql_delete(conn,sql2)
    #记录日志
    info = '知识分类已删除' + kc_name
    db_add_log(conn=conn,app_id=app_id,obj_id='t_km_kc',desc_txt=info)
#更新知识分类
def db_kc_update(conn,app_id,old_kc_name,new_kc_name):
    sql = "update a set Fname = '%s' from t_km_kc  a where Fapp_id ='%s' and Fname ='%s'" % (new_kc_name,app_id,old_kc_name)
    data = sqlserver.sql_update(conn,sql)
    #写入日志
    info = "知识分类从" + old_kc_name + "变更为" + new_kc_name
    # 更新数据库
    db_add_log(conn, app_id, obj_id='t_km_kc', desc_txt=info)
def db_kc_getId(conn,app_id,kc_name):
    sql = "select Fid from t_km_kc where Fapp_id ='%s' and Fname ='%s'" % (app_id,kc_name)
    print(sql)
    res = sqlserver.sql_select(conn,sql)
    ncount =len(res)
    if ncount >0 :
        kc_id = res[0][0]
    else:
        kc_id = "-1"
    return kc_id
#查询名称
def db_kc_getName(conn,app_id,kc_id):
    sql = "select  Fname from t_km_kc where Fapp_id ='%s' and Fid='%s'" % (app_id,kc_id)
    data = sqlserver.sql_select(conn,sql)
    ncount = len(data)
    if ncount > 0:
        res = data[0][0]
    else:
        res = "error"
    return res
#查询上级ID
def db_kc_getParentId(conn,app_id,kc_name):
    sql = "select  FparentId  from t_km_kc where Fapp_id ='%s' and Fname = '%s'" % (app_id,kc_name)
    data = sqlserver.sql_select(conn,sql)
    ncount = len(data)
    if ncount > 0:
        res = data[0][0]
    else:
        res = "error"
    return res
#查询上级分类名称
def db_kc_getParentName(conn,app_id,kc_name):
    parent_id = db_kc_getParentId(conn,app_id,kc_name)
    res = db_kc_getName(conn,app_id,parent_id)
    return res
#############################################################################
# 知识点更新
#
#
#
#
#############################################################################
#向数据库插入知识点
def db_kn_insert(conn,data):
    sql = "insert into t_km_kn (Fapp_id,Fkc_id,Fkc_name,Fkn_id,Fkn_name) values('%s','%s','%s','%s','%s')" % data
    sqlserver.sql_insert(conn,sql)

#检验知识点是否已经存在
def db_is_kn_new(conn,app_id,kn_name):
    sql = "select Fkn_name from t_km_kn where Fapp_id = '%s' and Fkn_name ='%s'" % (app_id,kn_name)
    data = sqlserver.sql_select(conn,sql)
    ncount = len(data)
    if ncount > 0:
        res = False
    else:
        res = True
    return res
#向数据库批量插入知识点
def db_kn_insertBatchUnique(conn,app_id,arrayData):
    for i in range(len(arrayData)):
        item = arrayData[i]
        data = rdtpl.list_as_tuple(item)
        #判断是否存在
        kn_name = data[4]
        if db_is_kn_new(conn,app_id,kn_name):
            #写入数据
            db_kn_insert(conn, data)
        else:
            pass
# 查询知识点数据
def db_kn_select(conn,app_id,kn_name):
    sql = "select Fapp_id,Fkc_id,Fkc_name,Fkn_id,Fkn_name  from t_km_kn where Fapp_id ='%s' and  Fkn_name = '%s'" % (app_id,kn_name)
    data = sqlserver.sql_select(conn,sql)
    #data = rdarr.array_tupleItem_as_list(data)
    ncount = len(data)
    if ncount >0:
        res = data[0]
    else:
        res=""
    return res
#获取知识点的ID
def db_kn_getId(conn,app_id,kn_name):
    sql = "select Fkn_id from t_km_kn where Fapp_id ='%s' and  Fkn_name = '%s'" % (app_id,kn_name)
    data = sqlserver.sql_select(conn, sql)
    # data = rdarr.array_tupleItem_as_list(data)
    ncount = len(data)
    if ncount > 0:
        res = data[0][0]
    else:
        res = ""
    return res
# 获取知识点名称
def db_kn_getName(conn,app_id,kn_id):
    sql = "select Fkn_name  from t_km_kn where Fapp_id ='%s' and   Fkn_id = '%s'" % (app_id,kn_id)
    data = sqlserver.sql_select(conn, sql)
    # data = rdarr.array_tupleItem_as_list(data)
    ncount = len(data)
    if ncount > 0:
        res = data[0][0]
    else:
        res = ""
    return res
#删除知识点
def db_kn_delete(conn,app_id,kn_name):
    #针对删除数据进行备份
    sql_bak = "insert into t_km_knDel select * from t_km_kn where Fapp_id ='%s' and Fkn_name ='%s'" % (app_id,kn_name)
    sqlserver.sql_insert(conn,sql_bak)
    #删除数据
    sql_del = "delete  from t_km_kn where Fapp_id ='%s' and Fkn_name ='%s'" % (app_id,kn_name)
    sqlserver.sql_delete(conn,sql_del)
    #写入日志
    info = "知识点" + kn_name + "删除成功"
    db_add_log(conn=conn,app_id=app_id,obj_id="t_km_kn",desc_txt=info)
#更新知识点
def db_kn_update(conn,app_id,old_kn_name,new_kn_name):
    # 备份旧的数据
    sql_bak = "insert into t_km_knDel select * from t_km_kn where Fapp_id ='%s' and Fkn_name ='%s'" % (app_id, old_kn_name)
    sqlserver.sql_insert(conn, sql_bak)
    # 更新新的数据
    sql_update = "update a set Fkn_name = '%s'  from t_km_kn  a where Fapp_id ='%s' and Fkn_name ='%s'" % (new_kn_name,app_id,old_kn_name)
    sqlserver.sql_update(conn,sql_update)
    # 写入操作日志
    info = "知识点从" + old_kn_name +"变更为" + new_kn_name
    db_add_log(conn=conn,app_id=app_id,obj_id='t_km_kn',desc_txt=info)
##################################################################################
# db for knowledge leaf
#
#
#
#
################################################################################
#插入相似问
def db_kl_insert(conn,app_id,data):
    sql = "insert into t_km_kl (Fapp_id,Fkn_id,Fkn_name,Fkl_id,Fkl_name) values('%s','%s','%s','%s','%s')" % data
    sqlserver.sql_insert(conn,sql)
#判断是否是一个知识点的新的相似问
def db_is_kl_new(conn,app_id,kn_name,kl_name):
    sql = "select  Fkl_id from t_km_kl where Fapp_id='caasb' and Fkn_name ='kntest' and Fkl_name='kltest'" % (app_id,kn_name,kl_name)
    data = sqlserver.sql_select(conn,sql)
    ncount = len(data)
    if ncount >0:
        res = False
    else:
        res = True
    return res
#批量插入相似问
def db_kl_insertBatchUnique(conn,app_id,arrayData):
    for i in range(len(arrayData)):
        item = arrayData[i]
        data = rdtpl.list_as_tuple(item)
        #判断是否存在
        kn_name = data[2]
        kl_name = data[4]
        if db_is_kl_new(conn,app_id,kn_name,kl_name):
            #写入数据
            db_kl_insert(conn,app_id,data)
        else:
            pass









if __name__ == '__main__':
    helloworld('hawken')
    print(helloworld.__annotations__)
    # 初始化数据知识分类数据
    conn = sqlserver.conn_create("115.159.201.178", "sa", "Hoolilay889@", "rdbe")
    app_id = "caasb"
    #initial_kc(conn,app_id)
    # vinitial_kc(conn,app_id)
    # 测试分类数据上传
    #mydata = [['caas', '71688', '网商_test', '0', 0]]
    # insert_kc_batch(conn,mydata)
    # 测试查询
    # kc_query = select_kc(conn, 'caas')
    # print(kc_query)
    # print测试上传功能
    #up = upload_kc(conn,'caas',mydata,1)
    #print(up)
    # 处理字段查看
    #bbc = kc_unSearched(conn,'caas')
    #print(bbc)


    # 查看字段更新
    # kc_updated(conn,'caas','71688')
    # 删除字段
    #kc_del(conn,'caas','707150')
    print(db_is_new_user(conn,app_id,'test'))
    print(db_is_new_user(conn,app_id,'test2'))
    #db_insert_user(conn,app_id,'test3','1234','http://www.baidu.com/logo.jpg')
    print(db_select_user(conn,app_id,'test2'))
    #删除用户
    #db_delete_user(conn,app_id,'test3')
    #print(db_get_userId(conn,app_id,'test'))
    #print(db_kc_getId(conn,app_id,'发现_活动'))
    #print(db_kc_getName(conn,app_id,'730775'))
    #print(db_kc_getParentName(conn,app_id,'通用'))
    #print(db_kc_getId(conn, app_id, 'rdtest2'))
    #kn_data=('caasb','145','bbc','132','fdsb')
    #db_kn_insert(conn,kn_data)
    #print(db_kn_select(conn,app_id,'fdsb'))
    #print(db_is_kn_new(conn, app_id, 'sample2'))
    sqlserver.conn_close(conn)