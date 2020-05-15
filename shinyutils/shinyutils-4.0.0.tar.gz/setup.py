# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['shinyutils', 'tests']

package_data = \
{'': ['*'], 'shinyutils': ['data/*']}

extras_require = \
{'color': ['crayons', 'rich>=1.0,<2.0'],
 'plotting': ['matplotlib>=3.2,<4.0', 'seaborn>=0.10,<0.11']}

setup_kwargs = {
    'name': 'shinyutils',
    'version': '4.0.0',
    'description': 'Personal collection of common utilities',
    'long_description': '# shinyutils\nVarious utilities for common tasks. :sparkles: :sparkles: :sparkles:\n\n## Setup\nInstall with `pip`. Additional features can be enabled with the `[<feature>]` syntax shown below. Available optional features are:\n* `color`: color support for logging and argument parsing\n* `plotting`: support for `matplotlib` and `seaborn`\n```bash\npip install shinyutils  # basic install\npip install "shinyutils[color]"  # install with color support\npip install "shinyutils[color,plotting]"  # install with color and plotting support\npip install "shinyutils[all]"  # install with all optional features\n```\n\n## Components\n\n### `subcls`\nUtility functions for dealing with subclasses.\n\n#### Functions\n* __`get_subclasses(cls)`__: returns a list of all the subclasses of `cls`.\n* __`get_subclass_names(cls)`__: returns a list of names of all subclasses of `cls`.\n* __`get_subclass_from_name(base_cls, cls_name)`__: return the subclass of `base_cls` named `cls_name`.\n\n### `argp`\nUtilities for argument parsing.\n\n#### `LazyHelpFormatter`\n`HelpFormatter` with sane defaults, and colors (courtesy of `crayons`)! To use, simply pass `formatter_class=LazyHelpFormatter` when creating `ArgumentParser` instances.\n```python\narg_parser = ArgumentParser(formatter_class=LazyHelpFormatter)\nsub_parsers = arg_parser.add_subparsers(dest="cmd")\nsub_parsers.required = True\n# `formatter_class` needs to be set for sub parsers as well.\ncmd1_parser = sub_parsers.add_parser("cmd1", formatter_class=LazyHelpFormatter)\n```\n\n#### `CommaSeparatedInts`\n`ArgumentParser` type representing a comma separated list of ints (example `1,2,3,4`).\n```python\narg_parser.add_argument("--csi", type=CommaSeparatedInts())\n```\n\n#### `OutputFileType`\n`ArgumentParser` type representing an output file. The file\'s base directory is created if needed. The returned value is a file object.\n\n#### `OutputDirectoryType`\n`ArgumentParser` type representing an output directory. The directory is created if it doesn\'t exist.\n\n#### `ClassType`\n`ArgumentParser` type representing sub-classes of a given base class. The returned value is a class.\n```python\nclass Base:\n    pass\n\nclass A(Base):\n    pass\n\nclass B(Base):\n    pass\n\narg_parser.add_argument("--cls", type=ClassType(Base), default=A)\n```\n\n#### `shiny_arg_parser`\n`ArgumentParser` object with LazyHelpFormatter, and logging argument.\n\n### `logng`\nUtilities for logging.\n#### `build_log_argp`\nCreates an argument group with logging arguments.\n```\n>>> arg_parser = ArgumentParser()\n>>> build_log_argp(arg_parser)\n>>> arg_parser.print_help()\nusage: test.py [-h] [--log-level {DEBUG,INFO,WARNING,ERROR,CRITICAL}]\n\noptional arguments:\n  -h, --help            show this help message and exit\n  --log-level {DEBUG,INFO,WARNING,ERROR,CRITICAL}\n```\n\n#### `conf_logging`\nConfigures global logging using arguments returned by `ArgumentParser.parse_args`. `log_level` can be over-ridden with the keyword argument. Colors (enabled by default if `rich` is installed) can be toggled.\n```python\nargs = arg_parser.parse_args()\nconf_logging(args)\nconf_logging(args, log_level="INFO")  # override `log_level`\nconf_logging(use_colors=False)  # disable colors\n```\nWhen imported, `shinyutils` calls `conf_logging` without any arguments.\n\n### `matwrap`\nWrapper around `matplotlib` and `seaborn`.\n\n#### Usage\n```python\nfrom shinyutils.matwrap import MatWrap as mw  # do not import `matplotlib`, `seaborn`\n\nmw.configure()  # this should be called before importing any packages that import matplotlib\n\nfig = mw.plt().figure()\nax = fig.add_subplot(111)  # `ax` can be used normally now\n\n# Use class methods in `MatWrap` to access `matplotlib`/`seaborn` functions.\nmw.mpl()  # returns `matplotlib` module\nmw.plt()  # returns `matplotlib.pyplot` module\nmw.sns()  # returns `seaborn` module\n```\n\n#### Configuration\nUse `mw.configure` to configure plots. Arguments (defaults in bold) are:\n* `context`: seaborn context (__paper__/poster/talk/notebook)\n* `style`: seaborn style (white/whitegrid/dark/darkgrid/__ticks__)\n* `font`: any font available to fontspec (default __Latin Modern Roman__)\n* `latex_pkgs`: additional latex packages to be included before defaults\n* `**rc_extra`: matplotlib rc parameters to override defaults\n```\n',
    'author': 'Jayanth Koushik',
    'author_email': 'jnkoushik@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jayanthkoushik/shinyutils',
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
