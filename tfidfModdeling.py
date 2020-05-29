def tfidfModelling(bag):
  dictionary = Dictionary(bag)
  corpus = [dictionary.doc2bow(doc) for doc in bag]
  return(TfidfModel(corpus),corpus,dictionary)
