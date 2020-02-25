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
        setlf.masterarray = []
        self.adjectives = ['JJ','JJR','JJS']
        self.nouns = ['NN','NNS','NNP','NNPS','POS','PRP','PRP$']
        self.nouns_dt = ['NN','NNS','NNP','NNPS','POS','PRP','PRP$','DT']
        self.verbs = ['VB','VBD','VBP','VBZ']
        self.full_verbs = ['VB','VBD','VBP','VBZ','VBG','VBN']
        self.adj_dt = ['JJ','JJR','JJS','DT']
        
        
    def make_array(self):
        self.StyleArray = np.zeros((self.quantity,14+50)) #Change this 35 if you change the number of rows appended!
        
        for row in range(self.quantity):
            arrayrow = []
            SF = StyleFinder(self.df["story_text"].iloc[row]) #-
            arrayrow.append(SF.sentencel_mean()) #1
            arrayrow.append(SF.sentencel_std()) #2
            arrayrow.append(SF.wordl_mean()) #3
            arrayrow.append(SF.wordl_std()) #4
            arrayrow.append(SF.lex_diversity(self.size)) #5
            #Punctuation frequency
            arrayrow.append(SF.super_frequency(",")) #6
            arrayrow.append(SF.super_frequency(":")) #7
            arrayrow.append(SF.super_frequency(";")) #8
            arrayrow.append(SF.super_frequency(["\" ","\' "])) #9
            arrayrow.append(SF.super_frequency("...")) #10
            arrayrow.append(SF.super_frequency("!")) #11
            arrayrow.append(SF.super_frequency("-")) #12
            arrayrow.append(SF.super_frequency("--")) #13
            arrayrow.append(SF.super_frequency(")")) #14
            #Stop word grammar frequency
            arrayrow.append(SF.super_frequency("with",self.adjectives,self.adjectives,cancelvar='negk'))#1
            arrayrow.append(SF.super_frequency("with",self.adjectives,self.adjectives,cancelvar='nega'))#2
            arrayrow.append(SF.super_frequency("with",'_',self.nouns))#3
            arrayrow.append(SF.super_frequency("and",self.adjectives,self.adjectives))#4
            arrayrow.append(SF.super_frequency("and",["come","go"]))#5
            arrayrow.append(SF.super_frequency("but",'_',"not"))#6
            arrayrow.append(SF.super_frequency("but",'_',"for"))#7
            arrayrow.append(SF.super_frequency("but",'all',self.verbs))#8
            arrayrow.append(SF.super_frequency("but",'all',self.nouns_dt))#9
            arrayrow.append(SF.super_frequency("EX"))#10
            arrayrow.append(SF.super_frequency("Cause","DT",cancelvar='nega'))#11
            arrayrow.append(SF.super_frequency(["however","whyever","whoever","whatever","whenever","wherever"]))#12
            arrayrow.append(SF.super_frequency("said"))#13
            arrayrow.append(SF.super_frequency("while","DT",cancelvar='nega'))#14
            arrayrow.append(SF.super_frequency("as",['.',';','!','?'],self.nouns_dt))#15
            arrayrow.append(SF.super_frequency("as",['.',';','!','?'],self.nouns_dt,cancelvar='nega'))#16
            arrayrow.append(SF.super_frequency("as",'_',"though"))#17
            arrayrow.append(SF.super_frequency("as",'_',"JJ"))#18
            arrayrow.append(SF.super_frequency("as",["not","isn't","wasn't","weren't","ain't"]))#19
            arrayrow.append(SF.super_frequency("VBG",['.',',']))#20
            arrayrow.append(SF.super_frequency("VBG",self.verb))#21
            arrayrow.append(SF.super_frequency("VBG",self.adj_dt))#22
            arrayrow.append(SF.super_frequency("VBG",["IN","RB"]))#23
            arrayrow.append(SF.super_frequency(["although","though"],['-',',']))#24
            arrayrow.append(SF.super_frequency(["although","though"],'_',self.adjectives))#25
            arrayrow.append(SF.super_frequency(["although","though"],'_',self.nouns))#26
            arrayrow.append(SF.super_frequency(["although","though"],'_',['VBG']))#27
            arrayrow.append(SF.super_frequency("cause",'DT'))#28
            arrayrow.append(SF.super_frequency("that",'IN'))#29
            arrayrow.append(SF.super_frequency("to",self.nouns))#30
            arrayrow.append(SF.super_frequency("to",self.verbs,self.verbs,cancelvar='negk'))#31
            arrayrow.append(SF.super_frequency("to",self.adjectives))#32
            arrayrow.append(SF.super_frequency("to",'_',self.verbs))#33
            arrayrow.append(SF.super_frequency("why"))#34
            arrayrow.append(SF.super_frequency("how"))#35
            arrayrow.append(SF.super_frequency("if",'even'))#36
            arrayrow.append(SF.super_frequency("if",'even',cancelvar='nega'))#37
            arrayrow.append(SF.super_frequency("if",self.verbs))#38
            arrayrow.append(SF.super_frequency(["would","could","should","might","ought"],'MD',cancelvar="cpos"))#39
            arrayrow.append(SF.super_frequency("just",["RB","MD"],cancelvar="cpos"))#40
            arrayrow.append(SF.super_frequency("then",["and","."]))#41
            arrayrow.append(SF.super_frequency("then",self.nouns,'.'))#42
            arrayrow.append(SF.super_frequency(["there","here"],self.verbs))#43
            arrayrow.append(SF.super_frequency(["there","here"],self.nouns))#44
            arrayrow.append(SF.super_frequency(["there","here"],"IN"))#45
            arrayrow.append(SF.super_frequency(["i","me","we","us","my","mine","our","ours"]))#46
            arrayrow.append(SF.super_frequency(["you","your","yours"]))#47
            arrayrow.append(SF.super_frequency("might"))#48
            arrayrow.append(SF.super_frequency("maybe"))#49
            arrayrow.append(SF.super_frequency(['its','it\'s']))#50
            
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
    
    