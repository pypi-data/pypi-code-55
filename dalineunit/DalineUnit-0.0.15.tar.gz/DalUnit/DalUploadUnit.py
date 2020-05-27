import click
import json

runscript = '''
import click
from concurrent import futures
import grpc
import puwrapper_pb2
import puwrapper_pb2_grpc
from %s import %s

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
    pcu = %s() 
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
    puwrapper_pb2_grpc.add_PURequestServicer_to_server(
        %s(), server)
    server.add_insecure_port("[::]:{}".format(port))
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
'''

@click.command()
@click.option('--folder', help='target folder')
def run(folder):
    #read in unit info
    dicInfo={}
    if folder is None:
        print('Folder should be set, use --help see help!')
        return
    infoF = folder+'\\info.json'
    file_info = open(infoF, 'r')
    # content = file_info.read()    
    # print(file_info)
    dicInfo = json.load(file_info)
    file_info.close()    
    if 'name' not in dicInfo:
        print('Info.json format wrong, no name field found!')
        return    
    #write runscript
    name = dicInfo['name']
    scriptF = folder+'\\run.py'
    file_script = open(scriptF, 'w')
    file_script.write(runscript%(name,name,name,name))
    file_script.close( )


if __name__ == '__main__':
    run()
