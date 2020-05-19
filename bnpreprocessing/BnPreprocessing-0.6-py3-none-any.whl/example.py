# -*- coding: utf-8 -*-
"""
Created on Sat Apr 25 14:49:35 2020

@author: Kowsher
"""

import BnPreprocessing as bp

s = "আমরা কাজ করবো কিভাবে? ডকুমেন্টটা তৈরী করতে আমাদের সবাইকে কি করতে হবে? নিজেদের(গ্রুপ-৬ এর সবাই) মধ্যে  কাজ ভাগ করবো কেমনে?"

s = bp.remove_punc(s)
print(s)

s = bp.remove_sw(s)
print(s)