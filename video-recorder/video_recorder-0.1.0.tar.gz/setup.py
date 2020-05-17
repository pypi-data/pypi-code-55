from setuptools import setup,find_packages

setup(

    name='video_recorder',
    version='0.1.0',
    keywords=('pip','video','recorder','mp4','cv2'),
    description="easy script to record video via USB camera",
    long_description="easy script to record video via USB camera,very easy to use: video_recorder.Video_Recorder()",
    licence='MIT Licence',
    url='https://github.com/jim0575/desktop-tutorial',
    author='james',
    author_email="jim0575@qq.com",
    packages=find_packages(),
    include_package_data=True,
    platforms='any',
    install_requires=[]
    )
