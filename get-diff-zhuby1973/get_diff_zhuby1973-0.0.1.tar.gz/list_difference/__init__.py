#!/usr/bin/python
import os
import sys

def get_diff(list1, list2):
   difference = set(list1).symmetric_difference(set(list2))
   list_difference = list(difference)
   if len(list_difference) == 0:
       print("same list[]")
   else:
       print('please check below difference:')
       print(list_difference)