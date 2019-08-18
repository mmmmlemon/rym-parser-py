#everything about stats

import math
from tabulate import tabulate
import configparser

graph_symb = "■"

#some global functions n shit
#draw graph (data and labels for data)
def draw_graph(array_data, array_names):
    for i in range(len(array_data)):
        num = array_data[i]
        num_round = math.ceil(num / 2)
        scores_line = graph_symb
        for ii in range(int(num_round)):
            scores_line += graph_symb
        scores_line += " - " + str(array_data[i]) + "({})".format(array_names[i])
        print(scores_line)

#BASIC STATS
def basic_stats(array):
    #calculate everything
    #total num of albums
    print ("Basic statistics")
    albums_total_count = len(array)
    print("Albums total: " + str(albums_total_count))

    #calculate average score
    avg_total = 0
    for i in range (albums_total_count):
        avg_total += array[i][4]
    avg_total = avg_total / albums_total_count
    avg_total = math.ceil(avg_total*10)/10
    print("Average score: " + str(avg_total) + " / 10")

    #TOTAL NUM OF ALL SCORES
    all_scores_list = []
    all_scores_names = []

    for score in range (1, 11):
        count = 0
        for i in range (len(array)):
            if array[i][4] == score:
                count+=1
        all_scores_list.append(count)
        all_scores_names.append(score)
        
    
    #TOTAL NUM OF ALBUMS IN EACH DECADE
    all_decades_count = []
    all_decades_names = []
    
    #create list with all the years, divide it by 10 and floor it, hence we have a list of decades (1970 / 10 + floor = 197)
    all_years_divided = []
    for i in range(len(array)):
        num = array[i][3]
        all_years_divided.append(math.floor(num / 10))
    
    #sort by ascending
    all_years_divided = sorted(all_years_divided)
    #remove duplictaesand and we get a lsit of decades
    all_decades = list(dict.fromkeys(all_years_divided))
    
    #for each element in decades list we do this...
    for d in range(len(all_decades)):
        current_dec = all_decades[d]
        count = 0
        for i in range(len(all_years_divided)):
            if(all_years_divided[i] == current_dec):
                count += 1
        
        all_decades_count.append(count)
        #if decade is 0, then the year of release is unknown
        if(current_dec == 0):
            all_decades_names.append("Year of release is unknown")
        else:
            all_decades_names.append(str(current_dec) + "0")


    #CALCULATE YEAR WITH THE BIGGEST NUM OF ALBUMS
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
    
    
    #CALCULATE THE YEAR WITH THE BIGGEST AVG SCORE
    all_rating_dict = dict.fromkeys(all_years_nodupes)
    
    for y in range(len(all_years_nodupes)):
        current_year = all_years_nodupes[y]
        count = 0
        score = 0
        for i in range(len(array)):
            if(current_year==array[i][3]):
                count += 1
                score += int(array[i][4])
        
        config = configparser.ConfigParser()
        config.read("conf.ini")

        amount = int(config['TOPS']['top-year'])
        
        if(count >= amount):
            all_rating_dict[current_year] = math.ceil((score/count) * 100) /100
        else:
            del all_rating_dict[current_year]

    max_rating = max(all_rating_dict, key=all_rating_dict.get)
    max_rating_score = all_rating_dict[max_rating]
    
    min_rating = min(all_rating_dict, key=all_rating_dict.get)
    min_rating_score = all_rating_dict[min_rating]
    
    #CALCULATE THE DECADE WITH THE BEST AVG SCORE
    max_decade_dict = dict.fromkeys(all_decades)
    
    for d in range(len(all_decades)):
        current_decade = all_decades[d]
        count = 0
        score = 0
        for i in range(len(array)):
            if(current_decade==math.floor(array[i][3]/10)):
                count += 1
                score += int(array[i][4])
        
        config = configparser.ConfigParser()
        config.read("conf.ini")

        amount = int(config['TOPS']['top-decades'])
        
        if(count >= amount):
            max_decade_dict[current_decade] = math.ceil((score/count) * 100) /100
        else:
            del max_decade_dict[current_decade]
    
    
    max_decade_rating = max(max_decade_dict, key=max_decade_dict.get)
    max_decade_score = max_decade_dict[max_decade_rating]
    
    min_decade_rating = min(max_decade_dict, key=max_decade_dict.get)
    min_decade_score = max_decade_dict[min_decade_rating]
    
    
    #printing all the shizzz...

    #decade with best avg score
    print("Decade with best avg score: {}0 ({}/10)".format(str(max_decade_rating), str(max_decade_score)))
    
    #decade with worst avg score
    print("Decade with worst avg score: {}0 ({}/10)".format(str(min_decade_rating), str(min_decade_score)))
                
    #Year with biggest num of albums
    print("Year with biggest count of albums: {}-й ({} шт.)".format(str(max_year), str(max_year_count)))
    
    #year with best avg score
    print("Year with best avg score: {}-й ({}/10)".format(str(max_rating), str(max_rating_score)))
    
    #year with worst avg score
    print("Year with worst avg score: {}-й ({}/10)".format(str(min_rating), str(min_rating_score)))

    #draw graphs
    #ratings graph
    print("\nTotal amount of ratings")
    draw_graph(all_scores_list, all_scores_names)
    #decades graph
    print("\nTotal amount of albums by decade")
    draw_graph(all_decades_count, all_decades_names)

    #decades avg score
    print("\nDecades avg score")
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
        print("No data about this artist")
    else:
        avg_score = math.ceil((avg_score/len(new_array)) * 100) /100
        print("Avg rating: {}/10".format(avg_score))
        print("The best score: {}/10".format(max(score_list)))
        print("The worst score: {}/10".format(min(score_list)))
        print("Total: {}".format(len(new_array)))
        if(command == "default"):
            print(tabulate(new_array, headers = ['RYM Code', 'Artist', 'Album', 'Year', 'Score'], tablefmt="grid"))
        elif(command == "top"):
            new_array = sorted(new_array, key=lambda x: (x[4]), reverse=True)
            print(tabulate(new_array, headers = ['RYM Code', 'Artist', 'Album', 'Year', 'Score'], tablefmt="grid"))
    

