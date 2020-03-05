import numpy as np
import nltk
import pickle
from nltk.tokenize import word_tokenize,sent_tokenize
from nltk import Text
from StyleFinder import StyleFinder
import scipy.sparse as sparse

class MassStylesMini():
    
    
    def __init__(self,text):
        # StyleArray is initiated as nothing, text is just storing it, the rest are just signals to particular POS
        #Then an unnecessary list of columns.
        self.text=text
        self.StyleRow=None
        self.adjectives = ['JJ','JJR','JJS']
        self.nouns = ['NN','NNS','NNP','NNPS','POS','PRP','PRP$']
        self.nouns_dt = ['NN','NNS','NNP','NNPS','POS','PRP','PRP$','DT']
        self.verbs = ['VB','VBD','VBP','VBZ']
        self.full_verbs = ['VB','VBD','VBP','VBZ','VBG','VBN']
        self.adj_dt = ['JJ','JJR','JJS','DT']
        self.columns_list = ["sent_length_mean","sent_length_std",'word_length_mean',"word_length_std",
                            "lexical_diversity","comma_freq","colon_freq","semicolon_freq","quote_freq",
                            "ellipses_freq","exclamation_freq","endash_freq","emdash_freq","paren_freq",
                            "with_freq_1","with_freq_2","with_freq_3","adj_and_freq","come_and_freq","but_not_freq",
                            "but_for_freq","all_but_freq_1","all_but_freq_2","EX_freq","cause_freq","ever_freq",
                            "said_freq","while_freq","as_noun_freq","as_conjunc_freq","as_though_freq","as_good_freq",
                            "not_as_freq","gerund_freq_1","gerund_freq_2","gerund_freq_3","gerund_freq_4",
                            "though_freq_1","though_freq_2","though_freq_3","though_freq_4","cause_nv_freq",
                            "that_freq","noun_to_freq","verb_to_freq","adj_to_freq","to_verb_freq","why_freq",
                            "how_freq","even_if_freq","deven_if_freq","if_verb_freq","would_could_freq",
                            "just_freq","then_stop_freq","then_freq","there_verb_freq","there_noun_freq",
                            "there_conj_freq","first_person_freq","second_person_freq","might_freq","maybe_freq",
                            "its_freq"]
        
    def make_array(self):
        #Change columns_list if you change the number of rows appended!
        arrayrow = []
        SF = StyleFinder(self.text) #-
        arrayrow.append(SF.sentencel_mean()) #1
        arrayrow.append(SF.sentencel_std()) #2
        arrayrow.append(SF.wordl_mean()) #3
        arrayrow.append(SF.wordl_std()) #4
        arrayrow.append(SF.lex_diversity(1000)) #5
        #Punctuation frequency
        arrayrow.append(SF.super_frequency(",")) #6
        arrayrow.append(SF.super_frequency(":")) #7
        arrayrow.append(SF.super_frequency(";")) #8
        arrayrow.append(SF.super_frequency(["\"",'\''])) #9
        arrayrow.append(SF.super_frequency("...")) #10
        arrayrow.append(SF.super_frequency("!")) #11
        arrayrow.append(SF.super_frequency("-")) #12
        arrayrow.append(SF.super_frequency("--")) #13
        arrayrow.append(SF.super_frequency(")")) #14
        #Stop word grammar frequency
        arrayrow.append(SF.super_frequency("with",self.adjectives,self.adjectives,cancelvar='negk'))#1
        arrayrow.append(SF.super_frequency("with",self.adjectives,self.adjectives,cancelvar='nega'))#2
        arrayrow.append(SF.super_frequency("with",'_',self.nouns_dt))#3
        arrayrow.append(SF.super_frequency("and",self.adjectives,self.adjectives))#4
        arrayrow.append(SF.super_frequency("and",["come","go"]))#5
        arrayrow.append(SF.super_frequency("but",'_',"not"))#6
        arrayrow.append(SF.super_frequency("but",'_',"for"))#7
        arrayrow.append(SF.super_frequency("but",'all',self.verbs))#8
        arrayrow.append(SF.super_frequency("but",'all',self.nouns_dt))#9
        arrayrow.append(SF.super_frequency("EX"))#10
        arrayrow.append(SF.super_frequency(["cause","causes","caused","causing"],"DT",cancelvar='nega'))#11
        arrayrow.append(SF.super_frequency(["however","whyever","whoever","whatever","whenever","wherever"]))#12
        arrayrow.append(SF.super_frequency("said"))#13
        arrayrow.append(SF.super_frequency("while","DT",cancelvar='nega'))#14
        arrayrow.append(SF.super_frequency("as",['.',';','!','?'],self.nouns_dt))#15
        arrayrow.append(SF.super_frequency("as",['.',';','!','?'],self.nouns_dt,cancelvar='nega'))#16
        arrayrow.append(SF.super_frequency("as",'_',"though"))#17
        arrayrow.append(SF.super_frequency("as",'_',"JJ"))#18
        arrayrow.append(SF.super_frequency("as",["not","isn't","wasn't","weren't","ain't"]))#19
        arrayrow.append(SF.super_frequency("VBG",['.',',']))#20
        arrayrow.append(SF.super_frequency("VBG",self.verbs))#21
        arrayrow.append(SF.super_frequency("VBG",self.adj_dt))#22
        arrayrow.append(SF.super_frequency("VBG",["IN","RB"]))#23
        arrayrow.append(SF.super_frequency(["although","though"],['-',',']))#24
        arrayrow.append(SF.super_frequency(["although","though"],'_',self.adjectives))#25
        arrayrow.append(SF.super_frequency(["although","though"],'_',self.nouns))#26
        arrayrow.append(SF.super_frequency(["although","though"],'_',['VBG']))#27
        arrayrow.append(SF.super_frequency("cause",'DT'))#28
        arrayrow.append(SF.super_frequency("that",'IN'))#29
        arrayrow.append(SF.super_frequency("to",self.nouns_dt))#30
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
        arrayrow.append(SF.super_frequency("then",["and",".","?","!"]))#41
        arrayrow.append(SF.super_frequency("then",self.nouns,'.'))#42
        arrayrow.append(SF.super_frequency(["there","here"],self.verbs))#43
        arrayrow.append(SF.super_frequency(["there","here"],self.nouns))#44
        arrayrow.append(SF.super_frequency(["there","here"],"IN"))#45
        arrayrow.append(SF.super_frequency(["i","me","we","us","my","mine","our","ours"]))#46
        arrayrow.append(SF.super_frequency(["you","your","yours"]))#47
        arrayrow.append(SF.super_frequency("might"))#48
        arrayrow.append(SF.super_frequency("maybe"))#49
        arrayrow.append(SF.super_frequency('its')+SF.super_frequency('it','_','\'s'))#50


        self.StyleRow = arrayrow
        return None
    
    