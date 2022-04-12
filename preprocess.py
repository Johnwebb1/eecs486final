"""
This file must work to preprocess the tweet selection.
Preprocessing must include:
- Cleaning tweet of punctuation, and emojis (tokenize)
- Dealing with Hashtags (complete-guide-to-twitter-sentiment-analysis-part-one)
- Dealing with tagged users (@'s)
- Dealing with non english tweets (remove using textblob or langdetect)
    - Must clean text before using either.

Similar to what is done in class.
"""

import sys
import string
import re
from langdetect import detect
from porterStemmer import PorterStemmer

# This function handles hashtags in the text.
# This function returns all hashtags found within the text input
# The list of hashtags will be returned to be analyzed in additional files.
def get_hashtags(text):
    hashtags = re.findall('(#[A-Za-z]+[A-Za-z0-9-_]+)', text)
    return hashtags

# This function handles emojis in the text.
# This function strips emojis and returns the text input without emojis
def emoji_handler(text):
    new_text = re.sub(r'[\U00002600s-\U0010ffff]', '', text)
    emoji_regex = re.compile('[\U00002600-\U0010ffff]', flags=re.UNICODE)
    newest_text = emoji_regex.sub(r'', text)
    return newest_text

# This function handles cleaning the text.
# This function works to clean the text parameter for futher evaluation.
def clean_tweet(text):
    text = text.lower()
    # Selects @ sign for mentions. Takes out tagged username all together.
    text = re.sub(r'@[A-Za-z0-9_]+', '', text)
    # Remove hashtags
    text = re.sub(r'#', '', text)
    # Remove retweets:
    text = re.sub(r'rt : ', '', text)
    # Selects urls and removes them
    text = re.sub(r'https?:\/\/[A-Za-z0-9\.\/]+', '', text)
    # Selects outlier characters and removes them. Including &
    text = re.sub(r'ðŸ™&amp;', '', text)
    # Selects punctuation and removes
    punctuation = r"[-+().?!,;:'\"]"
    text = re.sub(punctuation, r"", text)
    # All unicode above ascii characters
    hor_ellipse = re.compile('[\U0000007B-\U0010ffff]', flags=re.UNICODE)
    text = hor_ellipse.sub(r'', text)
    # Selects newlines and removes them
    text = re.sub(r'\n', ' ', text)
    return text


# This function identifies the language of the tweet
# This function takes in a piece of text and then returns the language identified
def language_check(text):
    sample_string = ""
    lower_text = text.lower()
    tokens = lower_text.split()
    for token in tokens:
        if (all((ord(c) < 123 and ord(c) > 96) for c in token)):
            sample_string += token + " "
    if sample_string == "":
        return "na"
    else:
        return detect(sample_string)

# This function implements the PorterStemmer functionality from the porter stemmer file
# This function takes in a piece of text and then returns the
def stemWords(text):
    porterStemmer = PorterStemmer()
    newList = []
    tokens = text.split()
    for word in tokens:
        stemmedWord = porterStemmer.stem(word, 0, len(word)-1)
        newList.append(stemmedWord)
    return " ".join(newList)


def preprocess(tweet_text):
    hashtag_list = get_hashtags(tweet_text)
    tweet_text = emoji_handler(tweet_text)
    cleaned_tweet = clean_tweet(tweet_text)
    language = language_check(cleaned_tweet)
    processed_tweet = cleaned_tweet.strip()
    if language != "en":
        return "", []
    else:
        return processed_tweet, hashtag_list
