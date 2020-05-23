# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aiocqlengine']

package_data = \
{'': ['*']}

install_requires = \
['aiocassandra>=2.0,<3.0', 'cassandra-driver>=3.20,<4.0']

setup_kwargs = {
    'name': 'aiocqlengine',
    'version': '0.2.0',
    'description': 'Async wrapper for cqlengine of cassandra python driver.',
    'long_description': '# aiocqlengine\nAsync wrapper for cqlengine of cassandra python driver.\n\nThis project is built on [cassandra-python-driver](https://github.com/datastax/python-driver) and [aiocassandra](https://github.com/aio-libs/aiocassandra).\n\n[![Actions Status](https://github.com/charact3/aiocqlengine/workflows/unittest/badge.svg)](https://github.com/charact3/aiocqlengine/actions)\n\n## Installation\n```sh\n$ pip install aiocqlengine\n```\n\n## Change log\n`0.1.1`\n- Add `AioBatchQuery`:\n  ```python\n  batch_query = AioBatchQuery()\n  for i in range(100):\n      Model.batch(batch_query).create(id=uuid.uuid4())\n  await batch_query.async_execute()\n  ```\n\n`0.2.0`\n- Patch the `aiosession` for `ResultSet`, now need to import session by:\n  ```python\n  from aiocqlengine.session import aiosession_for_cqlengine\n  ```\n- Add new method of `AioModel` for paging:\n  ```python\n  async for results in AioModel.async_iterate(fetch_size=100):\n      # Do something with results\n      pass\n  ```\n\n## Example usage\n\n```python\nimport asyncio\nimport uuid\nimport os\n\nfrom aiocqlengine.models import AioModel\nfrom aiocqlengine.query import AioBatchQuery\nfrom aiocqlengine.session import aiosession_for_cqlengine\nfrom cassandra.cluster import Cluster\nfrom cassandra.cqlengine import columns, connection, management\n\n\nclass User(AioModel):\n    user_id = columns.UUID(primary_key=True)\n    username = columns.Text()\n\n\nasync def run_aiocqlengine_example():\n    # Model.objects.create() and Model.create() in async way:\n    user_id = uuid.uuid4()\n    await User.objects.async_create(user_id=user_id, username=\'user1\')\n    await User.async_create(user_id=uuid.uuid4(), username=\'user2\')\n\n    # Model.objects.all() and Model.all() in async way:\n    print(list(await User.async_all()))\n    print(list(await User.objects.filter(user_id=user_id).async_all()))\n\n    # Model.object.update() in async way:\n    await User.objects(user_id=user_id).async_update(username=\'updated-user1\')\n\n    # Model.objects.get() and Model.get() in async way:\n    user = await User.objects.async_get(user_id=user_id)\n    await User.async_get(user_id=user_id)\n    print(user, user.username)\n\n    # Model.save() in async way:\n    user.username = \'saved-user1\'\n    await user.async_save()\n\n    # Model.delete() in async way:\n    await user.async_delete()\n\n    # Batch Query in async way:\n    batch_query = AioBatchQuery()\n    User.batch(batch_query).create(user_id=uuid.uuid4(), username="user-1")\n    User.batch(batch_query).create(user_id=uuid.uuid4(), username="user-2")\n    User.batch(batch_query).create(user_id=uuid.uuid4(), username="user-3")\n    await batch_query.async_execute()\n\n    # Async iterator\n    async for users in User.async_iterate(fetch_size=100):\n        pass\n\n    # The original cqlengine functions were still there\n    print(len(User.objects.all()))\n\n\ndef create_session():\n    cluster = Cluster()\n    session = cluster.connect()\n\n    # Create keyspace, if already have keyspace your can skip this\n    os.environ[\'CQLENG_ALLOW_SCHEMA_MANAGEMENT\'] = \'true\'\n    connection.register_connection(\'cqlengine\', session=session, default=True)\n    management.create_keyspace_simple(\'example\', replication_factor=1)\n    management.sync_table(User, keyspaces=[\'example\'])\n\n    # Wrap cqlengine connection with aiosession\n    aiosession_for_cqlengine(session)\n    session.set_keyspace(\'example\')\n    connection.set_session(session)\n    return session\n\n\ndef main():\n    # Setup connection for cqlengine\n    session = create_session()\n\n    # Run the example function in asyncio loop\n    loop = asyncio.get_event_loop()\n    loop.run_until_complete(run_aiocqlengine_example())\n\n    # Shutdown the connection and loop\n    session.cluster.shutdown()\n    loop.close()\n\n\nif __name__ == \'__main__\':\n    main()\n```\n\n## License\nThis project is under MIT license.\n',
    'author': 'Darren',
    'author_email': 'charact3@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
