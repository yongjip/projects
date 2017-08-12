import re
import pandas as pd
import numpy as np
import twitter
import json
import pytz
import time
from datetime import datetime, timezone
from dateutil import tz
from nltk.tokenize import word_tokenize, sent_tokenize, PunktSentenceTokenizer
from twitter_api_credential_info import *


data_file = 'data/trump_tweets.txt'
database = 'data/trump_tweets_downloaded.csv'
screen_name = "realDonaldTrump"
user_id = 25073877

col_names = ['source', 'text', 'created_at', 'retweet_count', 'favorite_count', 'is_retweet', 'id_str']

def get_existing_data(data_path):
    with open(data_path) as json_file:
        data = json.load(json_file)
    return data


def get_source_from_a_tag(a_tag):
    out = re.findall(r"\<a.+\>([^\<\>]+)\<\/a\>", a_tag)[0]
    return out


def str_to_datetime(time_created):
    time_created = datetime.strptime(time_created, '%a %b %d %H:%M:%S %z %Y')
    return time_created


def utc_to_est_tz(utc_dt):
    est_tz = pytz.timezone('US/Eastern')
    return utc_dt.replace(tzinfo=timezone.utc).astimezone(tz=est_tz)


def str_from_datetime(created_at):
    return created_at.strftime('%m-%d-%Y %H:%M:%S')


api = twitter.Api(consumer_key=consumer_key,
                  consumer_secret=consumer_secret,
                  access_token_key=access_token_key,
                  access_token_secret=access_token_secret)



# Trump's Twitter ID == 25073877
timeline = api.GetUserTimeline(user_id=user_id, count=200)
new_data = [instance.AsDict() for instance in timeline]


try:
    existing_data = get_existing_data(data_file)
    data = {**new_data, **existing_data}
except:
    data = new_data


with open(data_file, 'w') as outfile:
    json.dump(data, outfile)


new_data = pd.DataFrame(data, columns = col_names)

new_data.loc[:, "source"] = new_data.loc[:, "source"].map(get_source_from_a_tag)

created_times = new_data.loc[:, "created_at"]
created_times = created_times.map(str_to_datetime)
created_times = created_times.map(utc_to_est_tz)
created_times = created_times.map(str_from_datetime)
new_data.loc[:, "created_at"] = created_times

new_data.loc[new_data.loc[:, 'is_retweet'].notnull(), 'is_retweet'] = "true"
new_data.loc[new_data.loc[:, 'is_retweet'].isnull(), 'is_retweet'] = "false"

text_overlap = pd.merge(df, new_data, on="id_str", how='inner')
text_overlap = text_overlap.loc[:, "text"]
df.query("text not in text_overlap")


i = -1
text = data[i]['text']
tweet_time = data[i]['created_at']
time_zone = data[i]['user']['time_zone']
retweet_count = data[i]['retweet_count']

word_tokens = word_tokenize(text)
sent_tokens = sent_tokenize(text)


df = pd.read_csv(database)
