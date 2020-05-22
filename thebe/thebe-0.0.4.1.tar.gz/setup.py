from setuptools import setup, find_packages

def readme():
        with open('README.rst') as f:
                    return f.read()

setup(
        name='thebe',
        version='0.0.4.1',
        description='Automatically runs and displays python code in browser.',
        author_email='hairyhenry@gmail.com',
        url='https://github.com/hotsoupisgood/Satyrn',
        include_package_data=True,
#        packages = ['thebe', 'thebe/templates', 'thebe/static', 'thebe/core', 'thebe/logs'],
        packages=find_packages(),
#        package_data={
#            'thebe':['thebe.py'], 'templates': ['*'], 'static': ['*'], 'core': ['*'], 'logs': ['all.log']
#                },
#        data_files = [('thebe', ['logs/*.log'])],
        install_requires=[
            'flask',
            'flask_socketio',
            'pygments',
            'dill',
            'pypandoc'
            ],
        entry_points={
            'console_scripts': [
                'thebe = thebe.thebe:main',
                ]
            },
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ],
        python_requires='>=3.7',
        )
