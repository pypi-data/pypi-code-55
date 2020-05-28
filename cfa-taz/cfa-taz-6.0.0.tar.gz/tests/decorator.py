#!/usr/bin/env python
# -*- coding: utf-8 -*-


def waitingdots(func):
    def wrapper(*args, **kwargs):
        print("...")
        return func(*args, **kwargs)

    return wrapper
