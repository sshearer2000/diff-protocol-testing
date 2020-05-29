# -*- coding: utf-8 -*-
"""Sydney and Frankie - Difficulty Protocol Code.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/12Fdy8D3-9nCQ1wUsuMv5euOROtB7VbFW

# Import statements
"""

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

"""# Function to rename long-worded columns"""

def rename_col(csv, og_name, new_name):
    csv.rename(columns={og_name:new_name},inplace=True)

"""# Import csv files as dataframes
To be able to import csv files, make sure to upload files first via the tabs on the left
"""

stud = pd.read_csv('Difficulty Protocol Data - Student Protocol.csv',encoding="utf-8",index_col=0)
profta = pd.read_csv('Difficulty Protocol Data - Faculty_TA Protocol.csv',encoding="utf-8",index_col=0)

"""# Rename columns"""

rename_col(stud,'Timestamp','time')
rename_col(stud,'Participant ID','id')
rename_col(stud, 'What topics did you cover in class this week?','topics_covered')
rename_col(stud,'What kinds of activities did you focus on out of class this week?  [Reading/Research]','reading_research')
rename_col(stud, 'What kinds of activities did you focus on out of class this week?  [Continuing/Finishing In-Class Work]','finishing_class_work')
rename_col(stud, 'What kinds of activities did you focus on out of class this week?  [Homework Problems/Assignments]','homework')
rename_col(stud, 'What kinds of activities did you focus on out of class this week?  [Out-of-Class Labs]', 'out_of_class_labs')
rename_col(stud, 'What kinds of activities did you focus on out of class this week?  [Multi-Week Project Experience]','multi_week_project')
rename_col(stud, 'What kinds of activities did you focus on out of class this week?  [Other]','other_outside_class')
rename_col(stud, 'What concepts/activities did you or your peers struggle most with this week?','struggle_concepts')
rename_col(stud, 'What questions did you or your peers raise to your instructor/TAs this week?','questions_raised')
rename_col(stud, 'Were there any questions from your peers that surprised you this week?','surprise_questions')

rename_col(profta, 'Timestamp','time')
rename_col(profta,'Participant ID', 'id')
rename_col(profta, 'What is your role in the course you are reflecting on? ','role')
rename_col(profta, 'What topics did you cover this week?','topics_covered')
rename_col(profta, 'What kinds of activities did your students focus  on this week out of class?  [Reading/Research]','reading_research')
rename_col(profta, 'What kinds of activities did your students focus  on this week out of class?  [Continuing/Finishing In-Class Work]','finishing_class_work')
rename_col(profta, 'What kinds of activities did your students focus  on this week out of class?  [Homework Problems/Assignments]','homework')
rename_col(profta, 'What kinds of activities did your students focus  on this week out of class?  [Out-of-Class Labs]', 'out_of_class_labs')
rename_col(profta, 'What kinds of activities did your students focus  on this week out of class?  [Multi-Week Project Experience]','multi_week_project')
rename_col(profta, 'What kinds of activities did your students focus  on this week out of class?  [Other]','other_outside_class')
rename_col(profta, 'By observation, what concepts or processes did students struggle with?','struggle_concepts')
rename_col(profta, 'What questions did students raise this week?','questions_raised')
rename_col(profta, 'Which student questions were surprising to you?','surprise_questions')

"""# Replace NA values with strings"""

stud.topics_covered = stud.topics_covered.replace({None:'NA'})
stud.reading_research = stud.reading_research.replace({None:'NA'})
stud.finishing_class_work = stud.finishing_class_work.replace({None:'NA'})
stud.homework = stud.homework.replace({None:'NA'})
stud.out_of_class_labs = stud.out_of_class_labs.replace({None:'NA'})
stud.multi_week_project = stud.multi_week_project.replace({None:'NA'})
stud.other_outside_class = stud.other_outside_class.replace({None:'NA'})
stud.struggle_concepts = stud.struggle_concepts.replace({None:'NA'})
stud.questions_raised = stud.questions_raised.replace({None:'NA'})
stud.surprise_questions = stud.surprise_questions.replace({None:'NA'})

