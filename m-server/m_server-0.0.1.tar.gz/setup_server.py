from setuptools import setup, find_packages

setup(name="m_server",
      version="0.0.1",
      description="m_server",
      author="Sergei Chaban",
      author_email="s_chaban@mail.ru",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome']
      )
