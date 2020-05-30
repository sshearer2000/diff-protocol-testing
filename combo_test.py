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
              
# number M of top words by TF IDF to display
M = 8

for question in qs:
  print("Question: %s --------------------" % question)

  # load student answers
  stu_ans = lemm_answers[question]["stud"]
  # concatenate into string, remove quotation marks, and remove square brackets
  stu_ans = str(stud_ans)[1:-1].replace("'", "")  

  # load professor answers
  profta_ans = lemm_answers[question]["profta"]
  # concatenate into string, remove quotation marks, and remove square brackets
  profta_ans = str(profta_ans)[1:-1].replace("'", "")  

  corpus = [stud_ans, profta_ans]

  # compute TF-IDF of words in the 3 documents
  vectorizer = TfidfVectorizer()
  X = vectorizer.fit_transform(corpus)
  X = X.todense()
  words = vectorizer.get_feature_names()

  print("Unique words in answers to '%s': %d." % (question, X.shape[1]))

  # print top M words by TF-IDF score
  X = np.asarray(X)

  group_names = ["stud", "profta"]
  top_words = {"stud": [], "profta": []}

  # find the M terms with the highest TF-IDF scores
  for i in range(X.shape[0]):
    doc_vals = X[i]
    srt = np.argsort(doc_vals)[::-1][:M]
    
    # print the M words with highest TF-IDF scores
    for j in range(M):
      top_words[group_names[i]].append(words[srt[j]])

  # container for counting frequencies of high TF-IDF words
  top_words_freqs = {"stu": [], "ta": [], "prof": []}

  for group in group_names:
    for w in range(len(top_words[group])):
      word = top_words[group][w]

      # counter for how many rows the word appears in
      encountered = 0  

      for i in range(len(lemm_answers[question][group])):
        enc = False
        answer = nlp(lemm_answers[question][group][i])

        for token in answer:
          # if at least one of the word tokens is equal to the word, encountered
          if word == token.text:
            enc = True
        
        if enc: encountered += 1

      # append the word and the frequency (rows encountered/total rows)
      top_words_freqs[group].append("%s (%d/%d)" % (word, encountered, len(lemm_answers[question][group])))

  # write result for this question to a Pandas dataframe
  out_df = pd.DataFrame()
  for key in top_words_freqs:
    out_df[key] = top_words_freqs[key]
  out_df.to_csv(data_path + "top_terms/" + question + ".csv", index=False)

  # print the high TF-IDF words and their associated row frequencies
  for group in group_names:
    print(group)
    for i in range(len(top_words_freqs[group])):
      print("%d. %s." % (i+1, top_words_freqs[group][i]))

  print("---------------------------\n")    
