
################################# Description ##################################

# reddit_utils contains functions to
# easily turn csv's of reddit comments or posts to a bag of words,
# to count and rank those words,
# to quickly create datetime columns,
# to store the dictionary of cities to states

################################### Imports ####################################

import string
from collections import Counter
import pandas as pd
import re
import datetime

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

def remove_nan(posts):
    '''
    Removes NaN items from a list.
    '''
    return [x for x in posts if type(x) != float]

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
    posts = remove_nan(posts)
    s = ' '.join(posts)
    s = remove_links(s)
    s = remove_non_ascii(s)
    s = remove_punct(s)
    document = s.lower()
    document = document.split()
    if stemmer:
        document = [stemmer.lemmatize(word) for word in document]

    return document

#################### Functions for Counting/Ranking Words ####################

def create_count_col(counts):
    '''
    Helper function
    Takes in Counter object and makes it a dataframe.
    Returns said dataframe
    '''
    df = pd.DataFrame.from_dict(counts, orient='index').reset_index()
    df = df.rename(columns={'index': 'type', 0: 'count'})

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
    and spits out a dataframe of words and their counts
    '''
    corpus = df_to_bow(df, stemmer)
    corpus_counts = Counter(corpus)
    df_count = create_count_col(corpus_counts)

    return df_count


def rank(df, count_col, stemmer=None):
    '''
    Takes in a dataframe, makes a bag of words, counts each bag,
    and spits out a dataframe of words, counts, and ranks
    '''
    corpus = df_to_bow(df, count_col, stemmer)
    corpus_counts = Counter(corpus)
    df_count = create_count_col(corpus_counts)
    df_rank = create_rank_col(df_count)

    return df_rank


#################### Functions for UTC to Datetime ####################

def utc_to_datetime(df,utc_colname):
    '''
    Function that takes in a dataframe, the column name for UTC timestamps,
    and returns the same dataframe with additional columns of Python
    datetime objects.  The full datetime, datetime to the hour, to the
    day, and to the month are added.
    '''
    dt = []
    dm = []
    dd = []
    dh = []
    for index,row in df.iterrows():
        date = datetime.datetime.fromtimestamp(row[utc_colname])
        dt.append(date)
        dm.append(date.replace(day = 1, hour=0, minute=0,
                               second=0, microsecond=0))
        dd.append(date.replace(hour=0, minute=0, second=0,
                               microsecond=0))
        dh.append(date.replace(minute=0, second=0, microsecond=0))
    df['datetime'] = dt
    df['month'] = dm
    df['day'] = dd
    df['hour'] = dh
    return df


############################# Miscellaneous #############################


def get_states_for_cities():
    '''
    City to state dictionary, sseful for placing cities "inside of" states
    (for maps, combining datasets, etc)
    '''

    city_to_state = {'StLouis':'missouri', 'Austin':'texas',
                     'Atlanta':'georgia', 'WashingtonDC':'washingtondc',
                     'SanDiego':'california', 'Seattle':'washington',
                     'Chicago':'illinois', 'Portland':'oregon',
                     'Houston':'texas', 'Boston':'massachusetts',
                     'Dallas':'texas', 'LosAngeles':'california',
                     'Baltimore':'maryland', 'Denver':'colorado',
                     'Philadelphia':'pennsylvania', 'SanFrancisco':'california',
                     'Pittsburgh':'pennsylvania', 'NYC':'newyork'}

    return city_to_state


########################################################################


# Example usages (Uncomment and run to test them, don't forget to recomment):

# # Read in data
# stlouis_comments = pd.read_csv('reddit_data/cities/StLouis/StLouis.csv', nrows = 1000)
# # Get count and rank of all words in df
# stlouis_comments_ranked = rank(stlouis_comments, count_col = 'body')
# print(stlouis_comments_ranked.head())
#
# # Read in data
# stlouis_posts = pd.read_csv('reddit_data/cities/StLouis/StLouis_posts.csv', na_values = 'Nan', nrows = 1000)
# # Get count and rank of all words in df
# stlouis_posts_ranked = rank(stlouis_posts, count_col = 'selftext')
# print(stlouis_posts_ranked.head())

# # Read in data
# stlouis_comments = pd.read_csv('reddit_data/cities/StLouis/StLouis.csv', nrows = 1000)
# # Get datetimes for month, day, hour
# stlouis_comments_with_dates = utc_to_datetime(stlouis_comments, 'created_utc')
# print(stlouis_comments_with_dates[['datetime','month','day','author']].head())