# Shows forex currency + how many times its been mentioned on twitter within 24hrs + trade symbol +
# percentage of change in mentions + sentiment from twitter by breaking each sentence the symbol has been
# mentioned in into individual words then rating the words using a lexicon of words and feelings a score
# has been assigned from -1 to 1, then based on the score a rating of POSITIVE or NEGITIVE is given 
# using a threshold. Results are saved in a txt file and printed to terminal

# RUN: python3 forex.py
# OUTPUT: terminal + output.txt

# http://NimbusCapital.Ltd
# Scott@NimbusCapital.Ltd
# @NimbusCapital


# Usefull for adding to trade strategies using internet sentiment and tweet mentions can help spot, 
# ie: Pump And Dump
#


import codecs
from bs4 import BeautifulSoup
import requests
import tweepy
from textblob import TextBlob
import sys
import csv

#Authenticate / Digital login to twitter
# USE YOUR OWN TWITTER TOKENS PLEASE NOT MINE
# http://apps.twitter.com TO REGISTER FOR TOKEN DONT USE MINE !
#http://all-hashtag.com/

consumer_key= 'CwvJW5yKe29EC4akSnSp61gnt' 
consumer_secret= 'mgsKIuCgwUppWYM2aRhwEgdrlOjtAuthPAvcpZgq7bheCAcuKW'

bearer_token='AAAAAAAAAAAAAAAAAAAAAAfZkwEAAAAAns3DdIkzE0X8t84rmxoK2NIC%2BmE%3DtKcS4l5jZFAz8V0Eawv1vjaiy49O3s1wzKGlBh29ReB3Jlr7nY'

access_token='1502973603855446024-XBrq0Q3qof8TiYvBRKBFbIHkFZaoMX'
access_token_secret='DotEoZOhsNaJV4ojLBITsWqXK1pSXwxsfrrfqodJfnq1s'

# We set the above varibles to our API keys from TWITTER
# Below we use the TWEEYP libary we imported to auth to twitter API
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

client = tweepy.Client(bearer_token) #OAuth 2.0

records = [] # store all of the records in this list

#symbolList = page.content.decode().split("\n") # whacking the symbols into a list
symbolList = ["GPB/CHF","USD/CHF"]

def get_sentiment(text):
    # Use TextBlob to analyze the sentiment of the text
    analysis = TextBlob(text)
    sentiment = analysis.sentiment.polarity

    # Return the sentiment score on a scale from -1.0 to 1.0
    return sentiment

for symbol in symbolList: # illeterating threw out list   
    symbol = symbol.replace("/","")
    print(symbol)
    #check for tiwtter sentiment
    #Search for tweets
    public_tweets = client.search_recent_tweets("#" + symbol) # we use tweepy libary again to search for HASHTAG + NAME 

    #Sentiment
    for tweet in public_tweets: # for every tweet we find mentioned...
        
        analysis = TextBlob(str(tweet)) # break it into single words
        sentiment = analysis.sentiment.polarity # work out sentiment
        if sentiment >= 0: # give it english
            polarity = 'Positive'
        else:
            polarity = 'Negative'
        #print(cleanedtext, polarity)

    floatstring = "%.9f" % sentiment
    record = '%s|%s|%s' % (symbol, floatstring, polarity) # get string ready for output file
    records.append(record)
    print(symbol)
    print("      |" + floatstring + "|" + polarity) # print to screen !!

fl = codecs.open('outputForex-nimbusCapital.txt', 'wb', 'utf8') #store to output file
line = ';'.join(records)
fl.write(line + u'\r\n')
fl.close() #end store to output file


# FIN - Scott 




		
