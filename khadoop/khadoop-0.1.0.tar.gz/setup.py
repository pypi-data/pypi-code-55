# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['khadoop', 'khadoop.yarn']

package_data = \
{'': ['*']}

install_requires = \
['mypy>=0.770,<0.771', 'tox>=3.15.1,<4.0.0']

setup_kwargs = {
    'name': 'khadoop',
    'version': '0.1.0',
    'description': '',
    'long_description': '# README\n\n##\xa0Bookmarks\n\n- https://stackoverflow.com/questions/23058663/where-are-logs-in-spark-on-yarn\n\n## YARN logs\n\nIn YARN terminology, executors and application masters run inside “containers”.\n\nIf log aggregation is turned on (with the `yarn.log-aggregation-enable` config), container logs are copied to HDFS and deleted on the local machine.\n\nThese logs can be viewed from anywhere on the cluster with the yarn logs command.\n\n`yarn logs -applicationId <app ID>`\n\nnote:\n\n> The only thing you need to follow to get correctly working history server for Spark is to close your Spark context in your application. Otherwise, application history server does not see you as COMPLETE and does not show anything (despite history UI is accessible but not so visible).\n\nOn HDFS they are located can be found by looking at your YARN configs `yarn.nodemanager.remote-app-log-dir` and `yarn.nodemanager.remote-app-log-dir-suffix`\n\nHelpfull question on [cloudera support question]https://community.cloudera.com/t5/Support-Questions/Yarn-log-history/m-p/164682/highlight/true#M127049\n\nYarn typically stores history of all the application in\n\n- Mapreduce History server (only for Mapreduce jobs)\n- Application Timeline Server ( all type of yarn applications).\n\n```xml\n<property>\n  <name>yarn.timeline-service.enabled</name>\n  <value>true</value>\n</property>\n\n```\n\n```xml\n<property>\n<name>yarn.timeline-service.webapp.address</name>\n<value>host1:8188</value>\n</property>\n```\n',
    'author': 'Khalid',
    'author_email': 'khalidck@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
