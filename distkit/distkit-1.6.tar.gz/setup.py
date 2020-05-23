import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(name='distkit',
                 version='1.6',
                 description='Gaussian and Binomial distributions',
                 long_description=long_description,
                 long_description_content_type="text/markdown",
                 url="https://github.com/abhinav314/distkit",
                 packages=['distkit'],
                 author='Abhinav Chanda',
                 author_email='abhinav468@gmail.com',
                 classifiers=[
                     "Programming Language :: Python :: 3",
                     "License :: OSI Approved :: MIT License",
                     "Operating System :: OS Independent",
                 ],
                 python_requires='>=3.0',
                 zip_safe=False)
