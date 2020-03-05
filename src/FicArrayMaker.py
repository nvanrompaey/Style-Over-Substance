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
from concurrent.futures import ProcessPoolExecutor
import os
from multiprocessing import cpu_count




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

columns_len = len(columns_list)

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
    soup = BeautifulSoup(" ".join(text),features="lxml")
    return soup.get_text()

def style_it(text):
    #Performs a mass styles on the fiction in question
    MSty = MassStylesMini(text)
    MSty.make_array()
    return MSty.StyleRow

def normalize_array(arr):
    #Normalizes to make better cosine similarity predictions
    TFT = TfidfTransformer()
    array = TFT.fit_transform(arr).toarray()
    return array

def pickle_it_again(df,filename):
    outfile= open(filename,'wb')
    pickle.dump(df,outfile)
    outfile.close()
    
def style_featurize(series,lent = columns_len):
    #
    filename = series
    text = textfinder(filename)
    if len(word_tokenize(text))>=1000:
        style_row = style_it(text)
    else:
        style_row = np.empty(lent)
    
    return style_row

def main():
    SecondFile = "FicStyleFeatures.pickle"
    #df = unpickle("DFTestMini")
    df = unpickle()
    style_array = []
    #Unpickle the file, then for each row, perform a Style Analysis and return the row in question.
    print("Array Found... Applying Style Featurization")
    num = 1
    max_num = df.index.values.size
    
    #Add full parallelization!
    cpus = cpu_count()-1
    with ProcessPoolExecutor(max_workers=cpus) as executor:
        for i in executor.map(style_featurize,df['archive']):
            num+=1
            style_array.append(i)
            if num%1000==0:
                print(f"{num} of {max_num} stories style-featurized.")


    print("Normalizing Style Array...")       
    #Then Normalize the whole array
    style_array = normalize_array(style_array)
    
    print("Adding to dataframe...")
    #Then slap on the entire array.
    df.iloc(axis=1)[2:] = style_array
    
    print("Pickling Dataframe...")
    #And pickle the result
    pickle_it_again(df,SecondFile)
    print("Done.")
        


if __name__ == "__main__":
    main()
