import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="zhangwei_helper",
    # username
    version="0.0.7",
    author="zwzw911",
    author_email="zwzw911110@163.com",
    description="A package include all common part,like function,enum,written \
                 by zhangwei(zwzw911)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/zwzw911/zhangwei_helper",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
    ],
    python_requires='>=3.6',
)