#!/usr/bin/env python3
import sys
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
access_token = environment.a_token
access_secret = environment.a_secret
# Only one used for twitter api v2.0
bearer_token = environment.b_token

nba_ids = {'Atlanta Hawks': 17292143, 'Boston Celtics': 18139461,
'Brooklyn Nets': 18552281, 'Charlotte Hornets': 21308488, 'Chicago Bulls': 16212685,
'Cleveland Cavaliers': 19263978, 'Dallas Mavericks': 22185437, 'Denver Nuggets': 26074296,
'Detroit Pistons': 16727749, 'Golden State Warriors': 26270913, 'Houston Rockets': 19077044,
'Indiana Pacers': 19409270, 'Los Angeles Clippers': 19564719, 'Los Angeles Lakers': 20346956,
'Memphis Grizzlies': 7117962, 'Miami Heat': 11026952, 'Milwaukee Bucks': 15900167,
'Minnesota Timberwolves': 20196159, 'New Orleans Pelicans': 24903350, 'New York Knicks': 20265254,
'Oklahoma City Thunder': 24925573, 'Orlando Magic': 19537303, 'Philadelphia 76ers': 16201775,
'Phoenix Suns': 18481113, 'Portland Trail Blazers': 6395222, 'Sacramento Kings': 667563,
'San Antonio Spurs': 18371803, 'Toronto Raptors': 73406718, 'Utah Jazz': 18360370,
'Washington Wizards': 14992591
}

def mainPipeline1(arg_file_input, num_tweets_per_team_input):
    # Set name of output_file per team here
    arg_file = arg_file_input
    # Check that output file is in arguments
    if not arg_file:
        print("Error: No output file specified. Exit(1)")
        exit(1)
    # Set number of tweets per team here
    num_tweets_per_team = int(num_tweets_per_team_input)
    # Check that num_tweets per team: 0 < num <= 150
    if num_tweets_per_team < 1:
        print("Error: Number of tweets per team must be > 1. Exit(1)")
        exit(1)
    if num_tweets_per_team > 150:
        print("Error: Number of tweets per team must be < 110. Exit(1)")
        exit(1)
    # Setting output file with data
    output_file = "data/" + arg_file

    # Setting Client: *Used for Twitter endpoints V2.0*
    client = tweepy.Client(bearer_token= bearer_token)

    tweet_dict = {}
    hashtag_dict = {}
    start = time.time()
    # Loop through NBA Teams -> Get max_results amount of followers
    for team_name in nba_ids:
        tweet_count = 0
        # Get max_results = 20 amount of followers
        nba_tweets = client.get_users_tweets(id=nba_ids[team_name], max_results=25)
        for nba_tweet in nba_tweets.data:
            users = client.get_liking_users(id=nba_tweet.id, max_results=100)
            if users.data == None:
                continue
            if len(users.data) > 89:
                break
        # Loop through followers returned -> Get max_results amount of tweets
        for user in users.data:
            if tweet_count >= num_tweets_per_team:
                break
            tweets = client.get_users_tweets(id=user.id, max_results=15)
            if tweets.data == None:
                continue
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
                if tweet_count >= num_tweets_per_team:
                    break
        # Dumping to save progress
        out_file = open(output_file, "w")
        json.dump(tweet_dict, out_file, indent="")
        out_file.close()
        # To avoid overloading twitter api (900 requests per 15 minutes)
        time.sleep(75)

    print("program took ", time.time() - start, " seconds")
    out_file = open(output_file, "w")
    json.dump(tweet_dict, out_file, indent="")
    out_file.close()

def main():
    # Set name of output_file per team here
    arg_file = sys.argv[1]
    # Check that output file is in arguments
    if not arg_file:
        print("Error: No output file specified. Exit(1)")
        exit(1)
    # Set number of tweets per team here
    num_tweets_per_team = int(sys.argv[2])
    # Check that num_tweets per team: 0 < num <= 150
    if num_tweets_per_team < 1:
        print("Error: Number of tweets per team must be > 1. Exit(1)")
        exit(1)
    if num_tweets_per_team > 150:
        print("Error: Number of tweets per team must be < 110. Exit(1)")
        exit(1)
    # Setting output file with data
    output_file = "data/" + arg_file

    # Setting Client: *Used for Twitter endpoints V2.0*
    client = tweepy.Client(bearer_token= bearer_token)

    tweet_dict = {}
    hashtag_dict = {}
    start = time.time()
    # Loop through NBA Teams -> Get max_results amount of followers
    for team_name in nba_ids:
        tweet_count = 0
        # Get max_results = 20 amount of followers
        nba_tweets = client.get_users_tweets(id=nba_ids[team_name], max_results=25)
        while nba_tweets.data == None:
            nba_tweets = client.get_users_tweets(id=nba_ids[team_name], max_results=100)
        for nba_tweet in nba_tweets.data:
            users = client.get_liking_users(id=nba_tweet.id, max_results=100)
            if users.data == None:
                continue
            if len(users.data) > 89:
                break
        # Loop through followers returned -> Get max_results amount of tweets
        for user in users.data:
            if tweet_count >= num_tweets_per_team:
                break
            tweets = client.get_users_tweets(id=user.id, max_results=15)
            if tweets.data == None:
                continue
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
                if tweet_count >= num_tweets_per_team:
                    break
        # Dumping to save progress
        out_file = open(output_file, "w")
        json.dump(tweet_dict, out_file, indent="")
        out_file.close()
        # To avoid overloading twitter api (900 requests per 15 minutes)
        time.sleep(75)

    print("program took ", time.time() - start, " seconds")
    out_file = open(output_file, "w")
    json.dump(tweet_dict, out_file, indent="")
    out_file.close()


if __name__ == "__main__":
    main()
