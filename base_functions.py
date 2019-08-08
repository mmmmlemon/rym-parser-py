#содержит базовые функции программы
import os
import io
import configparser
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
        album_display = sorted(album_display,key=lambda x: (x[1],x[3]))

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
        
    if(len(new_array) == 0):
        print("Нет записей за этот год")
    else:
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

#ф-ция, справка по командам
def help():
    print("bs - Общая статистика")
    print ("as - Список всех альбомов")
    print ("chf - Изменить имя файла с данными")

