import re
import pandas as pd
import numpy as np
import tweepy
import json
import pytz
import time
from datetime import datetime, timezone
from twitter_api_credential_info import *


new_data_file_path = 'data/new_trump_tweets.json'
database_path = 'data/all_trump_tweets.json'
screen_name = "realDonaldTrump"
user_id = 25073877
#col_names = ['source', 'text', 'created_at', 'retweet_count', 'favorite_count', 'is_retweet', 'id_str']
unnecessary_keys = ["user", "id_str", 'in_reply_to_status_id_str', 'in_reply_to_user_id_str', 'quoted_status_id_str']

access_key = access_token_key
access_secret = access_token_secret

#authorize twitter, initialize tweepy
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)
screen_name = "realDonaldTrump"



def load_json(file_path):
    with open(file_path, "r") as json_file:
        data = json.load(json_file)
    return data


def get_source_from_a_tag(a_tag):
    out = re.findall(r"\<a.+\>([^\<\>]+)\<\/a\>", a_tag)[0]
    return out


def str_from_twitter_to_datetime(time_created):
    time_created = datetime.strptime(time_created, '%a %b %d %H:%M:%S %z %Y')
    return time_created


def str_from_db_to_datetime(time_created):
    time_created = datetime.strptime(time_created, '%m-%d-%Y %H:%M:%S')
    return time_created


def utc_to_est_tz(utc_dt):
    est_tz = pytz.timezone('US/Eastern')
    return utc_dt.replace(tzinfo=timezone.utc).astimezone(tz=est_tz)


def str_from_datetime(created_at):
    return created_at.strftime('%a %b %d %H:%M:%S %z %Y')


def get_idx_to_remove_duplicates(new_data, time_last_updated, str_to_datetime):
    for i, data in enumerate(new_data):
        if str_to_datetime(data["created_at"]) < time_last_updated:
            remove_after_this = i
            break
    return remove_after_this


def dump_json(file_path, json_data):
    with open(file_path, "w") as outfile:
        json.dump(json_data, outfile)


def get_last_updated_timestamp_for(json_data, str_to_datetime):
    time_last_updated = json_data[0]["created_at"]
    time_last_updated = str_to_datetime(time_last_updated)
    return time_last_updated


def standardize_dataframe_format(df):
    '''
    :param df:
    1. clean source string removing HTML a tag
    2. change timezone: UTC -> EST
    3. if "is_retweet" is Null then "false"
        else "ture"
    :return: cleaned_df
    '''
    new_df.loc[:, "source"] = new_df.loc[:, "source"].map(get_source_from_a_tag)

    created_times = new_df.loc[:, "created_at"]
    created_times = created_times.map(str_from_twitter_to_datetime)
    created_times = created_times.map(utc_to_est_tz)
    created_times = created_times.map(str_from_datetime)
    new_df.loc[:, "created_at"] = created_times

    new_df.loc[new_df.loc[:, 'is_retweet'].notnull(), 'is_retweet'] = "true"
    new_df.loc[new_df.loc[:, 'is_retweet'].isnull(), 'is_retweet'] = "false"
    return new_df


# Trump's Twitter ID == 25073877

new_tweets = api.user_timeline(user_id=user_id,count=200)
new_tweets = [status._json for status in new_tweets]
new_tweets = [{key: value for key, value in tweet.items() if key not in unnecessary_keys}
       for tweet in new_tweets]

new_df = pd.DataFrame(new_tweets, dtype=str)
new_df.loc[:, 'source'] = new_df['source'].map(get_source_from_a_tag)
new_json = new_df.to_json(orient='records')

database = load_json(database_path)
updated_db = new_tweets + database
updated_df = pd.DataFrame(updated_db).drop_duplicates('text')

updated_df.to_json(database_path, orient='records')

