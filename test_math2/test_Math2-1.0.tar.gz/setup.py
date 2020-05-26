from distutils.core import setup

setup(
    name='test_Math2',  # 对外模块名字
    version='1.0',        # 版本号
    description='这是第一个对外发布模块，测试',    # 描述
    author='gaoqi',     #作者
    author_email='123@qq.com',
    py_modules=['test_Math2.demo1', 'test_Math2.demo2']     # 要发布的模块
)
