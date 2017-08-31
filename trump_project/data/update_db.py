import tweepy
from trumpy.recent_3200_tweets_collector import Recent3200TweetsCollector
from twitter_api_credential_info import *
from trumpy.etl import ETL
from trumpy.db_updater import DBUpdater
from session import url

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token_key, access_token_secret)
api = tweepy.API(auth)
screen_name = "realDonaldTrump"
user_id = 25073877

if __name__ == "__main__":
    # Get new tweets
    updater = Recent3200TweetsCollector()
    updater.api = api
    updater.get_tweets_by_id(user_id)
    # New data format: list of dictionaries
    new_data = updater.data
    # Save the tweets
    etl = ETL()
    new_df = etl.transform(new_data)

    updater = DBUpdater()
    updater.data = new_df.T.to_dict().values()
    updater.url = url
    updater.update_db()
