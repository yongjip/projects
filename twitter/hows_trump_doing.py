import re
import nltk
from textblob import TextBlob
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib import style
style.use("ggplot")


df = pd.read_csv("trump_tweets_downloaded.csv")
df = df[df["is_retweet"] == "false"]

len_df = len(df)
i = 0

polarities = []
subjectivities = []
times = []
data_list = []
for i in df.index:
    tweet = df.loc[i, "text"]
    trump_tweet = TextBlob(tweet)
    time_created = df.loc[i, "created_at"]
    datetime_object = datetime.strptime(time_created, '%m-%d-%Y %H:%M:%S')
    polarity = trump_tweet.sentiment.polarity
    subjectivity = trump_tweet.sentiment.subjectivity

    times.append(datetime_object)
    polarities.append(polarity)
    subjectivities.append(subjectivity)
    data_list.append((datetime_object, trump_tweet, trump_tweet.sentiment))


plt.plot(times[: 20], polarities[: 20])
