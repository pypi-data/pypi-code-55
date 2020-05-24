#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (C) 2019  David Arroyo Menéndez

# Author: David Arroyo Menéndez <davidam@gnu.org>
# Maintainer: David Arroyo Menéndez <davidam@gnu.org>

# This file is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.

# This file is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with Damemysql; see the file LICENSE.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor,
# Boston, MA 02110-1301 USA,

from unittest import TestCase
import MySQLdb
import pickle

class TestMySQL(TestCase):
    def test_cursor(self):
        db = MySQLdb.connect(host="localhost", user="root", db="sqlexamples")
        cursor = db.cursor()
        s = str(cursor)
        self.assertEqual('<MySQLdb.cursors.Cursor', s[0:23])

    def test_create(self):
        db = MySQLdb.connect(host="localhost", user="root", db="sqlexamples")
        c = db.cursor()
        c.execute("""DROP TABLE breakfast""")
        c.execute("""CREATE TABLE breakfast (name varchar(100), spam int, eggs int, sausage int, price int)""")
        c.executemany(
            """INSERT INTO breakfast (name, spam, eggs, sausage, price)
            VALUES (%s, %s, %s, %s, %s)""",
            [
                ("Spam and Sausage Lover's Plate", 5, 1, 8, 7.95 ),
                ("Not So Much Spam Plate", 3, 2, 0, 3.95 ),
                ("Don't Wany ANY SPAM! Plate", 0, 4, 3, 5.95 )
            ] )
        db.query("""SELECT spam, eggs, sausage FROM breakfast
         WHERE price < 5""")
        r=db.store_result()
        self.assertEqual(r.fetch_row(), ((3, 2, 0),))
