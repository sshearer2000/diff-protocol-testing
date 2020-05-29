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
