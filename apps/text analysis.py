import pandas as pd
import re
import nltk
from nltk.corpus import stopwords

meaningful_words = []
joined_words_table = []
keywords = []
replace_s = re.compile(r"'s")
keep_a_z = re.compile('[^a-z]')
stopswords = set(stopwords.words("english-v2-uspto-sklearn")) 

# Get the input text from the keyboard

text_list = []
text_keywords = str(input("Please enter some keywords:\n"))
text_list.append((text_keywords))

# Create an input dataframe

inputDF = pd.DataFrame()
inputDF['text'] = text_list

for row in inputDF.itertuples():
    for keyword in nltk.sent_tokenize(row[1]):
        keyword=keyword.lower()
        keyword = replace_s.sub(' ', keyword) 
        keyword = keep_a_z.sub(' ', keyword) 
        print("keywords include:", keyword)
        for word in nltk.word_tokenize(keyword):
            if word!='' and word.isalpha():
                if not word in stopswords:
                    meaningful_words.append((word))
                    print("\"", word, "\"", "is not a stopword")
                else:
                    print("\"", word, "\"", "is a stopword")


        joined_words = ( " ".join(meaningful_words))
        meaningful_words=[]
        joined_words_table.append((joined_words))
    joined_keywords = ( " ".join(joined_words_table))
    joined_words_table=[]
    keywords.append((joined_keywords))
              
inputDF['text']= keywords

print("final keywords:", keywords) 