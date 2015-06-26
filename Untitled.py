# -*- coding: utf-8 -*-
"""
Created on Thu Jun 25 20:46:48 2015

@author: Shu-Macbook
"""

        
#import nltk
#from nltk.corpus import stopwords
import movie_db as mdb

movie_id = ["wall_e","inception","marvels_the_avengers",\
        "guardians_of_the_galaxy","interstellar_2014"]


#def nltk_analysis(text):
#    stopwords = stopwords.words('english')


def test():
    i = 1
    rating = mdb.getReview("select Comment from %s where Rating > 4" %movie_id[i])
    print rating
    
if __name__ == "__main__":
    test()