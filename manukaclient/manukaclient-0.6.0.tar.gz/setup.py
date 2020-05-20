#!/usr/bin/env python

import setuptools

from pbr.packaging import parse_requirements

entry_points = {
    'openstack.cli.extension':
    ['account = manukaclient.osc.plugin'],
    'openstack.account.v1':
    [
        'account user list = manukaclient.osc.v1.users:ListUsers',
        'account user search = manukaclient.osc.v1.users:SearchUsers',
        'account user show = manukaclient.osc.v1.users:ShowUser',
        'account user set = manukaclient.osc.v1.users:UpdateUser',
        'account pending-user show = manukaclient.osc.v1.users:ShowPendingUser',
        'account pending-user list = manukaclient.osc.v1.users:ListPendingUsers',
        'account pending-user delete = manukaclient.osc.v1.users:DeletePendingUser',
        'account external-id set = manukaclient.osc.v1.external_ids:UpdateExternalId',
        'account external-id delete = manukaclient.osc.v1.external_ids:DeleteExternalId',
    ]
}


setuptools.setup(
    name='manukaclient',
    version='0.6.0',
    description=('Client for the Nectar Account system'),
    author='Sam Morrison',
    author_email='sorrison@gmail.com',
    url='https://github.com/NeCTAR-RC/python-manukaclient',
    packages=[
        'manukaclient',
    ],
    include_package_data=True,
    setup_requires=['pbr>=3.0.0'],
    install_requires=parse_requirements(),
    license="Apache",
    zip_safe=False,
    classifiers=(
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ),
    entry_points=entry_points,
)
