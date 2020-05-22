import argparse

#Parse commandline argument
parser = argparse.ArgumentParser(description='Display python information live in browser.')
parser.add_argument('file', metavar='F', help='python file to run')
parser.add_argument('port', metavar='P', help='port num')
args = parser.parse_args()

def getFile():
    return args.file

def getPort():
    return int(args.port)
