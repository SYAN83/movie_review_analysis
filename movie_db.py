# -*- coding: utf-8 -*-
"""
Created on Sun Jun 21 15:39:07 2015

@author: Shu-Macbook
"""

from movie_review import *
import sqlite3

#movie_list = ["Inception","Interstellar 2014","Mad Max: Fury Road",\
#                "WALL.E","PK","Eternal Sunshine of the Spotless Mind"]
#movie_list = ["Its Such a Beautiful Day","marvels The Avengers",\
#"Guardians of the Galaxy","Donnie Darko","X-Men: Days of Future Past",\
#"Star Trek"]
#movie_list = ["x_men_days_of_future_past"]

def scrape():
    for movie in movie_list:
        mv = MovieReview(movie)
        mv.tomatoReview()
    
def showTables(): 
    conn = sqlite3.connect(MovieReview.tomatodb)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    print(cursor.fetchall())
    conn.close()

def getReview(query):
    conn = sqlite3.connect(MovieReview.tomatodb)
    cur = conn.cursor()
    cur.execute(query)
    data = pd.DataFrame(cur.fetchall())
    conn.close()
    return data
    
def main():
    scrape()
#    print RTMovieRev.mydb
#    showTables()
#    print getReview("select * from its_such_a_beautiful_day limit 5")


if __name__ == "__main__":
    main()