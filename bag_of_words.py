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
