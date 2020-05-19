"""
Excercise # 7 of https://www.w3resource.com/python-exercises/date-time-exercise/index.php
Write a Python program to print yesterday, today, tomorrow.

"""
import datetime
today = datetime.date.today()
yesterday = today - datetime.timedelta(days=1)
tomorrow = today + datetime.timedelta(days=1)
print('Yesterday : ', yesterday)
print('Today : ', today)
print('Tomorrow : ', tomorrow)
