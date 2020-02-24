from epub_conversion.utils import convert_epub_to_lines as CETL
from epub_conversion.utils import open_book
import pandas as pd
from bs4 import BeautifulSoup
import pickle
import numpy as np
import nltk
from nltk.tokenize import word_tokenize,sent_tokenize
from nltk import Text
from nltk.probability import FreqDist
from StyleFinder import StyleFinder as SF
from MassStyles import MassStyles as MSty

'''
infile = open('descfimDF','rb')
fimdescDF = pickle.load(infile)
infile.close()

FimTextDF = fic_col_full(fimdescDF,'archive','story_text')

filename = 'fimtextDF'
outfile= open(filename,'wb')
pickle.dump(FimTextDF,outfile)
outfile.close()
'''

infile = open('FicText10000DF','rb')
fimtextDF = pickle.load(infile)
infile.close()

msty = MSty(fimtextDF,10000,1000)
msty.make_array()
msty.pickle_it()



