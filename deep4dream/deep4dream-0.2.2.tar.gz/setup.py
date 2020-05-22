import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="deep4dream", # Replace with your own username
    version="0.2.2",
    author="Falah.G.Saleh",
    author_email="falahgs07@gmail.com",
    description="A Keras implementation of Deep Dream for any image",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://iraqprogrammer.wordpress.com/",
    packages=["deep4dream"],
	keywords = ['neural','artistic','neural-dream','dream','keras','neural-art','feature-visualization','machine-learning-art','ai-art','deepdream','tensorflow','inceptionv3'],
	install_requires=[            # I get to this in a second
          'keras',
          'scipy',
      ],
    classifiers=[
        "Programming Language :: Python :: 3",
		"Programming Language :: Python :: 3.5",
		"Programming Language :: Python :: 3.6",
		"Programming Language :: Python :: 3.7",
		"Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)