#импорт библиотеки для чтения с кодировками
import io
import os
#импорт бибилиотеки для рисования таблиц
from tabulate import tabulate
#бибилотека для чтения конфигов
import configparser

#импортируем свои файлы
from base_functions import *
from stat_functions import *

clear = lambda: os.system('cls')
config = configparser.ConfigParser()
config.read("conf.ini")


#главная ф-ция
def main_func():
    print("Rate Your Music Parser v 0.1")
    print("Пишите комнады внизу")
    command = ""
    global global_album_list
    global global_filename
    while command != "exit":
        print("cmd: ")
        command = input()
        #basic stats
        if command == "bs":
            if(global_album_list != 0):
                clear()
                basic_stats(global_album_list)
        #albums spreadsheet
        elif command == "as":
            if(global_album_list != 0):
                clear()
                show_album_spreadsheet(global_album_list)
        #change filename
        elif command == "chf":
            clear()
            print("New file name: ")
            filename = input()
            if(change_filename(filename) != 0):
                global_filename = change_filename(filename)
                global_album_list = load_file(global_filename)
                print ("Файл был изменен!")
        #help
        elif command == "help":
            clear()
            help()
        #exit the program
        elif command == "exit":
            break
        elif command == "g":
            clear()

        else:
            print("Нет такой команды")

global_filename = config['BASIC']['file']

global_album_list = load_file(global_filename)

#clear()

#запускаем главную ф-цию
main_func()


    



                









