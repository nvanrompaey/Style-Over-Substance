import numpy as np
import pandas as pd
import nltk
import re
from nltk import RegexpParser
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize,sent_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from MassStyles import MassStyles
from StyleFinder import StyleFinder

stop_words = set(stopwords.words('english'))

def simplify_replace(POST):
    #Takes a part of speech transformed string, and simplifies it down for fewer parts of speech types
    # Stop words are still important.
    x = re.sub(r'\bNN\w*\b','NN',POST).replace('EX','NN').replace('PRP','NN').replace('NN$','NN') #Contract Noun-types down
    x = re.sub(r'\bVB\w*\b','VB',x) #Contract Verb-types down
    x = re.sub(r'\bJJ\w*\b','JJ',x).replace('CD','JJ').replace('DT','JJ').replace('PDT','JJ') #Contract adjective-types down
    x = re.sub(r'\bRB\w*\b','RB',x) # Contract Adverb-types down
    x = x.replace('PRP$','POS') # Contract Possessives down
    x = x.replace('WP$','WP') # Contract Interrogatives/Relatives down
    x = x.replace('NN NN','NN') # Contract nouns further so we don't have tons of excessive ones
    return x

def clause_shrink(POST):
    # Takes a part of speech transformed string, and turns it into simple clause indicators
    return None
    
def POSparser(stringinq):
    #Takes a string as a name you want the new row to be called, 
    tokenized = sent_tokenize(stringinq)
    Taglist = []
    for i in tokenized:
        # DO THIS: minimize words and add dummy column
        wordsList = nltk.word_tokenize(i)
        tagged = nltk.pos_tag(wordsList)
        Taglist.append([i[1] for i in tagged])
        
    return [" ".join(a) for a in Taglist]

def simple_POSparser(stringinq):
    # Takes a string and after POSTing, simplifies down nouns and verbs.
    tokenized = sent_tokenize(stringinq)
    Taglist = []
    for i in tokenized:
        wordsList=nltk.word_tokenize(i)
        tagged = nltk.pos_tag(wordsList)
        Taglist.append([i[1] for i in tagged])
        
    return [simplify_replace(" ".join(a)) for a in Taglist]

def lazyPOSparser(stringinq):
    #Takes a string as a name you want the new row to be called, 
    # and a dataframe + column on which to perform the transformation
    tokenized = sent_tokenize(stringinq)
    Taglist = []
    for i in tokenized:
        # DO THIS: minimize words and add dummy column
        wordsList = nltk.word_tokenize(i)
        tagged = nltk.pos_tag(wordsList)
        Taglist.append([i[1] for i in tagged])
    flatlist = []
    for sublist in Taglist:
        for item in sublist:
            flatlist.append(item)
    return flatlist

def bad_analyzer(n):
    return None
    
    
    
def find_best_match(df,POSseries,n1,n2,story):
    # Takes a series based on a matrix, an ngram value pair, and a story index to compare.
    # Spits out a recommended story title and its POS shape
    if type(story) == str:
        try:
            story = df[df['title']==story].index.values[0]
        except IndexError:
            return "This story is not available."
    
    v = POSseries.index.to_series(index=range(POSseries.size))
    story = v[v==story].index.values[0]
    
    
    
    tfidf = TfidfVectorizer(ngram_range=(n1,n2),token_pattern=r"(?u)\b\w\w+\b|!|\?|\"|\'|,|")
    POSjoined = POSseries.apply(lambda x: " ".join(x))
    POSTFIDF = tfidf.fit_transform(POSjoined)
    feature_freq_df = pd.DataFrame.sparse.from_spmatrix(POSTFIDF)
    Targetfic = feature_freq_df.iloc[story].to_numpy().reshape(1,-1)
    closeficnums = np.array([cosine_similarity(Targetfic,
                                 feature_freq_df.iloc[x].to_numpy().reshape(1,-1)) if x!=story else -1 for x in range(1000)]).flatten()
    recc = np.argmax(closeficnums)
    reccreturn = v.iloc[recc]
    return df['title'].loc(axis=0)[reccreturn],closeficnums[recc],POSseries.loc(axis=0)[reccreturn]
    
    
def style_match(df,quantity,size,story):
    # Similar to the above, but takes a size instead of a n1/n2, and a quantity to determine how many stories will be in there.
    if type(story) == str:
        try:
            story = df[df['title']==story].index.values[0]
        except IndexError:
            return "This story is not available."
    
    v = df.index.to_series(index=range(df.shape[0]))
    story = v[v==story].index.values[0]
    
    msty = MassStyles(df,quantity,size)
    msty.make_array()
    styarr = msty.StyleArray
    closeficnums = np.array([cosine_similarity(styarr[story].reshape(1,-1),styarr[x].reshape(1,-1)) 
                             if x!=story else -2 for x in range(quantity)]).flatten()
    
    recc = np.argsort(closeficnums)
    reccreturn = v.iloc[recc[-3:]]
    three_choices = df['title'].loc(axis=0)[reccreturn]
    return [three_choices.iloc[2],closeficnums[recc[-1]][0,0]] ,[three_choices.iloc[1],closeficnums[recc[-2]][0,0]] , [three_choices.iloc[0], closeficnums[recc[-3]][0,0]]
    
def assumed_style_match(df,msty,quantity,story):
    if type(story) == str:
        try:
            story = df[df['title']==story].index.values[0]
        except IndexError:
            return "This story is not available."
        
        v = df.index.to_series(index=range(df.shape[0]))
    story = v[v==story].index.values[0]
    
    styarr = msty
    closeficnums = np.array([cosine_similarity(styarr[story].reshape(1,-1),styarr[x].reshape(1,-1)) 
                             if x!=story else -2 for x in range(quantity)]).flatten()
    
    recc = np.argsort(closeficnums)
    reccreturn = v.iloc[recc[-3:]]
    three_choices = df['title'].loc(axis=0)[reccreturn]
    return [three_choices.iloc[2],closeficnums[recc[-1]][0,0]] ,[three_choices.iloc[1],closeficnums[recc[-2]][0,0]] , [three_choices.iloc[0], closeficnums[recc[-3]][0,0]]

#list(movie_dummy.index.values) <-- a good way to deal with the index woes.