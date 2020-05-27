import py_compile
import shutil
py_compile.compile('__init__.py',r'.\CodePackage\__init__.pyc' )
py_compile.compile('Animal.py',r'.\CodePackage\Animal.pyc' )
py_compile.compile('Cat.py',r'.\CodePackage\Cat.pyc' )
# import compileall
# compileall.compile_dir(r'E:\Code\PythonTB')