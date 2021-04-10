import nltk

def stackfind(idea):
  from nltk.tokenize import word_tokenize
  nltk.download("book")
  nltk.download("omw")
  ml=[]

  idea=word_tokenize(idea)
  from nltk.corpus import stopwords
  stop_words=set(stopwords.words("english"))
  filtered=[]
  for w in idea:
    if w not in stop_words:
      filtered.append(w)

  from nltk.stem import WordNetLemmatizer
  lemmatizer=WordNetLemmatizer()
  stemmed=[]
  for w in filtered:
    stemmed.append(lemmatizer.lemmatize(w))

  from nltk.corpus import wordnet
  L1=[] #opencv
  synonymns1=[]

  for i in wordnet.synsets("image"):
    for l in i.lemmas():
      synonymns1.append(l.name())
  for i in wordnet.synsets("gesture"):
    for l in i.lemmas():
      synonymns1.append(l.name())


  i1=set(stemmed).intersection(synonymns1)
  if len(i1)>0:
    ml.append("opencv")

  L2=["video","detect","text"] #teseract
  synonymns2=[]
  for x in L2:
    for i in wordnet.synsets(x):
      for l in i.lemmas():
        synonymns2.append(l.name())

    

  i2=set(stemmed).intersection(L2)


  if len(i2)==3:
    ml.append("teseract")

  L4=["app","mobile"] #AppDev
  synonymns4=[]
  for x in L4:
    for i in wordnet.synsets(x):
      for l in i.lemmas():
        synonymns4.append(l.name())

  i4=set(stemmed).intersection(synonymns4)

  if len(i4)>0:
    ml.append("AppDev")

  L3=["video","edit","editing"] #AE
  synonymns3=[]
  for x in L3:
    for i in wordnet.synsets(x):
      for l in i.lemmas():
        synonymns3.append(l.name())

  i3=set(stemmed).intersection(synonymns3)

  if len(i3)>=2:
    print("AfterEffects")
    ml.append("AfterEffects")

  L5=["web","site","website","scrape"] #Website
  synonymns5=[]
  for x in L5:
    for i in wordnet.synsets(x):
      for l in i.lemmas():
        synonymns5.append(l.name())
    

  i5=set(stemmed).intersection(synonymns5)

  if len(i5)>=1:
    ml.append("HTML")
    ml.append("CSS")
    ml.append("JS")
  return ml
