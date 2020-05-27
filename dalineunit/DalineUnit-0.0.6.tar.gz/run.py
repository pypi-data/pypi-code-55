
import click
from concurrent import futures
import grpc
import json
import puwrapper_pb2
import puwrapper_pb2_grpc
from webfetcher import webfetcher

class DALJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, bytes):
            return str(obj, encoding='utf-8')
        return json.JSONEncoder.default(self, obj)

class RequestService(puwrapper_pb2_grpc.PURequestServicer):
    def Request(self, request, context):
        key = dict()
        key['data'] = 'web'
        key['url'] = request.strReq
        key['craw_config'] = {'headers': {'Accept-Encoding': 'gzip, deflate'}}
        # webF = WebFetcher()
        # fetchRet = webF.fetch_web(key)
        retDic = dict()
        retDic['retCode']=2
        retDic['dbCostTime']='20200514'
        retDic['strContent']='hello kitty'
        retDic['strErrorInfo']=""
        retDic['strTraceBack']=""
        # if fetchRet['status_code'] != 200:
        #     retDic['strErrorInfo']=fetchRet['error']
        #     retDic['strTraceBack']=fetchRet['traceback']
        ret = puwrapper_pb2.RequestRetMsg(strRet=json.dumps(retDic,cls=DALJsonEncoder))
        return ret

@click.command()
@click.option('--wport', default=0, help='java wrapper grpc server port')
@click.option('--port', default=0, help='python grpc server port')
def serve(wport,port):
    if wport == 0:
        print('Wport should be set!')
        return
    if port == 0:
        print('Port should be set!')
        return
    pcu = webfetcher() 
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
    puwrapper_pb2_grpc.add_PURequestServicer_to_server(
        webfetcher(), server)
        # RequestService(), server)
    server.add_insecure_port("[::]:{}".format(port))
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
#     command example:  python run.py --wport=9091 --port=9092
