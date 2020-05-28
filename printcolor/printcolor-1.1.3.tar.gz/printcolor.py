#!/usr/bin/env python
import sys
class PrintColor:
    def __init__(self):
        self.__show_type = {"default":0, "hlt":1, "underline":4, "flash": 5}
        self.__front_type = {"black":30, "red": 31, "green":32, "yellow":33, "blue":34, "carmine":35, "cyan":36, "white":37}
        self.__back_type = {"black":40, "red": 41, "green":42, "yellow":43, "blue":44, "carmine":45, "cyan":46, "white":47}
    def color(self,*args,show="default", front="green",back=''):
        if back == '':
            try:
                show = self.__show_type[show]
                front = self.__front_type[front]
                print ("\033[%d;%dm%s \033[0m" % (show,front,' '.join(args)))
            except KeyError as e:
                print("Please confirm your prameters")
        else:
            try:
                show = self.__show_type[show]
                front = self.__front_type[front]
                back = self.__back_type[back]
                print ("\033[%d;%d;%dm%s \033[0m" % (show,front,back,' '.join(args)))
            except KeyError as e:
                print("Please confirm your prameters")
