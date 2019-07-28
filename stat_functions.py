import math
import plotly.graph_objects as go

#глобальные переменные
graph_symb = "■"
#цвета для оценок
score_colors = ['#820707', '#ff0000', '#ff8800', '#ffcc00', '#f6ff00', '#d4ff00', '#80ff00', '#22e32c', '#13bd46', '#00ffc3']
#всплывающие заголовки для оценок
score_hovertext = ['/10 - Неистовое убожество', '2/10 - Полный хлам',
'3/10 - Позор', '4/10 - Плохо', '5/10 - Посредственно', '6/10 - Нормально', '7/10 - Хорошо',
'8/10 - Отлично', '9/10 - Замечательно', '10/10 - Любимчик']

#всякие глобальные функции
#нарисовать график по массиву с данными

def draw_graph(array_data, array_names):
    for i in range(len(array_data)):
        num = array_data[i]
        num_round = math.ceil(num / 2)
        #print(num_round)
        scores_line = graph_symb
        for ii in range(int(num_round)):
            scores_line += graph_symb
        scores_line += " - " + str(array_data[i]) + "({})".format(array_names[i])
        print(scores_line)

#ф-ция, базовая статистика
def basic_stats(array):
    #подисчитываем статистику
    #всего альбомов
    print ("Общая статистика")
    albums_total_count = len(array)
    print("Всего альбомов: " + str(albums_total_count) + " шт.")

    #считаем среднюю оценку
    avg_total = 0
    for i in range (albums_total_count):
        avg_total += int(array[i][4])
    avg_total = avg_total / albums_total_count
    avg_total = math.ceil(avg_total*10)/10
    print("Средняя оценка: " + str(avg_total) + " / 10")

    #количество всех оценок
    all_scores_list = []
    all_scores_names = []

    for score in range (1, 11):
        count = 0
        for i in range (len(array)):
            if array[i][4] == str(score):
                count+=1
        all_scores_list.append(count)
        all_scores_names.append(score)
        
    #количество прослушанных альбомов по десятилетиям
    all_decades_list = []
    all_decades_names = []
    
    #создаем список со всеми годами
    all_years_divided = []
    for i in range(len(array)):
        num = array[i][3]
        all_years_divided.append(num)

    #print(all_years_divided)
    
    #количество прослушанных альбомов по годам
    # TO - DO
    
    #рисуем графики
    print("\nОбщее количество оценок")
    draw_graph(all_scores_list, all_scores_names)




