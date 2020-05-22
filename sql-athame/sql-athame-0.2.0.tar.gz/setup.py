# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sql_athame']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'sql-athame',
    'version': '0.2.0',
    'description': 'Python tool for slicing and dicing SQL',
    'long_description': '# sql-athame\n\nPython tool for slicing and dicing SQL\n\n## Example\n\n```python\nfrom sql_athame import sql\n\n\ndef get_orders(query):\n    where = []\n\n    if "id" in query:\n        where.append(sql("id = {}", query["id"]))\n    if "eventId" in query:\n        where.append(sql("event_id = {}", query["eventId"]))\n    if "startTime" in query:\n        where.append(sql("start_time = {}", query["startTime"]))\n    if "from" in query:\n        where.append(sql("start_time >= {}", query["from"]))\n    if "until" in query:\n        where.append(sql("start_time < {}", query["until"]))\n\n    return sql("SELECT * FROM orders WHERE {}", sql.all(where))\n\n\nprint(get_orders({}).query())\n# (\'SELECT * FROM orders WHERE TRUE\', [])\n\nprint(list(get_orders({})))\n# [\'SELECT * FROM orders WHERE TRUE\']\n\nprint(get_orders({"id": "xyzzy"}).query())\n# (\'SELECT * FROM orders WHERE TRUE AND id = $1\', [\'xyzzy\'])\n\nprint(list(get_orders({"id": "xyzzy"})))\n# [\'SELECT * FROM orders WHERE TRUE AND id = $1\', \'xyzzy\']\n\nprint(\n    *get_orders(\n        {"eventId": "plugh", "from": "2019-05-01", "until": "2019-08-26"}\n    )\n)\n# SELECT * FROM orders WHERE TRUE AND event_id = $1 AND start_time >= $2 AND start_time < $3 [\'plugh\', \'2019-05-01\', \'2019-08-26\']\n\n\nsuperquery = sql(\n    """\n    SELECT *\n      FROM ({subquery}) sq\n      JOIN other_table ot ON (ot.id = sq.id)\n      WHERE ot.foo = {foo}\n      LIMIT {limit}\n    """,\n    subquery=get_orders({"id": "xyzzy"}),\n    foo="bork",\n    limit=50,\n)\nprint(superquery.query())\n# ("""\n#     SELECT *\n#       FROM (SELECT * FROM orders WHERE TRUE AND id = $1) sq\n#       JOIN other_table ot ON (ot.id = sq.id)\n#       WHERE ot.foo = $2\n#       LIMIT $3\n#     """, [\'xyzzy\', \'bork\', 50])\n```\n',
    'author': 'Brian Downing',
    'author_email': 'bdowning@lavos.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/bdowning/sql-athame',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
