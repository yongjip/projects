'''
TweetUpdate.get_tweets_by_id and TweetUpdate.get_tweets_by_screen_name are modified
from function get_all_tweets from https://gist.github.com/yanofsky/5436496
The original function is written by yanofsky
'''
import json
from twitter_api_credential_info import *


def dump_json(file_path, json_data):
    with open(file_path, "w") as outfile:
        json.dump(json_data, outfile)


class TweetUpdater:
    def __init__(self, api=None):
        self.api = api
        self.data = []

    def get_tweets_by_id(self, user_id):
        all_tweets = self.data
        api = self.api

        new_tweets = api.user_timeline(user_id=user_id, count=200)
        new_tweets = [status._json for status in new_tweets]
        all_tweets.extend(new_tweets)
        oldest = all_tweets[-1]["id"] - 1

        while len(new_tweets) > 0:
            print("getting tweets before %s" % (oldest))
            # all subsequent requests use the max_id param to prevent duplicates
            new_tweets = api.user_timeline(user_id=user_id, count=200, max_id=oldest)
            new_tweets = [status._json for status in new_tweets]
            all_tweets.extend(new_tweets)
            # update the id of the oldest tweet less one
            oldest = all_tweets[-1]["id"] - 1
            print("...%s tweets downloaded so far" % (len(all_tweets)))

    def get_tweets_by_screen_name(self, screen_name):
        all_tweets = self.data
        api = self.api

        new_tweets = api.user_timeline(user_id=user_id, count=200)
        new_tweets = [status._json for status in new_tweets]
        all_tweets.extend(new_tweets)
        oldest = all_tweets[-1]["id"] - 1

        while len(new_tweets) > 0:
            print("getting tweets before %s" % (oldest))
            # all subsequent requests use the max_id param to prevent duplicates
            new_tweets = api.user_timeline(screen_name=screen_name, count=200, max_id=oldest)
            new_tweets = [status._json for status in new_tweets]
            all_tweets.extend(new_tweets)
            # update the id of the oldest tweet less one
            oldest = all_tweets[-1]["id"] - 1
            print("...%s tweets downloaded so far" % (len(all_tweets)))

    def dump_json(self, path):
        dump_json(path, self.data)

'''
if __name__ == "__main__":
    import tweepy
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token_key, access_token_secret)
    api = tweepy.API(auth)
    screen_name = "realDonaldTrump"
    user_id = 25073877
    output_file_path = 'data_container/new_trumps_tweets.json'

    updater = TweetUpdater()
    updater.api = api
    updater.get_tweets_by_id(user_id)
    updater.dump_json(output_file_path)
'''
