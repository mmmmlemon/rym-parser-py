#импорт библиотеки для чтения с кодировками
import io
import os
#импорт бибилиотеки для рисования таблиц
from tabulate import tabulate

#импортируем свои файлы
from base_functions import *
from stat_functions import *

clear = lambda: os.system('cls')

#главная ф-ция
def main_func():
    print("Rate Your Music Parser v 0.1")
    print("Пишите комнады внизу")
    command = ""
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
            change_filename(filename)
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

global_filename = "albums"
global_album_list = load_file(global_filename)

clear()


#запускаем главную ф-цию
main_func()


    



                









