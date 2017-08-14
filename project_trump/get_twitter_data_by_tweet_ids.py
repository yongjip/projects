import json
from datetime import datetime
import time
from twitter_api_credential_info import *
import tweepy


def load_json(file_path):
    with open(file_path, "r") as json_file:
        data = json.load(json_file)
    return data


def dump_json(file_path, json_data):
    with open(file_path, "w") as outfile:
        json.dump(json_data, outfile)


output_path = 'data/trump_tweets_part1_2.json'
tweet_id_path = 'data/all_ids_til_2016_12_7.json'
tweet_ids = load_json(tweet_id_path)


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token_key, access_token_secret)
api = tweepy.API(auth)


trump_tweets = []
trump_tweet_len = 0
while len(tweet_ids) != trump_tweet_len:
    for i, tweet_id in enumerate(tweet_ids[trump_tweet_len: ]):
        try:
            tweet = api.get_status(tweet_id)._json
            trump_tweets.append(tweet)
            trump_tweet_len += 1
        except Exception as e:
            print(e)
            break
    print("Sleep for 5 mins")
    print("current_tweet_len:", trump_tweet_len)
    time.sleep(300)


part1 = trump_tweets
dump_json(output_path, trump_tweets)
