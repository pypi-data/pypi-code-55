import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name = "pytorch-trainer",
    version = "0.0.3",
    author = "Shawn Zhang",
    author_email = "shawnzhang31@gmail.com",
    description="A mini training neural networks pipeline skeleton in PyTorch.",
    long_description = long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    url = "https://github.com/ShawnZhang31/trainer",
    packages = setuptools.find_packages(exclude=['tests', 'tests/*']),
    classifier = [
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",

        "Development Status :: 1 - Planning",

        'Intended Audience :: Developers',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Scientific/Engineering :: Image Recognition',
        'Topic :: Scientific/Engineering :: Information Analysis',
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    install_requires = [
        "torch >=1.0",
        "torchvision",
        'tqdm',
        'tensorboard',
    ]
)