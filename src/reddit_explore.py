import pandas as pd
import reddit_utils
import glob

import matplotlib.pyplot as plt
from matplotlib import rc
import matplotlib.dates as mdates
from datetime import timedelta


def summary_barh(df, iscity, col, title, out):
    '''
    Function to take in a dataframe, a column, title, and out directory
    to plot a horizontal bar chart by 'location'.  Meant to be used with
    summary file ('../data/reddit_data/reddit_data_summaries.csv').
    '''
    # Is it a city or a state?
    if iscity == True:
        data = df[df['city?'] == 1]
        rc('font', **{'family': 'serif', 'serif': ['Computer Modern'], 'size': 18})
    else:
        data = df[df['city?'] == 0]
        rc('font', **{'family': 'serif', 'serif': ['Computer Modern'], 'size': 12})
    rc('text', usetex=True)

    data = data.sort_values(col,ascending=True)
    fig = plt.figure(figsize=(6, 8))
    fig.subplots_adjust(left=0.3)
    ax = fig.add_subplot(111)
    ax.barh(y = data['location'], width = data[col])
    ax.grid()
    plt.title(title)
    plt.savefig(out)
    plt.show()
    plt.close()


def main():

    STATES_PATH = '../data/reddit_data_0418/states/'
    CITIES_PATH = '../data/reddit_data_0418/cities/'
    SUMMARY_DATA_PATH = '../data/reddit_data_0418/reddit_data_summaries.csv'
    cities = reddit_utils.get_list_of_cities()
    states = reddit_utils.get_list_of_states()

    data = []

    for city in cities:
        print(city)
        comments_path = CITIES_PATH+'/'+city+'/'+city+'_comments.csv'
        comments_df = pd.read_csv(comments_path)
        n_comments = len(comments_df)
        n_comment_authors = len(comments_df.author.unique())

        posts_path = CITIES_PATH+'/'+city+'/'+city+'_posts.csv'
        posts_df = pd.read_csv(posts_path)
        n_posts = len(posts_df)
        n_post_authors = len(posts_df.author.unique())
        ifcity = 1

        city_data = [city, ifcity, n_comments, n_comment_authors, n_posts, n_post_authors]
        data.append(city_data)


    for state in states:
        print(state)
        comments_path = STATES_PATH+'/'+state+'/'+state+'_comments.csv'
        comments_df = pd.read_csv(comments_path)
        n_comments = len(comments_df)
        n_comment_authors = len(comments_df.author.unique())

        posts_path = STATES_PATH+'/'+state+'/'+state+'_posts.csv'
        posts_df = pd.read_csv(posts_path)
        n_posts = len(posts_df)
        n_post_authors = len(posts_df.author.unique())
        ifcity = 0

        state_data = [state, ifcity, n_comments, n_comment_authors, n_posts, n_post_authors]
        data.append(state_data)

    summary_data = pd.DataFrame(data, columns = ['location', 'city?', 'n_comments', 'n_comment_authors', 'n_posts', 'n_post_authors'])
    print(summary_data.head())
    summary_data.to_csv(SUMMARY_DATA_PATH)

    # summary_data = pd.read_csv(SUMMARY_DATA_PATH)

    summary_barh(df=summary_data,
                 iscity=True,
                 col='n_comments',
                 title='Comments per City',
                 out='../figures/cities_ncomments.png')
    summary_barh(df=summary_data,
                 iscity=True,
                 col='n_posts',
                 title='Posts per City',
                 out='../figures/cities_nposts.png')
    summary_barh(df=summary_data,
                 iscity=False,
                 col='n_comments',
                 title='Comments per State',
                 out='../figures/states_ncomments.png')
    summary_barh(df=summary_data,
                 iscity=False,
                 col='n_posts',
                 title='Posts per State',
                 out='../figures/states_nposts.png')


if __name__ == "__main__":
    main()