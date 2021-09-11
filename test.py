import streamlit as st
import pandas as pd
import tweepy
import json
import os

# Twitter API credentials

consumer_key = os.environ['consumer_key']
consumer_secret = os.environ['consumer_secret']
access_key = os.environ['access_key']
access_secret = os.environ['access_secret']

# Create the API object
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)

# Streamlit App

st.title("Twitter Hashtag Analysis")
st.subheader("This app will fetch tweets from a hashtag and save them as csv file")

# Fetching tweets

hashtag = st.text_input("Enter the hashtag")

if st.button("Fetch"):
    tweets = api.search(hashtag, count=100)
    df = pd.DataFrame(data=[tweet.text for tweet in tweets], columns=['Tweets'])
    df['len'] = np.array([len(tweet.text) for tweet in tweets])
    df['ID'] = np.array([tweet.id for tweet in tweets])
    df['Date'] = np.array([tweet.created_at for tweet in tweets])
    df['Source'] = np.array([tweet.source for tweet in tweets])
    df['Likes'] = np.array([tweet.favorite_count for tweet in tweets])
    df['RTs'] = np.array([tweet.retweet_count for tweet in tweets])
    st.write(df)
    st.success("Done!")
    st.balloons()
    st.markdown("Data saved as csv file")
    df.to_csv(f"{hashtag}.csv")