profta.topics_covered = profta.topics_covered.replace({None:'NA'})
profta.reading_research = profta.reading_research.replace({None:'NA'})
profta.finishing_class_work = profta.finishing_class_work.replace({None:'NA'})
profta.homework = profta.homework.replace({None:'NA'})
profta.out_of_class_labs = profta.out_of_class_labs.replace({None:'NA'})
profta.multi_week_project = profta.multi_week_project.replace({None:'NA'})
profta.other_outside_class = profta.other_outside_class.replace({None:'NA'})
profta.struggle_concepts = profta.struggle_concepts.replace({None:'NA'})
profta.questions_raised = profta.questions_raised.replace({None:'NA'})
profta.surprise_questions = profta.surprise_questions.replace({None:'NA'})

"""# Tokenize function"""

#sentence tokenizer for bag of words and n-grams, returns tokenized sentences 
#for each column
def tokenize(csv,col):
    whole_text = ''
    for sentence in csv[col]:
        if not str(sentence).endswith(string.punctuation):
            sentence+='. '
            whole_text += str(sentence)
    tokenized = nltk.sent_tokenize(whole_text)
    return tokenized

"""# Stop Word Categories

1.   Getting rid of any descriptor words (i.e. briefly, basically, current, towards)
2.   Getting rid of typical classroom activities (i.e. talked, presented, covering)
3. Getting rid of words that don’t give any insight (i.e. barely, spent, able, end, began)

# Bag of words function
"""

#creates a bag of words for each function
def bag_of_words(tokenized):
    #extends stop words list with context specific frequent words
    stop_words = list(stopwords.words('english'))
    ext = ['2','briefly','primarily','talked','discussed','continuing',
           'students','discuss','spent','able','barely','end','covering',
           'basically','current','towards','began','none','na','n','nope','pre',
           'vs','mainly','sick','lots','weeks']
    stop_words.extend(ext)
    #removes non-alphabetical characters and white spaces
    for i in range(len(tokenized)):
        tokenized[i]=tokenized[i].lower()
        tokenized[i] = re.sub(r'\W',' ',tokenized[i])
        tokenized[i] = re.sub(r'\s+', ' ', tokenized[i])
    #removes blank answers
    for i in reversed(range(len(tokenized))):
        if tokenized[i]==' ':
            del tokenized[i]
    #creates list of lists, inside lists contains sentences tokenized by word
    list_of_lists = []
    for sentence in tokenized:
        tokens = nltk.word_tokenize(sentence)
        sentence_list = []
        #removes stopwords
        for token in tokens:
          if token in stop_words:
            continue
          else:
            sentence_list.append(token)
        list_of_lists.append(sentence_list)
    return list_of_lists

"""# Create n-grams function"""

