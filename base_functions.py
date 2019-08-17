#содержит базовые функции программы
import os
import io
import csv
import configparser
import math
from tabulate import tabulate
from pathlib import Path

#ф-ция, загрузить файл и преобразовать его в массив для последующей работы
def load_file(filename):
    if(os.path.isfile("./"+filename)):
        #открываем файл и читаем его содержимое
        file = io.open(filename, "r", encoding='utf8')

        #сохраняем содержимое файла в переменной строки
        file_string = file.read()

        #считаем количество строк в тексте
        num_of_lines = 0
        with io.open(filename, "r", encoding='utf8') as f:
            num_of_lines = sum(1 for _ in f)

        #ищем индекс начала слова Review, принимаем его за начальный, с него начинаем читать файл
        index_start = file_string.find("Review")

        #общий массив для всех альбомов
        album_array = []


        artists_csv_dict = {}

        with open('artists.txt', mode='r') as csv_file:
            reader = csv.reader(csv_file)
            artists_csv_dict = dict(reader)
        
        
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
                    if a == 6 or a == 7:
                        if txt == "":
                            txt = "0"
                        txt = int(txt)
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
        album_display = sorted(album_display,key=lambda x: (x[1].lower(),x[3]))

        return album_display
    else:
        print("Файл не существует")
        return 0
        
#ф-ция, вывод альбомов в виде таблицы
def show_album_spreadsheet(array, command):
    if (command == "default"):
        print(tabulate(array, headers = ['RYM Code', 'Artist', 'Album', 'Year', 'Score'], tablefmt="grid"))
    elif(command == "top"):
        album_display = sorted(array,key=lambda x: (x[4]), reverse=True)
        print(tabulate(album_display, headers = ['RYM Code', 'Artist', 'Album', 'Year', 'Score'], tablefmt="grid"))
    elif(command == "bottom"):
        album_display = sorted(array,key=lambda x: (x[4]))
        print(tabulate(album_display, headers = ['RYM Code', 'Artist', 'Album', 'Year', 'Score'], tablefmt="grid"))
        
def show_album_spreadsheet_by_year(array, year, command):
    new_array = []
    indexes = []
    for i in range(len(array)):
        if(array[i][3]==int(year)):
            new_array.append(array[i])
        
    scores_list = []
    #считаем средний рейтинг
    avg_score = 0
    for i in range(len(new_array)):
        avg_score += new_array[i][4]
        scores_list.append(new_array[i][4])
        
    avg_score = math.ceil((avg_score/len(new_array)) * 100) /100
    
    if(len(new_array) == 0):
        print("Нет записей за этот год")
    else:
        if(command == "default"):
            new_array = sorted(new_array, key=lambda x: (x[1].lower()))
        elif(command=="top"):
            new_array = sorted(new_array, key=lambda x: (x[4]),reverse = True)
            
        print("Средняя оценка за год: {}/10".format(avg_score))
        print("Самая высокая оценка: {}".format(max(scores_list)))
        print("Самая низкая оценка: {}".format(min(scores_list)))
        print(tabulate(new_array, headers = ['RYM Code', 'Artist', 'Album', 'Year', 'Score'], tablefmt="grid"))
   
#ф-ция, изменить имя файла
def change_filename(new_filename):
    my_file = Path("./"+new_filename)
    if my_file.is_file():
        source_filename = new_filename
        config = configparser.ConfigParser()
        config.read("conf.ini")
        config['BASIC'] = {'file': new_filename}
        with open('conf.ini', 'w') as configfile:
            config.write(configfile)
        return new_filename
    else:
        print("Нет такого файла")
        return 0

#ф-ция, изменить кол-во альбомов для топа исполнителей
def set_amount_for_top_art(amount):
     config = configparser.ConfigParser()
     config.read("conf.ini")
     config['TOPS']['top-art'] = amount
     with open('conf.ini', 'w') as configfile:
            config.write(configfile)
     print("Количество альбомов для top-art было изменено на {}".format(amount))
     
#ф-ция, изменить кол-во альбомов для топа исполнителей
def set_amount_for_top_years(amount):
     config = configparser.ConfigParser()
     config.read("conf.ini")
     config['TOPS']['top-years'] = amount
     with open('conf.ini', 'w') as configfile:
            config.write(configfile)
     print("Количество альбомов для top-years было изменено на {}".format(amount))
     
#ф-ция, изменить кол-во альбомов для топа десятилетий
def set_amount_for_top_decades(amount):
     config = configparser.ConfigParser()
     config.read("conf.ini")
     config['TOPS']['top-decades'] = amount
     with open('conf.ini', 'w') as configfile:
            config.write(configfile)
     print("Количество альбомов для top-decades изменено на {}".format(amount))

#ф-ция, добавить имя в список имен для замены - исполнители
#def add_artist_for_replace(old_name, new_name):
    

#ф-ция, справка по командам
def help():
    print("bs - Общая статистика")
    print ("\nas - Список всех альбомов")
    print ("as-top - Список всех альбомов (от высоких оценок к низким)")
    print ("as-bottom - Список всех альбомов (от низких оценок к высоким)")
    print ("as-year - Список альбомов за выбранный год")
    print ("as-year-top - Топ альбомов за выбранный год")
    print ("\nars - Общая статисткиа по исполнителю")
    print ("ars-top - Общая статисткиа по исполнителю с топом альбомов")
    print ("\ntop-art - Топ исполнителей по рейтингу")
    print("\ntop-art-count - Топ исполнителей по кол-ву записей")
    print ("top-years - Топ годов по рейтингу")
    print ("top-decades - Топ десятилетий по рейтингу")
    print ("\nchf - Изменить имя файла с данными")

