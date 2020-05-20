from distutils.core import setup
setup(
    name="mySalary", # 对外我们模块的名字
    version="1.0", # 版本号
    description="根据月薪计算年薪和日薪", #对模块的描述
    author="huenfeng", # 作者
    author_email="1511715823@qq.com",
    py_modules=["mySalary.Salary"] # 要发布的模块
)