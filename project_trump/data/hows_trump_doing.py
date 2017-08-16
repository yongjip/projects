"""
List of keys in the raw data:
    ['contributors', 'coordinates', 'created_at', 'entities',
    'extended_entities', 'favorite_count', 'favorited', 'geo', 'id',
    'id_str', 'in_reply_to_screen_name', 'in_reply_to_status_id',
    'in_reply_to_status_id_str', 'in_reply_to_user_id',
    'in_reply_to_user_id_str', 'is_quote_status', 'lang', 'place',
    'possibly_sensitive', 'possibly_sensitive_appealable', 'quoted_status',
    'quoted_status_id', 'quoted_status_id_str', 'retweet_count',
    'retweeted', 'retweeted_status', 'source', 'text', 'truncated', 'user']
"""
import pytz
import re
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk import tokenize
from textblob import TextBlob
import pandas as pd
from datetime import datetime, timezone
import matplotlib.pyplot as plt
from matplotlib import style
import json
style.use("ggplot")


def load_json(file_path):
    with open(file_path, "r") as json_file:
        data = json.load(json_file)
    return data


def preprocess_tweets(text):
    out = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", text).split())
    return out


def ampersand_replacer(text):
    out = re.sub(r"\&amp\;", "&", text)
    return out


def get_source_from_anchor_tag(a_tag):
    out = re.findall(r"\<a.+\>([^\<\>]+)\<\/a\>", a_tag)[0]
    return out


def utc_to_est_tz(utc_dt):
    est_tz = pytz.timezone('US/Eastern')
    return utc_dt.replace(tzinfo=timezone.utc).astimezone(tz=est_tz)


cols_to_drop = ['contributors', 'coordinates', 'favorited', 'geo', 'retweeted', 'in_reply_to_user_id', 'in_reply_to_user_id_str', 'possibly_sensitive', 'possibly_sensitive_appealable']
output_path = "cleaned_data/trumps_twitter_data_with_scores.json"
db_path = "raw_data_container/raw_trumps_tweets_all.json"
db = load_json(db_path)
main_df = pd.DataFrame(db, dtype=str)
main_df.drop(cols_to_drop, axis=1, inplace=True)
main_df.loc[:, "source"] = main_df.loc[:, "source"].map(get_source_from_anchor_tag)
main_df["is_retweeted"] = main_df.loc[:, "retweeted_status"].notnull()
#df_without_retweet = main_df[main_df["retweeted_status"].isnull()]


sid = SentimentIntensityAnalyzer()

polarities = []
list_of_scores = []
times = []
data_list = []
for i in main_df.index:
    twt = main_df.loc[i, "text"]
    time_created = main_df.loc[i, "created_at"]
    datetime_object = datetime.strptime(time_created, '%a %b %d %H:%M:%S %z %Y')
    twt = ampersand_replacer(twt)
    cleaned_twt = preprocess_tweets(twt)
    scores = sid.polarity_scores(cleaned_twt)
    list_of_scores.append(scores)
    polarity = scores["compound"]

    times.append(datetime_object)
    polarities.append(polarity)
    data_list.append((datetime_object, twt, scores))

main_df.loc[:, "polarity_scores"] = list_of_scores

plt.plot(times[: 20], polarities[: 20])
#plt.show()

main_df.to_json(output_path, orient="records")