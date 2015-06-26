# -*- coding: utf-8 -*-
"""
Created on Thu Jun 25 09:40:42 2015

@author: Shu-Macbook
"""

#import nltk
#from nltk.corpus import stopwords
from datetime import datetime
import collections
import movie_db as mdb
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

#import numpy as np
#import pandas as pd
#from scipy import stats
#import matplotlib as mpl
#stopwords = stopwords.words('english')
#tokens = nltk.word_tokenize(comment.values.tolist()[1][0])

def timeDiff(date, release, interval = 1):
    assert(isinstance(date, collections.Iterable))
    assert(type(release) is datetime)
    fmt_date = map(lambda x: ((datetime.strptime(x,"%Y/%m/%d")-release).days)\
        /interval, date)
    return fmt_date
    
def plotDateHist(time_diff, movie_id):
    sns.distplot(time_diff, bins=20)
    plt.title(movie_id.upper().replace("_", " "), fontsize = 15)    
    
def test():
    movie_id = ["wall_e","inception","marvels_the_avengers",\
        "guardians_of_the_galaxy","interstellar_2014"]
    release_date = ["2008/06/27","2010/07/13","2012/05/04",\
        "2014/08/01","2014/11/05"]
    i = 0
    rating = mdb.getReview("select Date, Rating from %s order by Date" %movie_id[i])
    release = datetime.strptime(release_date[i], "%Y/%m/%d")
    rating["Date"] = timeDiff(rating["Date"], release, interval = 30)
    plotDateHist(rating["Date"], movie_id[i])
#    with sns.axes_style("white"):
#        sns.jointplot(rating["Date"], rating["Rating"], kind="hex")

if __name__ == "__main__":  
    test()