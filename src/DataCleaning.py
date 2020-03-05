import numpy as np
import pandas as pd
import pickle
from bs4 import BeautifulSoup
import json

def safeget(x,s,a,b): 
    #If a dictionary exists within dictionary X, 
    # then try to find the value of key 'b' within the secondary
    if x[s].get(a) is not None:
        return x[s].get(a).get(b)
    else:
        return None

def emptynans(df,columns):
    #Takes Nan values for a column and fills with empty strings.
    for i in columns:
        df[i].fillna("",inplace=True)
    return None

def dummynans(df,columns):
    #Takes columns where nans are important and creates a 'has' where Nan is 0 and anything else is 1.
    for i in columns:
        df[f"has_{i}"] = df[i].apply(lambda x: x is not None).astype(int)
    df = df.drop(columns,axis=1,inplace=True)
    return None

def dummy_gen(df,column):
    # Create dummy variables for all the columns in question
    tempdf = pd.get_dummies(df, columns = column, drop_first=True, dummy_na=False)
    return tempdf
    
def quicktype(df,columns):
    #Change the type of a lot of columns at once
    for i in columns:
        df[i] = df[i].astype(int)
    return None

# AND HERE'S THE BIG ONE
#
#
#
    
def FicData(link):
    #link is 'FData/index.json'
    testdf = pd.read_json(link)
    testdf = testdf.transpose()
    # Resetting index to story id, which is a number, as opposed to a string that the json calls.
    testdf.set_index('id',inplace=True)
    
    #Dropping unneeded and redundant or single-value Columns
    # color is unneeded. Status, Published, and Submitted are all True for all values
    # Date modified is only present in a fraction of fics. URL contains redundant information. Chapters is too indepth.
    ficdf = testdf.drop(['color','status','published','submitted','date_modified','url','chapters'],axis=1)
    #Dropping rows where the story has 0 words.
    ficdf = ficdf.drop(ficdf.index[ficdf['num_words'] == 0],axis=0)
    
    #datetime to datetime
    ficdf["date_published"] = pd.to_datetime(ficdf["date_published"]).dt.date
    ficdf["date_updated"] = pd.to_datetime(ficdf["date_updated"]).dt.date
    
    #Fixing Nans
    # In this case, published dates
    ficdf['date_published'].fillna(ficdf['date_updated'],inplace=True)
    # Instead of dropping rows or keeping nans, empty strings will flow well with grammar-tracking
    emptynans(ficdf,['description_html','short_description','title'])
    
    #Creating dummy columns based on Nans
    dummynans(ficdf,['prequel','cover_image'])
    #And the rest of the dummies
    ficdf = dummy_gen(ficdf,['completion_status','content_rating'])
    
    #Pulling out author details
    ficdf['author_name'] = ficdf['author'].apply(lambda x: x.get('name'))
    ficdf['author_num_followers'] = ficdf['author'].apply(lambda x: x.get('num_followers'))
    ficdf['author_num_followers'].fillna(0,inplace=True)
    ficdf = ficdf.drop('author',axis=1)
    
    #And archive details
    ficdf['archive'] = ficdf['archive'].apply(lambda x: x.get('path'))
    
    #Change all appropriate types to integer, no floats
    quicktype(ficdf,['num_chapters','num_comments','num_dislikes',
                     'num_likes','num_words','num_views',
                     'total_num_views','rating'])
    #Extract all tags
    ficdf['tag_names'] = ficdf['tags'].apply(lambda x: [a.get('name') for a in x if a.get('type')!='series' ])
    ficdf = ficdf.drop('tags',axis=1)
    # and dummy them
    dummytag = pd.get_dummies(ficdf['tag_names'].apply(pd.Series).stack()).sum(level=0)
    ficdf = ficdf.join(dummytag,on='id')
    
    
    return testdf,ficdf


def FicMerge(df,link2):
    members = pd.read_csv(link2)
    members['Date'] = pd.to_datetime(members['Date']).dt.date
    members = members[['Date','Total']]
    members.columns = ["date_updated","total_users"]
    fullficdf = df.merge(members, left_on='date_updated',right_on='date_updated',how='left').set_index(df.index)
    fullficdf['view_ratio'] = fullficdf['num_views']/fullficdf['total_users']
    fullficdf['likes_ratio'] = fullficdf['num_likes']/fullficdf['total_users']
    
    return fullficdf
    
def FicCorr(df):
    corrcolumns = ['num_comments','num_dislikes','num_likes',
               'num_views','num_words','rating','total_num_views',
               'Twilight Sparkle','has_cover_image','completion_status_complete',
              'content_rating_mature','Rainbow Dash','Adventure','Romance',
               'Sex','Violence','Slice of Life','Sad','Tragedy','view_ratio','likes_ratio']
    return df[corrcolumns].corr()
    
    
    
def DescFic(df):
    fimdescDF = df.loc(axis=1)[['title','archive','description_html']]
    fimdescDF['description_long'] = fimdescDF['description_html'].apply(lambda x: 
                                                                    BeautifulSoup(x).get_text('/n'
                                                                                    ).replace('/n',' '
                                                                                    ).replace('  ',' '))
    return fimdescDF
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    