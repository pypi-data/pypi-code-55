"""
Exercise # 1 of https://www.w3resource.com/python-exercises/date-time-exercise/index.php
1. Write a Python script to display the various Date Time formats.
"""
from datetime import datetime
import locale

# Idioma "es-ES" (código para el español de España)
locale.setlocale(locale.LC_ALL, 'es-CO')  # Lo sgte no vendria en ingles a no ser por esta linea 5
# print(locale.setlocale.__doc__) De que trata locale?
dt = datetime.now()
print(dt.strftime("%Y-%m-%d %H:%M:%S"))  # strftime es la formatação
print(dt.strftime("%A %d %B %Y %I:%M"))  # strftime es la formatação // %I 12h - %H 24h
print(dt.strftime("%A %d de %B del %Y - %H:%M"))

print(dt)
print('año', dt.year)         # año
print('mes', dt.month)        # mes
print('day', dt.day)          # día

print('hora', dt.hour)         # hora
print('minutos', dt.minute)       # minutos
print('segundos', dt.second)       # segundos
print('microsegundos', dt.microsecond)  # microsegundos

print("{}:{}:{}".format(dt.hour, dt.minute, dt.second))
print("{}/{}/{}".format(dt.day, dt.month, dt.year))

dt = datetime(2020, 5, 25)  # Creando dates
print(dt.strftime("%A %d de %B del %Y - %H:%M"))
