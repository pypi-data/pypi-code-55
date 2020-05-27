# -*- coding: utf-8 -*-
#
# Copyright (c) 2020 Instituto Tecnológico de Canarias, S.A.
#
# This file is part of GsRest
# (see https://github.com/esuarezsantana/gsrest).
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
"""Helper functions for the gsrest package.
"""

import functools


# I tried to create delegated properties dynamically like this:
#
#     for sub in some_subattributes:
#         setattr(cls, sub, property(
#             lambda obj: getattr(obj.attr, sub),
#             lambda obj, value: setattr(obj.attr, sub, value)
#             ))
#
# but there is bug in this snippet. The lambda function closes the variable
# 'sub' lexically, so just gets evaluated when the lambda function is called.
# So that, only the last loop value of 'sub' is applied to every lambda call.
#
# The solution comes taking the variable out of the lambda.
# See https://stackoverflow.com/a/2295368
#
# A working snippets using double lambda would look like this:
#
#     for sub in some_subattributes:
#         setattr(cls, sub, property(
#             (lambda x: lambda obj: getattr(self.attr, x))(sub),
#             (lambda x: lambda obj, value: setattr(self.attr, x, value))(sub)
#             ))
#
# but finally I came with a solution using next function.
#
#     for sub in some_subattributes:
#         setattr(cls, sub, property(*subaccessors('attr', sub)))
#
def subaccessors(*args):
    """Getter and setter functions for recursive attributes.

    This is best understood with an example. Say you have recursively
    aggregated several objects, so you can access a deep attribute like this:

    avalue = a.b.c.d
    a.b.c.d = anothervalue

    This function provides getter and setter methods, so we can access the
    inner attribute like this:

    getter, setter = subaccessors('b', 'c', 'd')
    avalue = getter(a)
    setter(a, anothervalue)

    Args:
        *args (str): Name of recursive attributes.

    Returns:
        getter (callable): accesor to get the value of the deep attribute
        setter (callable): accesor to set the value of the deep attribute

    """

    def getter(self):
        return functools.reduce(getattr, args, self)

    def setter(self, value):
        subobj = functools.reduce(getattr, args[:-1], self)
        setattr(subobj, args[-1], value)

    return getter, setter


def separate_on_pred(alist, pred):
    """Split a list in head and tail based on a predicate.

    Elements will belong to the head list until the predicate is satisfied (not
    included in the head). Then, the rest of the elements will belong to the
    tail, including the first element to satisfy the predicate.

    Args:
        alist (list): The list to be splitten.
        pred (callable): A function that returns a boolean for a list element.

    Returns:
        head(list): The head of the list.
        tail(list): The tail of the list.

    """

    def reduce_fun(triad, elem):
        if triad[2] or pred(elem):
            return triad[0], triad[1] + [elem], True
        return triad[0] + [elem], triad[1], False

    head, tail, _ = functools.reduce(reduce_fun, alist, ([], [], False))
    return head, tail


def set_if_missing(obj, attribute, value):
    """Sets an attribute to an object if missing or bools to False.

    Args:
        obj (Any): the object
        attribute (str): the attribute name
        value (Any): the attribute value

    """
    if not hasattr(obj, attribute) or not getattr(obj, attribute):
        setattr(obj, attribute, value)


def camelcase(word):
    """Turns an underscore_word to camelCase.

    See https://stackoverflow.com/a/6425628.
    """
    return "".join(
        (x.capitalize() or "_") if n else x
        for n, x in enumerate(word.split("_"))
    )
