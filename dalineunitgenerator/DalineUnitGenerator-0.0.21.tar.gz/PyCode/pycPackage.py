import py_compile
import shutil
py_compile.compile('__init__.py',r'.\pyc\Animal.pyc' )
py_compile.compile('Animal.py',r'.\pyc\Animal.pyc' )
py_compile.compile('Cat.py',r'.\pyc\Cat.pyc' )
# import compileall
# compileall.compile_dir(r'E:\Code\PythonTB')