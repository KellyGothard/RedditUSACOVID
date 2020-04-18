import pandas as pd
import reddit_utils
import glob

import matplotlib.pyplot as plt
from matplotlib import rc
import matplotlib.dates as mdates
from datetime import timedelta

STATES_PATH = '../data/reddit_data/states/'
CITIES_PATH = '../data/reddit_data/cities/'
SUMMARY_DATA_PATH = '../data/reddit_data/reddit_data_summaries.csv'
cities = reddit_utils.get_list_of_cities()
states = reddit_utils.get_list_of_states()

data = []

# for city in cities:
#     print(city)
#
#     comments_path = CITIES_PATH+'/'+city+'/'+city+'_comments.csv'
#     comments_df = pd.read_csv(comments_path)
#     n_comments = len(comments_df)
#     n_comment_authors = len(comments_df.author.unique())
#
#     posts_path = CITIES_PATH+'/'+city+'/'+city+'_posts.csv'
#     posts_df = pd.read_csv(posts_path)
#     n_posts = len(posts_df)
#     n_post_authors = len(posts_df.author.unique())
#
#     ifcity = 1
#
#     city_data = [city, ifcity, n_comments, n_comment_authors, n_posts, n_post_authors]
#     data.append(city_data)
#
# for state in states:
#     print(state)
#
#     comments_path = STATES_PATH+'/'+state+'/'+state+'_comments.csv'
#     comments_df = pd.read_csv(comments_path)
#     n_comments = len(comments_df)
#     n_comment_authors = len(comments_df.author.unique())
#
#     posts_path = STATES_PATH+'/'+state+'/'+state+'_posts.csv'
#     posts_df = pd.read_csv(posts_path)
#     n_posts = len(posts_df)
#     n_post_authors = len(posts_df.author.unique())
#
#     ifcity = 0
#
#     state_data = [state, ifcity, n_comments, n_comment_authors, n_posts, n_post_authors]
#     data.append(state_data)
#
# summary_data = pd.DataFrame(data, columns = ['location', 'city?', 'n_comments', 'n_comment_authors', 'n_posts', 'n_post_authors'])
# print(summary_data.head())
# summary_data.to_csv(SUMMARY_DATA_PATH)


summary_data = pd.read_csv(SUMMARY_DATA_PATH)
cities_data = summary_data[summary_data['city?']==1]
cities_data = cities_data.sort_values('n_comments',ascending=True)
rc('font', **{'family': 'serif', 'serif': ['Computer Modern'], 'size': 18})
rc('text', usetex=True)

fig = plt.figure(figsize=(6, 8))
fig.subplots_adjust(left=0.3)
ax = fig.add_subplot(111)
ax.barh(y = cities_data['location'], width = cities_data['n_comments'])
ax.set_xticks([0,50000,100000,150000,200000,250000])
ax.set_xticklabels(['0','50K','100K','150K','200K','250K'])
ax.grid()
plt.title('Comments per City')
plt.savefig('../figures/cities_ncomments.png')
plt.show()
plt.close()

cities_data = cities_data.sort_values('n_posts',ascending=True)

fig = plt.figure(figsize=(6, 8))
fig.subplots_adjust(left=0.3)
ax = fig.add_subplot(111)
ax.barh(y = cities_data['location'], width = cities_data['n_posts'])
# ax.set_xticks([0,50000,100000,150000,200000,250000])
# ax.set_xticklabels(['0','50K','100K','150K','200K','250K'])
ax.grid()
plt.title('Posts per City')
plt.savefig('../figures/cities_nposts.png')
plt.show()
plt.close()


states_data = summary_data[summary_data['city?']==0]
states_data = states_data.sort_values('n_comments',ascending=True)
rc('font', **{'family': 'serif', 'serif': ['Computer Modern'], 'size': 12})
rc('text', usetex=True)

fig = plt.figure(figsize=(6, 12))
fig.subplots_adjust(left=0.3)
ax = fig.add_subplot(111)
ax.barh(y = states_data['location'], width = states_data['n_comments'])
ax.set_xticks([0,20000,40000,60000,80000])
ax.set_xticklabels(['0','20K','40K','60K','80K'])
plt.title('Comments per State')
ax.grid()
plt.savefig('../figures/states_ncomments.png')
plt.show()
plt.close()

states_data = states_data.sort_values('n_posts',ascending=True)

fig = plt.figure(figsize=(6, 12))
fig.subplots_adjust(left=0.3)
ax = fig.add_subplot(111)
ax.barh(y = states_data['location'], width = states_data['n_posts'])
# ax.set_xticks([0,50000,100000,150000,200000,250000])
# ax.set_xticklabels(['0','50K','100K','150K','200K','250K'])
plt.title('Posts per State')
ax.grid()
plt.savefig('../figures/states_nposts.png')
plt.show()
plt.close()
