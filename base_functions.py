#contains the basic functions of the program, like loading the data file, changing the data file name etc.

import os
import io
import csv
import configparser
import math
import html
from tabulate import tabulate
from pathlib import Path

#load the data from the data file
def load_file(filename):
    #check if data file exists
    if(os.path.isfile("./"+filename)):
        #open the file and read it
        file = io.open(filename, "r", encoding='utf8')

        #saving the contents of file in file_string var
        file_string = file.read()

        #count the number of strings in the data file
        num_of_lines = 0
        with io.open(filename, "r", encoding='utf8') as f:
            num_of_lines = sum(1 for _ in f)

        #first we find the "Review" word index, take it as a start position, and read the rest of the file from here
        index_start = file_string.find("Review")

        #a list of LISTS for all the albums
        #each index is a list inside of a "album_array" list, that has all the info about the album
        album_array = []

        #a dictionary for artists name replacements 
        artists_csv_dict = {}
        
        #loading the name replacements
        with open('artists.csv', mode='r', encoding='utf-8') as csv_file:
            reader = csv.reader(csv_file)
            artists_csv_dict = dict(reader)
        
        #trim spaces in replacements (wtf where they even come from???)
        for a in artists_csv_dict.values():
            a = a.strip()
        
        #a hell lot of shitcoding down here
        
        #yeah boii lets start a loop
        #takes all the data about all the albums and add it into the "album_array" list
        for i in range (1, num_of_lines):
            #a list for the current album 
            current_album = []

            #each string of data has 12 params, hence we do a 12 iterations
            for a in range (0, 12):
                #find the indexes of first and last quot mark to get the data between them
                #first quot mark 
                idx_firstQ = file_string.find('\"', index_start) + 1
                #last quot mark
                idx_lastQ = file_string.find('\"', idx_firstQ)
                #get the data between them, with indexes
                txt = file_string[idx_firstQ:idx_lastQ]
                
                #if the data is not empty, and also if it's not one of these parameters, then we append it to the "current_album" list
                if txt != "" and a != 10 and a != 8 or a == 6 or a == 1 or a == 2 or a == 3 or a == 4:
                    #i dont fukn remember what this is, but it does smth important
                    if a == 6 or a == 7:
                        if txt == "":
                            txt = "0"
                        txt = int(txt)
                    
                    current_album.append(txt)
                
                index_start = file_string.find(",",idx_lastQ)

            #when we got all the data about the album, find the "\n" and take it as the new starting position
            idx_nl = file_string.find('\n',idx_lastQ)
            index_start = idx_nl
            album_array.append(current_album)

        #new list of albums, that will me formatted and edited for further use
        album_display = album_array

        #merges artist first name and second name together (like "The" + "Beatles" = "The Beatles")
        for i in range(len(album_display)):
            #in case the artists does not have the first name, we will merge it with the empty character
            space_char = ""
            #in case the artist does have the first name, we will merge it with space character
            if album_display[i][1] != "":
                space_char = " "
            album_display[i][1] += space_char + album_display[i][2]
            #some unnecessary data about artist names that we don't need
            #2 index is used three times because every time you delete data all the indexes shift
            del album_display[i][2]
            del album_display[i][2]
            del album_display[i][2]
            
        #replaces artists names where necessary (like replace "Bowie" with "David Bowie")
        #also, removes HTML characters that appear in some places
        for i in range(len(album_display)):
            current_name = album_display[i][1]
            unescaped_current_name = html.unescape(current_name)
            
            #replaces name
            if(unescaped_current_name in artists_csv_dict):
                album_display[i][1] = artists_csv_dict[unescaped_current_name]
                album_display[i][1] = album_display[i][1].strip().replace("\"","")
            
            #removes HTML chars
            album_display[i][1] = html.unescape(album_display[i][1])
            album_display[i][2] = html.unescape(album_display[i][2])
        
        #sort by artist name, then by release year
        album_display = sorted(album_display,key=lambda x: (x[1].lower(),x[3]))
        
        #return the list of albums for further use
        return album_display
    else:
        #if data file doesn't exit
        print("Data file doesn't exist")
        return 0
        
