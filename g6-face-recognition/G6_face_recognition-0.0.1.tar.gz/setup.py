from setuptools import setup, find_packages

requirements = [
    'opencv-contrib-python',
    'scikit-image',
    'scipy',
    'numpy',
    'matplotlib',
    'imutils',
]


def readme():
    with open('README.md') as f:
        README = f.read()
    return README


setup(
    name="G6_face_recognition",
    version="0.0.1",
    description="A Python package to face recognition.",
    long_description=readme(),
    long_description_content_type="text/markdown",
    author="Gate6",
    # author_email="gate6.info@gate6.com",
    author_email="rajendra.khabiya@gate6.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        "Programming Language :: Python :: 3",

    ],
    # packages=find_packages(),
    packages=["G6_face_recognition"],

    include_package_data=True,
    install_requires=requirements,
    # install_requires=["requests"],
    entry_points={
        'console_scripts': [
            'G6_face_recognition=G6_face_recognition.main:main',
        ]
    },
# what's used to render the link text on PyPI.
    project_urls={  # Optional
        'Source': 'https://github.com/gate6/iris-recognition-sample-code/tree/face-recognition',
    },
)

