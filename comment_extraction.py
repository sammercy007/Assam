# -*- coding: utf-8 -*-
"""
Created on Mon Mar  2 18:56:17 2020

@author: chandan
"""

import json
from urllib.parse import urlparse, urlencode, parse_qs
import requests
import re
from bs4 import BeautifulSoup
from googletrans import Translator

#function for open the video url
def openURL(URL, params):
    r = requests.get(URL + "?", params=params)
    return r.text

#function to get clean text- remove the html code
def cleanhtml(raw_html):
  cleantext = BeautifulSoup(raw_html, "lxml").text
  return cleantext

#fuction for load the comments
def load_comments(mat):
    translator = Translator()
    f = open("NRC_Comments_14.txt","a+")
    for item in mat["items"]:
        comment = item["snippet"]["topLevelComment"]
        author = comment["snippet"]["authorDisplayName"]
        text = comment["snippet"]["textDisplay"]
        text = cleanhtml(text)
        emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        u"\U0001f926-\U0001f937"
        u'\U00010000-\U0010ffff'
        u"\u200d"
        u"\u2640-\u2642"
        u"\u2600-\u2B55"
        u"\u23cf"
        u"\u23e9"
        u"\u231a"
        u"\u3030"
        u"\ufe0f"
    
                           "]+", flags=re.UNICODE)
        tex = emoji_pattern.sub(r'',text)
        #translate all text into english
        tex = translator.translate(tex).text
        
        print("Comment by {}: {}".format(author, tex))
        
        
        try:  
            f.write(tex+"\n")
        except:
            print("Error")
    f.close()

    
YOUTUBE_COMMENT_URL = 'https://www.googleapis.com/youtube/v3/commentThreads'
mxRs = 20
vid = str()
videourl = 'https://www.youtube.com/watch?v=Cd2Sc4yGs6I'
key = 'AIzaSyAmHHi3lkdynzJefwC4KnMIOAyzOUkLQr4'            

f1 = open("NRC_URL.txt","a+")
f1.write(videourl+"\n")
f1.close()        

try:
    video_id = urlparse(str(videourl))
    q = parse_qs(video_id.query)
    vid = q["v"][0]

except:
    print("Invalid YouTube URL")

parms = {
            'part': 'snippet,replies',
            'maxResults': mxRs,
            'videoId': vid,
            'key': key
        }

try:

    matches = openURL(YOUTUBE_COMMENT_URL, parms)
    i = 2
    mat = json.loads(matches)
    nextPageToken = mat.get("nextPageToken")
    print("\nPage : 1")
    print("------------------------------------------------------------------")
    load_comments(mat)

    while nextPageToken:
        parms.update({'pageToken': nextPageToken})
        matches = openURL(YOUTUBE_COMMENT_URL, parms)
        mat = json.loads(matches)
        nextPageToken = mat.get("nextPageToken")
        print("\nPage : ", i)
        print("------------------------------------------------------------------")

        load_comments(mat)

        i += 1
    print(i)        
except KeyboardInterrupt:
    print("User Aborted the Operation")

except:
    print("Cannot Open URL or Fetch comments at a moment")            
            




#videourl = 'https://www.youtube.com/watch?v=WCTjFHyvEaM'
#key = 'AIzaSyAmHHi3lkdynzJefwC4KnMIOAyzOUkLQr4'        
#get_video_comment(videourl, key)