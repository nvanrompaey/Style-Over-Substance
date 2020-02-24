import numpy as np
import pandas as pd
import nltk
import pickle
from nltk.tokenize import word_tokenize,sent_tokenize
from nltk import Text
from nltk.probability import FreqDist
from StyleFinder import StyleFinder


class MassStyles():
    
    
    def __init__(self,df,quantity,size):
        # Quantity is just how many rows you want. Size is 'something per X words' where X is size.
        self.df = df.iloc[:quantity]
        self.quantity=quantity
        self.size=size
        self.StyleArray=None
        
        
    def make_array(self):
        self.StyleArray = np.zeros((self.quantity,35)) #Change this 35 if you change the number of rows appended!
        
        for row in range(self.quantity):
            arrayrow = []
            SF = StyleFinder(self.df["story_text"].iloc[row]) #-
            arrayrow.append(SF.sentencel_mean()) #1
            arrayrow.append(SF.sentencel_std()) #2
            arrayrow.append(SF.wordl_mean()) #3
            arrayrow.append(SF.wordl_std()) #4
            arrayrow.append(SF.lex_diversity(self.size)) #5
            #Punctuation frequency
            arrayrow.append(SF.token_frequency(",",self.size)) #6
            arrayrow.append(SF.token_frequency(":",self.size)) #7
            arrayrow.append(SF.token_frequency(";",self.size)) #8
            arrayrow.append(SF.token_frequency("\" ",self.size)+SF.token_frequency("\' ",self.size)) #9
            arrayrow.append(SF.token_frequency("...",self.size)) #10
            arrayrow.append(SF.token_frequency("!",self.size)) #11
            arrayrow.append(SF.token_frequency("-",self.size)) #12
            arrayrow.append(SF.token_frequency("--",self.size)) #13
            arrayrow.append(SF.token_frequency(")",self.size)) #14
            #Stop word frequency
            arrayrow.append(SF.token_frequency("and",self.size)) #15 check
            arrayrow.append(SF.token_frequency("but",self.size)) #16 check
            arrayrow.append(SF.token_frequency("however",self.size)) #17 check
            arrayrow.append(SF.token_frequency("said",self.size)) #18 check
            arrayrow.append(SF.token_frequency("while",self.size)) #19 check
            arrayrow.append(SF.token_frequency("as",self.size)) #20 check
            arrayrow.append(SF.token_frequency("ing",self.size)) #21 check
            arrayrow.append(SF.token_frequency("though",self.size)) #22 check
            arrayrow.append(SF.token_frequency("with",self.size)) #23 check
            arrayrow.append(SF.token_frequency("cause",self.size)) #24 check
            arrayrow.append(SF.token_frequency("to",self.size)) #25 check
            arrayrow.append(SF.token_frequency("this",self.size)) #26 negate <=====
            arrayrow.append(SF.token_frequency("that",self.size)) #27 check
            arrayrow.append(SF.token_frequency("why",self.size)) #28 check
            arrayrow.append(SF.token_frequency("how",self.size)) #29 check
            arrayrow.append(SF.token_frequency("if",self.size)) #30 check
            arrayrow.append(SF.token_frequency("then",self.size)) #31 check
            arrayrow.append(SF.token_frequency("there",self.size)) #32 check
            arrayrow.append(SF.token_frequency("might",self.size)) #33 check
            arrayrow.append(SF.token_frequency("maybe",self.size)) #34 check
            arrayrow.append(SF.token_frequency("its",self.size)+SF.token_frequency('it\'s',self.size)) # 35 check
            
            #And set the new row to the current row
            self.StyleArray[row] = arrayrow
        return None
            
    def pickle_it(self,filename='FicStyleArray'):
        if self.StyleArray is not None:
            
            outfile= open(filename,'wb')
            pickle.dump(self.StyleArray,outfile)
            outfile.close()
                
        else:
            print("There's nothing to pickle. Please run 'make_array()' first.")
                
            
        return None
    
    