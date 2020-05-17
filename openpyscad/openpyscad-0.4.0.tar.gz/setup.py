# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['openpyscad']

package_data = \
{'': ['*']}

install_requires = \
['six>=1.14.0,<2.0.0']

setup_kwargs = {
    'name': 'openpyscad',
    'version': '0.4.0',
    'description': 'Python library to generate OpenSCAD source code',
    'long_description': '[![Build Status](https://travis-ci.org/taxpon/openpyscad.svg?branch=develop)](https://travis-ci.org/taxpon/openpyscad) [![Coverage Status](https://coveralls.io/repos/github/taxpon/openpyscad/badge.svg?branch=develop)](https://coveralls.io/github/taxpon/openpyscad?branch=develop) [![Python2](https://img.shields.io/badge/python-2-blue.svg)](#) [![Python3](https://img.shields.io/badge/python-3-blue.svg)](#)\n# OpenPySCAD\nPython library to generate [OpenSCAD](http://www.openscad.org/) source code. This library provides intuitive interface when you handle 3D data.\nOpenPySCAD supports python3(3.5+).\n\n## Install\n```bash\npip install openpyscad\n```\n\n## How to use\n- Write python code as follows:\n```python\nimport openpyscad as ops\nc1 = ops.Cube([10, 20, 10])\nc2 = ops.Cube([20, 10, 10])\n(c1 + c2).write("sample.scad")\n```\n\n- Generated code will be written in the "sample.scad". OpenSCAD can detect the change of your code and reload automatically. That\'s so cool :D\n```openscad\nunion(){\n    cube([10, 20, 10]);\n    cube([20, 10, 10]);\n};\n```\n\n## Generated code examples\n\n### 3D Shapes\n\nPython:\n```python\nSphere(r=10, _fn=100)\nCube([10, 10, 10])\nCylinder(h=10, r=10)\np = Polyhedron(\n    points=[\n        [10, 10, 0], [10, -10, 0], [-10, -10, 0], [-10, 10, 0],  [0, 0, 10]\n    ],\n    faces=[\n        [0, 1, 4], [1, 2, 4], [2, 3, 4], [3, 0, 4],  [1, 0, 3], [2, 1, 3]\n    ]\n)\n```\n\nGenerated OpenSCAD code:\n```openscad\nsphere(r=10, $fn=100);\ncube(size=[10, 10, 10]);\ncylinder(h=10, r=10);\npolyhedron(points=[[10, 10, 0], [10, -10, 0], [-10, -10, 0], [-10, 10, 0], [0, 0, 10]], faces=[[0, 1, 4], [1, 2, 4], [2, 3, 4], [3, 0, 4], [1, 0, 3], [2, 1, 3]]);\n```\n\n### Boolean Operations\n\nPython:\n```python\n# Union\nCube([20, 10, 10]) + Cube([10, 20, 10])\n\n# You can also write like this\nu = Union()\nu.append(Cube[20, 10, 10])\nu.append(Cube[10, 20, 10])\n\n# Difference\nCube([20, 10, 10]) - Cube([10, 20, 10])\n\n# You can also write like this\ni = Difference()\ni.append(Cube[20, 10, 10])\ni.append(Cube[10, 20, 10])\n\n# Intersection\nCube([20, 10, 10]) & Cube([10, 20, 10])\n\n# You can also write like this\ni = Intersection()\ni.append(Cube[20, 10, 10])\ni.append(Cube[10, 20, 10])\n```\n\nGenerated OpenSCAD code:\n```openscad\n// Union\nunion(){\n    cube([20, 10, 10])\n    cube([10, 20, 10])\n};\n\n// Difference\ndifference(){\n    cube([20, 10, 10]);\n    cube([10, 20, 10]);\n};\n\n// Intersection\nintersection(){\n    cube([20, 10, 10]);\n    cube([10, 20, 10]);\n};\n```\n\n### Transformations\n\nPython:\n```python\n# Translate\nCube([20, 10, 10]).translate([10, 10, 10])\n\n# Rotate\nCube([20, 10, 10]).rotate([0, 0, 45])\n\n# Scale\nCube([20, 10, 10]).scale([2, 1, 1])\n\n# Resize\nCube([20, 10, 10]).resize([2, 1, 1])\n\n# Mirror\nCube([20, 10, 10]).mirror([1, 1, 1])\n\n# Color\nCube([20, 10, 10]).color("Red")\n\n# Offset\nCircle(10).offset(10)\n```\n\nGenerated OpenSCAD code:\n```openscad\n// Translate\ntranslate(v=[10, 10, 10]){\n    cube([20, 10, 10]);\n};\n\n// Rotate\nrotate(v=[0, 0, 45]){\n    cube([20, 10, 10]);\n};\n\n// Scale\nscale(v=[2, 1, 1]){\n    cube([20, 10, 10]);\n};\n\n// Resize\nresize(newsize=[2, 1, 1]){\n    cube(size=[20, 10, 10]);\n};\n\n// Mirror\nmirror([1, 1, 1]){\n    cube(size=[20, 10, 10]);\n};\n\n// Color\ncolor("Red"){\n    cube(size=[20, 10, 10]);\n};\n\n// Offset\noffset(r=10){\n    circle(r=10);\n};\n```\n\n### Modifiers\nOpenPySCAD provides [modifiers](https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/Modifier_Characters) interfaces ("*", "!", "#" and "%").\n\nPython:\n```python\nc1 = Cube(10)\nc1.disable()         # add "*" character\nc1.show_only()       # add "!" character\nc1.is_debug()        # add "#" character\nc1.is_transparent()  # add "&" character\n```\n\n## Interested in contribution?\nPlease read [CONTRIBUTING.md](./CONTRIBUTING.md). \n\n',
    'author': 'Takuro Wada',
    'author_email': 'taxpon@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/taxpon/openpyscad',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
