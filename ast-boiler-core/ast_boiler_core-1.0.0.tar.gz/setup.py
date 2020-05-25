import io
from setuptools import setup
from setuptools import find_packages

with io.open("README.md", "r", encoding="utf8") as f:
    readme = f.read()

setup(
    name='ast_boiler_core',
    version="1.0.0",
    author="Alex Astafev",
    author_email="efsneiron@gmail.com",
    description="core for flask",
    keywords="boiler, core, flask",
    long_description=readme,
    long_description_content_type="text/markdown",
    python_requires='>=3.6',
    zip_safe=False,
    include_package_data=True,
    packages=find_packages(),
    install_requires=['flask', 'python-dotenv'],
    extras_require={"test": ["pytest", "coverage"]},
    entry_points={
        "console_scripts": [
            "boiler = ast_boiler_core.command:cli",
        ],
    }
)