#creates bag of n-grams
def extract_ngrams(col,num):
    #creates a list of lists of the sentences tokenized by word
    list_of_lists = []
    #extends stop words with frequent unneccesary words
    stop_words = list(stopwords.words('english'))
    #descriptor words (i.e. briefly, basically, current, towards)
    des = ['briefly','mostly','basically','different','forward','primarily',
           'barely','first','many','new','much','already','heavily','hardest',
           'actually','particularly','really','best','lot','extremely','super',
           'unclear','previous','good','clearly','exactly','better','previosuly',
           'less','early','next','mainly','hard','frustrating','well','curious',
           'enough','surprised','kinda','scary','lots','late','fair','seemingly',
           'difficult','actual','old','biggest','specific','successfully',
           'comfortable','sufficient','long','clear','minimally','cool']
    #typical classroom activities (i.e. talked, presented, covering)
    acts = ['worked','covered','period','class','zoom','applying','finishing',
            'continue','discussing','discuss','discussed','learned','practice',
            'covering','writing','week','students','contine','focused','devoted',
            'practiced','peers','struggled','semester','confused','know',
            'understand','asked','babynames','campaign','baumer','asking','told',
            'weeks','students','material','professor','work','questions','thought',
            'cover','spoke','grasping','picked','spent','people','peoples','bmi',
            'encountered','help','focus','peer','group','looking','problems',
            'course','campus','grasp','person','struggle','talked','related',
            'based','mentioned','clark','learn']
    #words that don’t give any insight (i.e. spent, able, end, began,vs, etc)
    etc = ['etc','also','began','time','around','5','2','able','holding',
           'animal','shelter','going','added','changed','end','towards','pros',
           'cons','like','1','3','amount','number','vs','bit','anything','getting',
           'although','could','get','anyone','still','4','past','us','everything',
           'figured','e','put','because','n','part','trouble','im','didnt','comes',
           'mind','cant','let','none','hitting','issues','way','choose','wayyyy',
           'came','love','go','since','though','something','would','within','along',
           'hear','look','see','remember','nothing','stands','other','others',
           'need','givern','certain','kinds','matters','among','across','come',
           'feel','putting','opinion','manner','needed','moving','arise',
           'constitutes','made','kind','brought','one','never','seemed','pain',
           'heard','reality','two','ever','difficulties','works','however','knows']
    stop_words.extend(des)
    stop_words.extend(acts)
    stop_words.extend(etc)
    for sentence in col:
      new_sent = ''
      for word in sentence.split():
        #removes stop words
        if word not in stop_words:
          new_sent += word
          new_sent += ' '
      n_grams=ngrams(nltk.word_tokenize(new_sent),num)
      ret = [' '.join(grams) for grams in n_grams]
      list_of_lists.append(ret)
    return list_of_lists

"""# Create student bags of words"""

#Topics Covered
stud_topics_tkn = tokenize(stud,'topics_covered')
stud_topics_bag = bag_of_words(stud_topics_tkn)
print(stud_topics_bag)

stud_topics_ngrams = []
ngram_list = extract_ngrams(stud_topics_tkn,2)
for ngram in ngram_list:
    stud_topics_ngrams.append(ngram)
print("Student Topics:",stud_topics_ngrams,'\n')

#Concepts Struggled
stud_struggles_tkn = tokenize(stud,'struggle_concepts')
stud_struggles_bag = bag_of_words(stud_struggles_tkn)

stud_struggles_ngrams = []
ngram_list = extract_ngrams(stud_struggles_tkn,2)
for ngram in ngram_list:
    stud_struggles_ngrams.append(ngram)
print("Student Struggles:",stud_struggles_ngrams,'\n')

#Questions Asked
stud_questions_tkn = tokenize(stud,'questions_raised')
stud_questions_bag = bag_of_words(stud_questions_tkn)

stud_questions_ngrams = []
ngram_list = extract_ngrams(stud_questions_tkn,2)
for ngram in ngram_list:
    stud_questions_ngrams.append(ngram)
print("Student Questions:",stud_questions_ngrams,'\n')

#Surprise Questions
stud_surprise_tkn = tokenize(stud,'surprise_questions')
stud_surprise_bag = bag_of_words(stud_surprise_tkn)

stud_surprise_ngrams = []
ngram_list = extract_ngrams(stud_surprise_tkn,2)
for ngram in ngram_list:
    stud_surprise_ngrams.append(ngram)
print("Student Surprise Questions:",stud_surprise_ngrams,'\n')

"""# Create Prof./TA Bag of Words"""

#Topics Covered
profta_topics_tkn = tokenize(profta,'topics_covered')
profta_topics_bag = bag_of_words(profta_topics_tkn)

profta_topics_ngrams = []
ngram_list = extract_ngrams(profta_topics_tkn,2)
for ngram in ngram_list:
    profta_topics_ngrams.append(ngram)
