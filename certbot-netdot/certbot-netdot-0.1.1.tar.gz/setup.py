from setuptools import setup


try:
    long_desc = open("README.md").read()
except:
    print("Skipping README.md for long description as it was not found")
    long_desc = None

setup(
    name="certbot-netdot",
    version="0.1.1",
    description="Netdot DNS authentication plugin for Certbot",
    long_description=long_desc,
    long_description_content_type="text/markdown",
    license="MIT",
    author="Mattias Amnefelt",
    author_email="mattiasa@cantemo.com",
    url="https://www.github.com/Cantemo/certbot-netdot",
    py_modules=["certbot_netdot"],
    install_requires=[
        "acme>=1.4.0",
        "certbot>=1.4.0",
        "pynetdot>=1.5.0",
        "zope.interface>=5.0.0",
    ],
    entry_points={
        "certbot.plugins": [
            "auth = certbot_netdot:NetdotAuthenticator",
        ],
    },
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Environment :: Plugins",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Topic :: Internet :: Name Service (DNS)",
        "Topic :: System :: Systems Administration",
        "Topic :: Utilities",
    ],
)
