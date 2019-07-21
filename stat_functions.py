import math
import plotly.graph_objects as go

#глобальные переменные
#цвета для оценок
score_colors = ['#820707', '#ff0000', '#ff8800', '#ffcc00', '#f6ff00', '#d4ff00', '#80ff00', '#22e32c', '#13bd46', '#00ffc3']
#всплывающие заголовки для оценок
score_hovertext = ['1/10 - Неистовое убожество', '2/10 - Полный хлам',
'3/10 - Позор', '4/10 - Плохо', '5/10 - Посредственно', '6/10 - Нормально', '7/10 - Хорошо',
'8/10 - Отлично', '9/10 - Замечательно', '10/10 - Любимчик']

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

    layout = go.Layout(
    xaxis = go.layout.XAxis(
        tickmode = 'linear',
        tick0 = 1,
        dtick = 1
    ))

    
    fig = go.Figure(data=go.Bar(x=all_scores_names,y=all_scores_list, marker_color=score_colors, hovertext = score_hovertext),layout_title_text="Общая статистика ({} альбомов)".format(albums_total_count), layout=layout)
    fig.show()