print("Professor/TA Topics:",profta_topics_ngrams,'\n')

#Concepts Struggled
profta_struggles_tkn = tokenize(profta,'struggle_concepts')
profta_struggles_bag = bag_of_words(profta_struggles_tkn)

profta_struggles_ngrams = []
ngram_list = extract_ngrams(profta_struggles_tkn,2)
for ngram in ngram_list:
    profta_struggles_ngrams.append(ngram)
print("Professor/TA Struggles:",profta_struggles_ngrams,'\n')

#Questions Asked
profta_questions_tkn = tokenize(profta,'questions_raised')
profta_questions_bag = bag_of_words(profta_questions_tkn)

profta_questions_ngrams = []
ngram_list = extract_ngrams(profta_questions_tkn,2)
for ngram in ngram_list:
    profta_questions_ngrams.append(ngram)
print("Professor/TA Questions:",profta_questions_ngrams,'\n')

#Surprise Questions
profta_surprise_tkn = tokenize(profta,'surprise_questions')
profta_surprise_bag = bag_of_words(profta_surprise_tkn)

profta_surprise_ngrams = []
ngram_list = extract_ngrams(profta_surprise_tkn,2)
for ngram in ngram_list:
    profta_surprise_ngrams.append(ngram)
print("Professor/TA Surprise Questions:",profta_surprise_ngrams,'\n')

"""# Fitting TFIDF Model"""

def tfidfModelling(bag):
  dictionary = Dictionary(bag)
  corpus = [dictionary.doc2bow(doc) for doc in bag]
  return(TfidfModel(corpus),corpus,dictionary)

"""#Top 10 tf-idf words"""

def top10Idf (bag):
  model, corpus,dictionary = tfidfModelling(bag)
  weights = []
  for doc in corpus:
    for combo in model[doc]:
      weights.append(combo)
  #sorted weighted list
  weights = sorted(weights, key=lambda w : w[1], reverse=True)
  new_weights = []
  #make list unique
  for word in weights:
    if word not in new_weights:
      new_weights.append(word)
  #print top 10 words based on tfidf
  for term_id, weight in new_weights[0:10]:
    print(dictionary.get(term_id), weight)
  print("\n") 
  #return top 10 words based on tfidf
  return [(dictionary[pair[0]],pair[1]) for pair in new_weights[0:10]]

"""# Prints the Top 10 for Prof/TA & Students"""

#Topics Covered
print("Professor/TA Topics:")
top_profta_topics = top10Idf(profta_topics_bag)
print("Student Topics:")
top_stud_topics = top10Idf(stud_topics_bag)

#Struggles Encountered
print("Professor/TA Struggles:")
top_profta_struggles = top10Idf(profta_struggles_bag)
print("Student Struggles:")
top_stud_struggles = top10Idf(stud_struggles_bag)

#Questions Asked
print("Professor/TA Questions:")
top_profta_questions = top10Idf(profta_questions_bag)
print("Student Questions:")
top_stud_questions = top10Idf(stud_questions_bag)

#Surprise Questions Asked
print("Professor/TA Surprise Questions:")
top_profta_surprise = top10Idf(profta_surprise_bag)
print("Student Surprise Questions:")
top_stud_surprise = top10Idf(stud_surprise_bag)

"""# Prints the top 10 N-Grams"""

#Topics Covered
print("Professor/TA Topics:")
top_profta_topics2 = top10Idf(profta_topics_ngrams)
print("Student Topics:")
top_stud_topics2 = top10Idf(stud_topics_ngrams)

#Struggles Encountered
print("Professor/TA Struggles:")
top_profta_struggles2 = top10Idf(profta_struggles_ngrams)
print("Student Struggles:")
top_stud_struggles2 = top10Idf(stud_struggles_ngrams)

