# -*- coding: utf-8 -*-

""" 货币

        1. 币种
        2. 金额
"""

from .amount import Amount


__author__ = 'Qingxu Kuang<kuangqingxu@transfereasy.com>'
__version__ = '1.0.5'


class Money(object):

    def __init__(self, *, currency, amount):

        self._currency = currency
        self._amount = Amount(amount)

    @property
    def currency(self):
        return self._currency

    @property
    def amount(self):
        return self._amount

    def __str__(self):
        return f'{self._amount} {self._currency}'

    def __repr__(self):
        return self.__str__()

    def __add__(self, other):
        if not isinstance(other, Money):
            raise TypeError(
                'Cannot add a Money instance with a non-Money instance'
            )
        if self._currency != other.currency:
            raise TypeError(
                f'Cannot add money with different currencies {self._currency} and {other.currency}'
            )

        return self.__class__(
            currency=self._currency,
            amount=self._amount.value + other.amount.value
        )

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        return self.__add__(-other)

    def __rsub__(self, other):
        return other - self

    def __abs__(self):
        return self.__class__(
            currency=self._currency,
            amount=abs(self._amount.value)
        )

    def __neg__(self):
        return self.__class__(
            currency=self._currency,
            amount=-self._amount.value
        )

    def __eq__(self, other):
        if isinstance(other, Money):
            return (
                self._currency == other.currency
            ) and (
                self._amount == other.amount
            )
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __gt__(self, other):
        if not isinstance(other, Money):
            raise TypeError(
                'Money instance cannot be compared with non-Money instance.'
            )
        if self._currency == other.currency:
            return self._amount > other.amount
        else:
            raise TypeError(
                'Different currency instance cannot be compared.'
            )

    def __lt__(self, other):
        if not isinstance(other, Money):
            raise TypeError(
                'Money instance cannot be compared with non-Money instance.'
            )
        if self._currency == other.currency:
            return self._amount < other.amount
        else:
            raise TypeError(
                'Different currency instance cannot be compared.'
            )

    def __ge__(self, other):
        return (self == other) or (self > other)

    def __le__(self, other):
        return (self == other) or (self < other)
