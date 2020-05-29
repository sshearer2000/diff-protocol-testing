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
