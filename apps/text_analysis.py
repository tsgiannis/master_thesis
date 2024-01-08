import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
import os


def keywords_processing(input_keywords):
    meaningful_words = []
    meaningless_words = []
    joined_words_table = []
    keywords = []
    replace_s = re.compile(r"'s")
    keep_a_z = re.compile('[^a-z]')
    ROOT_DIRECTORY = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    stopwords_path =os.path.join(ROOT_DIRECTORY,'resources','english-v2-uspto-sklearn.txt')
    with open(stopwords_path) as f:
        stopwords = f.read().splitlines()
    # Create an input dataframe
    text_list = input_keywords.split()

    inputDF = pd.DataFrame()
    inputDF['text'] = text_list
    for row in inputDF.itertuples():
        keyword = row[1]
        keyword = keyword.lower()
        keyword = replace_s.sub(' ', keyword)
        keyword = keep_a_z.sub(' ', keyword)
            #print("keywords include:", keyword)
        if keyword != '' and keyword.isalpha():
            if not keyword in stopwords:
                meaningful_words.append((keyword))
            else:
                meaningless_words.append((keyword))

    return meaningful_words,meaningless_words

if __name__ == '__main__':

    meaningful,meaningless = keywords_processing('magnetic light and')
    print(meaningful)
    print(meaningless)



