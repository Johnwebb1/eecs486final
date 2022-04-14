#Rohan Saha rohansa
import sys
import os
import pathlib
import preprocess
import math
import json

teams = ["Cleveland Cavaliers", "Atlanta Hawks", "Golden State Warriors",
"New Orleans Pelicans", "Milwaukee Bucks", "Memphis Grizzlies","Boston Celtics",
"Brooklyn Nets", "New York Knicks",
"Philadelphia 76ers", "Toronto Raptors", "Chicago Bulls",
"Detroit Pistons", "Indiana Pacers",
"Charlotte Hornets", "Miami Heat", "Orlando Magic", "Washington Wizards",
"Denver Nuggets", "Minnesota Timberwolves", "Oklahoma City Thunder",
"Portland Trail Blazers", "Utah Jazz", "Los Angeles Clippers",
"Los Angeles Lakers", "Phoenix Suns", "Sacramento Kings", "Dallas Mavericks",
"Houston Rockets", "San Antonio Spurs"]

def trainNaiveBayes(data, test):
    vocab = 0
    team_words = {}
    team_tweets = {}
    word_prob = {}
    size = 0
    class_prob = {}
    for user in data:
        if test == user:
            continue
        else:
            size += 1
        orig_string = data[user]['text']
        if data[user]["team"] not in team_tweets:
            team_words[data[user]["team"]] = 0
            team_tweets[data[user]["team"]] = 0
        team_tweets[data[user]["team"]] += 1
        tokens = orig_string.split()
        for word in tokens:
            if word not in word_prob:
                vocab += 1
                word_prob[word] = {}
                for team in teams:
                    word_prob[word][team] = 0
            team_words[data[user]["team"]] += 1
            word_prob[word][data[user]["team"]] += 1
    for team in teams:
        class_prob[team] = team_tweets[team] / size
    for word in word_prob:
        for team in teams:
            word_prob[word][team] = (word_prob[word][team] + 1) / (team_words[team] + vocab)
    teams_no_word = {}
    for team in teams:
        teams_no_word[team] = 1 / (team_words[team] + vocab)
    return class_prob, word_prob, teams_no_word


def testNaiveBayes(test, class_prob, word_prob, teams_no_word, data):
    team_scores = {}
    for team in teams:
        team_scores[team] = math.log(class_prob[team])
    orig_string = data[test]["text"]
    tokens = orig_string.split()
    dupl = []
    for word in tokens:
        if word in dupl:
            continue
        if word in word_prob:
            for team in teams:
                team_scores[team] += math.log(word_prob[word][team])
        else:
            for team in teams:
                team_scores[team] += math.log(teams_no_word[team])
        dupl.append(word)
    max = float('-inf')
    answer = ""
    for team in team_scores:
        if max < team_scores[team]:
            max = team_scores[team]
            answer = team
    return answer


def mainPipeline4(file_input):
    file = file_input
    correct = 0
    output_file = open("naivebayes.output", 'w')
    f = open(file)
    data = json.load(f)
    count = 0
    for test in data:
        class_prob, word_prob, teams_no_word = trainNaiveBayes(data, test)
        answer = testNaiveBayes(test, class_prob, word_prob, teams_no_word, data)
        output_file.write(test + " " + answer + "\n")
        count += 1
        if data[test]["team"] == answer:
            correct += 1
    print(correct / count)

    f.close()


def main():
    file = sys.argv[1]
    correct = 0
    output_file = open("naivebayes.output", 'w')
    f = open(file)
    data = json.load(f)
    count = 0
    for test in data:
        class_prob, word_prob, teams_no_word = trainNaiveBayes(data, test)
        answer = testNaiveBayes(test, class_prob, word_prob, teams_no_word, data)
        output_file.write(test + " " + answer + "\n")
        count += 1
        if data[test]["team"] == answer:
            correct += 1
    print(correct / count)

    f.close()

if __name__ == "__main__":
    main()
