import py_compile
import shutil
py_compile.compile('DalBaseUnit.py',r'.\__pycache__\runDep\DalBaseUnit.pyc' )
py_compile.compile('OracleOper.py',r'.\__pycache__\runDep\OracleOper.pyc')
py_compile.compile('puwrapper_pb2.py',r'.\__pycache__\runDep\puwrapper_pb2.pyc')
py_compile.compile('puwrapper_pb2_grpc.py',r'.\__pycache__\runDep\puwrapper_pb2_grpc.pyc')
shutil.copyfile('requirements.txt',r'.\__pycache__\runDep\requirements.txt')

py_compile.compile('OracleOper.py','.\__pycache__\genDep\OracleOper.pyc')
py_compile.compile('Template.py','.\__pycache__\genDep\Template.pyc')
py_compile.compile('DalDecorate.py','.\__pycache__\genDep\DalDecorate.pyc')
py_compile.compile('DalGenScript.py','.\__pycache__\genDep\DalGenScript.pyc')
py_compile.compile('DesignFile.py','.\__pycache__\genDep\DesignFile.pyc')
py_compile.compile('GenTestData.py','.\__pycache__\genDep\GenTestData.pyc')
shutil.copyfile('requirements.txt',r'.\__pycache__\genDep\requirements.txt')

py_compile.compile('DalBaseUnit.py',r'DalineUnit\DalBaseUnit.pyc' )
py_compile.compile('OracleOper.py',r'DalineUnit\OracleOper.pyc')
py_compile.compile('puwrapper_pb2.py',r'DalineUnit\puwrapper_pb2.pyc')
py_compile.compile('puwrapper_pb2_grpc.py',r'DalineUnit\puwrapper_pb2_grpc.pyc')
py_compile.compile('OracleOper.py',r'DalineUnit\OracleOper.pyc')
py_compile.compile('Template.py',r'DalineUnit\Template.pyc')
py_compile.compile('DalDecorate.py',r'DalineUnit\DalDecorate.pyc')
py_compile.compile('DalGenScript.py',r'DalineUnit\DalGenScript.pyc')
py_compile.compile('DesignFile.py',r'DalineUnit\DesignFile.pyc')
py_compile.compile('GenTestData.py',r'DalineUnit\GenTestData.pyc')

# import compileall
# compileall.compile_dir(r'E:\Code\PythonTB')