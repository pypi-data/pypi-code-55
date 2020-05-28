import py_compile
import shutil
py_compile.compile('__init__.py',r'.\pyc\__init__.pyc' )
py_compile.compile('Animal.py',r'.\pyc\Animal.pyc' )
py_compile.compile('Cat.py',r'.\pyc\Cat.pyc' )
shutil.copyfile(r'.\pyc\Cat.pyc','..\CodePackage\Cat.pyc')
shutil.copyfile(r'.\pyc\Animal.pyc','..\CodePackage\Animal.pyc')

# import compileall
# compileall.compile_dir(r'E:\Code\PythonTB')