from setuptools import setup, find_packages

setup(
    name='lyd_demo',
    version='1.0',
    description='just for test',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
    ],
    #author='bin381',
    #url='https://github.com',
    #author_email='1231',
    #license='MIT',
    packages=find_packages(),  # 需要处理哪里packages，当然也可以手动填，例如['pip_setup', 'pip_setup.ext']
    include_package_data=False,
    zip_safe=True,
)
