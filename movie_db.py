# -*- coding: utf-8 -*-
"""
Created on Sun Jun 21 15:39:07 2015

@author: Shu-Macbook
"""

import movie_review as mr
import pandas as pd
import sqlite3

#movie_list = ["Inception","Interstellar 2014","Mad Max: Fury Road",\
#                "WALL.E","PK","Eternal Sunshine of the Spotless Mind"]
#movie_list = ["Its Such a Beautiful Day","marvels The Avengers",\
#"Guardians of the Galaxy","Donnie Darko","X-Men: Days of Future Past",\
#"Star Trek"]
movie_list = ["Entourage"]
#movie_list = ["Alone in the Dark","40 Days and Nights","Battlefield Earth",\
#"Super Shark","100 Degrees Below Zero","Airplane vs Volcano","Alien Abduction"]

def scrape():
    for movie in movie_list:
        mv = mr.MovieReview(movie)
        mv.tomatoReview()
    
def getTableName(): 
    conn = sqlite3.connect(mr.MovieReview.tomatodb)
    table = pd.read_sql("SELECT name FROM sqlite_master WHERE type='table';", \
        con=conn)
    conn.close()
    return table

def getReview(query):
    conn = sqlite3.connect(mr.MovieReview.tomatodb)
    try:
        data = pd.read_sql(query, con=conn)
    except sqlite3.DatabaseError as e:
        print e.message()
        return None
    except TypeError:
        return None
    conn.close()
    return data
    
def main():
#    scrape()
    print getTableName()
    print getReview("select * from movie_title")


if __name__ == "__main__":
    main()