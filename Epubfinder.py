from epub_conversion.utils import convert_epub_to_lines as CETL
from epub_conversion.utils import open_book
import pandas as pd
from bs4 import BeautifulSoup

def textfinder(name):
    # 'name' is the name of the file in question being converted
    # Spits out a text file without html markings
    book = open_book(f"FData/{name}")
    text = CETL(book)
    soup = BeautifulSoup(" ".join(text))
    return soup.get_text()

def fic_col_monster(df,col,newcol,n):
    df2 = df.iloc[:n]
    #Takes a dataframe, a column in question, and spits out a 
    # new column with the name newcol that prints super cool stuff
    df2[newcol] = df2[col].apply(lambda x: textfinder(x))
    return df2

def fic_col_full(df,col,newcol):
    df2 = df
    #Takes the whole dataframe and column, then spits out a new colum with the given name
    df2[newcol] = df2[col].apply(lambda x: textfinder(x))
    return df2
    