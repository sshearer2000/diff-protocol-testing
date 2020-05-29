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
