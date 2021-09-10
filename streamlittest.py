# **Step 1:** Import the necessary libraries
import pandas as pd
import numpy as np
import streamlit as st
import tweepy
import json
import csv

# **Step 2:** Create a Twitter developer account and create an app to get the credentials
CONSUMER_KEY = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
CONSUMER_SECRET = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
ACCESS_TOKEN = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
ACCESS_TOKEN_SECRET = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"

# **Step 3:** Create a function to get the tweets
def get_tweets(username):
    # Authorization to consumer key and consumer secret 
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET) 
  
    # Access to user's access key and access secret 
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET) 
  
    # Calling api 
    api = tweepy.API(auth) 
  
    # 200 tweets to be extracted 
    number_of_tweets=200
    tweets = api.user_timeline(screen_name=username) 
  
    # Empty Array 
    tmp=[]  
  
    # create array of tweet information: username,  
    # tweet id, date/time, text 
    tweets_for_csv = [tweet.text for tweet in tweets] # CSV file created  
    for j in tweets_for_csv: 
  
        # Appending tweets to the empty array tmp 
        tmp.append(j)  
  
    # Printing the tweets 
    print(tmp) 

# **Step 4:** Create a function to export the tweets to a CSV file
def to_csv(username):
    # Authorization to consumer key and consumer secret 
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET) 
  
    # Access to user's access key and access secret 
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET) 
  
    # Calling api 
    api = tweepy.API(auth) 
  
    # 200 tweets to be extracted 
    number_of_tweets=200
    tweets = api.user_timeline(screen_name=username) 
  
    # Empty Array 
    tmp=[]  
  
    # create array of tweet information: username,  
    # tweet id, date/time, text 
    tweets_for_csv = [tweet.text for tweet in tweets] # CSV file created  
    for j in tweets_for_csv: 
  
        # Appending tweets to the empty array tmp 
        tmp.append(j)  
  
    # Printing the tweets 
    print(tmp) 
  
    # Writing to the csv file 
    with open(username + '_tweets.csv', 'w') as file: 
        writer = csv.writer(file) 
        writer.writerows(tweets_for_csv) 

# **Step 5:** Create a Streamlit app
st.title("Twitter API")
st.subheader("Extract tweets from a Twitter user account")

# **Step 6:** Create a text box to enter the username
username = st.text_input("Enter the username of the Twitter account you want to extract tweets from:")

# **Step 7:** Create a button to get the tweets
button_clicked = st.button("Get Tweets")

# **Step 8:** Create a function to display the tweets
if button_clicked:
    st.success("Extracting tweets...")
    get_tweets(username)
    st.success("Done!")
    st.subheader("Tweets")
    st.write(get_tweets(username))
    st.subheader("CSV File")
    to_csv(username)
    st.write(username + "_tweets.csv")
