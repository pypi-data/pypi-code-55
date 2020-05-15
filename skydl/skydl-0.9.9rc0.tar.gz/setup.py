"""
要分别在不同平台下的python3.6/3.7/3.8下打wheel包以适配mac/windows/linux多平台下的安装。
可以参考：
1.$pip3 install megengine -f https://megengine.org.cn/whl/mge.html
======
MegEngine-0.3.1-cp35-cp35m-manylinux2010_x86_64.whl
MegEngine-0.3.1-cp36-cp36m-manylinux2010_x86_64.whl
MegEngine-0.3.1-cp37-cp37m-manylinux2010_x86_64.whl
MegEngine-0.3.1-cp38-cp38-manylinux2010_x86_64.whl
MegEngine-0.3.2-cp35-cp35m-manylinux2010_x86_64.whl
MegEngine-0.3.2-cp36-cp36m-manylinux2010_x86_64.whl
MegEngine-0.3.2-cp37-cp37m-manylinux2010_x86_64.whl
MegEngine-0.3.2-cp38-cp38-manylinux2010_x86_64.whl
2.https://pypi.org/project/tensorflow/#files
3.$pip3 install -U -f setup_wheel_list.html
打包cython可以参考：https://github.com/art-vasilyev/demo-source-protect
"""
import os
# import numpy
import skydl
import codecs
import sysconfig
from setuptools import setup, find_packages, Extension
# import distutils.command.install_headers as install_headers
from setuptools.command.build_py import build_py as _build_py
from Cython.Build import cythonize

################
# package_data = []
# header = package_data
# class InstallHeaders(install_headers):
#     """Use custom header installer because the default one flattens subdirectories"""
#     def run(self):
#         if not self.distribution.headers:
#             return
#         for header in self.distribution.headers:
#             subdir = os.path.dirname(os.path.relpath(header, '../include/pybind11'))
#             print(f"---------------------------------self.install_dir={self.install_dir}")
#             install_dir = os.path.join(self.install_dir, subdir)
#             self.mkpath(install_dir)
#             (out, _) = self.copy_file(header, install_dir)
#             self.outfiles.append(out)
# noinspection PyPep8Naming
class build_py(_build_py):
    def find_package_modules(self, package, package_dir):
        # ext_suffix在macosx下的值: '.cpython-36m-darwin.so'
        ext_suffix = sysconfig.get_config_var('EXT_SUFFIX')
        modules=super().find_package_modules(package, package_dir)
        filtered_modules=[]
        for (pkg, mod, filepath) in modules:
            if os.path.exists(filepath.replace('.py', ext_suffix)):
                continue
            filtered_modules.append((pkg, mod, filepath,))
        return filtered_modules
###############
EXCLUDE_PYX_FILES = [
    # "skydl/cython/examples/demo/cdemo.pyx",
    # "skydl/cython/examples/mcpp/test/container_unit_tests.pyx"
]
def get_ext_paths(root_dir, exclude_files):
    """get .py filepaths for compilation"""
    paths = []
    for root, dirs, files in os.walk(root_dir):
        for filename in files:
            # print(f"os.path.splitext(filename)={os.path.splitext(filename)}") # e.g. ('adapter', '.pyx')
            if os.path.splitext(filename)[1] != '.pyx' and os.path.splitext(filename)[1] != '.cc':  # pybind11只编译cython文件，如:adapter.pyx文件
                continue
            file_path = os.path.join(root, filename)  # e.g. file_path: "skydl/cython/examples/cdemo.pyx"
            if file_path in exclude_files:
                continue
            paths.append(file_path)
    print(f"setup.py......get_ext_paths={paths}")
    return paths
###############
with open("README.md") as f:
    readme = f.read()

def read(fname):
    return codecs.open(os.path.join(os.path.dirname(__file__), fname)).read()

def read_install_requires():
    with open('requirements.txt', 'r') as f:
        res = f.readlines()
    res = list(map(lambda s: s.replace('\n', ''), res))
    return res
# build python
setup(
    name="skydl",
    version=skydl.__version__,
    description="",
    long_description=readme,
    install_requires=read_install_requires(),
    #setup_requires=["setuptools>=46.1.3", "wheel>=0.34.2", "cython>=3.0a1"], # very slow under python3.8
    author="tony",
    author_email="",
    license="BSD",
    url="",
    keywords=['robot', 'ai', 'reinforcement learning', 'machine learning', 'RL',
              'ML', 'tensorflow', 'pytorch', 'ray', 'skydl', 'high efficiency', 'deep learning'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Framework :: Robot Framework :: Library',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8'],
    packages=find_packages(exclude=[]),
    package_data={'': []},
    ext_modules=cythonize(
        [Extension(name=pyx_path.replace("/",".").replace(".cc",""),
                   language="c++",
                   sources=[pyx_path],
                   extra_compile_args=['-Wno-unused-function','-std=c++17'],
                   **{
                       "include_dirs": [
                           "../third_party/pybind11/include",
                           "../include",
                           "../src"
                       ],
                   })
         for pyx_path in get_ext_paths('skydl/pybind11', EXCLUDE_PYX_FILES)] +
        [Extension(name=pyx_path.replace("/", ".").replace(".pyx", ""),
                   language="c++",
                   sources=[pyx_path],
                   extra_compile_args=['-Wno-unused-function', '-std=c++17'],
                   # extra_link_args=['-framework', 'Boost'],
                   **{
                       "include_dirs": [
                           "../include"
                       ],
                       # "library_dirs": [
                       #     '/usr/local/lib',
                       #     '/usr/lib'
                       # ]
                   })
         for pyx_path in get_ext_paths('skydl/cython', EXCLUDE_PYX_FILES)],
        compiler_directives={
            "language_level": 3
        }
    ),
    cmdclass={
        # "install_headers": InstallHeaders,
        "build_py": build_py
    },
)