def top_artists(array):
    config = configparser.ConfigParser()
    config.read("conf.ini")

    top_art_amount = int(config['TOPS']['top-art'])

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
        if(count >= top_art_amount):
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
            print("{}. {} - {} ({} albums)".format(max_count,max_art, max_score, count_dict[max_art]))
            new_dict[max_art] = 0
            max_count += 1

def top_artists_by_count(array):
    artists_list = []
    for i in range(len(array)):
        artists_list.append(array[i][1])
    
    artists_dict = dict.fromkeys(artists_list)
    count_dict = {}
  
    for i in range(len(artists_list)):
        count = 0
        current_name = array[i][1]
        for j in range(len(array)):
            if(array[j][1] == current_name):
                count += 1
            artists_dict[current_name] = count

   
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
            print("{}. {} - {} albums".format(max_count,max_art, max_score))
            new_dict[max_art] = 0
            max_count += 1
    
def top_years(array):
    config = configparser.ConfigParser()
    config.read("conf.ini")

    amount = int(config['TOPS']['top-years'])
    
    years_list = []
    
    for i in range(len(array)):
        years_list.append(str(array[i][3]))
    
    years_dict = dict.fromkeys(years_list)
    count_dict = {}
    
    for i in range(len(years_list)):
        avg_score = 0
        count = 0
        current_name = str(array[i][3])
        for j in range(len(array)):
              if(str(array[j][3]) == current_name):
                  avg_score += array[j][4]
                  count += 1
        if(count >= amount):
            avg_score = math.ceil((avg_score/count) * 100) /100
            years_dict[current_name] = avg_score
            count_dict[current_name] = count
        else:
            years_dict[current_name] = 0
   
    new_dict = {}
    for k in years_dict.keys():
        if years_dict[k]>0:
            new_dict[k] = years_dict[k]
    
    max_count = 1
    while(max_count != 0):
        max_art = max(new_dict, key=new_dict.get)
        max_score = new_dict[max_art]
        
        if(max_score == 0):
            max_count = 0
        else:
            print("{}. {} - {} ({} albums)".format(max_count,max_art, max_score, count_dict[max_art]))
            new_dict[max_art] = 0
            max_count += 1
    
def top_decades(array):
    config = configparser.ConfigParser()
    config.read("conf.ini")

    amount = int(config['TOPS']['top-decades'])
    
    years_list = []
    
    for i in range(len(array)):
        years_list.append(math.floor(array[i][3] / 10))
    
    decades_dict = dict.fromkeys(sorted(years_list))
    
    decades_list = [k for k  in decades_dict]
    
    count_dict = {}

    for i in range(len(decades_list)):
        
        current_dec = decades_list[i]
        avg_score = 0
        count = 0
        
        for j in range(len(array)):
            current_year_divided = math.floor(array[j][3] / 10)
            if(current_dec == current_year_divided):
              
                avg_score += array[j][4]
                count += 1
              
        if(count >= amount):
            avg_score = math.ceil((avg_score/count) * 100) /100
            decades_dict[current_dec] = avg_score
            count_dict[current_dec] = count
        else:
            decades_dict[current_dec] = 0
                
    new_dict = {}
    for k in decades_dict.keys():
        if decades_dict[k]>0:
            new_dict[k] = decades_dict[k]
            
    
    max_count = 1
    while(max_count != 0):
        max_art = max(new_dict, key=new_dict.get)
        max_score = new_dict[max_art]
        
        if(max_score == 0):
            max_count = 0
        else:
            print("{}. {}0 - {} ({} albums)".format(max_count,max_art, max_score, count_dict[max_art]))
            new_dict[max_art] = 0
            max_count += 1
    

    
    
