

# ==========================================================================================================================================================
                                                                     #import the libraries
# ==========================================================================================================================================================


import tweepy
import re
import matplotlib.pyplot as plt
from tweepy import OAuthHandler
from textblob import TextBlob
import numpy as np

# ==========================================================================================================================================================
                                                                     #initialize the keys
# ==========================================================================================================================================================

consumer_key = 'xxxxxxxxxxxxxxxxxxxxxxx'
consumer_secret = 'xxxxxxxxxxxxxxxxxxxxxxx'
access_token = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
access_secret = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxx'

# ==========================================================================================================================================================
                                                                     #initialize the tokens
# ==========================================================================================================================================================

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth,timeout=10)
# ==========================================================================================================================================================
                                                                     #function to clean the tweets: standard procedure
# ==========================================================================================================================================================

def clean_tweet(tweet):
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

#function to get the tweets
def get_tweet_sentiment(tweet):
    analysis = TextBlob(clean_tweet(tweet))
    if analysis.sentiment.polarity > 0:
        return 'positive'
    elif analysis.sentiment.polarity == 0:
        return 'neutral'
    else:
        return 'negative'

#function to get the tweets
def get_tweets(query, count = 10):
    tweets = []
    try:
        fetched_tweets = api.search(q = query, count = count)
        for tweet in fetched_tweets:
            parsed_tweet = {}
            parsed_tweet['text'] = tweet.text
            parsed_tweet['sentiment'] = get_tweet_sentiment(tweet.text)
            if tweet.retweet_count > 0:
                if parsed_tweet not in tweets:
                    tweets.append(parsed_tweet)
            else:
                tweets.append(parsed_tweet)
        return tweets
    except tweepy.TweepError as e:
        print("Error : " + str(e))

# ==========================================================================================================================================================
                                                                     #function to get the tweets and plot the graph
# ==========================================================================================================================================================        
        
def main(queryname):
    tweets = get_tweets(queryname, count = 200)
    ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
    print("Positive tweets percentage: {} %".format(100*len(ptweets)/len(tweets)))
    ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']
    print("Negative tweets percentage: {} %".format(100*len(ntweets)/len(tweets)))
    print("Neutral tweets percentage: {} % ".format(100*(len(tweets) - len(ntweets) - len(ptweets))/len(tweets)))
    print("\n\nPositive tweets:")
    for tweet in ptweets[:10]:
        print(tweet['text'])
    print("\n\nNegative tweets:")
    for tweet in ntweets[:10]:
        print(tweet['text'])
    objects = ['Positive','Negative','Neutral']
    y_pos = np.arange(len(objects))
    performance = [100*len(ptweets)/len(tweets),100*len(ntweets)/len(tweets),100*(len(tweets) - len(ntweets) - len(ptweets))/len(tweets)]
    plt.bar(y_pos, performance, align='center', alpha=0.5)
    plt.xticks(y_pos, objects)
    plt.ylabel('Percentage')
    plt.title('Sentiment')
    plt.show()

# ==========================================================================================================================================================
                                                                     #  USAGE
# ==========================================================================================================================================================       

main("PyTorch")  
