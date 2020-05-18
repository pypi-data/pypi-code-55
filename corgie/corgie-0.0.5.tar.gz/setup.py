import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="corgie",
    version="0.0.5",
    author="Sergiy Popovych",
    author_email="sergiy.popovich@gmail.com",
    description="Connectomics Registration General Inference Engine",
    packages=setuptools.find_packages(),
    zip_safe=False,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/supersergiy/corgie",
    include_package_data=True,
    install_requires=[
      'torch',
      'gevent',
      'torchvision',
      'numpy',
      'six',
      'pyyaml',
      'mazepa',
      'click-option-group',
      'click',
      'procspec',
      'modelhouse'
    ],
    entry_points={
        "console_scripts": [
            "corgie = corgie.main:cli",
            "corgie-worker = corgie.worker:worker",
        ],
    },
    python_requires='>=3.7',
)
