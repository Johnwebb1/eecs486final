#!/usr/bin/env python3
import json
from transformers import pipeline
import matplotlib.pyplot as plt
import sys

"""
This file must work to provide a toxicity score for each tweet
This score will tell the program how "toxic" a tweet is.
In this program, "toxicity" is defined by combining sentiment, language, and
"""

def getScores(text, model):
    if len(text) > 128:
        text = text[:128]
    predicted = model(text)
    score = predicted[0]['score']
    if predicted[0]['label'] == 'NEU':
        score = 0
    elif predicted[0]['label'] == 'NEG':
        score = -score
    return score

def toxicityScores(groundTruthsFileInput):
    model = pipeline('sentiment-analysis', model="finiteautomata/bertweet-base-sentiment-analysis")
    teams_scores = {
        "Atlanta Hawks": {"num_tweets": 0, "scores_sum": 0},
        "Boston Celtics": {"num_tweets": 0, "scores_sum": 0},
        "Brooklyn Nets": {"num_tweets": 0, "scores_sum": 0},
        "Charlotte Hornets": {"num_tweets": 0, "scores_sum": 0},
        "Chicago Bulls": {"num_tweets": 0, "scores_sum": 0},
        "Cleveland Cavaliers": {"num_tweets": 0, "scores_sum":0},
        "Dallas Mavericks": {"num_tweets": 0, "scores_sum": 0},
        "Denver Nuggets": {"num_tweets": 0, "scores_sum": 0},
        "Detroit Pistons": {"num_tweets": 0, "scores_sum": 0},
        "Golden State Warriors": {"num_tweets": 0, "scores_sum": 0},
        "Houston Rockets": {"num_tweets": 0, "scores_sum": 0},
        "Indiana Pacers": {"num_tweets": 0, "scores_sum": 0},
        "Los Angeles Clippers": {"num_tweets": 0, "scores_sum": 0},
        "Los Angeles Lakers": {"num_tweets": 0, "scores_sum": 0},
        "Memphis Grizzlies": {"num_tweets": 0, "scores_sum": 0},
        "Miami Heat": {"num_tweets": 0, "scores_sum": 0},
        "Milwaukee Bucks": {"num_tweets": 0, "scores_sum": 0},
        "Minnesota Timberwolves": {"num_tweets": 0, "scores_sum": 0},
        "New Orleans Pelicans": {"num_tweets": 0, "scores_sum": 0},
        "New York Knicks": {"num_tweets": 0, "scores_sum": 0},
        "Oklahoma City Thunder": {"num_tweets": 0, "scores_sum": 0},
        "Orlando Magic": {"num_tweets": 0, "scores_sum": 0},
        "Philadelphia 76ers": {"num_tweets": 0, "scores_sum": 0},
        "Phoenix Suns": {"num_tweets": 0, "scores_sum": 0},
        "Portland Trail Blazers": {"num_tweets": 0, "scores_sum": 0},
        "Sacramento Kings": {"num_tweets": 0, "scores_sum": 0},
        "San Antonio Spurs": {"num_tweets": 0, "scores_sum": 0},
        "Toronto Raptors": {"num_tweets": 0, "scores_sum": 0},
        "Utah Jazz": {"num_tweets": 0, "scores_sum": 0},
        "Washington Wizards": {"num_tweets": 0, "scores_sum": 0}
    }

    teams_list = ["Atlanta Hawks","Boston Celtics","Brooklyn Nets","Charlotte Hornets",
            "Chicago Bulls","Cleveland Cavaliers","Dallas Mavericks","Denver Nuggets","Detroit Pistons",
            "Golden State Warriors","Houston Rockets","Indiana Pacers","Los Angeles Clippers",
            "Los Angeles Lakers","Memphis Grizzlies","Miami Heat","Milwaukee Bucks",
            "Minnesota Timberwolves","New Orleans Pelicans","New York Knicks","Oklahoma City Thunder",
            "Orlando Magic","Philadelphia 76ers","Phoenix Suns","Portland Trail Blazers",
            "Sacramento Kings","San Antonio Spurs","Toronto Raptors","Utah Jazz","Washington Wizards"
        ]

    naivebayes_file = open('naivebayes.output', 'r')
    rocchio_file = open('rocchio.output.txt', 'r')
    rocchio_basketball_file = open('rocchio.basketball.output.txt', 'r')
    rocchio_nonbasketball_file = open('rocchio.nonbasketball.output.txt', 'r')
    knn_file = open('knn.output', 'r')

    classifiers = {
        "Naive Bayes":
        {
            "accuracy": 0,
            "precision": 0,
            "recall": 0,
            "f1": 0,
            "predictions": naivebayes_file,
            "teams": {
                "Atlanta Hawks": {"precision": 0,"recall": 0,"avg_toxicity": 0},
                "Boston Celtics": {"precision": 0,"recall": 0,"avg_toxicity": 0},
                "Brooklyn Nets": {"precision": 0,"recall": 0,"avg_toxicity": 0},
                "Charlotte Hornets": {"precision": 0,"recall": 0,"avg_toxicity": 0},
                "Chicago Bulls": {"precision": 0,"recall": 0,"avg_toxicity": 0},
                "Cleveland Cavaliers": {"precision": 0,"recall": 0,"avg_toxicity": 0},
                "Dallas Mavericks": {"precision": 0,"recall": 0,"avg_toxicity": 0},
                "Denver Nuggets": {"precision": 0,"recall": 0,"avg_toxicity": 0},
                "Detroit Pistons": {"precision": 0,"recall": 0,"avg_toxicity": 0},
                "Golden State Warriors": {"precision": 0,"recall": 0,"avg_toxicity": 0},
                "Houston Rockets": {"precision": 0,"recall": 0,"avg_toxicity": 0},
                "Indiana Pacers": {"precision": 0,"recall": 0,"avg_toxicity": 0},
                "Los Angeles Clippers": {"precision": 0,"recall": 0,"avg_toxicity": 0},
                "Los Angeles Lakers": {"precision": 0,"recall": 0,"avg_toxicity": 0},
                "Memphis Grizzlies": {"precision": 0,"recall": 0,"avg_toxicity": 0},
                "Miami Heat": {"precision": 0,"recall": 0,"avg_toxicity": 0},
                "Milwaukee Bucks": {"precision": 0,"recall": 0,"avg_toxicity": 0},
                "Minnesota Timberwolves": {"precision": 0,"recall": 0,"avg_toxicity": 0},
                "New Orleans Pelicans": {"precision": 0,"recall": 0,"avg_toxicity": 0},
                "New York Knicks": {"precision": 0,"recall": 0,"avg_toxicity": 0},
                "Oklahoma City Thunder": {"precision": 0,"recall": 0,"avg_toxicity": 0},
                "Orlando Magic": {"precision": 0,"recall": 0,"avg_toxicity": 0},
                "Philadelphia 76ers": {"precision": 0,"recall": 0,"avg_toxicity": 0},
                "Phoenix Suns": {"precision": 0,"recall": 0,"avg_toxicity": 0},
                "Portland Trail Blazers": {"precision": 0,"recall": 0,"avg_toxicity": 0},
                "Sacramento Kings": {"precision": 0,"recall": 0,"avg_toxicity": 0},
                "San Antonio Spurs": {"precision": 0,"recall": 0,"avg_toxicity": 0},
                "Toronto Raptors": {"precision": 0,"recall": 0,"avg_toxicity": 0},
                "Utah Jazz": {"precision": 0,"recall": 0,"avg_toxicity": 0},
                "Washington Wizards": {"precision": 0,"recall": 0,"avg_toxicity": 0}
            }
        },
        "Rocchio":
        {
            "accuracy": 0,
            "precision": 0,
            "recall": 0,
            "f1": 0,
            "predictions": rocchio_file,
            "teams": {
                "Atlanta Hawks": {"precision": 0,"recall": 0,"avg_toxicity": 0},
                "Boston Celtics": {"precision": 0,"recall": 0,"avg_toxicity": 0},
                "Brooklyn Nets": {"precision": 0,"recall": 0,"avg_toxicity": 0},
                "Charlotte Hornets": {"precision": 0,"recall": 0,"avg_toxicity": 0},
                "Chicago Bulls": {"precision": 0,"recall": 0,"avg_toxicity": 0},
                "Cleveland Cavaliers": {"precision": 0,"recall": 0,"avg_toxicity": 0},
                "Dallas Mavericks": {"precision": 0,"recall": 0,"avg_toxicity": 0},
                "Denver Nuggets": {"precision": 0,"recall": 0,"avg_toxicity": 0},
                "Detroit Pistons": {"precision": 0,"recall": 0,"avg_toxicity": 0},
                "Golden State Warriors": {"precision": 0,"recall": 0,"avg_toxicity": 0},
                "Houston Rockets": {"precision": 0,"recall": 0,"avg_toxicity": 0},
                "Indiana Pacers": {"precision": 0,"recall": 0,"avg_toxicity": 0},
                "Los Angeles Clippers": {"precision": 0,"recall": 0,"avg_toxicity": 0},
                "Los Angeles Lakers": {"precision": 0,"recall": 0,"avg_toxicity": 0},
                "Memphis Grizzlies": {"precision": 0,"recall": 0,"avg_toxicity": 0},
                "Miami Heat": {"precision": 0,"recall": 0,"avg_toxicity": 0},
                "Milwaukee Bucks": {"precision": 0,"recall": 0,"avg_toxicity": 0},
                "Minnesota Timberwolves": {"precision": 0,"recall": 0,"avg_toxicity": 0},
                "New Orleans Pelicans": {"precision": 0,"recall": 0,"avg_toxicity": 0},
                "New York Knicks": {"precision": 0,"recall": 0,"avg_toxicity": 0},
                "Oklahoma City Thunder": {"precision": 0,"recall": 0,"avg_toxicity": 0},
                "Orlando Magic": {"precision": 0,"recall": 0,"avg_toxicity": 0},
                "Philadelphia 76ers": {"precision": 0,"recall": 0,"avg_toxicity": 0},
                "Phoenix Suns": {"precision": 0,"recall": 0,"avg_toxicity": 0},
                "Portland Trail Blazers": {"precision": 0,"recall": 0,"avg_toxicity": 0},
                "Sacramento Kings": {"precision": 0,"recall": 0,"avg_toxicity": 0},
                "San Antonio Spurs": {"precision": 0,"recall": 0,"avg_toxicity": 0},
                "Toronto Raptors": {"precision": 0,"recall": 0,"avg_toxicity": 0},
                "Utah Jazz": {"precision": 0,"recall": 0,"avg_toxicity": 0},
                "Washington Wizards": {"precision": 0,"recall": 0,"avg_toxicity": 0}
            }
        },
        "Rocchio Basketball":
        {
            "accuracy": 0,
            "precision": 0,
            "recall": 0,
            "f1": 0,
            "predictions": rocchio_basketball_file,
            "teams": {
                "Atlanta Hawks": {"precision": 0,"recall": 0,"avg_toxicity": 0},
                "Boston Celtics": {"precision": 0,"recall": 0,"avg_toxicity": 0},
                "Brooklyn Nets": {"precision": 0,"recall": 0,"avg_toxicity": 0},
                "Charlotte Hornets": {"precision": 0,"recall": 0,"avg_toxicity": 0},
                "Chicago Bulls": {"precision": 0,"recall": 0,"avg_toxicity": 0},
                "Cleveland Cavaliers": {"precision": 0,"recall": 0,"avg_toxicity": 0},
                "Dallas Mavericks": {"precision": 0,"recall": 0,"avg_toxicity": 0},
                "Denver Nuggets": {"precision": 0,"recall": 0,"avg_toxicity": 0},
                "Detroit Pistons": {"precision": 0,"recall": 0,"avg_toxicity": 0},
                "Golden State Warriors": {"precision": 0,"recall": 0,"avg_toxicity": 0},
                "Houston Rockets": {"precision": 0,"recall": 0,"avg_toxicity": 0},
                "Indiana Pacers": {"precision": 0,"recall": 0,"avg_toxicity": 0},
                "Los Angeles Clippers": {"precision": 0,"recall": 0,"avg_toxicity": 0},
                "Los Angeles Lakers": {"precision": 0,"recall": 0,"avg_toxicity": 0},
                "Memphis Grizzlies": {"precision": 0,"recall": 0,"avg_toxicity": 0},
                "Miami Heat": {"precision": 0,"recall": 0,"avg_toxicity": 0},
                "Milwaukee Bucks": {"precision": 0,"recall": 0,"avg_toxicity": 0},
                "Minnesota Timberwolves": {"precision": 0,"recall": 0,"avg_toxicity": 0},
                "New Orleans Pelicans": {"precision": 0,"recall": 0,"avg_toxicity": 0},
                "New York Knicks": {"precision": 0,"recall": 0,"avg_toxicity": 0},
                "Oklahoma City Thunder": {"precision": 0,"recall": 0,"avg_toxicity": 0},
                "Orlando Magic": {"precision": 0,"recall": 0,"avg_toxicity": 0},
                "Philadelphia 76ers": {"precision": 0,"recall": 0,"avg_toxicity": 0},
                "Phoenix Suns": {"precision": 0,"recall": 0,"avg_toxicity": 0},
                "Portland Trail Blazers": {"precision": 0,"recall": 0,"avg_toxicity": 0},
                "Sacramento Kings": {"precision": 0,"recall": 0,"avg_toxicity": 0},
                "San Antonio Spurs": {"precision": 0,"recall": 0,"avg_toxicity": 0},
                "Toronto Raptors": {"precision": 0,"recall": 0,"avg_toxicity": 0},
                "Utah Jazz": {"precision": 0,"recall": 0,"avg_toxicity": 0},
                "Washington Wizards": {"precision": 0,"recall": 0,"avg_toxicity": 0}
            }
        },
        "Rocchio Non-Basketball":
        {
            "accuracy": 0,
            "precision": 0,
            "recall": 0,
            "f1": 0,
            "predictions": rocchio_nonbasketball_file,
            "teams": {
                "Atlanta Hawks": {"precision": 0,"recall": 0,"avg_toxicity": 0},
                "Boston Celtics": {"precision": 0,"recall": 0,"avg_toxicity": 0},
                "Brooklyn Nets": {"precision": 0,"recall": 0,"avg_toxicity": 0},
                "Charlotte Hornets": {"precision": 0,"recall": 0,"avg_toxicity": 0},
                "Chicago Bulls": {"precision": 0,"recall": 0,"avg_toxicity": 0},
                "Cleveland Cavaliers": {"precision": 0,"recall": 0,"avg_toxicity": 0},
                "Dallas Mavericks": {"precision": 0,"recall": 0,"avg_toxicity": 0},
                "Denver Nuggets": {"precision": 0,"recall": 0,"avg_toxicity": 0},
                "Detroit Pistons": {"precision": 0,"recall": 0,"avg_toxicity": 0},
                "Golden State Warriors": {"precision": 0,"recall": 0,"avg_toxicity": 0},
                "Houston Rockets": {"precision": 0,"recall": 0,"avg_toxicity": 0},
                "Indiana Pacers": {"precision": 0,"recall": 0,"avg_toxicity": 0},
                "Los Angeles Clippers": {"precision": 0,"recall": 0,"avg_toxicity": 0},
                "Los Angeles Lakers": {"precision": 0,"recall": 0,"avg_toxicity": 0},
                "Memphis Grizzlies": {"precision": 0,"recall": 0,"avg_toxicity": 0},
                "Miami Heat": {"precision": 0,"recall": 0,"avg_toxicity": 0},
                "Milwaukee Bucks": {"precision": 0,"recall": 0,"avg_toxicity": 0},
                "Minnesota Timberwolves": {"precision": 0,"recall": 0,"avg_toxicity": 0},
                "New Orleans Pelicans": {"precision": 0,"recall": 0,"avg_toxicity": 0},
                "New York Knicks": {"precision": 0,"recall": 0,"avg_toxicity": 0},
                "Oklahoma City Thunder": {"precision": 0,"recall": 0,"avg_toxicity": 0},
                "Orlando Magic": {"precision": 0,"recall": 0,"avg_toxicity": 0},
                "Philadelphia 76ers": {"precision": 0,"recall": 0,"avg_toxicity": 0},
                "Phoenix Suns": {"precision": 0,"recall": 0,"avg_toxicity": 0},
                "Portland Trail Blazers": {"precision": 0,"recall": 0,"avg_toxicity": 0},
                "Sacramento Kings": {"precision": 0,"recall": 0,"avg_toxicity": 0},
                "San Antonio Spurs": {"precision": 0,"recall": 0,"avg_toxicity": 0},
                "Toronto Raptors": {"precision": 0,"recall": 0,"avg_toxicity": 0},
                "Utah Jazz": {"precision": 0,"recall": 0,"avg_toxicity": 0},
                "Washington Wizards": {"precision": 0,"recall": 0,"avg_toxicity": 0}
            }
        },
        "KNN":
        {
            "accuracy": 0,
            "precision": 0,
            "recall": 0,
            "f1": 0,
            "predictions": knn_file,
            "teams": {
                "Atlanta Hawks": {"precision": 0,"recall": 0,"avg_toxicity": 0},
                "Boston Celtics": {"precision": 0,"recall": 0,"avg_toxicity": 0},
                "Brooklyn Nets": {"precision": 0,"recall": 0,"avg_toxicity": 0},
                "Charlotte Hornets": {"precision": 0,"recall": 0,"avg_toxicity": 0},
                "Chicago Bulls": {"precision": 0,"recall": 0,"avg_toxicity": 0},
                "Cleveland Cavaliers": {"precision": 0,"recall": 0,"avg_toxicity": 0},
                "Dallas Mavericks": {"precision": 0,"recall": 0,"avg_toxicity": 0},
                "Denver Nuggets": {"precision": 0,"recall": 0,"avg_toxicity": 0},
                "Detroit Pistons": {"precision": 0,"recall": 0,"avg_toxicity": 0},
                "Golden State Warriors": {"precision": 0,"recall": 0,"avg_toxicity": 0},
                "Houston Rockets": {"precision": 0,"recall": 0,"avg_toxicity": 0},
                "Indiana Pacers": {"precision": 0,"recall": 0,"avg_toxicity": 0},
                "Los Angeles Clippers": {"precision": 0,"recall": 0,"avg_toxicity": 0},
                "Los Angeles Lakers": {"precision": 0,"recall": 0,"avg_toxicity": 0},
                "Memphis Grizzlies": {"precision": 0,"recall": 0,"avg_toxicity": 0},
                "Miami Heat": {"precision": 0,"recall": 0,"avg_toxicity": 0},
                "Milwaukee Bucks": {"precision": 0,"recall": 0,"avg_toxicity": 0},
                "Minnesota Timberwolves": {"precision": 0,"recall": 0,"avg_toxicity": 0},
                "New Orleans Pelicans": {"precision": 0,"recall": 0,"avg_toxicity": 0},
                "New York Knicks": {"precision": 0,"recall": 0,"avg_toxicity": 0},
                "Oklahoma City Thunder": {"precision": 0,"recall": 0,"avg_toxicity": 0},
                "Orlando Magic": {"precision": 0,"recall": 0,"avg_toxicity": 0},
                "Philadelphia 76ers": {"precision": 0,"recall": 0,"avg_toxicity": 0},
                "Phoenix Suns": {"precision": 0,"recall": 0,"avg_toxicity": 0},
                "Portland Trail Blazers": {"precision": 0,"recall": 0,"avg_toxicity": 0},
                "Sacramento Kings": {"precision": 0,"recall": 0,"avg_toxicity": 0},
                "San Antonio Spurs": {"precision": 0,"recall": 0,"avg_toxicity": 0},
                "Toronto Raptors": {"precision": 0,"recall": 0,"avg_toxicity": 0},
                "Utah Jazz": {"precision": 0,"recall": 0,"avg_toxicity": 0},
                "Washington Wizards": {"precision": 0,"recall": 0,"avg_toxicity": 0}
            }
        }
    }

    groundTruthsFile = open(groundTruthsFileInput, 'r')

    datasetBaseName = groundTruthsFileInput[:len(groundTruthsFileInput) - 5]

    file1 = datasetBaseName + "_tagged_sport.json"
    file2 = datasetBaseName + "_tagged_nonsport.json"

    groundTruthFileSport = open(file1, 'r')
    groundTruthFileNonsport = open(file2, 'r')

    groundTruths = json.load(groundTruthsFile)
    groundTruthsSport = json.load(groundTruthFileSport)
    groundTruthsNonsport = json.load(groundTruthFileNonsport)

    tweet_scores = {}
    print("starting tweet score calculations")
    for tweetID in groundTruths:
        text = groundTruths[tweetID]["text"]
        tweet_scores[tweetID] = getScores(text, model)

    # calculate accuracy / average toxicity scores
    print("starting classifier accuracy/toxicity scores")
    for classifier in classifiers:
        total_correct = 0
        total_tweets = 0
        curr_scores = teams_scores.copy()
        for prediction in classifiers[classifier]["predictions"]:
            tweet_id = prediction.split()[0]
            line = prediction.split()
            pred = ""
            for i in range(1,len(line)):
                pred += line[i] + " "
            pred = pred[:-1]
            tweet = groundTruths[tweet_id]["text"]
            temp_scores = tweet_scores[tweet_id]
            curr_scores[pred]["num_tweets"] += 1
            curr_scores[pred]["scores_sum"] += temp_scores
            total_tweets += 1
            if pred == groundTruths[tweet_id]["team"]:
                total_correct += 1
        classifiers[classifier]["predictions"].seek(0)
        if total_tweets > 0:
            classifiers[classifier]["accuracy"] = total_correct / total_tweets
        for team in curr_scores:
            if curr_scores[team]["num_tweets"] > 0:
                classifiers[classifier]["teams"][team]["avg_toxicity"] = curr_scores[team]["scores_sum"] / curr_scores[team]["num_tweets"]

    # calculate precision / recall / f score
    print("starting classifiers precision/reacall/f scores")
    for classifier in classifiers:
        totalPrecision = 0
        totalRecall = 0
        for team in teams_list:
            relevantTeams = 0
            if classifier == "Rocchio Basketball":
                for tweet in groundTruthsSport:
                    if team == groundTruthsSport[tweet]["team"]:
                        relevantTeams += 1
            elif classifier == "Rocchio Non-Basketball":
                for tweet in groundTruthsNonsport:
                    if team == groundTruthsNonsport[tweet]["team"]:
                        relevantTeams += 1
            else:
                for tweet in groundTruths:
                    if team == groundTruths[tweet]["team"]:
                        relevantTeams += 1
            totalRetrieved = 0
            relevantRetrieved = 0
            for prediction in classifiers[classifier]["predictions"]:
                totalRetrieved += 1
                line = prediction.split()
                predTeam = ""
                for i in range(1,len(line)):
                    predTeam += line[i] + " "
                predTeam = predTeam[:-1]
                if team == predTeam:
                    relevantRetrieved += 1
            classifiers[classifier]["predictions"].seek(0)
            if relevantTeams > 0:
                classifiers[classifier]["teams"][team]["precision"] = relevantRetrieved / relevantTeams
                totalPrecision += relevantRetrieved / relevantTeams
            else:
                classifiers[classifier]["teams"][team]["precision"] = relevantRetrieved
                totalPrecision += relevantRetrieved
            if totalRetrieved > 0:
                classifiers[classifier]["teams"][team]["recall"] = relevantRetrieved / totalRetrieved
                totalRecall += relevantRetrieved / totalRetrieved
            else:
                classifiers[classifier]["teams"][team]["recall"] = relevantRetrieved
                totalRecall += relevantRetrieved
        p = totalPrecision / len(teams_list)
        r = totalRecall / len(teams_list)
        classifiers[classifier]["precision"] = p
        classifiers[classifier]["recall"] = r
        if r > 0 or p > 0:
            classifiers[classifier]["f1"] = (2*p*r) / (1*p+r)
        else:
            classifiers[classifier]["f1"] = (2*p*r)

    best_classifier = ""
    best_acc = -100
    out = open("toxicity.output", "w")
    for classifier in classifiers:
        acc = classifiers[classifier]["accuracy"]
        p = classifiers[classifier]["precision"]
        r = classifiers[classifier]["recall"]
        f1 = classifiers[classifier]["f1"]
        if acc > best_acc:
            best_acc = acc
            best_classifier = classifier
        out.write(classifier + ":" + '\n')
        out.write("    Accuracy: " + str(acc) + '\n')
        out.write("    Precision: " + str(p) + '\n')
        out.write("    Recall: " + str(r) + '\n')
        out.write("    F1: " + str(f1) + '\n')
        for team in classifiers[classifier]["teams"]:
            out.write("        " + team + ", Average Toxicity: " + str(classifiers[classifier]["teams"][team]["avg_toxicity"]) + '\n')

    for tweet in groundTruths:
        team = groundTruths[tweet]["team"]
        text = groundTruths[tweet]["text"]
        score = tweet_scores[tweet]
        teams_scores[team]["num_tweets"] += 1
        teams_scores[team]["scores_sum"] += score

    graph_names = {
        "Atlanta Hawks": "Hawks",
        "Boston Celtics": "Celtics",
        "Brooklyn Nets": "Nets",
        "Charlotte Hornets": "Hornets",
        "Chicago Bulls": "Bulls",
        "Cleveland Cavaliers": "Cavaliers",
        "Dallas Mavericks": "Mavericks",
        "Denver Nuggets": "Nuggets",
        "Detroit Pistons": "Pistons",
        "Golden State Warriors": "Warriors",
        "Houston Rockets": "Rockets",
        "Indiana Pacers": "Pacers",
        "Los Angeles Clippers": "Clippers",
        "Los Angeles Lakers": "Lakers",
        "Memphis Grizzlies": "Grizzlies",
        "Miami Heat": "Heat",
        "Milwaukee Bucks": "Bucks",
        "Minnesota Timberwolves": "Wolves",
        "New Orleans Pelicans": "Pelicans",
        "New York Knicks": "Knicks",
        "Oklahoma City Thunder": "Thunder",
        "Orlando Magic": "Magic",
        "Philadelphia 76ers": "76ers",
        "Phoenix Suns": "Suns",
        "Portland Trail Blazers": "Blazers",
        "Sacramento Kings": "Kings",
        "San Antonio Spurs": "Spurs",
        "Toronto Raptors": "Raptors",
        "Utah Jazz": "Jazz",
        "Washington Wizards": "Wizards"
    }

    names = []
    scores = []
    out.write('\n' + "Ground Truth Team Average Toxicity:\n")
    for team in teams_scores:
        if teams_scores[team]["num_tweets"] != 0:
            teams_scores[team]["scores_sum"] = teams_scores[team]["scores_sum"] / teams_scores[team]["num_tweets"]
        else:
            teams_scores[team]["scores_sum"] = 0.000001
        out.write('    '+team+", Average Toxicity: "+str(teams_scores[team]["scores_sum"])+"\n")
        names.append(graph_names[team])
        scores.append(teams_scores[team]["scores_sum"])

    plt.bar(names, scores)
    plt.title("Ground Truth Team Average Toxicity")
    plt.xlabel("NBA Team")
    plt.ylabel("Average Toxicity")
    plt.xticks(rotation=90, fontsize=6)
    plt.savefig("ground_truth_graph.png")
    plt.clf()

    names = []
    scores = []
    for team in classifiers[best_classifier]["teams"]:
        names.append(graph_names[team])
        if classifiers[best_classifier]["teams"][team]["avg_toxicity"] == 0:
            scores.append(0.000001)
        else:
            scores.append(classifiers[best_classifier]["teams"][team]["avg_toxicity"])
    plt.bar(names, scores)
    title = best_classifier + " Team Average Toxicity"
    plt.title(title)
    plt.xlabel("NBA Team")
    plt.ylabel("Average Toxicity")
    plt.xticks(rotation=90, fontsize=6)
    plt.savefig("best_classifier_graph.png")

    naivebayes_file.close()
    rocchio_file.close()
    rocchio_basketball_file.close()
    rocchio_nonbasketball_file.close()
    knn_file.close()
    groundTruthsFile.close()
    groundTruthFileSport.close()
    groundTruthFileNonsport.close()

def main():
    groundTruthsFile = ""
    if sys.argv[1]:
        groundTruthsFile = sys.argv[1]
    else:
        print("Ground Truth Json file needed as input to program")
        exit(1)
    toxicityScores(groundTruthsFile)

if __name__ == "__main__":
    main()