import glob
import pandas as pd
import reddit_utils


def get_relative_freq():

    bcel_df = reddit_utils.utc_to_datetime(pd.DataFrame(pushshift.daycounts(word=w, subreddit='Braincels')), 'key')
    bcel_total_df = reddit_utils.utc_to_datetime(pd.DataFrame(pushshift.daycounts(subreddit='Braincels')), 'key')
    bcel_df = bcel_df.merge(bcel_total_df, on='day', how='outer')
    bcel_df['doc_count'] = bcel_df['doc_count_x'] / bcel_df['doc_count_y']


def main():
    STATES_PATH = '../data/reddit_data/states/'
    CITIES_PATH = '../data/reddit_data/cities/'
    SUMMARY_DATA_PATH = '../data/reddit_data/reddit_data_summaries.csv'
    cities = reddit_utils.get_list_of_cities()
    states = reddit_utils.get_list_of_states()

    for city in cities:
        print(city)

        comments_path = CITIES_PATH+'/'+city+'/'+city+'_comments.csv'
        comments_df = pd.read_csv(comments_path)

        posts_path = CITIES_PATH+'/'+city+'/'+city+'_posts.csv'
        posts_df = pd.read_csv(posts_path)


    for state in states:
        print(state)

        comments_path = STATES_PATH+'/'+state+'/'+state+'_comments.csv'
        comments_df = pd.read_csv(comments_path)

        posts_path = STATES_PATH+'/'+state+'/'+state+'_posts.csv'
        posts_df = pd.read_csv(posts_path)


    fig = plt.figure(figsize=(6, 8))
    fig.subplots_adjust(left=0.3)
    ax = fig.add_subplot(111)
    ax.plot(x = comments_df['day'], y = comments_df['freq'])
    ax.grid()
    plt.title(title)
    plt.savefig(out)
    plt.show()
    plt.close()

if __name__ == "__main__":
    main()