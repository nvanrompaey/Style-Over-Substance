import numpy as np
import nltk
from nltk import pos_tag
from nltk.tokenize import word_tokenize,sent_tokenize
from nltk.probability import FreqDist


class StyleFinder():
    
    
    def __init__(self,fic):
        
        self.fic = fic
        self.words = word_tokenize(self.fic) #Tokenize up the words
        self.sentences = sent_tokenize(self.fic) #Tokenize up with sentences
        self.sent_len = [len(sentence.split()) for sentence in self.sentences] # Get the length of each sentence
        self.word_len = [len(word) for word in set(self.words)]
        self.poslist = ['CC','CD','DT','EX','FW','IN','JJ',
                        'JJR','JJS','LS','MD','NN','NNS','NNPS',
                        'PDT','POS','PRP','PRP$','RB','RBR',
                        'RBS','RP','TO','UH','VB','VBD','VBG',
                        'VBN','VBP','VBZ','WDT','WP','WP$','WRB']
        self.postagged = nltk.pos_tag(self.words)

        
    def sentencel_mean(self):
        #Mean sentence length
        return np.mean(self.sent_len)
    
    def sentencel_std(self):
        #Standard Deviation sentence length
        return np.std(self.sent_len)
    
    def lex_diversity(self,size):
        #Take the number of unique tokens per 'size' number of words and divide it by the number of words total.
        return (len(set(self.words))*size)/len(self.words)
 
    def wordl_mean(self):
        #Mean word length
        return np.mean(self.word_len)
    
    def wordl_std(self):
        # Standard Deviation word length
        return np.std(self.word_len)
    
    
    '''
        The following are all frequency-related functions, starting with a full function.
        The components of this greater function are:
            - negate_ana      (>find all [NOT word 1, word Central,     word 3])
            - negate_ana_no_k (>find all [NOT word 1, word Central,           ])
            - negate_kata     (>find all [    word 1, word Central, NOT word 3])
            - negate_kata_no_a(>find all [            word Central, NOT word 3])
            - negate_both     (>find all [NOT word 1, word Central, NOT word 3])
            - negate_none     (>find all [    word 1, word Central,     word 3])
            - no_ana          (>find all [            word Central,     word 3])
            - no_kata         (>find all [    word 1, word Central,           ])
            - center_only     (>find all [            word Central            ])
            - center_pos      (>find all [           (word Central,POS)       ])
            
        Each component will be able to see whether the word1/word Central/word 3 is a POS, (except for Center + POS)
        and will return appropriate sums based on counts.
            
    '''
    
    def super_frequency(self,wordy, ana='_',kata='_',size,cancelvar='gobbledygook'):
        #Takes an 'ana', which is the word before the chosen word, 'wordy', which is the chosen stop word/gerund,
        # and 'kata', which is the word after the chosen word. 'size' follows into the frequency per 'size' number of words.
        # 'cancelvar' is a variable that determines whether ana or kata need canceling, that is...
        #
        # cancelvar 'nega' => negate_ana
        #           'negk' => negate_kata
        #           'negb' => negate_ana_kata
        #           'cpos' => center_pos
        # using '_' indicates blank entry. Wordy shouldn't be '_' but can be.
        #Please keep your ana and kata LOWERCASE for regular words, and UPPERCASE for POS tags.
        
        if type(ana) == str:
            ana = [ana]
        if type(kata) == str:
            kata = [kata]
        if type(wordy) == str:
            wordy = [wordy]
        # Make sure they're all in list format first to make the functions go smoothly. 3 lists of 1 element so negligible    
        # storage.
        
        if type(ana) != list:
            return "Please insert a string or list for 'ana'"
        if type(kata) != list:
            return "Please insert a string or list for 'kata'"
        if type(wordy) != list:
            return "Please insert a string or list for 'wordy'"
        #And make sure that it was a string or list inserted, not an array or int or something weird.
        
        if all(x in self.poslist for x in wordy):
            w_n = 1
        else:
            w_n = 0
            
        if all(x in self.postlist for x in ana):
            a_n = 1
        else:
            a_n = 0
        
        if all(x in self.postlist for x in kata):
            k_n = 1
        else:
            k_n = 0
        #This makes it easy to determine which side of each function part is being used: The POS part or the regular part.
        
        #Below chooses the function based on the logic seen above.
        if cancelvar == 'nega':
            if kata = '_':
                counter = negate_ana_no_k(ana,wordy,[a_n,w_n,k_n])
            else:
                counter = negate_ana(ana,wordy,kata,[a_n,w_n,k_n])
                
        elif cancelvar== 'negk':
            if ana = '_':
                counter = negate_kata_no_a(wordy,kata,[a_n,w_n,k_n])
            else:
                counter = negate_kata(ana,wordy,kata,[a_n,w_n,k_n])
                
        elif cancelvar == 'negb':
            counter = negate_ana_kata(ana,wordy,kata,[a_n,w_n,k_n])
        elif cancelvar == 'cpos':
            counter = center_pos(wordy,kata)

        else:
            if ana = '_' and kata = '_':
                counter = center_only(wordy)
            elif ana = '_':
                counter = no_ana(wordy,kata,[a_n,w_n,k_n])
            elif kata = '_':
                counter = no_kata(wordy,kata,[a_n,w_n,k_n])
            else:
                counter = negate_none(ana,wordy,kata,[a_n,w_n,k_n])
                
        return counter*size/len(self.words)
        
        
    def negate_ana(self,ana,wordy,kata,wak):
        #Takes ana, wordy, and kata, and returns a count of NOT ana, wordy, kata, given the lists.
        '''FINISH'''
        return None

    def negate_ana_no_k(self,ana,wordy,wak):
        #Takes ana, wordy, and kata, and returns a count of NOT ana, wordy, given the lists.
        '''FINISH'''
        return None
        
    def negate_kata(self,ana,wordy,kata,wak):
        #Takes ana, wordy, and kata, and returns a count of ana, wordy, NOT kata, given the lists.
        '''FINISH'''
        return None

    def negate_kata_no_a(self,wordy,kata,wak):
        #Takes ana, wordy, and kata, and returns a count of wordy, NOT kata, given the lists.
        '''FINISH'''
        return None
    
    def negate_ana_kata(self,ana,wordy,kata,wak):
        #Takes ana, wordy, and kata, and returns a count of NOT ana, wordy, NOT kata, given the lists.
        '''FINISH'''
        return None
    
    def negate_none(self,ana,wordy,kata,wak):
        #Takes ana, wordy, and kata, and returns a count of ana, wordy, kata, given the lists.
        '''FINISH'''
        return None
    
    def no_ana(self,wordy,kata,wak):
        #Takes wordy, and kata, and returns a count of wordy, kata, given the lists.
        
        
        
        return None    

    def no_kata(self,ana,wordy,wak):
        #Takes wordy, and kata, and returns a count of wordy, kata, given the lists.
        counter = []
    
        for i in self.words:
            try:
                if uplow_switch(i[wak[0]],wak[0]) in ana and uplow_switch(i[wak[1],wak[1]]) in wordy:
                    counter.append(1)
                else:
                    counter.append(0)
            except IndexError:
                counter.append(0)
                
        return np.sum(counter)
    
    def center_only(self,wordy,wak):
        #Takes wordy and returns a count of wordy, given the lists.
        return np.sum([1 if uplow_switch(i[wak],wak) in wordy else 0 for i in self.postagged])


    def center_pos(self,wordy,postag):
        #Takes wordy, and a POS tag and returns a count of wordy, kata, given the lists.

        return np.sum([1 if i[0].lower() in wordy and i[1] in postag else 0 for i in self.postagged])
    
    def uplow_switch(word,wakval):
        if wakval == 0:
            return word.lower()
        else:
            return word.upper()