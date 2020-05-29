def wordcloud(dictionary):
  wc = WordCloud(background_color='black',max_words=2000,width=1024,height=720,colormap="spring")
  wc.generate_from_frequencies(dict(dictionary))
  return wc
