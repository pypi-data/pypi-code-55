import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

packages = ['requests']

setuptools.setup(
    name="needle-sdk",
    version="1.8.2",
    author="Needle.sh team",
    author_email="hello@needle.sh",
    description="Needle.sh SDK for Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://needle.sh",
    install_requires=packages,
    packages=['needle_sdk'],
    package_data={
        'needle_sdk': ['core/classes.py', 'core/needle_app.py', 'core/utilities.py', 'core/wrappers.py',
                       'core/libinjection2/linux/_libinjection.so', 'core/libinjection2/linux/libinjection.py',
                       'core/libinjection2/mac_x86_64/_libinjection.so',
                       'core/libinjection2/mac_x86_64/libinjection.py',
                       'core/data/js_event', 'core/data/unix_cmd', 'core/data/scan']
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.0',
)
