from datetime import timedelta
import ujson
import pandas as pd
from datetime import datetime
import re
import requests
import time
import math
import pprint

def process(df,vectorizer,stemmer):
    punctuations = '''!()\-[]{};:'"\,<>./?@#$%^&*_~|''';
    documents = []
    posts = list(df['body'])
    s = ''
    for post in posts:
        for char in punctuations:
            post = post.replace(char, '')
        posttext = post.replace('\n','') + ' '
        s += posttext
        document = re.sub(r'^https?:\/\/.*[\r\n]*', '', s, flags=re.MULTILINE)
        document = document.lower()
        document = document.split()
        document = [stemmer.lemmatize(word) for word in document]
        document = ' '.join(document)
        documents.append(document)
    v = vectorizer.fit_transform(documents).toarray()
    return v

def make_request(uri, max_retries = 5):
    def fire_away(uri):
        response = requests.get(uri)
        assert response.status_code == 200
        return ujson.loads(response.content)
    current_tries = 1
    while current_tries < max_retries:
        try:
            time.sleep(0.2)
            response = fire_away(uri)
            return response
        except:
            time.sleep(0.2)
            current_tries += 1
    return fire_away(uri)

def pull_comments_for_subreddit(subreddit, start_at, end_at):
    def map_posts(posts):
        return list(map(lambda post: {
            'id': post['id'],
            'created_utc': post['created_utc'],
            'body': post['body'],
            'author':post['author']
        }, posts))
    
    SIZE = 500
    URI_TEMPLATE = r'https://api.pushshift.io/reddit/search/comment?subreddit={}&after={}&before={}&size={}'
    
    post_collections = map_posts( \
        make_request( \
            URI_TEMPLATE.format( \
                subreddit, start_at, end_at, SIZE))['data'])
    n = len(post_collections)
    while n == SIZE:
        last = post_collections[-1]
        new_start_at = last['created_utc'] - (10)
        
        more_posts = map_posts( \
            make_request( \
                URI_TEMPLATE.format( \
                    subreddit, new_start_at, end_at, SIZE))['data'])
        
        n = len(more_posts)
        post_collections.extend(more_posts)
    return post_collections


def pull_comments_for_author(author, start_at, end_at):
    def map_posts(posts):
        return list(map(lambda post: {
            'id': post['id'],
            'created_utc': post['created_utc'],
            'body': post['body'],
            'author':post['author'],
            'subreddit':post['subreddit']
        }, posts))
    
    SIZE = 500
    URI_TEMPLATE = r'https://api.pushshift.io/reddit/search/comment?author={}&after={}&before={}&size={}'
    
    post_collections = map_posts( \
        make_request( \
            URI_TEMPLATE.format( \
                author, start_at, end_at, SIZE))['data'])
    n = len(post_collections)
    
    while n == SIZE:
        last = post_collections[-1]
        new_start_at = last['created_utc'] - (10)
        
        more_posts = map_posts( \
            make_request( \
                URI_TEMPLATE.format( \
                    author, new_start_at, end_at, SIZE))['data'])
        
        n = len(more_posts)
        post_collections.extend(more_posts)
        
    return post_collections


def pull_posts_for_subreddit(subreddit, start_at, end_at):
    def map_posts(posts):
        return list(map(lambda post: {
            'id': post['id'],
            'author': post['author'],
            'subreddit': post['subreddit'],
            'title': post['title'],
            'selftext': post['selftext'],
            "link_flair_text": post["link_flair_text"],
            'created_utc': post['created_utc']
        }, posts))

    SIZE = 500
    URI_TEMPLATE = r'https://api.pushshift.io/reddit/search/submission?subreddit={}&after={}&before={}&size={}'

    data = make_request(URI_TEMPLATE.format(subreddit, start_at, end_at, SIZE))['data']
    try:
        post_collections = map_posts(data)
    except:
        for row in data:
            if 'selftext' not in row.keys():
                row['selftext'] = 'Nan'
            if 'link_flair_text' not in row.keys():
                row['link_flair_text'] = 'Nan'
        print('N rows after editing: ' + str(len(data)))
        post_collections = map_posts(data)

    n = len(post_collections)
    while n == SIZE:
        last = post_collections[-1]
        new_start_at = last['created_utc'] - (10)

        data = make_request(URI_TEMPLATE.format(subreddit, new_start_at, end_at, SIZE))['data']
        try:
            more_posts = map_posts(data)
        except:
            for row in data:
                if 'selftext' not in row.keys():
                    row['selftext'] = 'Nan'
                if 'link_flair_text' not in row.keys():
                    row['link_flair_text'] = 'Nan'
            print('N rows after editing: ' + str(len(data)))
            more_posts = map_posts(data)

        n = len(more_posts)
        post_collections.extend(more_posts)
    return post_collections

