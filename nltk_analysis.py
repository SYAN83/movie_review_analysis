# -*- coding: utf-8 -*-
"""
Created on Thu Jun 25 20:46:48 2015

@author: Shu-Macbook
"""

        
import nltk
from nltk.corpus import stopwords
import movie_db as mdb

#movie_id = ["wall_e","inception","marvels_the_avengers",\
#        "guardians_of_the_galaxy","interstellar_2014"]
movie_a = ["inception","interstellar_2014","mad_max_fury_road","wall_e","pk",\
    "eternal_sunshine_of_the_spotless_mind","its_such_a_beautiful_day",\
    "guardians_of_the_galaxy","donnie_darko","x_men_days_of_future_past",\
    "marvels_the_avengers","evangerionshingekijobanha","jurassic_world",\
    "the_disappearance_of_haruhi_suzumiya"]
movie_b = ["jurassic_shark_2013","aliens_vs_avatars","age_of_ice",\
    "zombie_massacre","alone_in_the_dark","battlefield_earth","super_shark",\
    "airplane_vs_volcano","alien_abduction","r500_mph_storm","entourage"]
   

class NLAnalysis(object):
    stopwords = stopwords.words('english')
    def __init__(self, raw_text):
        self.length = len(raw_text)
        tokens = nltk.word_tokenize(raw_text.lower())
        self.text = nltk.Text(tokens)
        self.freq = nltk.FreqDist(self.text)
        self.word_set = set(self.text)
        self.length = len(self.text)
        self.setlength = len(self.word_set)
        
        self.richness = self.setlength / float(self.length)
        
        self.text_clean = [w for w in self.text \
            if w.isalpha() and w not in NLAnalysis.stopwords]
        self.freq_clean = nltk.FreqDist(self.text_clean)
        self.word_set_clean = set(self.text_clean)
        self.length_clean = len(self.text_clean)
        self.setlength_clean = len(self.word_set_clean)
        
        self.richness_clean = self.setlength_clean / float(self.length_clean)
        
        
    def concordance(self, word):
        self.text.concordance(word)
    def similar(self, word):
        self.text.similar(word)
    def percentage(self, word, total):
        return 100 * self.text.count(word) / self.length
    def frequency(self,word=None,n=10,stopwords = False,plot=False,cumulative=False):
        if stopwords:
            freq = self.freq
        else:
            freq = self.freq_clean
        if word == None:
            if plot:
                freq.plot(n, cumulative=cumulative)
            return freq.most_common(n)
        else:
            return freq[word]
    
    def __str__(self):
        return """        Word count: %d / %d
        Unique word count: %d / %d
        Lexical richness: %f / %f
        """%(self.length_clean,self.length,self.setlength_clean,\
        self.setlength,self.richness_clean,self.richness)


def test():
    query = "select Comment from inception where Rating = 3"
    comments = mdb.getReview(query)
    text = " ".join(comments["Comment"])
    nla = NLAnalysis(text)
    print nla
    print type(nla.frequency(n=30, stopwords = False))
#    print nla.frequency("effects")
#    print nla.length
#    print nla.richness
#    print nla.frequency(n=50)
    
if __name__ == "__main__":
    test()