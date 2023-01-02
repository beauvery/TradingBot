# Shows forex currency + how many times its been mentioned on twitter within 24hrs + trade symbol +
# percentage of change in mentions + sentiment from twitter by breaking each sentence the symbol has been
# mentioned in into individual words then rating the words using a lexicon of words and feelings a score
# has been assigned from -1 to 1, then based on the score a rating of POSITIVE or NEGITIVE is given 
# using a threshold. Results are saved in a txt file and printed to terminal

# RUN: python3 forex.py

# Usefull for adding to trade strategies using internet sentiment and tweet mentions can help spot, 
# ie: Pump And Dump
# if raise MissingCorpusError() ::: simply run ::: python -m textblob.download_corpora ///or/// python -m nltk.downloader stopword

import codecs
from bs4 import BeautifulSoup
import requests
import tweepy
from textblob import TextBlob, Word
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from textblob import Word
import re
import sys
import csv

#Authenticate / Digital login to twitter
# USE YOUR OWN TWITTER TOKENS
# http://apps.twitter.com TO REGISTER FOR TOKEN DONT USE MINE !
#http://all-hashtag.com/

consumer_key= 'CwvJW5yKe29EC4akSnSp61gnt' 
consumer_secret= 'mgsKIuCgwUppWYM2aRhwEgdrlOjtAuthPAvcpZgq7bheCAcuKW'

bearer_token='AAAAAAAAAAAAAAAAAAAAAAfZkwEAAAAAns3DdIkzE0X8t84rmxoK2NIC%2BmE%3DtKcS4l5jZFAz8V0Eawv1vjaiy49O3s1wzKGlBh29ReB3Jlr7nY'

access_token='1502973603855446024-XBrq0Q3qof8TiYvBRKBFbIHkFZaoMX'
access_token_secret='DotEoZOhsNaJV4ojLBITsWqXK1pSXwxsfrrfqodJfnq1s'

"""# Set up the Twitter API client
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
client = tweepy.Client(bearer_token) #OAuth 2.0"""

auth = tweepy.OAuth1UserHandler(consumer_key, consumer_secret, access_token, access_token_secret)
client = tweepy.Client(bearer_token)

# Search for tweets about what you want
symbol = "dax" 

# use tweepy libary again to search for HASHTAG + NAME 
tweets2 = client.search_recent_tweets("#" + symbol, max_results=20)
print(tweets2,"\n------------------------")


def get_sentiment(text):
    # Use TextBlob to analyze the sentiment of the text
    analysis = TextBlob(text)
    sentiment = analysis.sentiment.polarity

    # Return the sentiment score on a scale from -1.0 to 1.0
    return sentiment

def clean_text1(text):
    # Remove emojis and other markups
    text = re.sub(r'[^\w\s]', '', text)
    
    # Tokenize the text and lowercase all words
    words = [word.lower() for word in TextBlob(text).words]
    
    # Remove stopwords
    stop_words = nltk.corpus.stopwords.words('english')
    words = [word for word in words if word not in stop_words]
    
    # Remove words that are too short or commonly used in social media
    words = [word for word in words if len(word) > 2 and word not in ["lol", "omg", "wtf"]]
    
    # Lemmatize the remaining words
    words = [Word(word).lemmatize() for word in words]
    
    # Join the words back into a single string
    cleaned_text1 = " ".join(words)
    
    return cleaned_text1

# store all of the records in this list
records = []

for tweet in tweets2:
    
    if len(tweet)  > 0:
        #text = tweet.text
        texts = str(tweet)
        cleaned_text = clean_text1(texts)
        sentiment = get_sentiment(cleaned_text)  # Replace this with your own sentiment analysis function
        
        if sentiment >= 0: # give it english
            polarity = 'Positive'
        else:
            polarity = 'Negative'
        #print(cleanedtext, polarity)

        floatstring = "%.9f" % sentiment
        record = '%s|%s|%s' % (symbol, floatstring, polarity) # get string ready for output file
        records.append(record)
        
        print(f"Tweet: {cleaned_text}\nSentiment: {sentiment}\n")

        floatstring = "%.9f" % sentiment
        record = '%s|%s|%s' % (symbol, floatstring, polarity) # get string ready for output file
        records.append(record)

        print(symbol, " | " + floatstring + " | " + polarity) # print to screen !!

    else:
        break
    

fl = codecs.open('outputForex_pbs_twittersearch.txt', 'wb', 'utf8') #store to output file
line = ';'.join(records)
fl.write(line + u'\r\n')
fl.close() #end store to output file
