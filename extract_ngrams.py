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
