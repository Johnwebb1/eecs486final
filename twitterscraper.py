#!/usr/bin/env python3
import os
import time
import json
import tweepy

"""
This file must work to scrape tweets using the twitter api and tweepy library.
This file should write the data in json format to a file in the data folder.
"""

#Authentication information
api_consumer_key = "5kbDBhjfQvD1wMrU1LUCzWpSe"
api_consumer_secret = "qRBInfIySQHuY62EME4Ye6K90q65Jtr9LFjGeiqbjDDMyvanmx"
bearer_token = "AAAAAAAAAAAAAAAAAAAAAAapawEAAAAALYDG3fhEkMQhptEbQlkiafPndd8%3Df8xDASGwY2yulUdXXyurvIWUL5xxEH8hhLYZjyGnOAWZypfWOu"
access_token = "1508909827778568199-NLZd2nxQ9sVVqsZzQVVClTpvRTVWkf"
access_secret = "oRt9b2JORICdScib6fD6YjioVVfllkICIjN8ZbZmH8ajB"

nba_teams = {
    "Atlanta Hawks": "ATLHawks",
    "Boston Celtics": "celtics",
    "Brooklyn Nets": "BrooklynNets",
    "Charlotte Hornets": "hornets",
    "Chicago Bulls": "chicagobulls",
    "Cleveland Cavaliers": "cavs",
    "Dallas Mavericks": "dallasmavs",
    "Denver Nuggets": "nuggets",
    "Detroit Pistons": "DetroitPistons",
    "Golden State Warriors": "warriors",
    "Houston Rockets": "HoustonRockets",
    "Indiana Pacers": "Pacers",
    "Los Angeles Clippers": "LAClippers",
    "Los Angeles Lakers": "Lakers",
    "Memphis Grizzlies": "memgrizz",
    "Miami Heat": "MiamiHEAT",
    "Milwaukee Bucks": "Bucks",
    "Minnesota Timberwolves": "Timberwolves",
    "New Orleans Pelicans": "PelicansNBA",
    "New York Knicks": "nyknicks",
    "Oklahoma City Thunder": "okcthunder",
    "Orlando Magic": "OrlandoMagic",
    "Philadelphia 76ers": "sixers",
    "Phoenix Suns": "Suns",
    "Portland Trail Blazers": "trailblazers",
    "Sacramento Kings": "SacrementoKings",
    "San Antonio Spurs": "spurs",
    "Toronto Raptors": "Raptors",
    "Utah Jazz": "utahjazz",
    "Washington Wizards": "WashWizards"
}

nba_ids = {'Atlanta Hawks': 17292143, 'Boston Celtics': 18139461,
'Brooklyn Nets': 18552281, 'Charlotte Hornets': 21308488, 'Chicago Bulls': 16212685,
'Cleveland Cavaliers': 19263978, 'Dallas Mavericks': 22185437, 'Denver Nuggets': 26074296,
'Detroit Pistons': 16727749, 'Golden State Warriors': 26270913, 'Houston Rockets': 19077044,
'Indiana Pacers': 19409270, 'Los Angeles Clippers': 19564719, 'Los Angeles Lakers': 20346956,
'Memphis Grizzlies': 7117962, 'Miami Heat': 11026952, 'Milwaukee Bucks': 15900167,
'Minnesota Timberwolves': 20196159, 'New Orleans Pelicans': 24903350, 'New York Knicks': 20265254,
'Oklahoma City Thunder': 24925573, 'Orlando Magic': 19537303, 'Philadelphia 76ers': 16201775,
'Phoenix Suns': 18481113, 'Portland Trail Blazers': 6395222, 'Sacramento Kings': 79538141,
'San Antonio Spurs': 18371803, 'Toronto Raptors': 73406718, 'Utah Jazz': 18360370,
'Washington Wizards': 14992591
}

# Setting Authentication: *Not used for Twitter endpoints V2.0*
auth = tweepy.OAuthHandler(api_consumer_key, api_consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth, wait_on_rate_limit = True)

# Setting Client: *Used for Twitter endpoints V2.0*
client = tweepy.Client(bearer_token= bearer_token)

tweet_dict = {}
# Loop through NBA Teams -> Get max_results amount of followers
for screen_name in nba_teams:
    # Get max_results amount of followers
    users = client.get_users_followers(id=nba_ids[screen_name], max_results=6)
    # Loop through followers returned -> Get max_results amount of tweets
    for user in users.data:
        print("User Info")
        print(user)
        print(user["id"])
        print("Tweets")
        tweets = client.get_users_tweets(id=user["id"], max_results=5)
        if tweets.data == None:
            continue
        for tweet in tweets.data:
            tweet_dict[tweet["id"]] = {
                "text": tweet["text"],
                "tweet_id": tweet["id"]
            }
    time.sleep(40)

print(tweet_dict)
