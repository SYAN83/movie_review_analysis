# -*- coding: utf-8 -*-
"""
Created on Mon Jun 22 14:28:44 2015

@author: Shu-Macbook
"""

import tomato_scraper as ts
import re, sqlite3
import pandas as pd

rt_main = "http://www.rottentomatoes.com/"

movie_a = ["inception","interstellar_2014","mad_max_fury_road","wall_e","pk",\
    "eternal_sunshine_of_the_spotless_mind","its_such_a_beautiful_day",\
    "guardians_of_the_galaxy","donnie_darko","x_men_days_of_future_past",\
    "marvels_the_avengers","evangerionshingekijobanha","jurassic_world",\
    "the_disappearance_of_haruhi_suzumiya"]
#release_a = ["2008/06/27","2010/07/13","2012/05/04",\
#        "2014/08/01","2014/11/05"]
movie_b = ["jurassic_shark_2013","aliens_vs_avatars","age_of_ice",\
    "zombie_massacre","alone_in_the_dark","battlefield_earth","super_shark",\
    "airplane_vs_volcano","alien_abduction","r500_mph_storm","entourage"]
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
        """Read and save all availabe reviews into Database
            Set output=True to get output"""
        review_df = ts.reviewDateFrame(self.name, n)
        
        if db and len(review_df) > 0:
            conn = sqlite3.connect(MovieReview.tomatodb)
            table_name = self.tomatoid
            if re.search("^\d", table_name):
                table_name = "r" + table_name
            review_df.to_sql(table_name, con=conn, index=False, if_exists="replace")
            conn.close()
            print "Reviews saved to %s\n" %MovieReview.tomatodb
            
        if output:
            return review_df
        
    def getTomato(self, query):
        conn = sqlite3.connect(MovieReview.tomatodb)
        cur = conn.cursor()
        cur.execute(re.sub("self.table", self.tomatoid, query.lower()))
        result = pd.DataFrame(cur.fetchall())
        conn.close()
        return result

def toMovieList(movie_list):
    conn = sqlite3.connect(MovieReview.tomatodb)
    table_name = "movie_title"
    movie_list.to_sql(table_name, con=conn, index=False, if_exists="replace")
    conn.close()
    print "Movie titles saved to %s\n" %MovieReview.tomatodb        

def test():
#    mv = MovieReview(movie)
#    mv.tomatoReview(2000, output=True, db=True)
#    print mv.getTomato("select * from self.table")        
    movie_list_a = pd.DataFrame(movie_a, columns=["Title"])
    movie_list_a["Ranking"] = "High"
    movie_list_b = pd.DataFrame(movie_b, columns=["Title"])
    movie_list_b["Ranking"] = "Low"
    movie_list = movie_list_a.append(movie_list_b)
    print movie_list.tail(5)
    toMovieList(movie_list)
    
if __name__ == "__main__":
#    test("X- MEN: DAYS OF FUTURE PAST")
    test()
#    test("JURASSIC WORLD")
