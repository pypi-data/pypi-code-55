from setuptools import setup
from platform import system

install_requires = ["keyboard", "moviepy", "pyaudio", "pyautogui", "pygame"]
install_requires.append('getch')

setup(
    name='ScreenRecorder',
    version='1.0.4',
    author='foo',
    author_email='foo@foo.com',
    url='https://pypi.org/project/ScreenRecorder',
    description='A screen recorder.',
    install_requires=[install_requires[:-1]
                      if system() == 'Windows' else install_requires],
    python_requires='>=3.6',
    py_modules=['ScreenRecorder'],
    license='MIT',
    platforms=["Windows", "Linux", "Mac OS-X", ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: Chinese (Simplified)',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ]
)
