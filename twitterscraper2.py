#!/usr/bin/env python3
import os
import time
import json
import tweepy
import environment
from preprocess import preprocess

"""
This file must work to scrape tweets using the twitter api and tweepy library.
This file should write the data in json format to a file in the data folder.
"""

#Authentication information
api_consumer_key = environment.api_key
api_consumer_secret = environment.api_secret
bearer_token = environment.b_token
access_token = environment.a_token
access_secret = environment.a_secret

# nba_ids = {'Atlanta Hawks': 17292143, 'Boston Celtics': 18139461,
# 'Brooklyn Nets': 18552281, 'Charlotte Hornets': 21308488, 'Chicago Bulls': 16212685,
# 'Cleveland Cavaliers': 19263978, 'Dallas Mavericks': 22185437, 'Denver Nuggets': 26074296,
# 'Detroit Pistons': 16727749, 'Golden State Warriors': 26270913, 'Houston Rockets': 19077044,
# 'Indiana Pacers': 19409270, 'Los Angeles Clippers': 19564719, 'Los Angeles Lakers': 20346956,
# 'Memphis Grizzlies': 7117962, 'Miami Heat': 11026952, 'Milwaukee Bucks': 15900167,
# 'Minnesota Timberwolves': 20196159, 'New Orleans Pelicans': 24903350, 'New York Knicks': 20265254,
# 'Oklahoma City Thunder': 24925573, 'Orlando Magic': 19537303, 'Philadelphia 76ers': 16201775,
# 'Phoenix Suns': 18481113, 'Portland Trail Blazers': 6395222, 'Sacramento Kings': 79538141,
# 'San Antonio Spurs': 18371803, 'Toronto Raptors': 73406718, 'Utah Jazz': 18360370,
# 'Washington Wizards': 14992591
# }

nba_ids = {
    'Sacramento Kings': 667563,
    'San Antonio Spurs': 18371803,
    'Toronto Raptors': 73406718,
    'Utah Jazz': 18360370,
    'Washington Wizards': 14992591
}


# Setting Authentication: *Not used for Twitter endpoints V2.0*
auth = tweepy.OAuthHandler(api_consumer_key, api_consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth, wait_on_rate_limit = True)

# Setting Client: *Used for Twitter endpoints V2.0*
client = tweepy.Client(bearer_token= bearer_token)

tweet_dict = {}
hashtag_dict = {}
start = time.time()
# Loop through NBA Teams -> Get max_results amount of followers
for team_name in nba_ids:
    tweet_count = 0
    api_count = 0
    # Get max_results amount of followers
    nba_tweets = client.get_users_tweets(id=nba_ids[team_name], max_results=20)
    while nba_tweets.data == None:
        nba_tweets = client.get_users_tweets(id=nba_ids[team_name], max_results=20)
    for nba_tweet in nba_tweets.data:
        users = client.get_liking_users(id=nba_tweet.id, max_results=100)
        if users.data == None:
            continue
        if len(users.data) > 79:
            break
    # Loop through followers returned -> Get max_results amount of tweets
    for user in users.data:
        print(len(users.data))
        if tweet_count > 89:
            break
        tweets = client.get_users_tweets(id=user.id, max_results=15)
        if tweets.data == None:
            continue
        api_count += len(tweets.data)
        for tweet in tweets.data:
            raw_tweet, hashtags = preprocess(str(tweet))
            if raw_tweet == "":
                continue
            tweet_count += 1
            tweet_dict[tweet.id] = {
                "text": raw_tweet,
                "team": team_name,
                "user": user.username
            }
            if tweet_count > 89:
                break
            for hashtag in hashtags:
                if hashtag in hashtag_dict:
                    if team_name in hashtag_dict[hashtag]:
                        hashtag_dict[hashtag][team_name] += 1
                    else:
                        hashtag_dict[hashtag][team_name] = 1
                else:
                    hashtag_dict[hashtag] = {
                        team_name: 1
                    }
    # To avoid overloading twitter api (900 requests per 15 minutes)
    running = time.time() - start
    print(running)
    print(team_name, " -> ", tweet_count)
    print(len(tweet_dict))
    time.sleep(180)

print("program took ", time.time() - start, " seconds")
out_file = open("data/last_bit.json", "w")
json.dump(tweet_dict, out_file, indent="")
out_file.close()
out_file = open("data/last_bit_hashtags.json", "w")
json.dump(hashtag_dict, out_file, indent="")
out_file.close()
