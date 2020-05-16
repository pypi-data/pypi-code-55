import setuptools
from version import VERSION


with open("README.md", "r") as fh:
    long_description = fh.read()

DESCRIPTION = """
AI Test Automation Designer Using Robot Framework.
"""[1:-1]

CLASSIFIERS = """
Programming Language :: Python :: 3
License :: OSI Approved :: MIT License
Operating System :: OS Independent
Topic :: Software Development :: Testing
Development Status :: 5 - Production/Stable
"""[1:-1]

setuptools.setup(
    name="cqe-aitestbot",
    version=VERSION,
    author="Sridhar VP",
    author_email="sridharvpmca@gmail.com",
    description="Cognitive Quality Engineer - AI Driven Test Automation Designer",
    long_description=DESCRIPTION,
    long_description_content_type="text/markdown",
    url='https://github.com/cognitiveqe/cqe-aitestbot/',
    keywords='Python AI Driven Test Automation',
    license='MIT',
    packages=setuptools.find_packages(),
    entry_points={
        'console_scripts': [
            'ai_test_bot = ai_test_designer.ai_test_designer:main'
        ]
    },
    platforms='any',
    classifiers=CLASSIFIERS.splitlines(),
    python_requires='>=3.6',
    install_requires=[
        'pandas',
        'numpy',
        'requests',
        'robotframework',
        'robotframework-requests',
        'robotframework-requestspro',
        'progress',
    ],
)
