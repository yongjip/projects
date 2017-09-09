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
import json


def load_json(file_path):
    with open(file_path, "r") as json_file:
        data = json.load(json_file)
    return data


def preprocess_tweets(text):
    # remove URLs from text
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


class ETL:
    def __init__(self, data=None):
        self.data = data
        self.df = None

    def load_json(self, input_path):
        with open(input_path, "r") as json_file:
            self.data = json.load(json_file)

    def transform(self, data=None):
        if data is not None:
            self.data = data
        db = self.data

        cols_to_drop = ['contributors', 'coordinates', 'favorited', 'geo', 'retweeted', 'in_reply_to_user_id', 'in_reply_to_user_id_str', 'possibly_sensitive', 'possibly_sensitive_appealable']
        cols_to_drop += ['user', 'entities', 'extended_entities', 'place', 'retweeted_status', 'quoted_status']

        main_df = pd.DataFrame(db, dtype=str)
        main_df.loc[:, "source"] = main_df.loc[:, "source"].map(get_source_from_anchor_tag)
        main_df.loc[:, 'text'] = main_df.loc[:, 'text'].map(ampersand_replacer)
        main_df.loc[:, "is_retweeted"] = main_df.loc[:, "retweeted_status"].notnull()

        for col_name in cols_to_drop:
            main_df.drop(col_name, axis=1, inplace=True) if col_name in main_df.columns else None

        sid = SentimentIntensityAnalyzer()

        list_of_scores = []
        for i in main_df.index:
            twt = main_df.loc[i, "text"]
            cleaned_twt = preprocess_tweets(twt)
            scores = sid.polarity_scores(cleaned_twt)
            list_of_scores.append(scores)

        main_df.loc[:, "positive_ratings"] = list(map(lambda x: x['pos'], list_of_scores))
        main_df.loc[:, "negative_ratings"] = list(map(lambda x: x['neg'], list_of_scores))
        main_df.loc[:, "neutral_ratings"] = list(map(lambda x: x['neu'], list_of_scores))
        main_df.loc[:, "compound_score"] = list(map(lambda x: x['compound'], list_of_scores))
        main_df = main_df.where((pd.notnull(main_df)), None) # Convert NaN -> None. Postgres reads NaN as string
        self.df = main_df
        return main_df

    def dump_json(self, output_path):
        self.df.to_json(output_path, orient="records")

