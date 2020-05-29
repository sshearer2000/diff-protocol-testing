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
