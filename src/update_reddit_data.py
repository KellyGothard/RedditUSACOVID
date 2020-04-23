import pandas as pd
import os

import reddit_utils


def main():

    STATES_PATH = '../data/reddit_data/states/'
    CITIES_PATH = '../data/reddit_data/cities/'
    TOADD_STATES_PATH = '../data/data_update/states/'
    TOADD_CITIES_PATH = '../data/data_update/cities/'
    cities = reddit_utils.get_list_of_cities()
    states = reddit_utils.get_list_of_states()

    data = []

    for city in cities:
        print(city)
        comments_path = CITIES_PATH+'/'+city+'/'+city+'_comments.csv'
        comments_df = pd.read_csv(comments_path)
        toadd_comments_path = TOADD_CITIES_PATH+'/'+city+'/'+city+'.csv'
        toadd_comments_df = pd.read_csv(toadd_comments_path)

        updated_comments_df = comments_df.append(toadd_comments_df)
        updated_comments_df = updated_comments_df.drop_duplicates(subset='id')

        OUTPATH = '../data/reddit_data_0418/cities/'+city+'/'
        try:
            os.mkdir(OUTPATH)
        except:
            print('dir already exists')
        updated_comments_df.to_csv(OUTPATH+city+'_comments.csv')


        posts_path = CITIES_PATH+'/'+city+'/'+city+'_posts.csv'
        posts_df = pd.read_csv(posts_path)
        toadd_posts_path = TOADD_CITIES_PATH+'/'+city+'/'+city+'_posts.csv'
        toadd_posts_df = pd.read_csv(toadd_posts_path)

        updated_posts_df = posts_df.append(toadd_posts_df)
        updated_posts_df = updated_posts_df.drop_duplicates(subset='id')
        updated_posts_df.to_csv(OUTPATH+city+'_posts.csv')

    for state in states:
        print(state)
        comments_path = STATES_PATH+'/'+state+'/'+state+'_comments.csv'
        comments_df = pd.read_csv(comments_path)
        toadd_comments_path = TOADD_STATES_PATH+'/'+state+'/'+state+'.csv'
        toadd_comments_df = pd.read_csv(toadd_comments_path)

        updated_comments_df = comments_df.append(toadd_comments_df)
        updated_comments_df = updated_comments_df.drop_duplicates(subset='id')

        OUTPATH = '../data/reddit_data_0418/states/'+state+'/'
        try:
            os.mkdir(OUTPATH)
        except:
            print('dir already exists')

        updated_comments_df.to_csv(OUTPATH+state+'_comments.csv')


        posts_path = STATES_PATH+'/'+state+'/'+state+'_posts.csv'
        posts_df = pd.read_csv(posts_path)
        toadd_posts_path = TOADD_STATES_PATH+'/'+state+'/'+state+'_posts.csv'
        toadd_posts_df = pd.read_csv(toadd_posts_path)

        updated_posts_df = posts_df.append(toadd_posts_df)
        updated_posts_df = updated_posts_df.drop_duplicates(subset='id')
        updated_posts_df.to_csv(OUTPATH+state+'_posts.csv')




if __name__ == "__main__":
    main()