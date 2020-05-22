#!/usr/bin/python3
# ДАННЫЙ ПРИМЕР ВЫВОДИТ СЫРЫЕ ЗНАЧЕНИЯ АЦП:

from time import sleep
from curses import wrapper

# Подключаем библиотеку для работы с джойстиком I2C-flash.
from pyiArduinoI2Cjoystick import *

# Объявляем объект для работы с библиотекой, указывая адрес модуля на шине.
j = pyiArduinoI2Cjoystick(0x09)

# Если объявить объект без указания адреса, то адрес будет найден автоматически.
#j = pyiArduinoI2Cjoystick()


def main(stdscr):

    stdscr.clear()

    print("Текущие координаты: (нажмите <ctrl+c> для выхода)", end="\r\n")

    # Получаем и выводим АЦП по отдельности:

    print("X=", end='')

    # Выводим показания АЦП снятые с потенциометра установленного
    # на оси X джойстика, значение от 0 до 4095.
    print(j.ax, end='')

    print(", Y=", end='')

    # Выводим показания АЦП снятые с потенциометра установленного
    # на оси Y джойстика, значение от 0 до 4095.
    print(j.ay, end='')

    # Получаем сразу оба значения АЦП джойстика:
    x, y = j.getADC()

    print( ", X:Y=" + str(x) + ":" + str(y), end="\r\n")

    sleep(.1)

    stdscr.refresh()

while True:

    wrapper(main)
