#Imports
import string
from collections import Counter
import pandas as pd
import re
import datetime

##### City to state dictionary
# Useful for placing cities "inside of" states (for maps, combining datasets, etc)
city_to_state = {'StLouis':'missouri', 'Austin':'texas',
                 'Atlanta':'georgia', 'WashingtonDC':'washingtondc',
                 'SanDiego':'california', 'Seattle':'washington',
                 'Chicago':'illinois', 'Portland':'oregon',
                 'Houston':'texas', 'Boston':'massachusetts',
                 'Dallas':'texas', 'LosAngeles':'california',
                 'Baltimore':'maryland', 'Denver':'colorado',
                 'Philadelphia':'pennsylvania', 'SanFrancisco':'california',
                 'Pittsburgh':'pennsylvania', 'NYC':'newyork'}


#################### Functions for DataFrame to Bag of Words ####################

def remove_punct(s):
    '''
     Remove punctuation from a string and return modified string
    '''
    return s.translate(str.maketrans('', '', string.punctuation))

def remove_links(s):
    '''
    An attempt at removing links. Commented out lines are
    previous/alternate attempts at removing links.
    '''
    return re.sub(r'^https?:\/\/.*[\r\n]*', '', s, flags=re.MULTILINE)
    # s = re.sub(r'\b\w*https\w*\b', '', s, flags=re.MULTILINE)
    # s = re.sub(r'\b\w*www\w*\b', '', s, flags=re.MULTILINE)
    # return s

def remove_nonstr(posts):
    '''
    Removes non string items in a list.  Takes care of Nan.
    '''
    for p in posts:
        if type(p) != str:
            posts.remove(posts[posts.index(p)])
    return posts

def remove_non_ascii(s):
    '''
    Get rid of non-ascii characters.  This takes out characters from
    some languages, emojis, etc
    '''
    return s.encode('ascii', errors='ignore').strip().decode('ascii')

def remove_linebreaks(s):
    '''
    Removes pesky unwanted line breaks
    '''
    return s.translate(str.maketrans("\n\t\r", "   "))


def df_to_bow(df, textcol, stemmer=None):
    '''
    Function takes in a dataframe and specified column with desired text.
    For example, if each row in a dataframe was a comment and the column for
    the text was body, you would pass 'body' for textcol.
    Option is there for a stemmer from sklearn, but not required.
    Returns a list of all one-grams from the specified column
    '''
    posts = list(df[textcol])
    posts = remove_nonstr(posts)
    s = ' '.join(posts)
    s = remove_links(s)
    s = remove_non_ascii(s)
    s = remove_punct(s)
    document = s.lower()
    document = document.split()
    if stemmer:
        document = [stemmer.lemmatize(word) for word in document]

    return document


def create_count_col(counts):
    '''
    Helper function
    Takes in Counter object and makes it a dataframe.
    Returns said dataframe
    '''
    df = pd.DataFrame.from_dict(counts, orient='index').reset_index()
    df = df.rename(columns={'index': 'word', 0: 'count'})

    return df


def create_rank_col(df, col='count'):
    '''
    Helper function
    Takes in a dataframe and a specified column.  Creates rank column
    based on values in specified count column.
    Returns updated dataframe
    '''
    df["rank"] = df[col].rank(method='average', ascending=False)
    df = df.sort_values(by=[col], ascending=False)

    return df


def count(df, stemmer=None):
    '''
    Takes in a dataframe, makes a bag of words, counts each bag,
    and spits out a dataframe fo words and their counts
    '''
    corpus = df_to_bow(df, stemmer)
    corpus_counts = Counter(corpus)
    df_count = create_count_col(corpus_counts)

    return df_count


def rank(df, by='words', stemmer=None):
    if by == 'words':
        corpus = df_to_bow(df, stemmer)
        corpus_counts = Counter(corpus)
        df_count = create_count_col(corpus_counts)
        print(df_count.head())
        df_rank = create_rank_col(df_count)
    else:
        df_rank = create_rank_col(df)

    return df_rank