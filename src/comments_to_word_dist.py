import reddit_utils
import pandas as pd
from nltk.stem import PorterStemmer


def main():

    CITIES_PATH = '../data/reddit_data_0418/cities/'
    top5 = reddit_utils.get_top5_cities()

    for city in top5:

        COMMENTS_PATH = CITIES_PATH+city+'/'+city+'_comments.csv'
        df = pd.read_csv(COMMENTS_PATH)

        ps = PorterStemmer()
        df_rank = reddit_utils.rank(df,'body',ps)
        print(df_rank.head())

if __name__ == "__main__":
    main()