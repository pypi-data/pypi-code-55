#!/usr/bin/python3
# ДАННЫЙ ПРИМЕР ВЫВОДИТ КООРДИНАТЫ ДЖОЙСТИКА:

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

    # Получаем и выводим координаты по отдельности: #

    print("X=", end='')

    # Выводим координату по оси X, значение от -100 до 100.
    print(j.x, end='')

    print(", Y=", end='')

    # Выводим координату по оси Y, значение от -100 до 100.
    print(j.y, end='')

    # Получаем сразу обе координаты:
    x, y = j.getPosition()

    print(", X:Y=", end='')

    # Выводим координату по оси X, значение от -100 до 100.
    print(x, end='')

    print(":", end='')

    # Выводим координату по оси X, значение от -100 до 100.
    print(y, end="\r\n")

    sleep(.1)

    stdscr.refresh()

while True:

    wrapper(main)
