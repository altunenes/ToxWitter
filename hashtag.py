from wordcloud import WordCloud
#import the libraries
from twitter import OAuth,TwitterStream
from tweepy import OAuthHandler
import nltk
nltk.download('stopwords')

import tweepy
import pandas as pd
import matplotlib.pyplot as plt
import re
from textblob import TextBlob
import string
from nltk.corpus import stopwords


#initialize the keys
#initialize the tokens

consumer_key = 'xxxxxxxxxxxxxxxxxxx'
consumer_secret = 'xxxxxxxxxxxxxxx'
access_token = 'xxxxxxxxxx'
access_secret = 'xxxxxxxx'
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth,timeout=10)
oauth = OAuth(access_token, access_secret, consumer_key, consumer_secret)
twitter_stream = TwitterStream(auth=oauth)
# Get the total number of stopwords in the tweets
# ==========================================================================================================================================================
                                                                     #stopwords 
# ==========================================================================================================================================================
stop = stopwords.words('turkish')
new_words=('a','b', 'c', 'd',"e","f","g","h","i","j","k","l","m","n","o","ö","p","i","rt","RT")
for i in new_words:
    stop.append(i)


# Create a function to clean the tweets
def clean_tweet(tweet):
    return ' '.join(re.sub('(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)', ' ', tweet).split())


# Create a function to analyze the tweets
def analyze_sentiment(tweet):
    analysis = TextBlob(tweet)
    if analysis.sentiment.polarity > 0:
        return 'Positive'
    elif analysis.sentiment.polarity == 0:
        return 'Neutral'
    else:
        return 'Negative'

# Create a function to get the tweets
def get_tweets(query, count = 10):
    tweets = []
    try:
        fetched_tweets = api.search(q = query, count = count)
        for tweet in fetched_tweets:
            parsed_tweet = {}
            parsed_tweet['text'] = tweet.text
            parsed_tweet['sentiment'] = analyze_sentiment(tweet.text)
            if tweet.retweet_count > 0:
                if parsed_tweet not in tweets:
                    tweets.append(parsed_tweet)
            else:
                tweets.append(parsed_tweet)
        return tweets
    except tweepy.TweepError as e:
        print("Error : " + str(e))

==========================================================================================================================================================
                                                                     #Print Hashtag
==========================================================================================================================================================  
        
        
# Get tweets
tweets = get_tweets(query = '#AsıMasıOlmıycam', count = 200)

# Convert the tweets to a dataframe
data = pd.DataFrame(tweets)

# Clean the tweets
data['clean_text'] = data['text'].apply(clean_tweet)

# Get the total number of words in the tweets
data['word_count'] = data['clean_text'].apply(lambda x: len(str(x).split(" ")))

# Get the total number of characters in the tweets
data['char_count'] = data['clean_text'].str.len()

# Get the average word length
def avg_word(sentence):
  words = sentence.split()
  return (sum(len(word) for word in words)/len(words))

data['avg_word'] = data['clean_text'].apply(lambda x: avg_word(x))


data['stopwords'] = data['clean_text'].apply(lambda x: len([x for x in x.split() if x in stop]))

# Get the total number of hashtags in the tweets
data['hastags'] = data['clean_text'].apply(lambda x: len([x for x in x.split() if x.startswith('#')]))

# Get the total number of numerics in the tweets
data['numerics'] = data['clean_text'].apply(lambda x: len([x for x in x.split() if x.isdigit()]))

# Get the total number of uppercase words in the tweets
data['upper'] = data['clean_text'].apply(lambda x: len([x for x in x.split() if x.isupper()]))

# Get the total number of tweets with upper case words starting words
data['upper_start'] = data['clean_text'].apply(lambda x: len([x for x in x.split() if x[0].isupper()]))

# Get the total number of punctuation in the tweets
data['punctuation'] = data['text'].apply(lambda x: len([c for c in str(x) if c in string.punctuation]))

# Get the total number of emojis in the tweets
emoji_pattern = re.compile("["
         u"\U0001F600-\U0001F64F"  # emoticons
         u"\U0001F300-\U0001F5FF"  # symbols & pictographs
         u"\U0001F680-\U0001F6FF"  # transport & map symbols
         u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
         u"\U00002702-\U000027B0"
         u"\U000024C2-\U0001F251"
         "]+", flags=re.UNICODE)

data['emojis'] = data['text'].apply(lambda x: len([x for x in x.split() if emoji_pattern.search(x)]))

# Get the total number of mentions in the tweets
data['mentions'] = data['text'].apply(lambda x: len([x for x in x.split() if x.startswith('@')]))

# Get the total number of urls in the tweets
data['urls'] = data['text'].apply(lambda x: len([x for x in x.split() if x.startswith('http')]))

# Get the total number of stopwords in the tweets
data['stopwords'] = data['clean_text'].apply(lambda x: len([x for x in x.split() if x in stop]))

# Get the total number of words in the tweets
data['word_count'] = data['clean_text'].apply(lambda x: len(str(x).split(" ")))

# Get the total number of characters in the tweets
data['char_count'] = data['clean_text'].str.len()
def word_frequency(df):
    #create a list of all the words in the dataframe
    word_list = []
    for i in range(len(df)):
        word_list.append(df.iloc[i][0])
    #create a list of all the unique words in the dataframe
    unique_word_list = []
    for i in range(len(word_list)):
        if word_list[i] not in unique_word_list:
            unique_word_list.append(word_list[i])
    #create a dictionary of the frequency of each word
    word_frequency_dict = {}
    for i in range(len(unique_word_list)):
        word_frequency_dict[unique_word_list[i]] = word_list.count(unique_word_list[i])
    #create a dataframe of the word frequency dictionary
    word_frequency_df = pd.DataFrame(word_frequency_dict, index = [0])
    word_frequency_df = word_frequency_df.T
    word_frequency_df.columns = ['frequency']
    #sort the dataframe by the frequency of each word
    word_frequency_df = word_frequency_df.sort_values(by = 'frequency', ascending = True)
    return word_frequency_df

def get_word_frequency(df, column):
    #create a list of all the words in the phrase
    words = []
    for i in range(len(df)):
        words.append(df[column][i].split())
    #create a list of all the unique words in the phrase
    unique_words = []
    for i in range(len(words)):
        for j in range(len(words[i])):
            if words[i][j] not in unique_words:
                unique_words.append(words[i][j])
    #create a dictionary of the frequency of each unique word in the phrase
    word_frequency = {}
    for i in range(len(unique_words)):
        word_frequency[unique_words[i]] = 0
    for i in range(len(words)):
        for j in range(len(words[i])):
            word_frequency[words[i][j]] += 1
    return word_frequency

word_frequency=get_word_frequency(data,"text")

def plot_word_cloud(wordfrequency):
    wordcloud = WordCloud(width = 1000, height = 500).generate_from_frequencies(wordfrequency)
    plt.figure(figsize = (15,8))
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.show()


plot_word_cloud(word_frequency)