#shows all the albums in a form of spreadsheet
def show_album_spreadsheet(array, command):
    if (command == "default"):
        print(tabulate(array, headers = ['RYM Code', 'Artist', 'Album', 'Year', 'Score'], tablefmt="grid"))
    elif(command == "top"):
        album_display = sorted(array,key=lambda x: (x[4]), reverse=True)
        print(tabulate(album_display, headers = ['RYM Code', 'Artist', 'Album', 'Year', 'Score'], tablefmt="grid"))
    elif(command == "bottom"):
        album_display = sorted(array,key=lambda x: (x[4]))
        print(tabulate(album_display, headers = ['RYM Code', 'Artist', 'Album', 'Year', 'Score'], tablefmt="grid"))
       
#show all the albums in a certain year in a form of a spreadsheet
def show_album_spreadsheet_by_year(array, year, command):
    new_array = []
    indexes = []
    for i in range(len(array)):
        if(array[i][3]==int(year)):
            new_array.append(array[i])
        
    scores_list = []
    #calculate avg rating
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
   
#change the data file name
def change_filename(new_filename):
    my_file = Path("./"+new_filename)
    if my_file.is_file():
        source_filename = new_filename
        config = configparser.ConfigParser()
        config.read("conf.ini")
        config['BASIC']['file'] = new_filename
        with open('conf.ini', 'w') as configfile:
            config.write(configfile)
        return new_filename
    else:
        print("No such file")
        return 0

#change the amount of albums to check for top of artists
def set_amount_for_top_art(amount):
     config = configparser.ConfigParser()
     config.read("conf.ini")
     config['TOPS']['top-art'] = amount
     with open('conf.ini', 'w') as configfile:
            config.write(configfile)
     print("The amount for top-art was changed to {}".format(amount))
     
#change the amount of albums to check for top of years
def set_amount_for_top_years(amount):
     config = configparser.ConfigParser()
     config.read("conf.ini")
     config['TOPS']['top-years'] = amount
     with open('conf.ini', 'w') as configfile:
            config.write(configfile)
     print("The amount for top-years was changed to {}".format(amount))
     
#change the amount of albums to check for top of decades
def set_amount_for_top_decades(amount):
     config = configparser.ConfigParser()
     config.read("conf.ini")
     config['TOPS']['top-decades'] = amount
     with open('conf.ini', 'w') as configfile:
            config.write(configfile)
     print("The amount for top-decades as chnaged to {}".format(amount))

#add name of artists for replacement
def add_artist_for_replace(old_name, new_name):
    with open('artists.csv','a', encoding='utf-8') as fd:
        fd.write("\n\"{}\",\"{}\"".format(old_name, new_name))
    
    print("New name has been added!")

#ф-ция, справка по командам
def help():
    print("bs - Basic statistics")
    print ("\nas - List of all albums")
    print ("as-top - List of all albums (best to worst)")
    print ("as-bottom - List of all albums (worst to best)")
    print ("as-year - List of all albums of a certain year")
    print ("as-year-top - List of all albums of a certain year (best to worst)")
    print ("\nars - Basic statistic on artist")
    print ("ars-top - Same as above, but the albums are best to worst")
    print ("\ntop-art - The Top of Artists by avg. rating")
    print("top-art-count - The Top of Artists by Number of Albums")
    print ("top-years - The Top of Years by avg. rating")
    print ("top-decades - The Top of Decades by avg. rating")
    print ("\nchf - Change the data file name")
    print("set-top-art - Change the amount of albums to check for The Top of Artists")
    print("set-top-years - Change the amount of albums to check for The Top of Years")
    print("set-top-decades - Change the amount of albums to check for The Top of Decades")
    print("add-art-replace - Add artist name for replacement")
    print("\nexit - Exit the program")

