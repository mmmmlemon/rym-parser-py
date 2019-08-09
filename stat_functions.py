import math
from tabulate import tabulate

#глобальные переменные
graph_symb = "■"

#всякие глобальные функции
#нарисовать график по массивам с данными
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
        avg_total += array[i][4]
    avg_total = avg_total / albums_total_count
    avg_total = math.ceil(avg_total*10)/10
    print("Средняя оценка: " + str(avg_total) + " / 10")

    #ОБЩЕЕ КОЛИЧЕСТВО ОЦЕНОК
    #количество всех оценок
    all_scores_list = []
    all_scores_names = []

    for score in range (1, 11):
        count = 0
        for i in range (len(array)):
            if array[i][4] == score:
                count+=1
        all_scores_list.append(count)
        all_scores_names.append(score)
        
    
    #КОЛИЧЕСТВО ЗАПИСЕЙ ПО ДЕКАДАМ
    all_decades_count = []
    all_decades_names = []
    
    #создаем список со всеми годами, делим год на 10 и окгругляем вниз, т.о получаем список декад
    all_years_divided = []
    for i in range(len(array)):
        num = array[i][3]
        all_years_divided.append(math.floor(num / 10))
    
    #сортируем список декад по возрастанию
    all_years_divided = sorted(all_years_divided)
    #убираем дубликаты и получаем итоговый список декад, при помощи этого списка будем считать 
    all_decades = list(dict.fromkeys(all_years_divided))
    
    #для каждого элемента в списке декад прогоняем цикл
    for d in range(len(all_decades)):
        current_dec = all_decades[d]
        count = 0
        for i in range(len(all_years_divided)):
            if(all_years_divided[i] == current_dec):
                count += 1
        
        all_decades_count.append(count)
        #если декада = 0, то год у записи неизвестен
        if(current_dec == 0):
            all_decades_names.append("Год неизвестен")
        else:
            all_decades_names.append(str(current_dec) + "0")


    #НАХОДИМ ГОД С НАИБОЛЬШИМ КОЛ-ВОМ ЗАПИСЕЙ
    all_years = []
    all_years_nodupes = []
    
    for i in range(len(array)):
        all_years.append(array[i][3])
    
    all_years_dict = dict.fromkeys(sorted(all_years))
    all_years_nodupes = list(all_years_dict)
    
    for y in range(len(all_years_nodupes)):
        current_year = all_years_nodupes[y]
        count = 0
        for i in range(len(all_years)):
            if(current_year == all_years[i]):
                count += 1
        all_years_dict[current_year] = count

    max_year = max(all_years_dict, key=all_years_dict.get)
    max_year_count = all_years_dict[max_year]
    
    
    #НАХОДИМ ГОД С НАИВЫСШИМ РЕЙТИНГОМ (если записей 5 и более)
    all_rating_dict = dict.fromkeys(all_years_nodupes)
    
    for y in range(len(all_years_nodupes)):
        current_year = all_years_nodupes[y]
        count = 0
        score = 0
        for i in range(len(array)):
            if(current_year==array[i][3]):
                count += 1
                score += int(array[i][4])
        
        if(count >= 5):
            all_rating_dict[current_year] = math.ceil((score/count) * 100) /100
        else:
            del all_rating_dict[current_year]

    max_rating = max(all_rating_dict, key=all_rating_dict.get)
    max_rating_score = all_rating_dict[max_rating]
    
    min_rating = min(all_rating_dict, key=all_rating_dict.get)
    min_rating_score = all_rating_dict[min_rating]
    
    #НАХОДИМ ДЕСЯТИЛЕТИЕ С ЛУЧШИМ РЕЙТИНГОМ
    max_decade_dict = dict.fromkeys(all_decades)
    
    for d in range(len(all_decades)):
        current_decade = all_decades[d]
        count = 0
        score = 0
        for i in range(len(array)):
            if(current_decade==math.floor(array[i][3]/10)):
                count += 1
                score += int(array[i][4])
        
        if(count >= 10):
            max_decade_dict[current_decade] = math.ceil((score/count) * 100) /100
        else:
            del max_decade_dict[current_decade]
    
    
    max_decade_rating = max(max_decade_dict, key=max_decade_dict.get)
    max_decade_score = max_decade_dict[max_decade_rating]
    
    min_decade_rating = min(max_decade_dict, key=max_decade_dict.get)
    min_decade_score = max_decade_dict[min_decade_rating]
    

    #десятилетие с лучшим ср. рейтингом
    print("Десятилетие с лучшим ср. рейтингом: {}0 ({}/10)".format(str(max_decade_rating), str(max_decade_score)))
    
    #десятилетие с худшим ср. рейтингом
    print("Десятилетие с худшим ср. рейтингом: {}0 ({}/10)".format(str(min_decade_rating), str(min_decade_score)))
                
    #год с наибольшим кол-вом записей
    print("Год с наибольшим кол-вом записей: {}-й ({} шт.)".format(str(max_year), str(max_year_count)))
    
    #год с наивысшим ср. рейтингом 
    print("Год с лучшим ср. рейтингом: {}-й ({}/10)".format(str(max_rating), str(max_rating_score)))
    
    #год с наименьшим ср. рейтингом 
    print("Год с худшим ср. рейтингом: {}-й ({}/10)".format(str(min_rating), str(min_rating_score)))

    #рисуем графики по полученным данным
    #график по оценкам
    print("\nОбщее количество оценок")
    draw_graph(all_scores_list, all_scores_names)
    #график по кол-ву альбомов по декадам
    print("\nКоличество записей по декадам")
    draw_graph(all_decades_count, all_decades_names)

    #ср. рейтинг у десятилетий
    print("\nСредний рейтинг у десятилетий")
    for i in max_decade_dict:
        print("{}0 - ({}/10)".format(i, max_decade_dict[i]))
    

