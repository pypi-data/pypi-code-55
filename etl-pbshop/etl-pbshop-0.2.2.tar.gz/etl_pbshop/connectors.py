import os
import pickle
from pandas import DataFrame
import json
from urllib.request import Request, urlopen
from base64 import b64encode
from urllib.parse import quote_plus
from urllib.error import HTTPError, URLError
import requests
from datetime import datetime
import sqlite3
from io import StringIO
import warnings

from .query_model import QueryFactory

try:
    import boto3
except:
    pass

try:
    from googleapiclient.discovery import build
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request as Request_g
    import pygsheets
except:
    pass

try:
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
except:
    pass

try:
    import pyodbc
    from pyodbc import OperationalError
except:
    pass

try:
    from simple_salesforce import Salesforce
except:
    pass


class Connectors(object):
    def __init__(self, config=None, log=None, services={'mssqlapi': 'DEV'}, methods=None):
        self.log = log
        self.conn = None
        self.enc = 'utf8'
        self.config = config
        if methods is not None:
            warn = "O nome do parametro 'methods' foi alterado para 'services'."
            warnings.warn(warn, DeprecationWarning)
            self.log.error(warn)
        # Replace 'services' with env file configuration
        services = self.config.CONNECTOR_SERVICES if self.config.CONNECTOR_SERVICES else services
        if isinstance(services, dict):
            self.methods = services.keys()
            self.service_environments = services
        else:
            self.methods = services
            self.service_environments = None
        if self.config.SQLITE_DEBUG_ENABLED or "sqlite" in self.methods:
            self.config.SQLITE_DEBUG_ENABLED = True
            self.sqlite = self.get_sqlite()
        if any(x in ["aws"] for x in services):
            if 's3' in self.service_environments['aws']:
                self.s3 = boto3.client('s3')
                if self.config.REMOTE_TOKEN_FILE == 's3':
                    self.s3.download_file(self.config.AWS['BUCKET_NAME'],
                                          self.config.AWS['OBJECT_NAME'],
                                          str(self.config.TOKEN_FILE))
            if 'dynamodb' in self.service_environments['aws']:
                self.dynamodb = boto3.client('dynamodb')
        if any(x in ["salesforce"] for x in services):
            # Using: https://github.com/simple-salesforce/simple-salesforce
            creds = self.config.get_credentials_value(
                "salesforce", ["user", "pass", "token_value"],
                env_name=self.service_environments["salesforce"])
            self.salesforce_username = creds[0]
            self.salesforce_domain = 'test' if '.qa' in self.salesforce_username or '.dev' in self.salesforce_username else None
            self.salesforce_conn = Salesforce(
                username=self.salesforce_username,
                password=creds[1],
                security_token=creds[2],
                domain=self.salesforce_domain)

        if any(x in ["GSUITE", "google"] for x in services):
            # Using: https://pygsheets.readthedocs.io/en/stable/
            self.creds = self.get_credentials()
            self.service_sheets = build('sheets', 'v4', credentials=self.creds)
            self.service_drive = build('drive', 'v3', credentials=self.creds)
            try:
                self.pygsheets_gc = pygsheets.authorize(
                    client_secret=self.config.SECRETS_FILE_PYGSHEETS,
                    credentials_directory=self.config.CREDENTIALS)
            except OSError:
                from shutil import copy2
                old_credentials_path = self.config.CREDENTIALS
                self.config.CREDENTIALS = '/tmp/credentials'
                os.system(f'rm -rf {self.config.CREDENTIALS}')
                os.makedirs(self.config.CREDENTIALS, exist_ok=True)
                os.system(f'cp {old_credentials_path}/* {self.config.CREDENTIALS}')
                os.system(f'chmod -R +w {self.config.CREDENTIALS}')
                try:
                    self.config.SECRETS_FILE_PYGSHEETS = copy2(self.config.SECRETS_FILE_PYGSHEETS,
                                                               self.config.CREDENTIALS)
                except Exception as e:
                    self.log.error(f"Can't copy credentials files: {str(e)} ")
                    self.config.SECRETS_FILE_PYGSHEETS = f'{self.config.CREDENTIALS}/client_secret.json'
                self.pygsheets_gc = pygsheets.authorize(
                    client_secret=self.config.SECRETS_FILE_PYGSHEETS,
                    credentials_directory=self.config.CREDENTIALS)
        if any(x in ["ODBC"] for x in services):
            self.params = 'Driver={ODBC Driver 17 for SQL Server};' \
                          f'SERVER={os.getenv("DB_SERVER")};' \
                          f'DATABASE={os.getenv("DB_NAME")};' \
                          f'UID={os.getenv("DB_USER")};' \
                          f'PWD={os.getenv("DB_PASS")}'
            if any(x in ["PYODBC"] for x in services):
                self.mssql_cursor = self.mssql_conector()
            elif any(x in ["SQLALCHEMY"] for x in services):
                self.conn = create_engine('mssql+pyodbc:///?odbc_connect=%s' % quote_plus(self.params))
                self.Session = sessionmaker(bind=self.conn)
                self.test_odbc("")

        # if any(x in ["API", "mssqlapi"] for x in services):
        self.headers = None
        self.json_data = None
        self.url_mssql = None
        try:
            self.create_connectors_api_mssql()
        except Exception as e:
            self.log.error(f"Ocorreu um erro ao instanciar conector com MSSQL Server \n{str(e)}")

    def commit_df(self, df, name, type='sql', force=False):
        if self.config.SQLITE_DEBUG_ENABLED and (not self.config.RUNNING_ON_AZURE or (self.config.test['mode'] and not force)):
            if isinstance(df, dict):
                for k_name, v_df in df.items():
                    return self.commit_df(v_df, k_name, type, force)
            if isinstance(df, DataFrame):
                if 'sql' in type and self.config.SQLITE_DEBUG_ENABLED:
                    df.to_sql(name, con=self.sqlite, if_exists='replace', index=False)
                if 'csv' in type:
                    df.to_csv(f"{name}.csv", header=True)

    def create_connectors_api_mssql(self):
        env_name = self.service_environments.get('mssqlapi', "PROD")
        user_passwd = self.config.get_credentials_value(system_name="mssqlapi", key_name=["user", "pass"], env_name=env_name)
        env_credentials = self.config.get_credentials_value(system_name="mssqlapi", key_name=("client_id", "database_name", "method_url"), env_name=env_name)
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Basic {self.encode_token(user_passwd=user_passwd)}"
        }
        self.json_data = {
            "ClientId": env_credentials["client_id"],
            "Message": None,
            "DatabaseName": env_credentials["database_name"],
        }
        self.url_mssql = env_credentials["method_url"]

    def send_api_mssql(self, query, type_as=None, retry=4):
        self.json_data["Message"] = query

        request = Request(method="POST",
                          url=self.url_mssql,
                          headers=self.headers,
                          data=bytes(json.dumps(self.json_data), self.enc))
        try:
            resp = urlopen(request).read()
        except HTTPError as e:
            content = e.read()
            self.log.error(f"Erro {content} ao enviar query {query}")
            if retry:
                return self.send_api_mssql(query, type_as, retry=retry-1)
            else:
                return None
        else:
            response = json.loads(resp)
            if type_as == 'list_trunc':
                response = list(list(x.values())[0][1:] for x in response)
            if type_as == 'list':
                response = list(list(x.values())[0] for x in response)
            return response

    def clear_table(self, table):
        query = QueryFactory().MODEL['DROP_ALL'].format(
            table=table
        )
        response = self.send_api_mssql(query)
        self.log.info(f"Cleaning table: {response}")

    def load_mssql(self, table, data, clear=False):
        if self.config.test["insert"] and clear:
            self.clear_table(table)
        n = 0
        vals = ''
        milestone = 1000  # limite do ms sql é de 1000
        data_lenght = len(data)
        cols = "[" + "],[".join(list(data.columns)) + "]"
        for _, line in data.iterrows():
            vals += "('" + "','".join([str(x).replace("'", "") for x in line.values]) + "'), "
            if n % milestone == 0 or n >= data_lenght - 1:
                vals = vals.rsplit(', ', maxsplit=1)[0]
                query = QueryFactory().MODEL['INSERT_ALL'].format(
                    table=table,
                    column=cols,
                    values=vals
                )
                if self.config.test["insert"]:
                    response = self.send_api_mssql(query)
                    self.log.info(f"Bulk insert {n} data. Resp: {response}")
                else:
                    self.log.debug(f"Modo teste: {self.config.test['mode']} Query: {query}")
                vals = ''
            n += 1
        if not self.config.test["insert"] and self.config.SQLITE_DEBUG_ENABLED:
            self.commit_df(data, table)
            # data.to_sql(table, self.sqlite, if_exists='replace', index=False)
        self.log.info(f"Inserted {data_lenght} data.")

    def test_odbc(self, table):
        session = self.Session()
        dados = session.query(table).all()
        for e in dados:
            self.log.debug(f"Teste dados: {e}")
        return

    def get_credentials(self):
        creds = None
        if os.path.exists(self.config.TOKEN_FILE):
            with open(self.config.TOKEN_FILE, 'rb') as token:
                creds = pickle.load(token)
            # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request_g())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.config.SECRETS_FILE, self.config.SCOPES)
                creds = flow.run_local_server(port=0)
            #with open(self.config.TOKEN_FILE, 'wb') as token:
            #    pickle.dump(creds, token)
        return creds

    def mssql_conector(self):
        try:
            self.conn = pyodbc.connect(self.params)
            cursor = self.conn.cursor()
            # @TODO Criar um jeito de verificar a conexão com tabela generica
            cursor.execute('SELECT top(10) * FROM PBDWPRD.stag.REDE_PB_SHOP_LOAD')
        except OperationalError as oe:
            if 'Login timeout expired' in str(oe):
                self.log.error("Timeout")
        else:
            return cursor

    def my_request(self, headers, url, data=None, method="POST", retry=10):
        try:
            request = Request(method=method, url=str(url), data=data,  headers=headers)
            resp = urlopen(request).read()
        except HTTPError as e:
            content = e.read()
            self.log.error(f"Erro '{content}' ao enviar {data} para {url}")
            return {'access_token': ''}
        except URLError as urle:
            if retry:
                self.log.error(f"Error: {str(urle)}\nTentativa {retry}, {data} {url}")
                return self.my_request(headers, url, data, method, retry=retry-1)
            self.log.exception(f"Max Retry: {retry}, Raising Error: {str(urle)}")
            raise urle
        except Exception as e:
            self.log.exception(f"Exception: {retry}, {data} {url} \nError: {str(e)}")
            raise e
        else:
            return json.loads(resp.decode(self.enc))

    def my_request_lib2(self, headers, url, data=None, method="POST", retry=10):
        try:
            response = requests.request(method, url, headers=headers, data=data)
            resp = response.text.encode(self.enc)
        except Exception as e:
            if retry:
                self.log.error(f"Error: {str(e)}\nTentativa {retry}")
                return self.my_request_lib2(headers, url, data, method, retry=retry-1)
            self.log.exception(f"Max Retry: {retry}, {data} {url} Raising Error: {str(e)}")
            raise e
        else:
            return json.loads(resp.decode(self.enc))

    def get_token(self, path="token", token=None, token_url=None, env=None, system=None):
        if token and token_url:
            pass
        elif env and system:
            user_passwd = self.config.get_credentials_value(system, ['user', 'pass'], env)
            token = self.encode_token(user_passwd=user_passwd)
            token_url = self.config.get_credentials_value(system, 'token_url', env)
            path = f"token_{env}"
        else:
            raise Exception("Ao menos um dos parametros deve ser passado: token e token_url ou")

        generate_new_token = True
        to_return = {}
        if os.path.exists(path):
            with open(path, "r") as tk:
                data = tk.read()
            to_return = eval(data)
            now = datetime.now()
            gerado = datetime.strptime(to_return.get("gerado"), self.config.DATE_TIME_FMT)
            dif_time = (now - gerado).total_seconds()
            if dif_time < int(to_return.get("expires_in")) - 7200:
                generate_new_token = False

        if generate_new_token and token:
            headers = {
                'Content-Type': "application/x-www-form-urlencoded",
                'accept': "*/*",
                'Authorization': f"Basic {token}",
                'Cache-Control': "no-cache",
                'Host': "rest-prd.portobello.com.br",
                'Content-Length': "39",
                'Connection': "keep-alive"
            }
            data = b"grant_type=client_credentials&scope=all"

            to_return = self.my_request(headers, token_url, data=data)

            to_return['gerado'] = str(datetime.now().strftime(self.config.DATE_TIME_FMT))
            if to_return:
                with open(path, "w") as tk:
                    tk.write(str(to_return))

        return to_return.get('access_token')

    def get_data(self, id=None, param=None, token=None, url=None, data=None, system=None, env=None, lib_request_flag=None):
        if not token:
            token = self.get_token(system=system, env=env)
        if not url:
            url = self.config.get_credentials_value(system_name=system, key_name='method_url', env_name=env)
        headers = {
            "Authorization": f"Bearer {token}",
        }
        if '{}' in url and id:
            url = url.format(id)
        if param:
            url += param

        request_lib = self.my_request_lib2 if lib_request_flag == 'requests' else self.my_request

        request_ret = request_lib(headers, url, data=data, method='GET')

        pp = self.config.PAGINATION.get(system)
        next = pp['next']['name']
        while next in request_ret:
            next_url = request_ret.pop(next)
            if pp['next']['level']:
                next_url = next_url.get(pp['next']['level'])
            next_ret = request_lib(headers, next_url, data=data, method='GET')
            if pp['data']['level']:
                request_ret[pp['data']['name']][pp['data']['level']].update(
                    next_ret[pp['data']['name']][pp['data']['level']])
            else:
                request_ret[pp['data']['name']] += next_ret[pp['data']['name']]

            if next in next_ret:
                request_ret[next] = next_ret[next]
        return request_ret[pp['data']['name']]

    def get_sqlite(self, file_name=None):
        file_name = self.config.SQLITE_DEBUG_FILE if file_name is None else file_name
        conn = sqlite3.connect(file_name)
        # cur = conn.cursor()
        return conn

    @staticmethod
    def encode_token(user=None, passwd=None, user_passwd=None, dec='utf8'):
        if user_passwd is None and user and passwd:
            data = f'{user}:{passwd}'
        elif isinstance(user_passwd, (list, set, tuple)) and user is None and passwd is None:
            data = ':'.join(user_passwd)
        else:
            raise Exception("Erro: 'encode_token': Deve ser passado apenas 'user' e 'passwd' ou 'user_passwd'")
        return b64encode(bytes(data, dec)).decode(dec)

    def request_microvix_csv(self, method=None, params=dict(), system="microvix", env="prod"):
        token = self.config.get_credentials_value(system_name=system, key_name='token_value', env_name=env)
        parameters = f'<Parameter id="chave">{token}</Parameter>'
        for key, value in params.items():
            parameters += f'<Parameter id="{key}">{value}</Parameter>'

        if not method:
            self.config.get_credentials_value(system_name=system, key_name='method_url', env_name=env)

        user = self.config.get_credentials_value(system_name=system, key_name='user', env_name=env)
        passwd = self.config.get_credentials_value(system_name=system, key_name='pass', env_name=env)

        data = f"""
            <LinxMicrovix><Authentication user="{user}"  password="{passwd}"/>
                <ResponseFormat>csv</ResponseFormat>
                <Command><Name>{method}</Name><Parameters>{parameters}</Parameters></Command>
            </LinxMicrovix>"""

        headers = {
            'Content-Type': "text/xml",
            'Authorization': f"Basic {self.encode_token(user, passwd)}",
            'Cache-Control': "no-cache"
        }
        try:
            request = requests.post(self.config.get_credentials_value(system_name=system, key_name='method_url', env_name=env),
                                    data=data, headers=headers)
            resp = request.text[6:-1].encode('ISO-8859-1').decode('utf-8').replace("\'", "")
            return StringIO(resp)
        except Exception as e:
            self.log.error(f"Erro: {e}")
            raise e

    def query_salesforce(self, query, keep_attributes=False):
        response = self.salesforce_conn.query_all(query)
        if response['done']:
            response = response['records']
        filtered_response = []
        for resp in list(response):
            if isinstance(resp, dict):
                for k, v in dict(resp).items():
                    if isinstance(v, dict):
                        if k == "attributes" and not keep_attributes:
                            resp.pop(k)
                            continue
                        if v.get("attributes"):
                            v.pop("attributes")
                        resp[f"{k}.{list(v.keys())[0]}"] = list(v.values())[0]
                        resp.pop(k)
            filtered_response.append(resp)
        return response

    def load_salesforce_api_consumption(self):
        import pandas as pd

        api_usage = self.salesforce_conn.api_usage
        data_raw = {
            'usage': [api_usage['api-usage'].used],
            'total': [api_usage['api-usage'].total],
            'percentual': [float(api_usage['api-usage'].used/api_usage['api-usage'].total) * 100],
            'timestamp': [self.config.NOW[:19]],
            'username': [self.salesforce_username],
            'service': [self.config.PROJECT_NAME]
        }

        df = pd.DataFrame.from_dict(data_raw)
        self.load_mssql(self.config.SALESFORCE["api_cons"], df)

