import tweepy
import pandas as pd
import sqlite3
import json
import datetime
from datetime import date
# simport texthero as hero
import regex as re
import string

pd.set_option('display.max_colwidth', None)


def get_all_tweets(screen_name, consumer_key="vL6ghmTFx1Ixc9KqDbGvlXnzF", consumer_secret='H1VRBRO3lbS84pcjrrn3rdTs4eaTacQuVjVnmu1wfUF3blh4D1', access_key="1107472701579497472-OVEXtMXCQYp8vMOmju5huyWvGlKCob", access_secret="OuyPqaB6v8F94x45LlaeSKw5S5fgnqnfXPrEsm28A0Swo"
                   ):
    # Twitter only allows access to a users most recent 3240 tweets with this method

    # authorize twitter, initialize tweepy
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)

    # initialize a list to hold all the tweepy Tweets
    alltweets = []

    # make initial request for most recent tweets (200 is the maximum allowed count)
    new_tweets = api.user_timeline(screen_name=screen_name, count=200)

    # save most recent tweets
    alltweets.extend(new_tweets)

    # save the id of the oldest tweet less one
    oldest = alltweets[-1].id - 1

    # keep grabbing tweets until there are no tweets left to grab
    while len(new_tweets) > 0:
        #print(f"getting tweets before {oldest}")

        # all subsiquent requests use the max_id param to prevent duplicates
        new_tweets = api.user_timeline(
            screen_name=screen_name, count=200, max_id=oldest)

        # save most recent tweets
        alltweets.extend(new_tweets)

        # update the id of the oldest tweet less one
        oldest = alltweets[-1].id - 1

    outtweets = [[tweet.id_str, tweet.created_at, tweet.text]
                 for tweet in alltweets]
    tweets_df = pd.DataFrame(outtweets, columns=['time', 'datetime', 'text'])

    return tweets_df


def get_options_flow():

    conn = sqlite3.connect('stocks.sqlite')

    ss = get_all_tweets(screen_name="WSJ")
    uw = get_all_tweets(screen_name="livemint")

    ss['source'] = 'WSJ'
    # ss['text'] = hero.remove_urls(ss['text'])
    ss['text'] = [n.replace('$', '') for n in ss['text']]

    uw['source'] = 'liveMint'
    # uw['text'] = hero.remove_urls(uw['text'])
    uw['text'] = [n.replace('$', '') for n in uw['text']]
    uw['text'] = [n.replace(':', '') for n in uw['text']]
    uw['text'] = [n.replace('\n', ' ') for n in uw['text']]
    uw['text'] = [n.replace('  ', ' ') for n in uw['text']]

    tweets = pd.concat([ss, uw])
    tweets.to_sql('tweets', conn, if_exists='replace')

    return print('done')
