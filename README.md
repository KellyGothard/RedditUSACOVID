# RedditUSACOVID
By analyzing comments from each US state’s associated subreddit, andsubreddits from major US cities such as New York City, we can pair online conversationtopics in each state with cell-phone-tracked movements, case counts, death counts, andto other significant events such as the date of stay-at-home enactment.

# Reddit Data Description
1. Collected from pushshift.io
2. 50 states and 18 cities chosen from these links:
  https://www.reddit.com/r/redditlists/comments/1meeed/us_state_subreddits_ranked_by_the_number_of/
  https://www.reddit.com/r/redditlists/comments/3yusqs/an_updated_list_of_the_most_popular_city/
3. Comments and posts from December 31st 2019 to April 6th for states, and to April 7th for cities.  Will get latest comments/posts at some point.
4. Our Reddit data are currently in reddit_data/.  The states are in reddit_data/states/ and the cities are in reddit_data/cities/.  Each city and state has its own directory.  Example: reddit_data/states/newjersey/ and reddit_data/cities/Atlanta/.  Inside each city/state directory, there are two csvs: locationname.csv and locationname_posts.csv.  The first one contains the comments from the location's respective subreddit (the name of the location directory) and the second one contains the posts.
5. The files that contain comments have the following comment attributes: the author, the subreddit it was published on, the text body, UTC timestamp, and the unique comment id.  The files for posts have these attributes: author, subreddit, post title, post text, post flair (sort of like a tag for topics), UTC timestamp, and post id.


# Mobility Data Description 

*see `/opt` for collection scripts*

### Google COVID-19 Mobility Reports

Scraped from PDFs and in CSV format, sourced from [this project.](https://github.com/vitorbaptista/google-covid19-mobility-reports)