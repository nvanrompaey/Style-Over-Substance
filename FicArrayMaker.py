from epub_conversion.utils import convert_epub_to_lines as CETL
from epub_conversion.utils import open_book
from sklearn.feature_extraction.text import TfidfTransformer
import numpy as np
import pandas as pd
import pickle
from bs4 import BeautifulSoup
import boto3
from io import BytesIO
from MassStylesMini import MassStylesMini
from nltk.tokenize import word_tokenize
import os



# testyy.iloc(axis=1)[2:].iloc(axis=0)[0] = np.array([1,2])
s3 = boto3.resource('s3')

columns_list = ["sent_length_mean","sent_length_std",'word_length_mean',"word_length_std",
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

def unpickle(filename='MiniFicDF',colly=columns_list):
    infile = open(filename,'rb')
    df = pickle.load(infile)
    infile.close()
    #Load the file, and then add on a bunch of empty rows with the given column names.
    #When MassStylesMini is called, it'll paste onto each empty column of a given row.
    for col in colly:
        df[col] = np.nan
    return df


def textfinder(name):
    # 'name' is the name of the file in question being converted
    # Spits out a text file without html markings
    #This requires boto in order to get the appropriate S3 file
    #Then requires BytesIO in order to convert the bytes into epub format
    #Then epub_conversion converts it into HTML style text
    obj = s3.Object("ficsuggest", name)
    sobj = obj.get()['Body'].read()
    stream = BytesIO(sobj)
    book = open_book(stream)
    text = CETL(book)
    soup = BeautifulSoup(" ".join(text))
    return soup.get_text()

def style_it(text):
    MSty = MassStylesMini(text)
    MSty.make_array()
    return MSty.StyleRow

def normalize_array(arr):
    TFT = TfidfTransformer()
    array = TFT.fit_transform(arr).toarray()
    return array

def pickle_it_again(df,filename):
    outfile= open(filename,'wb')
    pickle.dump(df,outfile)
    outfile.close()
    

def main():
    SecondFile = "FicStyleFeatures.pickle"
    #df = unpickle("DFTestMini")
    df = unpickle()
    style_array = []
    #Unpickle the file, then for each row, if there's 1000+ words, perform a Style Analysis and return the row in question.
    # If not, drop the row.
    for i in df.index.values:
        filename = df.loc(axis=1)['archive'][i]
        text = textfinder(filename)
        if len(word_tokenize(text))>=1000:
            style_row = style_it(text)
            style_array.append(style_row)
        else:
            df.drop(i,axis=0,inplace=True)
            
    #Then Normalize the whole array
    style_array = normalize_array(style_array)
    
    #Then slap on the entire array.
    df.iloc(axis=1)[2:] = style_array
    
    #And pickle the result
    pickle_it_again(df,SecondFile)
        


if __name__ == "__main__":
    main()
