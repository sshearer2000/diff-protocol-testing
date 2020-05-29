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
