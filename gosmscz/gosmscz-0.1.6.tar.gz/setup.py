from setuptools import setup, find_packages


with open('README.md', 'r') as f:
    long_description = f.read()


setup_requires = [
    'wheel',
    'setuptools',
    'setuptools_scm',
]

install_requires = [
    'requests'
]

setup(
    name='gosmscz',
    use_scm_version={
        'write_to': 'gosmscz/version.py'
    },
    author='Creatiweb s.r.o.',
    author_email='vitek@creatiweb.cz',
    description='Go SMS API client library',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://gitlab.com/creatiweb-sro/gosmscz',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    python_requires=">=3.7",
    setup_requires=setup_requires,
    install_requires=install_requires,
    tests_require=[],
)
