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
