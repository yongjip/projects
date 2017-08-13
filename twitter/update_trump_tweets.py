import re
import pandas as pd
import numpy as np
import twitter
import json
import pytz
import time
from datetime import datetime, timezone
from twitter_api_credential_info import *


json_data_file_path = 'data/trump_tweets.json'
database_path = 'data/trump_tweets_downloaded.json'
screen_name = "realDonaldTrump"
user_id = 25073877
col_names = ['source', 'text', 'created_at', 'retweet_count', 'favorite_count', 'is_retweet', 'id_str']


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
    return created_at.strftime('%m-%d-%Y %H:%M:%S')


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


api = twitter.Api(consumer_key=consumer_key,
                  consumer_secret=consumer_secret,
                  access_token_key=access_token_key,
                  access_token_secret=access_token_secret)

# Trump's Twitter ID == 25073877
timeline = api.GetUserTimeline(user_id=user_id, count=200)
new_data = [instance.AsDict() for instance in timeline]

existing_data = load_json(json_data_file_path)
time_last_updated = get_last_updated_timestamp_for(existing_data, str_from_twitter_to_datetime)

dont_need_after_this = get_idx_to_remove_duplicates(new_data, time_last_updated, str_from_twitter_to_datetime)
updated_data = new_data[: dont_need_after_this] + existing_data

dump_json(json_data_file_path, updated_data)

new_df = pd.DataFrame(new_data, columns=col_names, dtype=str)
new_df = standardize_dataframe_format(new_df)
standardized_new_data = list(new_df.T.to_dict().values())

main_data = load_json(database_path)
time_last_updated = get_last_updated_timestamp_for(main_data, str_from_db_to_datetime)
dont_need_after_this = get_idx_to_remove_duplicates(standardized_new_data, time_last_updated, str_from_db_to_datetime)
updated_main_data = standardized_new_data[: dont_need_after_this] + main_data

dump_json(database_path, updated_main_data)

