"""
MIT License

Copyright (c) 2020 LidaRandom

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
from typing import List, Dict

from .abc import Database, Field


class InMemoryDB(Database):
    """In memory storage."""

    __slots__ = ["_contracts"]

    def __init__(self, contracts: List[Dict[str, str]]):
        self._contracts = contracts

    def contracts(self, match_field: Field) -> List[Dict[str, str]]:
        matched_contracts = [
            contract
            for contract in self._contracts
            if contract[match_field.name()] == match_field.value()
        ]
        if len(matched_contracts) > 0:
            return matched_contracts
        raise Exception(
            "Invalid Field: name -> {}, value -> {}".format(
                match_field.name(), match_field.value()
            )
        )

    def contains(self, match_field: Field) -> bool:
        for contract in self._contracts:
            if contract[match_field.name()] == match_field.value():
                return True
        return False


__all__ = ["InMemoryDB"]
