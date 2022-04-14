# eecs486final
EECS 486 Final Project. Using twitter api and language processing to analyze sentiment, toxicity, and more. 

Title:
What team do you cheer for: text classification and sentiment analysis on twitter

Description:
Our suite of python programs and datasets are used to classify tweets into which NBA fan base they are a part 
of. In addition, our program is used to calculate text sentiment, and toxicity in order to make comparisons 
across NBA teams' fan base populations. Below we itemize each file and what functionality is contained in each.
We used a host of libraries in order to advance our program without compromising the originality of our 
implementation. These libraries include but are not limited to: tweepy, numpy, langdetect. All three are large, 
standard libraries frequently used in python programs. Challenges overcame for each file are mentioned below, 
but overall attaining effective data via the twitter api and implementing our classifiers were among the largest 
overall. In the future, this program could expand its functionality to enhance the quality of data gathered on 
twitter, and the number of inputs seen in our classifiers (ie. Sport, no sport).

To run the program:
* Having python3, and pip(3) is required. Updating to most recent version recommended

Setup steps:
Copy all files into a directory via github or download
CD into that directory
Install virtual environment (pip install virtualenv)
Create a virtual environment (python3 -m venv venv) 
Activate the environment (source venv/bin/activate)
Install dependencies in requirements.txt

Dependencies:
- In Requirements.txt -
pip3 install tweepy
pip3 install langdetect
pip3 install numpy
pip3 install torch
pip3 install transformers
pip3 install matplotlib

Run the mainProgram.py file using python3, with argument 1 being a .json file to store the data in, and argument
2 being the number of tweets to get per team.

mainProgram.py [data_file_name].json [num_of_tweets]
ex) python3 mainProgram.py data_90.json 90


Files:
Twitterscrapper.py
    Description:
        This file is only included for academic purposes. Do not try to use. This version has been upgraded to 
        twitterscraper2.py. The reason that this is now obsolete is because the quality of data was too low for
        our standards. By looking for users that have liked a tweet, our new implementation was able to single 
        out more active users.
Twitterscraper2.py
    Description:
        File that scrapes tweets to populate the data files in the data folder. The scraping function takes in 
        two arguments: [output file name] [number of tweets per team]. The implementation scrapes the most 
        recent tweets from each NBA official twitter account. Then, it finds users that liked one of those 
        selected tweets and scrapes their tweets. Thus, liking a tweet posted by an official NBA team's account 
        is a signal of fan hood in our program. Once it gathers that user's tweets, the text is preprocessed 
        before being input into our tweet dictionary. Each raw tweet is labeled with the user's username, and 
        the team name to whose fan base the user belongs. Once there are [number of tweets per team] tweets, it 
        will repeat the process with the next team until all NBA teams have [number of tweets per team] tweets 
        as being identified as tweeted by one of their fans. Afterwards, the tweet dictionary is JSON dumped into 
        data/[output file name] for the rest of the program to utilize.
    Produces: 
        data/ [output file name]
    Arguments:
        [output file name] Required : Must be a .json file
        [number of tweets per team] Required : Must be  (0, 150]
Preprocess.py
    Description:
        File that preprocesses the tweets that are scraped from twitterscraper2.py. This file cleans the tweet text
        to get the raw text. Associated with this process is eliminating tagged usernames, hashtags, emojis, 
        special characters, and non-english content. The implementation then returns both the cleaned text and a
        list of hashtags used in the tweet. The list of hashtags is open ended and can be used to further analyze 
        the fan bases but the original group did not have enough time to complete this process.
    Produces: 
        String: cleaned text, List: hashtags
    Arguments:
        String of original tweet.
Naivebayes.py
    Description:
        This file classifies the team that the user supports for each tweet in the dataset using naivebayes 
        classifiaction. The program uses the Leave-One-Out-Cross-Validation where we grab one tweet to classify 
        and then use the rest for training data. This program will do this for however many tweets there are in 
        the data sample.
Knn.py
    Description:
        This file classifies the team that the user supports for each tweet in the dataset using kNN classifiaction.
        Similar to naivebayes, the program uses the Leave-One-Out-Cross-Validation where we grab one tweet to 
        classify and then use the rest for training data. This program will do this for however many tweets there are 
        in the data sample. Additionally we picked the k value based on a smaller data set which showed us that the 
        k value with highest accuracy is 9.
Toxicity.py:
    Description:
        File that will calculate the average toxicity/sentiment for all NBA teams. It is calculated for each 
        classifier that was implemented and ran on the original dataset, along with running it on the original 
        ground truth dataset itself. The file also calculates the accuracy, precision, recall, and F1 score for 
        every classifier that was implemented. For the average toxicity/sentiment score, a score of 0 means the 
        average tweets were neutral, whereas a higher positive score represents a more positive sentiment, and a 
        negative score represents a more toxic or negative sentiment tweet.
    To run: 
        python3 toxicity.py [path_to_original_ground_truth_data_set.json]
    Files needed in same directory:
        naivebayes.output
        rocchio.output.txt
        rocchio.basketball.output.txt
        rocchio.nonbasketball.output.txt
        knn.output
    Files needed in data folder:
        [original_ground_truth_data_set].json
        [original_ground_truth_data_set]_tagged_sport.json
        [original_ground_truth_data_set]_tagged_nonsport.json
    Produces:
        toxicity.output
            File that contains the accuracy, precision, recall, f1 score, and average toxicity for each NBA team, 
            for every classifier.
        ground_truth_graph.png
            Graph that shows the average toxicity for every NBA team for the ground truth tweets from the imputed 
            dataset.
        best_classifier_graph.png
            Graph that shows the average toxicity for every NBA team for the classifier that performed with the 
            highest accuracy from the imputed dataset.
