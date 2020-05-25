import datetime

import pymongo
import pymysql
from bson import ObjectId
from flask import Flask, g, request, session
from flask_cors import CORS
from mongoengine import connect

from ForMark.ForLog import ForLog
from ForMark.ForPath import get_root_path
from ForMark.flask_session import Session
import os

from ForMark.model.foot import Foot
from ForMark.model.session import Session as SessionDB

# 1.1.17
pymysql.install_as_MySQLdb()


class ForApp():
    def __init__(self, import_name, MONGO_HOST_URL, secret_key,
                 log_folder=None, root_path=None,
                 need_before_request=True,
                 need_after_request=True,
                 page_size=10
                 ):
        self.import_name = import_name
        self.log_folder = log_folder

        if root_path is None:
            root_path = get_root_path(self.import_name)

        self.root_path = root_path
        # 初始化日志
        ForLog(os.path.join(self.root_path, log_folder))

        app = Flask(__name__)
        CORS(app, supports_credentials=True)  # 设置跨域
        # json支持中文显示
        app.config['JSON_AS_ASCII'] = False
        app.secret_key = secret_key
        app.config['MONGO_HOST_URL'] = 'MONGO_HOST_URL'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(days=7)

        # 设置默认session过期时间
        app.config['SESSION_TYPE'] = 'mongodb'
        app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(days=7)
        app.config[' SESSION_MONGODB'] = pymongo.MongoClient(MONGO_HOST_URL)
        app.config['SESSION_PERMANENT'] = True
        # 是否对发送到浏览器上session的cookie值进行加密
        app.config['SESSION_USE_SIGNER'] = False
        app.config['SESSION_KEY_PREFIX'] = 'eic_session:'  # 保存到session中的值的前缀
        app.config['SESSION_MONGODB_DB'] = SessionDB

        Session(app)

        if need_before_request:
            @app.before_request
            def before_request():
                g.request_start_time = datetime.datetime.now()
                ForLog.show("g.request_start_time", g.request_start_time)
                # request.json 只能够接受方法为POST、Body为raw，header 内容为 application/json类型的数据：
                # print(request.json if request.method == "POST" else request.args)
                # params = request.json if request.method.upper() in [
                #     "POST", "PUT"] else request.args
                # if params is None and request.method == 'POST' and request.files:
                #     params = request.form
                params = {}
                if request.args:
                    params.update(request.args.to_dict(flat=True))
                if request.is_json and request.get_data() and request.json:
                    if type(request.json) == type([]):
                        for x in request.json:
                            params.update(x)
                    else:
                        params.update(request.json)
                if request.form:
                    params.update(request.form.to_dict(flat=True))
                g.params = params
                ip = request.remote_addr
                # print("请求头",request.headers)
                try:
                    _ip = request.headers["X-Real-IP"]
                    if _ip is not None:
                        ip = _ip
                except Exception as e:
                    pass
                g.ip = ip
                g.error = False

                g.current_device = params.get('current_device', '')
                # 当前第几页
                page = params.get('page', '0')
                g.page = int(page) if page else 0
                # 每页面默认取出数量：20
                g.page_size = int(params.get('page_size', page_size))
                # 为了防止过分访问，限制最大50
                g.page_size = 20 if g.page_size < 1 or g.page_size > 50 else g.page_size
                g.page = 0 if g.page < 0 else g.page
        if need_after_request:
            @app.after_request
            def after_request(response):
                foot = Foot()
                # 访问用户ID
                user_id = session.get('user_id', None)
                if user_id:
                    foot.user_id = ObjectId(user_id)
                # 请求url
                foot.url = request.url
                # 请求原网址
                foot.referrer = request.referrer
                # IP
                foot.ip = g.ip

                # 请求开始时间：
                foot.request_start_time = g.request_start_time
                # 请求结束时间：
                foot.request_end_time = datetime.datetime.now()
                foot.cookies = request.cookies
                ForLog.show("请求的cookies", request.cookies)
                ForLog.show("请求的cookies type", type(request.cookies))
                headers_before = request.headers
                if headers_before:
                    headers = {}
                    for key, value in headers_before.to_wsgi_list():
                        headers[key] = value
                    foot.headers = headers

                # 请求方式
                foot.method = request.method
                # 错误异常
                foot.error = str(g.error) if g.error else None
                foot.save()
                return response

        @app.teardown_request
        def teardown_request(error):
            g.error = error

        ForLog.show("连接mongodb数据库", MONGO_HOST_URL)
        connect(host=MONGO_HOST_URL)
        self.app = app