#Questions Asked
print("Professor/TA Questions:")
top_profta_questions2 = top10Idf(profta_questions_ngrams)
print("Student Questions:")
top_stud_questions2 = top10Idf(stud_questions_ngrams)

#Surprise Questions Asked
print("Professor/TA Surprise Questions:")
top_profta_surprise2 = top10Idf(profta_surprise_ngrams)
print("Student Surprise Questions:")
top_stud_surprise2 = top10Idf(stud_surprise_ngrams)

"""# Function to make Word Cloud"""

def wordcloud(dictionary):
  wc = WordCloud(background_color='black',max_words=2000,width=1024,height=720,colormap="spring")
  wc.generate_from_frequencies(dict(dictionary))
  return wc

"""# Function to Plot Word Clouds in a Grid"""

def plotclouds(wc1,wc2,wc3,wc4,save):
  plt.subplot(2,2,1).imshow(wc1,interpolation='bilinear')
  plt.title("Tfidf")
  plt.axis("off")
  plt.subplot(2,2,2).imshow(wc2,interpolation='bilinear')
  plt.title("NGrams Tfidf")
  plt.axis("off")
  plt.subplot(2,2,3).imshow(wc3,interpolation='bilinear')
  plt.axis("off")
  plt.subplot(2,2,4).imshow(wc4,interpolation='bilinear')
  plt.axis("off")
  plt.savefig(save)
  plt.clf()

"""# Plotting Word Clouds"""

#Topics Covered
wc1 = wordcloud(top_profta_topics)
wc2 = wordcloud(top_profta_topics2)
wc3 = wordcloud(top_stud_topics)
wc4 = wordcloud(top_stud_topics2)
plotclouds(wc1,wc2,wc3,wc4,'cloud_topics')

#Questions Asked
wc1 = wordcloud(top_profta_questions)
wc2 = wordcloud(top_profta_questions2)
wc3 = wordcloud(top_stud_questions)
wc4 = wordcloud(top_stud_questions2)
plotclouds(wc1,wc2,wc3,wc4,'cloud_questions')

#Struggles Encountered
wc1 = wordcloud(top_profta_struggles)
wc2 = wordcloud(top_profta_struggles2)
wc3 = wordcloud(top_stud_struggles)
wc4 = wordcloud(top_stud_struggles2)
plotclouds(wc1,wc2,wc3,wc4,'cloud_struggles')

#Surprise Questions Asked
wc1 = wordcloud(top_profta_surprise)
wc2 = wordcloud(top_profta_surprise2)
wc3 = wordcloud(top_stud_surprise)
wc4 = wordcloud(top_stud_surprise2)
plotclouds(wc1,wc2,wc3,wc4,'cloud_surprise')

"""# Sentence TFIDF"""

def senttfidf(bag):
  model, corpus,dictionary = tfidfModelling(bag)
  big_list = []
  for doc in corpus: #Loops through each entry in the column
    weights = []
    for combo in model[doc]: #Loops through each Bigram-weight combination for each response
      weights.append(combo)
    weights = sorted(weights, key=lambda w : w[1], reverse=True) #Sorts the weights from highest to lowest for each response
    if len(weights) != 0: #makes sure that response is not blank
      big_list.append(weights[0]) #Appends only the highest weighted combination from each response to the overall list
  ret_list = []
  for term_id, weight in big_list: #Appends only the Bigram to ret_list
    ret_list.append(dictionary.get(term_id))
  return ret_list

"""#Create Similarity key/value Pairs"""

def create_similarity(lst_words):
  nlp = spacy.load('en_core_web_md')
  cat = {}
  for word in lst_words: 
    sim = {}
    for comp in lst_words:
      wd = nlp(word)
      cp = nlp(comp)
      sim[comp] = wd.similarity(cp) #Calculates similarity between two Bigrams
    sim = sorted(sim.items(), key=lambda kv: kv[1],reverse=True) #Sort similarities based on calculated similarity
    if sim[0][1] == 1.0: #Checks if its the same Bigram
      cat[word]=sim[1][0] #If it is, append next highest ranking Bigram
    else:
      cat[word]=sim[0][0] #Appends highest ranking Bigram
  return cat

