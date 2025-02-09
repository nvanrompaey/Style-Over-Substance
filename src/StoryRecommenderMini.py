import numpy as np
import pandas as pd
import pickle
import nltk
from sklearn.metrics.pairwise import cosine_similarity



def assumed_style_match(df,msty,quantity, story):
    #Given a story, it checks whether the title actually exists, and if so, returns it as its relevant ID.
    #If not, return a message.
    if type(story) == str:
        try:
            story = df[df['title']==story].index.values[0]
        except IndexError:
            return f"This story is not available. {quantity} stories not found."
    
    #Creates an index series to match ID with position for easier matching
        v = df.index.to_series(index=range(df.shape[0]))
    story = v[v==story].index.values[0]
    
    #Takes the style matrix and runs a cosine similarity
    styarr = msty
    closeficnums = np.array([cosine_similarity(styarr[story].reshape(1,-1),styarr[x].reshape(1,-1)) 
                             if x!=story else -2 for x in range(styarr.shape[0])]).flatten()
    
    #Picks out Quantity most similar pieces of fiction and returns their positions, then takes the relevant ID and recommends.
    recc = np.argsort(closeficnums)
    reccreturn = v.iloc[recc[-quantity:]]
    x_choices = df['title'].loc(axis=0)[reccreturn]
    x_list = [(x_choices.iloc[quantity-a],closeficnums[recc[-a]][0,0]) for a in range(1,quantity+1)]
    
    #This part just puts it into a fancy string.
    recommendation = f"Why not read '{x_list[0][0]}' with a similarity of {x_list[0][1]:.5f}"
    if len(x_list)>1:
        for reccy in x_list[1:]:
            recommendation = recommendation + f", or '{reccy[0]}' with a similarity of {reccy[1]:.5f}"
    recommendation = recommendation + "?"
    
    return recommendation

#And this function, although inefficient, works well for Dash.
def recommend_stories(story,quantity):
    infile = open('FicStyleFeatures.pickle','rb')
    featuredf = pickle.load(infile)
    infile.close()
    return assumed_style_match(featuredf.iloc(axis=1)[:2],featuredf.iloc(axis=1)[2:].to_numpy(),quantity,story)