def pull_posts_for_author(author, start_at, end_at):
    def map_posts(posts):
        return list(map(lambda post: {
            'id': post['id'],
            'created_utc': post['created_utc'],
            'title': post['title'],
            # 'selftext': post['selftext'],
            "link_flair_text" : post["link_flair_text"],
            'author': post['author'],
            'subreddit': post['subreddit']
        }, posts))

    SIZE = 500
    URI_TEMPLATE = r'https://api.pushshift.io/reddit/search/submission?author={}&after={}&before={}&size={}'

    post_collections = map_posts( \
        make_request( \
            URI_TEMPLATE.format( \
                author, start_at, end_at, SIZE))['data'])
    n = len(post_collections)

    while n == SIZE:
        last = post_collections[-1]
        new_start_at = last['created_utc'] - (10)

        more_posts = map_posts( \
            make_request( \
                URI_TEMPLATE.format( \
                    author, new_start_at, end_at, SIZE))['data'])

        n = len(more_posts)
        post_collections.extend(more_posts)

    return post_collections

def give_me_intervals(start_at, end_at, number_of_days_per_interval = 3):
    period = (86400 * number_of_days_per_interval)
    end = start_at + period
    yield (int(start_at), int(end))
    padding = 1
    while end <= end_at:
        start_at = end + padding
        end = (start_at - padding) + period
        yield int(start_at), int(end)
        
def daycounts(subreddit = None, author = None, word = None):
    time.sleep(0.3)
    if subreddit and not word and not author:
        r = requests.get('https://api.pushshift.io/reddit/search/submission/?subreddit='+subreddit+'&aggs=created_utc&frequency=day&size=0')
        try:
            day_counts = ujson.loads(r.content)
        except:
            print(r.text)
        else:
            return day_counts['aggs']['created_utc']
    if author and not word and not subreddit:
        r = requests.get('https://api.pushshift.io/reddit/search/submission/?author='+author+'&aggs=created_utc&frequency=day&size=0')
        try:
            day_counts = ujson.loads(r.content)
        except:
            print(r.text)
        else:
            return day_counts['aggs']['created_utc']
    if word and not author and not subreddit:
        r = requests.get('https://api.pushshift.io/reddit/search/submission/?q='+word+'&aggs=created_utc&frequency=day&size=0')
        day_counts = ujson.loads(r.content)
        return day_counts['aggs']['created_utc']
    if word and subreddit:
        try:
            r = requests.get('https://api.pushshift.io/reddit/search/submission/?q='+word+'&subreddit='+subreddit+'&aggs=created_utc&frequency=day&size=0')
        except:
            print(r.text)
        day_counts = ujson.loads(r.content)
        return day_counts['aggs']['created_utc']

def startdate(subreddit = None, author = None):
    if subreddit:
        t = daycounts(subreddit = subreddit)[0]
    if author:
        t = daycounts(author = author)[0]
    return (datetime.fromtimestamp(t['key']) - timedelta(days=1)).timestamp()

