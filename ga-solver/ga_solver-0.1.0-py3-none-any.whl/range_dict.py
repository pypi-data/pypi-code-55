"""
Provides the RangeDict class. Useful for problems
where one needs to find a value whose key lies
between a range
"""

from collections import UserDict

# pylint: disable=too-many-ancestors
class RangeDict(UserDict):
    """
    RangeDict allows the user to store values using ranges as keys.

    >>> ra = RangeDict()
    >>> ra[(0, 10)] = "a"
    >>> ra[(10, 20)] = "b"
    >>> ra[2]
    "a"
    >>> ra[5]
    "b"

    As the usual in computing, the ranges are closed in the lower bound and
    open in the upper bound. That is, the example above we have:

    >>> ra[10]
    "b"
    >>> ra[0]
    "a"
    >>> ra[20]
    KeyError
    """

    def __setitem__(self, key, item):
        """
        Sets a new item

        TODO:

            1. Check if key is a tuple
            2. Check if key[0] < key[1]
            3. Check if there are no overlaps
               between the current keys and
               the new one
            4. We can actually use range()
               objects as keys! They do not
               support decimals, w/ the
               `in` operator, though.
        """
        # pylint: disable=useless-super-delegation
        return super().__setitem__(key, item)

    def __getitem__(self, key):
        """
        Returns the item between the range

        TODO:

            We're dealing with numbers and ranges, there are lots of
            optimization to be done, like using a binary search!
        """
        for key_, value in self.data.items():
            if key_[0] <= key < key_[1]:
                return value

        return KeyError
