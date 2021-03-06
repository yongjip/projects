import tweepy
from trumpy.raw_twitter_data_merger import RawTwitterDataMerger
from trumpy.recent_3200_tweets_collector import Recent3200TweetsCollector
from twitter_api_credential_info import *


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token_key, access_token_secret)
api = tweepy.API(auth)
screen_name = "realDonaldTrump"
user_id = 25073877

if __name__ == "__main__":
    new_file_path = 'raw_data_container/new_trumps_tweets.json'
    database_path = 'raw_data_container/raw_trumps_tweets_all.json'

    # Get new tweets
    updater = Recent3200TweetsCollector()
    updater.api = api
    updater.get_tweets_by_id(user_id)
    # Save the tweets
    updater.dump_json(new_file_path)

    # Updates existing data using the new data
    merger = RawTwitterDataMerger()
    merger.merge(new_file_path, database_path)
    merger.drop_duplicates()
    merger.dump_json(database_path)
