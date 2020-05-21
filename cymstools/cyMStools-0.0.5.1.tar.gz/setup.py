import setuptools

# 读取项目的readme介绍
with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cyMStools",# 项目名称，保证它的唯一性，不要跟已存在的包名冲突即可
    version="0.0.5.1",
    author="zhyCAO", # 项目作者
    author_email="zhycao@outlook.com",
    description="mass spec tools", # 项目的一句话描述
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/daheitu/cyMStools",# 项目地址
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
