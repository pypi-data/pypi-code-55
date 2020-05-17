import setuptools

setuptools.setup(
    name="moclaphar",
    version="0.0.14",
    license='MIT',
    author="Jongkuk Lim",
    author_email="lim.jeikei@gmail.com",
    description="This packages mainly aims to make an easy process for dataset manipulation.",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/JeiKeiLim/moclaphar",
    packages=setuptools.find_packages(),
    classifiers=[
        # 패키지에 대한 태그
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    install_requires=[
        'scipy>=1.4.1',
        'matplotlib>=3.2.1',
        'seaborn>=0.10.1',
        'h5py>=2.10.0',
        'pandas>=1.0.3',
        'moviepy>=1.0.3',
      ],
)

"""
Dependencies 자동으로 처리되도록 수정 필요
필요 리스트

scipy
  - (numpy)
pandas
matplotlib
seaborn
moviepy
h5py


tensorflow는 사람마다 환경이 다를수 있으니 건너뛰는게 나을듯
생각해보니 위의 목록은 tensorflow 설치 후 확인한 목록임.
가상환경 다시 만들어서 리스트 다시 뽑아야 함

"""
