#!/usr/bin/env python
# -*- coding: utf-8 -*-
###############################################################################
# @copyright Copyright (C) Guichet Entreprises - All Rights Reserved
# 	All Rights Reserved.
# 	Unauthorized copying of this file, via any medium is strictly prohibited
# 	Dissemination of this information or reproduction of this material
# 	is strictly forbidden unless prior written permission is obtained
# 	from Guichet Entreprises.
###############################################################################

###############################################################################
# @package Repo tools
###############################################################################

from .version import __version_info__
from .version import __release_date__

__module_name__ = "gerepotools"
__version__ = '.'.join(str(c) for c in __version_info__)
__author__ = "Arnaud Boidard"
__copyright__ = "Copyright 2018, Guichet Entreprises"

__credits__ = ["Arnaud Boidard"]
__license__ = "MIT"
__maintainer__ = "Arnaud Boidard"
__email__ = "florent.tournois@gmail.fr"
__status__ = "Production"
__url__ = 'https://gitlab.com/guichet-entreprises.fr/tools/repo-tools'

__all__ = []
