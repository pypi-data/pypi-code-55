from distutils.core import setup
with open('README.md') as f:
    long_description = f.read()

setup(
    name = 'openglass-instructions',                 # How you named your package folder (MyLib)
    packages = ['ogins'],     # Chose the same as "name"
    version = '0.0.0',            # Start with a small number and increase it with every change you make
    license='MIT',                # Chose a license from here: https://help.github.com/articles/licensing-a-repository
    description = 'Information about OpenGlass VM bytecode opcodes',     # Give a short description about your library
    long_description=long_description,
    long_description_content_type="text/markdown",
    author = 'Sam Sloniker',                                     # Type in your name
    author_email = 'scoopgracie@gmail.com',            # Type in your E-Mail
    url = 'https://github.com/openglass-project/',     # Provide either the link to your github or to your website
    keywords = ['openglass'],     # Keywords that define your package best
    install_requires=[                        # I get to this in a second
            ],
    classifiers=[
        'Development Status :: 3 - Alpha',            # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Intended Audience :: Developers',            # Define that your audience are developers
        'License :: OSI Approved :: MIT License',     # Again, pick a license
        'Programming Language :: Python :: 3',            #Specify which pyhton versions that you want to support
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)
