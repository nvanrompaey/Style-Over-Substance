import numpy as np
import pickle
from MassStyles import MassStyles
from sklearn.metrics.pairwise import cosine_similarity

class FanficRecommender():
    
    def __init__(self,):
        self.v = None #Setting up our cosine array before it's set up.
        self.X = None #And setting up our not-cosine-array, just in case.
        
    def fit(self,array,titles):
        #Takes an array of values, or a MassStyles array.
        #titles are your list of all titles
        if type(array)==str:
            infile = open(array,'rb')
            self.X = pickle.load(infile)
            infile.close()
        else:
            self.X = array
            
        self.titles=titles
        numt = self.X.shape[0]
        self.v = np.zeros((numt,numt))
        for i in range(numt):
            v[i] = np.array(cosine_similarity(X[i].reshape(1,-1),X[a].reshape(1,-1)) if i!=a else -1 for a in range(numt)).flatten()
        return None
    
    def recommend_fic(self,item,n):
        # Time to Recommend, Heretics! Put in a title, get n titles back! Aaaaa!
        ind = self.titles.index(item)
        recc = np.argsort(v[ind])
        recclist = [self.titles[i] for i in np.flip(recc[-n:])]
        return recclist
    
    
    def pickle_it(self,filename='ficsimilarity'):
        if self.v is not None:
            
            outfile= open(filename,'wb')
            pickle.dump((self.titles,self.v),outfile)
            outfile.close()
                
        else:
            print("There's nothing to pickle. Please run '.fit()' first.")
        
    def reload_pickle(self,filename='ficsimilarity'):
        self.titles=titles
        infile = open(filename,'rb')
        self.titles,self.v = pickle.load(infile)
        infile.close()
        
        
        