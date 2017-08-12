import re
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk import tokenize
from textblob import TextBlob
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib import style
style.use("ggplot")


df = pd.read_csv("data/trump_tweets_downloaded.csv")
df = df[df["is_retweet"] == "false"]

len_df = len(df)
i = 0


def preprocess_tweets(text):
    out = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", text).split())
    return out


def ampersand_replacer(text):
    out = re.sub(r"\&amp\;", "&", text)
    return out


sid = SentimentIntensityAnalyzer()

polarities = []
times = []
data_list = []
for i in df.index:
    twt = df.loc[i, "text"]
    time_created = df.loc[i, "created_at"]
    datetime_object = datetime.strptime(time_created, '%m-%d-%Y %H:%M:%S')
    twt = ampersand_replacer(twt)
    cleaned_twt = preprocess_tweets(twt)
    scores = sid.polarity_scores(cleaned_twt)
    polarity = scores["compound"]

    times.append(datetime_object)
    polarities.append(polarity)
    data_list.append((datetime_object, twt, scores))


plt.plot(times[: 20], polarities[: 20])
plt.show()
