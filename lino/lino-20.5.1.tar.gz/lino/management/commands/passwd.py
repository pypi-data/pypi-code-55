# -*- coding: UTF-8 -*-
# Copyright 2020 by Rumma & Ko Ltd.
# License: BSD, see file LICENSE for more details.

"""
This defines the :manage:`passwd` management command.

.. management_command:: passwd

Set password for a user. Optionally create or update user.

Usage: cd to your project directory and say::

  $ python manage.py passwd USER

This will change the password of user `USER`.

Options:

.. option:: --noinput

    Do not prompt for user input of any kind.

SEE ALSO
========

- :doc:`/specs/users`
"""

from io import open
import logging
logger = logging.getLogger(__name__)

import os
from decimal import Decimal
import argparse

from clint.textui import progress

from django.db import models
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db.utils import DatabaseError
from django.utils.timezone import make_naive, is_aware, utc

from lino.utils import puts
from lino.core.utils import sorted_models_list, full_model_name
from lino.core.choicelists import ChoiceListField

from lino.utils.mldbc.fields import BabelCharField, BabelTextField


class Command(BaseCommand):
    # tmpl_dir = ''
    # args = "output_dir"

    def add_arguments(self, parser):
        parser.add_argument(
            'username',
            help='The user to update.')
        parser.add_argument('--noinput', action='store_false',
                            dest='interactive', default=True,
                            help='Do not prompt for input of any kind.')


    def handle(self, *args, **options):
        # if len(args) != 1:
        #     raise CommandError("No output_dir specified.")
            # print("No output_dir specified.")
            # sys.exit(-1)
        # import lino
        # lino.startup()
        username = options['username']
        obj = rt.models.users.User.objects.get(username=username)

        if os.path.exists(self.output_dir):
            if options['overwrite']:
                pass
                # TODO: remove all files?
            else:
                raise CommandError(
                    "Specified output_dir %s already exists. "
                    "Delete it yourself if you dare!" % self.output_dir)
        else:
            os.makedirs(self.output_dir)

        self.options = options

        #~ logger.info("Running %s to %s.", self, self.output_dir)
        self.write_files()
        logger.info("Wrote %s objects to %s and siblings." % (
            self.count_objects, self.main_file))
        if self.database_errors:
            raise CommandError(
                "There were %d database errors. "
                "The dump in %s is not complete.",
                self.database_errors, self.output_dir)
