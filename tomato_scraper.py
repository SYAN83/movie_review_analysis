# -*- coding: utf-8 -*-
"""
Created on Wed Jun 24 09:13:40 2015
Scraping movie reviews from www.rottentomatoes.com 
@author: Shu-Macbook
"""

from bs4 import BeautifulSoup
import urllib2
import re
import webbrowser
import pandas as pd
import datetime
import time, random

tomato_main = "http://www.rottentomatoes.com"
headers = ["Name", "Id", "Rating", "Date", "Comment"]

def reviewDateFrame(movie, n = None):
    rev_list=[]
    try:
        for review in getReview(getMovId(movie), n):
            rev_list.append(review)
    except urllib2.HTTPError:
        pass
    if len(rev_list) == 0:
        return rev_list
    else:
        print "\nTotal reviews for %s: %d\n" %(movie, len(rev_list))
    return pd.DataFrame(rev_list, columns = headers)

def getReview(mov_id, n):
    rev_url = getRevUrl(mov_id)
    i = 0
    while True:
        print "Getting reviews from %s" %rev_url
        try:
            rev_raw = BeautifulSoup(urllib2.urlopen(rev_url))
        except urllib2.HTTPError:
            break
#            raise urllib2.HTTPError("Unable to open URL %s" %rev_url)
        rev_bag = rev_raw.find_all("div", {"class" : "row review_table_row"})
        if len(rev_bag) == 0:
            return
        for rev_soup in rev_bag:
            if not n is None and i >= n:
                break
            yield getUserInfo(rev_soup) + \
            [getRating(rev_soup),getDate(rev_soup),getComment(rev_soup)]
            i += 1
        else:
            rev_url = nextRevUrl(rev_url)
            time.sleep(random.random())
            continue  # executed if the loop ended normally (no break)
        break
        
def getMovId(movie):
    return "_".join(re.sub('[^\w\s\d]', ' ', re.sub('[\-\']', "", movie)).lower().split())

def getMovUrl(mov_id):
    return "/".join([tomato_main, "m", mov_id, ""])
    
def getRevUrl(mov_id):
    rev_postfix = "reviews/?type=user"
    return "/".join([tomato_main, "m", mov_id, rev_postfix])

def nextRevUrl(url):
    if re.search("/reviews/\?type=user$", url):
        return re.sub("\?type=user$", "?page=2&type=user&sort=", url)
    elif re.search("/reviews/\?page=\d+&type=user&sort=", url):
        page_num = re.search("\d+", re.search("\?page=\d+", url).group()).group()
        page_num = int(page_num) + 1
        return re.sub("\?page=\d+", "?page=%d" %page_num, url)
    else:
        raise ValueError("Input URL format error\n\
            Input URL: %s" %url)


def getUserInfo(rev_soup): 
    user_info = rev_soup.find("a", {"class" : "bold unstyled articleLink"})
    try:
        user_name = user_info.string.encode('ascii','ignore')
        user_id = re.search("/\d+/$", user_info["href"]).group()
    except AttributeError:
        return ["",""]
    return [user_name,user_id.replace("/", "")]

def getRating(rev_soup):
    user_rating = rev_soup.find("span", {"class":"fl"})
    if user_rating is None:
        return 0.0
    else:
        rating = len(user_rating.find_all("span", {"class":"glyphicon glyphicon-star"}))
        return rating + .5 if user_rating.get_text().strip() == u'\xbd' else float(rating)

def getDate(rev_soup):
    date = str(rev_soup.find("span", {"class":"fr small subtle"}).get_text())
    formatted = ""
    try:
        formatted = datetime.datetime.strptime(date, '%B %d, %Y').strftime('%Y/%m/%d')
    except ValueError:
        return ""
    return formatted

def getComment(rev_soup):
    comment = rev_soup.find("div", {"class":"user_review"}).get_text("/",strip=True)
    return comment.encode('ascii','ignore')

def showSite(url):
    webbrowser.open(url)

def test():
    movie = "entourage"
    print reviewDateFrame(movie, 300)

if __name__ == "__main__":
    test()