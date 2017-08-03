import re
import pandas as pandas
import numpy as np
import twitter

def get_key_and_secrets():
    with open("info.txt", "r") as file:
        text = file.read()
    keys = text.split('\n')[1]
    keys = keys.split(',')
    return keys

keys = get_key_and_secrets()
consumer_key = keys[0]
consumer_secret = keys[1]
access_token_key = keys[2]
access_token_secret = keys[3]

api = twitter.Api(consumer_key=consumer_key,
                  consumer_secret=consumer_secret,
                  access_token_key=access_token_key,
                  access_token_secret=access_token_secret)

print(api.VerifyCredentials())

