"""
Exercise # 2 of https://www.w3resource.com/python-exercises/date-time-exercise/index.php
 - Write a Python program to determine whether a given year is a leap year
Execute on terminal python -m doctest -v example.py in order to test

>>> calc_year_leap(2004)
True
>>> calc_year_leap(2004)
True
>>> calc_year_leap(2008)
True
>>> calc_year_leap(2012)
True
>>> calc_year_leap(2016)
True
>>> calc_year_leap(2020)
True
>>> calc_year_leap(2024)
True
>>> calc_year_leap(2028)
True
>>> calc_year_leap(2032)
True
>>> calc_year_leap(2036)
True
>>> calc_year_leap(2040)
True
>>> calc_year_leap(2044)
True
>>> calc_year_leap(2048)
True
>>> calc_year_leap(2052)
True
>>> calc_year_leap(2056)
True
>>> calc_year_leap(2060)
True
>>> calc_year_leap(2064)
True
>>> calc_year_leap(2068)
True
>>> calc_year_leap(2072)
True
>>> calc_year_leap(2076)
True
>>> calc_year_leap(2080)
True
>>> calc_year_leap(2084)
True
>>> calc_year_leap(2088)
True
"""


def calc_year_leap(year):
    if (year/4).is_integer():
        return True
    else:
        return False


if __name__ == '__main__':
    print(calc_year_leap(2004))
