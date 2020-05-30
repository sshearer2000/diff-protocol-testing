#import statements 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import nltk
import spacy
nltk.download('punkt')
nltk.download('stopwords')
import string
import re
from pandas import DataFrame, Series
from nltk.util import ngrams
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from gensim.models.tfidfmodel import TfidfModel
from gensim.corpora.dictionary import Dictionary
from wordcloud import WordCloud
!python -m spacy download en_core_web_md #must restart runtime after running this line

#import csvs
stud = pd.read_csv('Difficulty Protocol Data - Student Protocol.csv',encoding="utf-8",index_col=0)
profta = pd.read_csv('Difficulty Protocol Data - Faculty_TA Protocol.csv',encoding="utf-8",index_col=0)

qs = ["topics", "questions", "struggles", "surprises"]

# indices of each question in each dataset
idx = {"topics": {"stu": 2, "ta": 3, "prof": 3},
       "questions": {"stu": -2, "ta":-3, "prof": -3},
       "struggles": {"stu": -3, "ta":-2, "prof": -2},
       "surprises": {"stu": -1, "ta":-1, "prof": -1}}
       
# container for saving ignored words actually encountered
ignored_encountered = set()

# specify source dataset for each group
dataset_dict = {"stu": stud, "profta": profta}

# container for lemmatized non-stopwords
lemm_answers = {"topics": {"stud": [], "profta": []},
              "questions": {"stud": [], "profta": []},
              "struggles": {"stud": [], "profta": []},
              "surprises": {"stud": [], "profta": []}}
              
# iterate through the 2 datasets (student, professor/TA)
for group in ["stud", "profta","]:
  # assign the correct dataset
  df = dataset_dict[group]

  # iterate through the 4 questions
  for q in qs:
    # select the correct column according to group and question
    col = df.values[:, idx[q][group]]

"""
      # tokenize and lemmatize with spacy's nlp
      processed = nlp(str(response).lower())
"""
    # create n-grams using previous functions
    processed = extract_ngrams(col,2)
    for ngram in ngram_list:
      stud_topics_ngrams.append(ngram)
      
    # container for the parsed column
    processed_str = ""
      
    for word in processed:

      # ignore \n
      if word.text == "\n":
        continue

      # ignore mathematical operators

      if word.text == "+":
        continue

      if word.text == ">":
         continue

      if word.is_punct:
        continue

      # ignore pronouns, but store in set of ignored and encountered words
      if word.lemma_ == "-PRON-":
        ignored_encountered.add(word.text)
        continue

      # ignore word, but store it
      if word.lemma_ in ignored_words:
        ignored_encountered.add(word.text)
        continue

      # ignore stop words, but store them
      if nlp.vocab[word.lemma].is_stop:
        ignored_encountered.add(word.text)
        continue

      processed_str += word.lemma_ + " "

    # remove trailing whitespace and newline characters
    processed_str = processed_str.strip().replace("\n", "")

    # save the string of useful words (without the whitespace at the end)
    lemm_answers[q][group].append(processed_str)
