# -*- coding: utf-8 -*-
"""
Created on Mon Jun 22 14:28:44 2015

@author: Shu-Macbook
"""

import tomato_scraper as ts
import sqlite3
import pandas as pd
import re

rt_main = "http://www.rottentomatoes.com/"

class MovieReview(object):
    tomatodb = "rotten_tomatoes_reviews.db"
    def __init__(self, movie):
        assert(type(movie) is str)
        self.name = movie
        self.tomatoid = ts.getMovId(movie)
        
    def __str__(self):
        return """
        Movie: %s
        Tomato Id: %s
        DataBase: %s
        """ %(self.name, self.tomatoid, MovieReview.tomatodb)
                
    def tomatoReview(self, n=None, output=False, db=True):

        review_df = ts.reviewDateFrame(self.name, n)
        if len(review_df) < 1:
            raise ValueError("DataFrame is empty")
        
        if db:
            conn = sqlite3.connect(MovieReview.tomatodb)
            review_df.to_sql(self.tomatoid, con=conn, index=False, if_exists="replace")
            conn.close()
            print "Reviews saved to %s" %MovieReview.tomatodb
            
        if output:
            return review_df
        
    def getTomato(self, query):
        conn = sqlite3.connect(MovieReview.tomatodb)
        cur = conn.cursor()
        cur.execute(re.sub("self.table", self.tomatoid, query.lower()))
        result = pd.DataFrame(cur.fetchall())
        conn.close()
        return result
        
def test(movie):
    mv = MovieReview(movie)
    print mv.tomatoReview(10, output=True, db=True)
#    print mv.getTomato("select * from self.table")
        
    
if __name__ == "__main__":
    test("X- MEN: DAYS OF FUTURE PAST")
#    test("Jurassic Shark")
#    test("JURASSIC WORLD")