def subreddit_comments(subreddit, n = 1000000000, START = None, END = None, save_csv = False, name = None, *args, **kwargs):
    if not START:
        START = startdate(subreddit=subreddit)
    if not END:
        END = math.ceil(datetime.utcnow().timestamp())
    posts = []
    for interval in give_me_intervals(START, END, 7):
        if len(posts)<n:
            pulled_posts = pull_comments_for_subreddit(
                subreddit, interval[0], interval[1])
            posts.extend(pulled_posts)
            time.sleep(.3)

    df = pd.DataFrame(posts)
    dt = datetime.fromtimestamp(START)
    
    if save_csv:
        if name:
            df.to_csv(name+'.csv')
        else:
            df.to_csv(subreddit+'_'+str(dt)+'_posts.csv')
    return df

def author_comments(AUTHOR, n = 1000000000, START = None, END = None, save_csv = False, *args, **kwargs):
    if not START:
        START = startdate(author=AUTHOR)
    if not END:
        END = math.ceil(datetime.utcnow().timestamp())
    posts = []
    for interval in give_me_intervals(START, END, 28):
        if len(posts)<n:
            pulled_posts = pull_comments_for_author(
                AUTHOR, interval[0], interval[1])
            posts.extend(pulled_posts)
            time.sleep(.1)

    df = pd.DataFrame(posts)
    dt = datetime.fromtimestamp(START)

    if save_csv:
        df.to_csv(AUTHOR+'_'+str(dt)+'_posts.csv')
        
    return df


def subreddit_posts(subreddit, n=1000000000, START=None, END=None, save_csv=False, name=None, *args, **kwargs):
    if not START:
        START = startdate(subreddit=subreddit)
    if not END:
        END = math.ceil(datetime.utcnow().timestamp())
    posts = []
    for interval in give_me_intervals(START, END, 7):
        if len(posts) < n:
            pulled_posts = pull_posts_for_subreddit(
                subreddit, interval[0], interval[1])
            posts.extend(pulled_posts)
            time.sleep(.3)

    df = pd.DataFrame(posts)
    dt = datetime.fromtimestamp(START)

    if save_csv:
        if name:
            df.to_csv(name + '.csv')
        else:
            df.to_csv(subreddit + '_' + str(dt) + '_posts.csv')
    return df


def author_posts(AUTHOR, n=1000000000, START=None, END=None, save_csv=False, *args, **kwargs):
    if not START:
        START = startdate(author=AUTHOR)
    if not END:
        END = math.ceil(datetime.utcnow().timestamp())
    posts = []
    for interval in give_me_intervals(START, END, 28):
        if len(posts) < n:
            pulled_posts = pull_posts_for_author(
                AUTHOR, interval[0], interval[1])
            posts.extend(pulled_posts)
            time.sleep(.1)

    df = pd.DataFrame(posts)
    dt = datetime.fromtimestamp(START)

    if save_csv:
        df.to_csv(AUTHOR + '_' + str(dt) + '_posts.csv')

    return df

def most_recent_posts_subreddit(subreddit, n=500):
    path = 'https://api.pushshift.io/reddit/search/comment/?subreddit='+subreddit+'&size='+str(n)
    response = requests.get(path)
    posts = ujson.loads(response.content)['data']
    df = pd.DataFrame(posts)
    time.sleep(0.5)
    
    return df

def get_author_subreddits(author):
    path = 'https://api.pushshift.io/reddit/search/comment/?author='+author+'&aggs=subreddit&frequency=day&size=0'
    try:
        r = requests.get(path)
        posts = ujson.loads(r.content)
    except:
        print(author)
    else:
        df = pd.DataFrame(posts['aggs']['subreddit'])
        time.sleep(0.2)
    
        return df

def author_counts(author):
    time.sleep(0.07)
    try:
        r = requests.get(
            'https://api.pushshift.io/reddit/search/comment/?author=' + author + '&aggs=author&size=0')
        day_counts = ujson.loads(r.content)
        total_count = day_counts['aggs']['author'][0]['doc_count']
    except:
        print('ERROR: '+author)
    else:
        return total_count

def get_top_subs_for_word(word, topn = 10):
    r = requests.get('https://api.pushshift.io/reddit/search/comment/?q='+word+'&aggs=subreddit')
    subs = ujson.loads(r.content)
    topn_subs = subs['aggs']['subreddit'][:topn]

    return topn_subs

    
    
def main():
    pass
if __name__=="__main__":
    main()
