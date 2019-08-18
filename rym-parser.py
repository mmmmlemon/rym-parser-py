#! /usr/bin/env python
# -*- coding: utf-8 -*-
import io
import os
#lib for table rendering
from tabulate import tabulate
#lib for .ini file
import configparser

#import all from base_func and stat_func files
from base_functions import *
from stat_functions import *

clear = lambda: os.system('cls')
config = configparser.ConfigParser()
config.read("conf.ini")


#main function
#it contains all commands a user can use in this programm
def main_func():
    print("Rate Your Music Parser v {}".format(config['BASIC']['dev_version']))
    print("Enter the commands below")
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
                show_album_spreadsheet(global_album_list, "default")
        #albums spreadsheet (best to worst)
        elif command == "as-top":
            if(global_album_list != 0):
                clear()
                show_album_spreadsheet(global_album_list, "top")
        #albums spreadsheet (worst to best)
        elif command == "as-bottom":
            if(global_album_list != 0):
                clear()
                show_album_spreadsheet(global_album_list, "bottom")
        #albums spreadsheet for a certain year
        elif command == "as-year":
            year = input("Input year: ")
            if(global_album_list != 0):
                clear()
                show_album_spreadsheet_by_year(global_album_list, year, "default")
        #albums spreadsheet for a certain year (best to worst)
        elif command == "as-year-top":
            year = input("Input year: ")
            if(global_album_list != 0):
                clear()
                show_album_spreadsheet_by_year(global_album_list, year, "top")
        #artist stats
        elif command == "ars":
            artist_name = input("Input artist name: ")
            clear()
            artist_basic_stat(global_album_list, artist_name, "default")
        #artist stats with albums best to worst
        elif command == "ars-top":
            artist_name = input("Input artist name: ")
            clear()
            artist_basic_stat(global_album_list, artist_name, "top")
        #top artists by avg. rating
        elif command == "top-art":
            clear()
            top_artists(global_album_list)
        #top artists by number of ratings
        elif command == "top-art-count":
            clear()
            top_artists_by_count(global_album_list)
        #top years by avg. rating
        elif command == "top-years":
            clear()
            top_years(global_album_list)
        #top decades by avg. rating
        elif command == "top-decades":
            clear()
            top_decades(global_album_list)
        #change filename with RYM data
        elif command == "chf":
            clear()
            print("New file name (with extension): ")
            filename = input()
            if(change_filename(filename) != 0):
                global_filename = change_filename(filename)
                global_album_list = load_file(global_filename)
                print ("File has been changed! ({})".format(filename))
        #change amount of albums for top-art
        elif command == "set-top-art":
            amount = input("New amount of albums to check: ")
            set_amount_for_top_art(amount)
        #change amount of albums for top-art
        elif command == "set-top-years":
            amount = input("New amount of albums to check: ")
            set_amount_for_top_years(amount)
        #change amount of albums for top-art
        elif command == "set-top-decades":
            amount = input("New amount of albums to check: ")
            set_amount_for_top_decades(amount)
        #add new artist name replacement
        elif command == "add-art-replace":
            old_name = input("Enter the name that should be replaced: ")
            new_name = input("Enter the new name: ")
            add_artist_for_replace(old_name, new_name)
            global_album_list = load_file(global_filename)
        #help
        elif command == "help":
            clear()
            help()
        #exit the program
        elif command == "exit":
            break
        else:
            print("No such command")

global_filename = config['BASIC']['file']

global_album_list = load_file(global_filename)

clear()

#start the main function
main_func()


    



                









