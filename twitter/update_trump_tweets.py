import re
import pandas as pandas
import numpy as np
import twitter
import json
import time
import datetime
from nltk.tokenize import word_tokenize, sent_tokenize, PunktSentenceTokenizer
from nltk.corpus import stopwords, state_union
from nltk import PorterStemmer
from twitter_api_credential_info import *

ps = PorterStemmer()

stop_words = set(stopwords.words('english'))


data_file = 'trump_tweets.txt'
screen_name = "realDonaldTrump"
user_id = 25073877


def get_existing_data(data_file):
    with open(data_file) as json_file:
        data = json.load(json_file)
    return data

api = twitter.Api(consumer_key=consumer_key,
                  consumer_secret=consumer_secret,
                  access_token_key=access_token_key,
                  access_token_secret=access_token_secret)

print(api.VerifyCredentials())

# Trump's Twitter ID == 25073877
timeline = api.GetUserTimeline(user_id=user_id, count=200)
new_data = [instance.AsDict() for instance in timeline]

try:
    existing_data = get_existing_data(data_file)
    data = {**new_data, **existing_data}
except:
    data = new_data

with open('trump_tweets.txt', 'w') as outfile:
    json.dump(data, outfile)

i=0
text = data[i]['text']
tweet_time = data[i]['created_at']
time_zone = data[i]['user']['time_zone']
retweet_count = data[i]['retweet_count']
word_tokens = word_tokenize(text)

for w in word_tokens:
    print(ps.stem(w))
sent_tokens = sent_tokenize(text)
