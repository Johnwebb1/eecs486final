import sys
import os
import pathlib
import preprocess
import math
import json

def indexDocument(test, data):
    inverted_index = {}
    max_tf = {}
    test_vect = {}
    test_max_tf = 0
    for id in data:
        tweet = data[id]['text']
        tokens = tweet.split()
        max_tf[id] = 0
        for word in tokens:
            if test == id:
                if word not in test_vect:
                    test_vect[word] = 0
                test_vect[word] += 1
                if test_max_tf < test_vect[word]:
                    test_max_tf = test_vect[word]
                continue
            if word not in inverted_index:
                inverted_index[word] = {}
            if id not in inverted_index[word]:
                inverted_index[word][id] = 0
            inverted_index[word][id] += 1
            if max_tf[id] < inverted_index[word][id]:
                max_tf[id] = inverted_index[word][id]
    return inverted_index, max_tf, test_vect, test_max_tf

def get_KNN(test, inverted_index, max_tf, size, test_vect, test_max_tf, data):
    idf = {}
    for word in inverted_index:
        idf[word] = math.log(size / len(inverted_index[word]), 10)
    for word in test_vect:
        if word not in idf:
            test_vect[word] = (test_vect[word] / test_max_tf)
        else:
            test_vect[word] = (test_vect[word] / test_max_tf) * idf[word]
    for word in inverted_index:
        for id in inverted_index[word]:
            inverted_index[word][id] = (inverted_index[word][id] / max_tf[id]) * idf[word]
    final_scores = {}
    for word in inverted_index:
        for id in data:
            if id == test:
                continue
            if id not in final_scores:
                final_scores[id] = 0
            if word not in test_vect and id not in inverted_index[word]:
                final_scores[id] += 0
            elif word in test_vect and id in inverted_index[word]:
                final_scores[id] += (inverted_index[word][id] - test_vect[word])**2
            elif word not in test_vect and id in inverted_index[word]:
                final_scores[id] += (inverted_index[word][id])**2
            else:
                final_scores[id] += (test_vect[word])**2
    for id in final_scores:
        final_scores[id] = math.sqrt(final_scores[id])
    return final_scores



def main():
    file = sys.argv[1]
    knn = int(sys.argv[2])
    output_file = open("knn.output", 'w')
    f = open(file)
    data = json.load(f)
    size = len(data) - 1
    inverted_index = {}
    max_tf = {}
    final_scores = {}
    count = 0
    correct = 0
    for test in data:
        knn_teams = {}
        inverted_index, max_tf, test_vect, test_max_tf = indexDocument(test, data)
        final_scores = get_KNN(test, inverted_index, max_tf, size, test_vect, test_max_tf, data)
        sorted_tuples = sorted(final_scores.items(), key=lambda item: item[1], reverse=False)
        for i in range(0,knn):
            team = data[sorted_tuples[i][0]]["team"]
            if team not in knn_teams:
                knn_teams[team] = 0
            knn_teams[team] += 1
        sorted_knn = sorted(knn_teams.items(), key=lambda item: item[1], reverse=True)
        answer = sorted_knn[0][0]
        if answer == data[test]["team"]:
            correct+=1
        count += 1
        output_file.write(test + " " + answer + "\n")
    f.close()






if __name__ == "__main__":
    main()
