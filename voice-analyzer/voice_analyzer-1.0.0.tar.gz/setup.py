import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='voice_analyzer',
    version='1.0.0',
    description='Human voice analyzer',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    include_package_data=True,
    url="https://github.com/artysold/voice-analyzer",
    author='Artem Soldatov',
    author_email='arty.sold@gmail.com',
    install_requires=[
       'numpy==1.17.4',
       'praat-parselmouth==0.3.3',
       'tensorflow==2.1.0'
    ]
)