def artist_basic_stat(array, artist_name, command):
    new_array = []
    avg_score = 0
    score_list = []
    for i in range(len(array)):
        if array[i][1].lower() == artist_name.lower():
            new_array.append(array[i])
            avg_score += array[i][4]
            score_list.append(array[i][4])
            
    if(len(new_array) == 0):
        print("Нет записей об этом исполнителе")
    else:
        avg_score = math.ceil((avg_score/len(new_array)) * 100) /100
        print("Средняя оценка: {}/10".format(avg_score))
        print("Самая высокая оценка: {}/10".format(max(score_list)))
        print("Самая низкая оценка: {}/10".format(min(score_list)))
        print("Всего записей: {}".format(len(new_array)))
        if(command == "default"):
            print(tabulate(new_array, headers = ['RYM Code', 'Artist', 'Album', 'Year', 'Score'], tablefmt="grid"))
        elif(command == "top"):
            new_array = sorted(new_array, key=lambda x: (x[4]), reverse=True)
            print(tabulate(new_array, headers = ['RYM Code', 'Artist', 'Album', 'Year', 'Score'], tablefmt="grid"))
    

def top_artists(array):
    artists_list = []
    
    for i in range(len(array)):
        artists_list.append(array[i][1])
    
    artists_dict = dict.fromkeys(artists_list)
    count_dict = {}
  
    for i in range(len(artists_list)):
        avg_score = 0
        count = 0
        current_name = array[i][1]
        for j in range(len(array)):
              if(array[j][1] == current_name):
                  avg_score += array[j][4]
                  count += 1
        if(count >= 5):
            avg_score = math.ceil((avg_score/count) * 100) /100
            artists_dict[current_name] = avg_score
            count_dict[current_name] = count
        else:
            artists_dict[current_name] = 0
   
    new_dict = {}
    for k in artists_dict.keys():
        if artists_dict[k]>0:
            new_dict[k] = artists_dict[k]
      
    
    max_count = 1
    while(max_count != 0):
        max_art = max(new_dict, key=new_dict.get)
        max_score = new_dict[max_art]
        
        if(max_score == 0):
            max_count = 0
        else:
            print("{}. {} - {} ({} шт.)".format(max_count,max_art, max_score, count_dict[max_art]))
            new_dict[max_art] = 0
            max_count += 1
    
    
    
    
    
