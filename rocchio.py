# Max Anderson
# mtando
# EECS 486 Final Project

# Rocchio Text Classification

import sys
import os
import math
import json
import numpy as np


def indexDocument(tweet, inv_idx, docID):
    tokens = tweet.split()

    # calculate word frequencies
    freqs = {}
    for i in tokens:
        if i in freqs:
            freqs[i] += 1
        else:
            freqs[i] = 1
    
    # copy current dictionary to update token counts
    mod_inv_idx = inv_idx

    # populate inverted index with frequencies
    for word in freqs:
        if word in mod_inv_idx:
            mod_inv_idx[word][docID] = freqs[word]
        else:
            mod_inv_idx[word] = {docID: freqs[word]}
    
    return mod_inv_idx


def predict(N, docID, tweet_vecs):
    # create training and testing datasets (leave-one-out)
    tweet_vec_copy = dict(tweet_vecs)
    testing_data = tweet_vec_copy.pop(docID)
    training_data = tweet_vec_copy
    
    # add up the document vectors for each team
    team_totals = {}
    for y in training_data:
        if training_data[y][0] not in team_totals:
            team_totals[training_data[y][0]] = np.array(training_data[y][1])
        else:
            team_totals[training_data[y][0]] += np.array(training_data[y][1])
            
    # calculate the cosine similarity between each team vector and the test vector
    sim_scores = {}
    for a in team_totals:
        temp = np.dot(team_totals[a], testing_data[1])
        sim_scores[a] = temp
        
    # take the highest cosine similarity as the prediction
    sim_scores_sorted = {key: val for key, val in sorted(sim_scores.items(), key = lambda ele: ele[1], reverse=True)}
    prediction = list(sim_scores_sorted.items())[0][0]

    if testing_data[0] == prediction:
        correct = 1
    else:
        correct = 0

    actual = testing_data[0]

    return prediction, actual, correct


def main():
    data = sys.argv[1]
    curr_file = open(data, "r")

    # load json data into list of tweets
    tweet_dict = json.loads(curr_file.read())
    curr_file.close()

    inverted_index = {}
    team_dict = {}
    x = 1
    for j in tweet_dict:
        full_tweet = tweet_dict[j]["text"].lower()
        team_dict[x] = tweet_dict[j]["team"]

        # create inverted index
        inverted_index = indexDocument(full_tweet, inverted_index, x)
        
        x += 1

    tweet_vectors = {}
    N = len(tweet_dict)

    # calculate tf-idf for every tweet
    for i in range(len(tweet_dict)):
        # calculate t
        doc_vec_t = {}
        for p1 in inverted_index:
            if (i+1) in inverted_index[p1]:
                doc_vec_t[p1] = inverted_index[p1][i+1]
            else:
                doc_vec_t[p1] = 0
        
        # calculate tf
        doc_vec_tf = {}
        for p2 in inverted_index:
            n = len(inverted_index[p2])
            f = math.log((N / n), 10)
            tf = doc_vec_t[p2] * f
            doc_vec_tf[p2] = tf

        # calculate tfc (normalization)
        vec_total = 0
        for p3 in inverted_index:
            vec_total += (doc_vec_tf[p3] ** 2)

        if vec_total == 0:
            vec_len = 1
        else:
            vec_len = math.sqrt(vec_total)

        final_doc_vec = []
        for n in doc_vec_tf:
            tfc = doc_vec_tf[n] / vec_len
            final_doc_vec.append(tfc)
        
        # add to dictionary of tweet vectors with corresponding team
        tweet_vectors[i+1] = (team_dict[i+1], final_doc_vec)     

    # test prints
    # print("After:", len(tweet_vectors))
    # print(len(tweet_vectors[1][1]))
    # print(len(tweet_vectors[2][1]))

    # output file
    outfile_name = "rocchio.output.txt"
    output_file = open(outfile_name, "w")

    z = 0
    num_correct = 0
    
    # get predictions for every tweet (leave-one-out)
    while z != N:
        p, a, c = predict(N, z+1, tweet_vectors)
        num_correct += c
        outstr = a + " " + p + "\n"
        output_file.write(outstr)
        
        z += 1

    # calculate accuracy
    acc = num_correct / len(tweet_dict)
    print("Accuracy: " + str(acc))

    outstr2 = "Accuracy: " + str(acc) + "\n"
    output_file.write(outstr2)
    output_file.close()
    

    return

if __name__ == "__main__":
    main()

