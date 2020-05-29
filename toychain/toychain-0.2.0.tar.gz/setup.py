# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['toychain']

package_data = \
{'': ['*']}

install_requires = \
['fastapi>=0.55.1,<0.56.0',
 'loguru>=0.4.1,<0.5.0',
 'requests>=2.23.0,<3.0.0',
 'uvicorn>=0.11.5,<0.12.0']

entry_points = \
{'console_scripts': ['node = toychain.__main__:run_node']}

setup_kwargs = {
    'name': 'toychain',
    'version': '0.2.0',
    'description': 'A blockchain toy project, in Python',
    'long_description': '<h1 align="center">\n  <b>toychain</b>\n</h1>\n\ntoychain is a very simplistic blockchain node modeling in Python.\nWhile the code is my own adaptation, the implementation is from the very good [tutorial][tutorial_link] by Daniel van Flymen.\nThis adaptation uses [`FastAPI`][fastapi_link] as a web framework, and [`uvicorn`][uvicorn_link] as ASGI server instead of the `Flask` app from van Flymen\'s tutorial.\n\n# Running\n\nThis repository uses `Poetry` as a build tool.\nGet a local copy through VCS and to set yourself up with `poetry install`.\n\nThe `poetry run node` command is predefined to start up a node, by default at `localhost:5000`.\nAdditionally, you can specify the host and port on which to run the node with the `--host` and `--port` flags.\nYou can then use the same command to spin up several nodes on different ports.\n\n## Docker\n\nIt is possible to run nodes as docker containers.\nTo do so, clone the repository then build the image with `docker build -t blockchain .`\n\nYou can then run the container by mapping the node\'s port to a desired one at `localhost` on your machine.\nTo map the node to port 5000, run:\n```bash\n$ docker run --init --rm -p 5000:5000 blockchain\n```\n\nTo emulate additional nodes, vary the public port number:\n```bash\n$ docker run --init --rm -p 5001:5000 blockchain\n$ docker run --init --rm -p 5002:5000 blockchain\n$ docker run --init --rm -p 5003:5000 blockchain\n```\n\nYou can then play around by POSTing to `/nodes/register` to add all your running instances to one another\'s networks, POSTing transactions, mining new blocks, and resolving the blockchain.\n\n# Functionality\n\n## The Chain\n\nThe blockchain is a simple list of blocks.\nA `block` in the chain consists of a dictionnary with the following keys:\n- the `index` at which it is located in the chain,\n- a `timestamp` of when the block was added to the chain,\n- the list of `transactions` recorded in the block,\n- the `proof` of validity for itself,\n- a `previous_hash` tag referencing the hash of the previous block in the chain, for immutability.\n\nA simple example block (with a single transaction) as a json payload would look like this:\n```json\nblock = {\n    "index": 1,\n    "timestamp": 1506057125.900785,\n    "transactions": [\n        {\n            "sender": "8527147fe1f5426f9dd545de4b27ee00",\n            "recipient": "a77f5cdfa2934df3954a5c7c7da5df1f",\n            "amount": 5,\n        }\n    ],\n    "proof": 324984774000,\n    "previous_hash": "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"\n}\n```\n\n## The Node Implementation\n\nThe blockchain functionality is provided by a single class, `BlockChain`, in the `toychain.blockchain` module.\nAn instance of the `BlockChain` class is used to run a node.\nEach node stores a full blockchain, the current transactions (not yet written in the chain), and the list of other nodes in the network.\nIt can:\n- Add a transaction to the list of current transactions,\n- Add a new (validated) block to the chain,\n- Run the proof of work algorithm (here simple, for the sake of computation time),\n- Validate the `proof` of a block,\n- Register other nodes on the network,\n- Infer an arbitrary node\'s blockchain\'s validity,\n- Resolve conflict through a consensus algorithm, checking all nodes\' chains in the network and adopting the longest valid one.\n\nA node is ran as a REST API using the `FastAPI` web framework, and is attributed a `UUID` at startup.\nThe implementation is in the `toychain.node` module, and the available endpoints of a node are:\n- `GET` endpoint `/mine` to trigger the addition of a new block to the chain,\n- `POST` endpoint `/transactions/new` to add a transaction to the node\'s list,\n- `GET` endpoint `/chain` to pull the full chain,\n- `POST` endpoint `/nodes/register` to register other nodes\' addresses as part of the network,\n- `GET` endpoint `/nodes/resolve`: to trigger a run of the consensus algorithm and resolve conflicts: the longest valid chain of all nodes in the network is used as reference, replacing the local one, and is returned.\n\nOnce the server is running (for instance with `python -m toychain`), an automatic documentation for those is served at the `/docs` and `/redoc` endpoints.\n\nLet\'s consider our node is running at `localhost:5000`.\nPOSTing a transaction to the node\'s `transactions/new` endpoint with cURL would be done as follows:\n```bash\ncurl -X POST -H "Content-Type: application/json" -d \'{\n "sender": "d4ee26eee15148ee92c6cd394edd974e",\n "recipient": "someone-other-address",\n "amount": 5\n}\' "http://localhost:5000/transactions/new"\n```\n\nLet\'s now consider that we have started a second node at `localhost:5000`.\nPOSTing a payload to register this new node to the first one\'s network with cURL would be done as follows:\n```bash\ncurl -X POST -H "Content-Type: application/json" -d \'{\n "nodes": ["http://127.0.0.1:5001"]\n}\' "http://localhost:5000/nodes/register"\n```\n\nIf you would rather use [`httpie`][httpie_link], those commands would be, respectively: \n```bash\necho \'{ "sender": "d4ee26eee15148ee92c6cd394edd974e", "recipient": "someone-other-address", "amount": 5 }\' | http POST http://localhost:5000/transactions/new\n```\n```bash\necho \'{ "nodes": ["http://127.0.0.1:5001"] }\' | http POST http://localhost:5000/nodes/register\n```\n\n[fastapi_link]: https://fastapi.tiangolo.com/\n[httpie_link]: https://httpie.org/\n[tutorial_link]: https://hackernoon.com/learn-blockchains-by-building-one-117428612f46\n[uvicorn_link]: https://www.uvicorn.org/',
    'author': 'Your Name',
    'author_email': 'you@example.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/fsoubelet/toychain',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
