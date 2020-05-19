"""
Exercise # 14 of https://www.w3resource.com/python-exercises/date-time-exercise/index.php
Write a Python program to find the date of the first Monday of a given week
Sample Year and week : 2015, 50
Expected Output : Mon Dec 14 00:00:00 2015
"""
import time


def calculate_first_monday_of_a_week(year, week):
    return time.asctime(time.strptime(f'{year} {week} 1', '%Y %W %w'))


print(calculate_first_monday_of_a_week(2015, 50))