"""#Creates First Round of Groupings"""

def recursive(key,dictionary, group_list):
  group_list.append(key)
  v = dictionary[key]
  if v not in group_list:
    recursive(v,dictionary,group_list)
  return group_list

def get_sets(word_assoc):
  lol = []
  for key in list(word_assoc.keys()):
      emp = [] #list for each groups
      emp = set(recursive(key,word_assoc,[]))
      lol.append(emp)
  return lol

"""#Create Final Groups"""

def create_groups(list_of_sets):
  i = len(list_of_sets) - 1
  while i > 0: #Loops from the back to the front
    j = i-1 #Checks the bigram before the current one
    while j >= 0:
      if not list_of_sets[i].isdisjoint(list_of_sets[j]): #Checks for at least one similar Bigram
        list_of_sets[i].update(list_of_sets[j]) #Merges the two sets into one set
        del list_of_sets[j] #Deletes the extra set
        i-= 1
      j-=1
    i-=1
  return list_of_sets #returns list of finalized sets

"""#Assistance from Faculty

https://docs.python.org/3/library/stdtypes.html#set-types-set-frozenset

Here's some pseudo-code suggestions based on your email and what you have:

Turn each list from get_groups(word_assoc) into a "set" type. (may want frozen set type ) (may need to turn sublists into set/frozenset first).

bgram_sets = frozenset(get_groups(word_assoc))

for x in bgram_sets:

  x.isdisjoint( bgrams_sets(excluding x) ) <-- gives true/false for set overlaps.

  Then do something with the false-values to merge sets etc. 

  --perhaps this could be done in a recursively called function instead that also merges the two sets if they aren't disjoint --

#Run all the functions to create final groups
"""

stud_topics_final_groups = create_groups(list(get_sets(create_similarity(senttfidf(stud_topics_ngrams)))))
print('Student Topic Groups:')
for group in stud_topics_final_groups:
  print(group)
print('\n')
profta_topics_final_groups = create_groups(list(get_sets(create_similarity(senttfidf(profta_topics_ngrams)))))
print('Professor/TA Topic Groups:')
for group in profta_topics_final_groups:
  print(group)

print('\n')
print('\n')

stud_struggles_final_groups = create_groups(list(get_sets(create_similarity(senttfidf(stud_struggles_ngrams)))))
print('Student Struggles Groups:')
for group in stud_struggles_final_groups:
  print(group)
print('\n')
profta_struggles_final_groups = create_groups(list(get_sets(create_similarity(senttfidf(profta_struggles_ngrams)))))
print('Professor/TA Struggles Groups:')
for group in profta_struggles_final_groups:
  print(group)

print('\n')
print('\n')

stud_questions_final_groups = create_groups(list(get_sets(create_similarity(senttfidf(stud_questions_ngrams)))))
print('Student Questions Groups:')
for group in stud_questions_final_groups:
  print(group)
print('\n')
profta_questions_final_groups = create_groups(list(get_sets(create_similarity(senttfidf(profta_questions_ngrams)))))
print('Professor/TA Questions Groups:')
for group in profta_questions_final_groups:
  print(group)

print('\n')
print('\n')

stud_surprise_final_groups = create_groups(list(get_sets(create_similarity(senttfidf(stud_surprise_ngrams)))))
print('Student Surprise Questions Groups:')
for group in stud_surprise_final_groups:
  print(group)
print('\n')
profta_surprise_final_groups = create_groups(list(get_sets(create_similarity(senttfidf(profta_surprise_ngrams)))))
print('Professor/TA Surprise Questions Groups:')
for group in profta_surprise_final_groups:
  print(group)