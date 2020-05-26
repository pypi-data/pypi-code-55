# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hadolintw']

package_data = \
{'': ['*']}

install_requires = \
['click>=5.0']

entry_points = \
{'console_scripts': ['hadolintw = hadolintw.main:main']}

setup_kwargs = {
    'name': 'hadolintw',
    'version': '1.2.1',
    'description': 'Pretty output for hadolint',
    'long_description': '[![Publish](https://github.com/mperezi/hadolint-wrapper/workflows/Publish/badge.svg)](https://github.com/mperezi/hadolint-wrapper/actions?query=workflow%3APublish)\n# hadolint-wrapper \n\n## What is hadolint?\n\n[Hadolint](https://github.com/hadolint/hadolint) stands for Haskell Dockerfile Linter and is:\n\n> A smarter Dockerfile linter that helps you build [best practice](https://docs.docker.com/engine/userguide/eng-image/dockerfile_best-practices) Docker images. \n\n## Example\n\n### Dockerfile\n\n```dockerfile\nFROM debian\nRUN export node_version="0.10" \\\n&& apt-get update && apt-get -y install nodejs="$node_verion"\nCOPY package.json usr/src/app\nRUN cd /usr/src/app \\\n&& npm install node-static\n\nEXPOSE 80000\nCMD "npm start"\n```\n\n### With hadolint\n\n```\n$ hadolint Dockerfile\nDockerfile:1 DL3006 Always tag the version of an image explicitly\nDockerfile:2 SC2154 node_verion is referenced but not assigned (did you mean \'node_version\'?).\nDockerfile:2 DL3009 Delete the apt-get lists after installing something\nDockerfile:2 DL3015 Avoid additional packages by specifying `--no-install-recommends`\nDockerfile:5 DL3003 Use WORKDIR to switch to a directory\nDockerfile:5 DL3016 Pin versions in npm. Instead of `npm install <package>` use `npm install <package>@<version>`\nDockerfile:8 DL3011 Valid UNIX ports range from 0 to 65535\nDockerfile:9 DL3025 Use arguments JSON notation for CMD and ENTRYPOINT arguments\n```\n\n### With hadolint wrapper\n\n```bash\n$ hadolintw Dockerfile\n```\n\n![sample-output](https://user-images.githubusercontent.com/43891734/76677889-a3de9680-65d3-11ea-9575-8ba289bcb149.png)\n\n## Installation\n\nOn OS X, the easiest way to install *hadolintw* is using [Homebrew](http://brew.sh/)\n\n```\n$ brew tap mperezi/tools\n$ brew install hadolint-wrapper\n```\n\nOn other platforms, install *hadolintw* using pip\n\n```\n$ pip install hadolintw\n```\n\n## Usage\n\n```\n$ hadolintw\nUsage: hadolintw [OPTIONS] DOCKERFILE [HADOLINT_ARGS]...\n\n  Provides a more clear output for hadolint\n\nOptions:\n  -d, --use-docker             use the dockerized version of hadolint\n  --color [never|auto|always]\n  --help                       Show this message and exit.\n```\n\nSet up as a wrapper:\n\n```\n$ alias hadolint=hadolintw\n$ hadolint Dockerfile --ignore DL3020\n# Please note that all hadolint options must come AFTER the Dockerfile\n```\n\n## FAQ\n\n### Does the wrapper keep the exit status of hadolint so that I can use it in my CI environment?\n\nNo problem.\n\n### My CI environment doesn\'t support colorized output. Can I disable it?\n\nBy default the wrapper can detect if the output is being written to a tty or a pipe or a file, enabling or disabling the color codes accordingly (`—color auto` is the default setting). However you can always turn this feature on or off regardless of the type of output destination:\n\n```\n$ hadolintw --color never Dockerfile\n```\n\n### In our team we have a `hadolint.yml` with some rules defined for our project. Can we still use it with the hadolint wrapper?\n\nSure.\n\n```\n$ hadolintw Dockerfile --config hadolint.yml\n```\n\n### The hadolint program is not available where my build is going to run but at least I have access to a Docker environment. Can I still run hadolint?\n\n[Be my guest](https://hub.docker.com/r/hadolint/hadolint).\n\n```\n$ hadolintw --use-docker Dockerfile\nUnable to find image \'hadolint/hadolint:latest\' locally\nlatest: Pulling from hadolint/hadolint\n8a8460b25d70: Pulling fs layer\n8a8460b25d70: Verifying Checksum\n8a8460b25d70: Download complete\n8a8460b25d70: Pull complete\nDigest: sha256:0cdbd1e0f5fd3135d17617bb510a85c0248eb70b041021fe5431d4d1501d41b9\nStatus: Downloaded newer image for hadolint/hadolint:latest\n...\n```\n\n',
    'author': 'mperezi',
    'author_email': 'mperezibars@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mperezi/hadolint-wrapper',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.0,<4.0.0',
}


setup(**setup_kwargs)
