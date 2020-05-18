from setuptools import setup, Extension
from Cython.Build import cythonize


with open("README.md", "r") as file:
    long_description = file.read()

dev_status = {
    "Alpha": "Development Status :: 3 - Alpha",
    "Beta": "Development Status :: 4 - Beta",
    "Pro": "Development Status :: 5 - Production/Stable",
    "Mature": "Development Status :: 6 - Mature",
}

setup(
    name="CyStack",
    ext_modules=cythonize(
        Extension(
            name="CyStack",
            sources=["Stack.pyx"],
            language=["c++"],
            extra_compile_args=["-std=c++17"],
        ),
        compiler_directives={
            'embedsignature': True,
            'language_level': 3,
        },
    ),
    author="Robert Sharp",
    author_email="webmaster@sharpdesigndigital.com",
    version="0.1.5",
    description="Custom Stack & Queue",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="Free for non-commercial use",
    classifiers=[
        dev_status["Beta"],
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Cython",
        "Programming Language :: C++",
    ],
    keywords=[
        "Stack", "Queue",
    ],
    python_requires='>=3.6',
)
