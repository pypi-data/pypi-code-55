#!/usr/bin/python3
# ДАННЫЙ ПРИМЕР МЕНЯЕТ НАПРАВЛЕНИЕ ОСЕЙ:

from time import sleep
from curses import wrapper
# Подключаем библиотеку для работы с джойстиком I2C-flash.
from pyiArduinoI2Cjoystick import *

# Объявляем объект joy для работы с библиотекой, указывая адрес модуля на шине.
j = pyiArduinoI2Cjoystick(0x09)

# Если объявить объект без указания адреса, то адрес будет найден автоматически.
#j = pyiArduinoI2Cjoystick()

a, b, c = 0, 0, 0


#  Изменение направления оси X:

# Читаем установленные  калибровочные значения для оси X в переменные a,b,c.
a, b, c = j.getCalibration_X()

# Сохраняем прочитанные калибровочные значения для оси X,
# но указываем аргументы в обратном порядке: c, b, a.
j.setCalibration_X(c, b, a)


#  Изменение направления оси Y:                  #

# Читаем установленные  калибровочные значения для оси Y в переменные a,b,c.
a, b, c = j.getCalibration_Y()

# Сохраняем прочитанные калибровочные значения для оси Y,
# но указываем аргументы в обратном порядке: c, b, a.
j.setCalibration_Y(c, b, a)

def main(stdscr):

    stdscr.clear()

    print("Текущие координаты: (нажмите <ctrl+c> для выхода)", end="\r\n")

    # Получаем координаты
    x, y = j.getPosition()

    # Выводим  координаты джойстика.
    print("X:Y="+str(x)+":"+str(y))

    print("\r")

    sleep(.1)

    stdscr.refresh()

while True:
    wrapper(main)
