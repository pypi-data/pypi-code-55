"""Server program"""

import sys
import os
import argparse
import logging
import configparser
import logs.config_server_log
from soc_settings.decorator import log
from soc_settings.utils import *
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication
from server.core import MessageProcessor
from server.server_dbase import ServerDBase
from server.main_window import MainWindow

# Инициализация логирования сервера.
logger = logging.getLogger('server')


# Парсер аргументов коммандной строки.
@log
def create_arg_parser(default_port, default_address):
    """
    Парсер аргументов коммандной строки
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', default=default_port, type=int, nargs='?')
    parser.add_argument('-a', default=default_address, nargs='?')
    parser.add_argument('--no_gui', action= 'store_true')
    namespace = parser.parse_args(sys.argv[1:])
    listen_address = namespace.a
    listen_port = namespace.p
    gui_flag = namespace.no_gui
    return listen_address, listen_port, gui_flag


# Загрузка файла конфигурации сервера
def config_load():
    config = configparser.ConfigParser()
    dir_path = os.path.dirname(os.path.realpath(__file__))
    config.read(f"{dir_path}/{'server.ini'}")
    # Если конфиг файл загружен правильно, запускаемся, иначе конфиг по умолчанию.
    if 'SETTINGS' in config:
        return config
    else:
        config.add_section('SETTINGS')
        config.set('SETTINGS', 'Default_port', str(DEFAULT_PORT))
        config.set('SETTINGS', 'Listen_Address', '')
        config.set('SETTINGS', 'Database_path', '')
        config.set('SETTINGS', 'Database_file', 'server_database.db3')
        return config


def main():
    # Загрузка файла конфигурации сервера
    config = config_load()
    # Загрузка параметров командной строки,
    # если нет параметров, то задаём значения по умолчанию
    listen_address, listen_port, gui_flag = create_arg_parser(
        config['SETTINGS']['Default_port'], config['SETTINGS']['Listen_Address'])

    # Инициализация базы данных
    database = ServerDBase(os.path.join(config['SETTINGS']['Database_path'], config['SETTINGS']['Database_file']))

    # Создание экземпляра класса - сервера и его запуск.
    server = MessageProcessor(listen_address, listen_port, database)
    server.daemon = True
    server.start()

    # Если указан параметр без GUI то запускаем простенький обработчик консольного ввода
    if gui_flag:
        while True:
            command = input('Введите exit для завершения работы сервера')
            if command == 'exit':
                # Если выход, то завершаем основной цикл сервера
                server.running = False
                server.join()
                break
    # Если не указан запуск без GUI, то запускаем GUI
    else:
        # Создаем графическое окружение для сервера
        server_app = QApplication(sys.argv)
        server_app.setAttribute(Qt.AA_DisableWindowContextHelpButton)
        main_window = MainWindow(database, server, config)

    # Запускаем GUI
    server_app.exec_()

    # По закрытию окон останавливаем обработчик сообщений
    server.running = False

if __name__ == '__main__':
    main()
