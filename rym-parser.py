#импорт библиотеки для чтения с кодировками
import io
import os
#импорт бибилиотеки для рисования таблиц
from tabulate import tabulate
import math

clear = lambda: os.system('cls')

#ф-ция, загрузить файл и преобразовать его в массив для последующей работы
def load_file(filename):

    if(os.path.isfile("./"+filename+".txt")):
        #открываем файл и читаем его содержимое
        file = io.open(filename+".txt", "r", encoding='utf8')

        #сохраняем содержимое файла в переменной строки
        file_string = file.read()

        #считаем количество строк в тексте
        num_of_lines = 0
        with io.open(filename + ".txt", "r", encoding='utf8') as f:
            num_of_lines = sum(1 for _ in f)

        #ищем индекс начала слова Review, принимаем его за начальный, с него начинаем читать файл
        index_start = file_string.find("Review")

        #общий массив для всех альбомов
        album_array = []

        #начинаем цикл, ходим по строкам и записываем данные в общий массив
        for i in range (1, num_of_lines):
            #массив для текущего альбома в цикле
            current_album = []

            #в каждой строке 12 параметров, вытаскиваем их все
            for a in range (0, 12):
                #определяем начало и конец кажого параметра при помощи кавычек
                #кавычка в начале
                idx_firstQ = file_string.find('\"', index_start) + 1
                #кавычка в конце
                idx_lastQ = file_string.find('\"', idx_firstQ)
                #получаем подстроку при помощи индексов кавычек
                txt = file_string[idx_firstQ:idx_lastQ]
                if txt != "" and a != 10 and a != 8 or a == 6 or a == 1 or a == 2 or a == 3 or a == 4:
                    current_album.append(txt)
                
                index_start = file_string.find(",",idx_lastQ)

            #когда получили все параметры, находим переход на новую строку и делаем его новой стартовой позицией
            idx_nl = file_string.find('\n',idx_lastQ)
            index_start = idx_nl
            album_array.append(current_album)

        #создаем новую переменную для форматирования и вывода, копируем в неё данные из старой
        album_display = album_array

        #объединяем наименования исполниелей
        for i in range(len(album_display)):
            space_char = ""
            if album_display[i][1] != "":
                space_char = " "
            album_display[i][1] += space_char + album_display[i][2]
            del album_display[i][2]
            del album_display[i][2]
            del album_display[i][2]


        #сортировка списка по алфавиту и году выпуска альбома
        album_display = sorted(album_display,key=lambda x: (x[1],x[3]))

        return album_display
    else:
        print("File does not exist")
        return 0

#ф-ция, вывод альбомов в виде таблицы
def show_album_spreadsheet(array):
    print(tabulate(array, headers = ['RYM Code', 'Artist', 'Album', 'Year', 'Score'], tablefmt="grid"))

#ф-ция, базовая статистика
def basic_stats(array):
    #подисчитываем статистику
    #всего альбомов
    print ("Basic statistics")
    albums_total_count = len(array)
    print("Albums total: " + str(albums_total_count) + " albums")

    #считаем среднюю оценку
    avg_total = 0
    for i in range (albums_total_count):
        avg_total += int(array[i][4])
    avg_total = avg_total / albums_total_count
    avg_total = math.ceil(avg_total*10)/10
    print("Avg. score: " + str(avg_total) + " / 10")

    #количество всех оценок
    all_scores_list = []

    for score in range (1, 11):
        count = 0
        for i in range (len(array)):
            if array[i][4] == str(score):
                count+=1
        all_scores_list.append(count)

    print("Scores total:")
    for i in range(len(all_scores_list)):
        num = all_scores_list[i]
        num_round = math.ceil(num / 10)
        scores_line = ""
        for ii in range(int(num_round)):
            scores_line += "■"
        scores_line += " - " + str(all_scores_list[i]) + "({})".format(i+1)
        print(scores_line)

def change_filename(new_filename):
    global global_filename
    global_filename = new_filename
    global global_album_list
    global_album_list = load_file(new_filename)
    if (global_album_list != 0):
        print("File name was successfully changed")

#ф-ция, справка по командам
def help():
    print("bs - Basic statistics")
    print ("as - Albums spreadsheet")
    print ("chf - Change the name of the data file")

#главная ф-ция
def main_func():
    print("Rate Your Music Parser v 0.1")
    print("Type commands below")
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
        else:
            print("No such command")


global_filename = "albums"
global_album_list = load_file(global_filename)

clear()

#запускаем главную ф-цию
main_func()


    



                









