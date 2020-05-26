# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['telethon_asyncpg',
 'telethon_asyncpg.client',
 'telethon_asyncpg.network',
 'telethon_asyncpg.sessions']

package_data = \
{'': ['*']}

install_requires = \
['Telethon>=1.13.0,<2.0.0', 'asyncpg>=0.20.1,<0.21.0']

setup_kwargs = {
    'name': 'telethon-asyncpg',
    'version': '0.2.0',
    'description': 'Asyncpg powered session for pgsql databases',
    'long_description': 'Async session for telethon\n==========================\n\nInstallation\n============\n\n::\n\n    pip install telethon_asyncpg\n    # Or with poetry\n    poetry add telethon_asyncpg\n\n\nUsage\n=====\n\n.. code-block:: python3\n\n    import ssl  # optional\n\n    from telethon import events, TelegramClient\n\n    from telethon_asyncpg import AsyncpgSession, install\n    install()\n\n    URI = ???  # URI-string\n    # dialect+driver://username:password@host:port/database\n\n    pgconf = dict(dsn=URI, min_size=5, max_size=5)\n    # to overcome problem with TLS connection to db pass\n    # ssl=ssl.SSLContext(protocol=ssl.PROTOCOL_TLS) to pgconf\n    session = AsyncpgSession(pgconf, session_id_factory=???)\n    # session_id_factory is any callable with "() -> str" signature\n    # default factory is uuid4 str generator. why factory? (it\'s not really factory ik)\n    bot = TelegramClient(session=session, api_id=???, api_hash=???)\n\n    @bot.on(events.NewMessage())\n    async def message_handler(message):\n        await message.reply("Hi!")\n\n    async def start():\n        await bot.start()\n        print(await bot.get_entity("martin_winks"))\n        await bot.run_until_disconnected()\n\n    if __name__ == \'__main__\':\n        import asyncio\n        asyncio.get_event_loop().run_until_complete(start())\n\n- `AsyncpgSession` can also use shared pool by `AsyncpgSession.with_pool` initializer-method\n\n.. code-block:: python\n\n    my_pool = asyncpg.create_pool(...)\n    session = AsyncpgSession.with_pool(my_pool, lambda: "session-id", True)\n\n\nCheck out the ``examples/`` folder for more realistic examples.\n\nContribution\n============\n\nCurrently we have only asyncpg session available, if you want to contribute with your wrapper - welcome. Take `AsyncpgSession` as an example.\n\nFor contributors\n================\n\nPatched TelegramClient <-> Session\n-----------------------------------\n\n- `TelegramClient` and `Session` object share `settings` `{session.meth: (args_seq, kwargs_mapping)}` dictionary. By protocol `TelegramClient` must add callable with args and kwargs. By protocol session must call this functions at start as it wants (e.g. pass more arguments such as `connection` object to session.method)\n\n- `TelegramClient` may call `session.start` several times per one session instance and session should control its start itself and if it\'s already started it shouldn\'t start again\n\n- `Session.save` method is guaranteed to be called as in usual telethon\n\n\nHacking\n-------\n\n::\n\n    # install poetry dependency manager\n    # Fork/Fork+Clone && cd {{cloned}}\n    poetry install\n    # happy hacking!\n\n\nReferences\n==========\n\nTelethon: `here <https://github.com/LonamiWebs/telethon>`_\nasyncpg pg-driver: `asyncpg <https://github.com/MagicStack/asyncpg>`_\n',
    'author': 'mpa',
    'author_email': 'mpa@snejugal.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ukinti/telethon_asyncpg',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
