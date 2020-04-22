import glob
import pandas as pd
import reddit_utils
import pushshift
import numpy as np

import matplotlib.pyplot as plt
from matplotlib import rc
import matplotlib.dates as mdates
import datetime
from datetime import timedelta

def get_relative_freq(word, subreddit, rolling=False):

    word_df = reddit_utils.utc_to_datetime(pd.DataFrame(pushshift.daycounts(word=word, subreddit=subreddit)), 'key')
    total_df = reddit_utils.utc_to_datetime(pd.DataFrame(pushshift.daycounts(subreddit=subreddit)), 'key')
    word_df = word_df.merge(total_df, on='day', how='outer')
    word_df['freq'] = word_df['doc_count_x'] / word_df['doc_count_y']

    if rolling:
        word_df['rolling_freq'] = word_df['freq'].rolling(window=7).mean()

    return word_df

def get_comment_timeseries(subreddit, rolling=False):

    total_df = reddit_utils.utc_to_datetime(pd.DataFrame(pushshift.daycounts(subreddit=subreddit)), 'key')

    if rolling:
        total_df['rolling_freq'] = total_df['doc_count'].rolling(window=7).mean()

    return total_df

def states_word_freq_tiled(states, counter, word):
    rc('font', **{'family': 'serif', 'serif': ['Computer Modern'], 'size': 14})
    rc('text', usetex=True)
    years_fmt = mdates.DateFormatter('%b\n%Y')
    i = 0
    NUM_ROWS = 6
    if len(states)%3 != 0:
        NUM_ROWS = 5
    NUM_COLS = 3

    fig, axs = plt.subplots(NUM_ROWS, NUM_COLS, sharex='col', sharey='row', figsize=(16,11))
    fig.subplots_adjust(hspace=0.2,wspace=0.15)
    c = -1
    r = 0

    d0 = '2019-12-31'
    d1 = '2020-04-19'
    d1 = datetime.date(int(d1.split('-')[0]), int(d1.split('-')[1]), int(d1.split('-')[2]))
    d0 = datetime.date(int(d0.split('-')[0]), int(d0.split('-')[1]), int(d0.split('-')[2]))
    delta = d1 - d0
    date_list = [d0 + timedelta(days=x) for x in range(0, delta.days, delta.days // 4)]
    for date in date_list[1:]:
        newdate = date.replace(day=1)
        date_list[date_list.index(date)] = newdate

    for state in states:
        print(state)
        c += 1
        if c == NUM_COLS:
            c = 0
            r += 1

        print(str(r)+', '+str(c))
        word_df = get_relative_freq('coronavirus', state, rolling=True)
        print(min(word_df['day']))
        print(max(word_df['day']))
        axs[r, c].plot(word_df.day, word_df.freq, lw=0.6, c = 'deepskyblue', alpha=0.8)
        axs[r, c].plot(word_df.day, word_df.rolling_freq, lw=1.5, c = 'deepskyblue', alpha=1)

        axs[r, c].set_title(state)
        # axs[r, c].set_yscale('log')

        axs[r, c].set_xlim([min(date_list),max(date_list)])
        axs[r, c].set_xticks(date_list)
        axs[r, c].set_ylim([0,0.4])
        axs[r, c].set_yticks([0, 0.1, 0.2, 0.3, 0.4])
        # axs[r, c].set_yticklabels(['-4','-3','-2','-1','0'])
        axs[r, c].tick_params(axis='both', which='major', labelsize=14)
        axs[r, c].grid()

    if len(states)%3 != 0:
        axs[-1, -1].axis('off')

    for ax in axs.flat:
        ax.xaxis.set_major_formatter(years_fmt)

    fig.suptitle('Rel. Frequency of \"'+word+'\" on State Subreddits')

    plt.savefig('../figures/'+word+'_states'+counter+'_tiled.png')
    # plt.show()
    plt.close()

def cities_word_freq_tiled(cities, word, tag):

    rc('font', **{'family': 'serif', 'serif': ['Computer Modern'], 'size': 14})
    rc('text', usetex=True)
    years_fmt = mdates.DateFormatter('%b\n%Y')
    i = 0
    NUM_ROWS = 6
    NUM_COLS = 3

    fig, axs = plt.subplots(NUM_ROWS, NUM_COLS, sharex='col', sharey='row', figsize=(16,11))
    fig.subplots_adjust(hspace=0.2,wspace=0.15)
    c = -1
    r = 0

    d0 = '2019-12-31'
    d1 = '2020-04-19'
    d1 = datetime.date(int(d1.split('-')[0]), int(d1.split('-')[1]), int(d1.split('-')[2]))
    d0 = datetime.date(int(d0.split('-')[0]), int(d0.split('-')[1]), int(d0.split('-')[2]))
    delta = d1 - d0
    date_list = [d0 + timedelta(days=x) for x in range(0, delta.days, delta.days // 4)]
    for date in date_list[1:]:
        newdate = date.replace(day=1)
        date_list[date_list.index(date)] = newdate

    for city in cities:
        print(city)
        c += 1
        if c == NUM_COLS:
            c = 0
            r += 1

        print(str(r)+', '+str(c))
        word_df = get_relative_freq('coronavirus', city, rolling=True)
        print(min(word_df['day']))
        print(max(word_df['day']))
        axs[r, c].plot(word_df.day, word_df.freq, lw=0.6, c = 'deepskyblue', alpha=0.8)
        axs[r, c].plot(word_df.day, word_df.rolling_freq, lw=1.5, c = 'deepskyblue', alpha=1)

        axs[r, c].set_title(city)
        # axs[r, c].set_yscale('log')

        axs[r, c].set_xlim([min(date_list),max(date_list)])
        axs[r, c].set_xticks(date_list)
        axs[r, c].set_ylim([0,0.4])
        axs[r, c].set_yticks([0, 0.1, 0.2, 0.3, 0.4])
        # axs[r, c].set_yticklabels(['-4','-3','-2','-1','0'])
        axs[r, c].tick_params(axis='both', which='major', labelsize=14)
        axs[r, c].grid()

    for ax in axs.flat:
        ax.xaxis.set_major_formatter(years_fmt)

    fig.suptitle('Rel. Frequency of \"'+word+'\" on City Subreddits')

    if tag:
        plt.savefig('../figures/'+tag+'_'+word+'_cities_tiled.png')
    else:
        plt.savefig('../figures/'+word+'_cities_tiled.png')
    # plt.show()
    plt.close()

def states_word_freq(states, word):

    rc('font', **{'family': 'serif', 'serif': ['Computer Modern'], 'size': 18})
    rc('text', usetex=True)
    years_fmt = mdates.DateFormatter('%b\n%Y')
    # colors = plt.cm.tab20(np.linspace(0,1,len(states)))
    # i = 0

    d0 = '2019-12-30'
    d1 = '2020-04-19'
    d1 = datetime.date(int(d1.split('-')[0]), int(d1.split('-')[1]), int(d1.split('-')[2]))
    d0 = datetime.date(int(d0.split('-')[0]), int(d0.split('-')[1]), int(d0.split('-')[2]))

    delta = d1 - d0
    date_list = [d0 + timedelta(days=x) for x in range(0, delta.days, delta.days // 6)]
    for date in date_list[1:]:
        newdate = date.replace(day=1)
        date_list[date_list.index(date)] = newdate

    fig = plt.figure(figsize=(8, 6))
    fig.subplots_adjust(bottom=0.2)
    ax = fig.add_subplot(111)
    for state in states:
        word_df = get_relative_freq('coronavirus',state, rolling=True)
        ax.plot(word_df['day'], word_df['rolling_freq'], c = 'blue', alpha = 0.4, lw=1.2, label=state)
        # i += 1

    ax.xaxis.set_major_formatter(years_fmt)
    # ax.legend(loc='upper left', ncol=3, fontsize=10, frameon=False)
    ax.set_xticks(date_list)
    plt.grid()
    plt.title('Rel. Frequency of \"'+word+'\" on State Subreddits')
    plt.savefig('../figures/'+word+'_states_rolling.png')
    # plt.show()
    plt.close()

def cities_word_freq(cities, word, tag=None):

    rc('font', **{'family': 'serif', 'serif': ['Computer Modern'], 'size': 18})
    rc('text', usetex=True)
    years_fmt = mdates.DateFormatter('%b\n%Y')
    colors = plt.cm.tab20(np.linspace(0,1,len(cities)))
    i = 0

    d0 = '2019-12-30'
    d1 = '2020-04-19'
    d1 = datetime.date(int(d1.split('-')[0]), int(d1.split('-')[1]), int(d1.split('-')[2]))
    d0 = datetime.date(int(d0.split('-')[0]), int(d0.split('-')[1]), int(d0.split('-')[2]))

    delta = d1 - d0
    date_list = [d0 + timedelta(days=x) for x in range(0, delta.days, delta.days // 6)]
    for date in date_list[1:]:
        newdate = date.replace(day=1)
        date_list[date_list.index(date)] = newdate

    fig = plt.figure(figsize=(8, 6))
    fig.subplots_adjust(bottom=0.2)
    ax = fig.add_subplot(111)
    for city in cities:
        word_df = get_relative_freq('coronavirus',city, rolling=True)
        ax.plot(word_df['day'], word_df['rolling_freq'], c = colors[i], alpha = 0.7, lw=1.2, label=city)
        i += 1

    ax.xaxis.set_major_formatter(years_fmt)
    ax.set_xticks(date_list)
    ax.legend(loc='upper left', ncol=2, fontsize=14, frameon=False)
    plt.grid()
    plt.title('Rel. Frequency of \"'+word+'\" on City Subreddits')
    if tag:
        plt.savefig('../figures/'+tag+'_'+word+'_cities_rolling.png')
    else:
        plt.savefig('../figures/'+word+'_cities_rolling.png')
    # plt.show()
    plt.close()

def states_timeseries(states):

    rc('font', **{'family': 'serif', 'serif': ['Computer Modern'], 'size': 18})
    rc('text', usetex=True)
    years_fmt = mdates.DateFormatter('%b\n%Y')
    # colors = plt.cm.tab20(np.linspace(0,1,len(states)))
    # i = 0

    d0 = '2019-12-30'
    d1 = '2020-04-19'
    d1 = datetime.date(int(d1.split('-')[0]), int(d1.split('-')[1]), int(d1.split('-')[2]))
    d0 = datetime.date(int(d0.split('-')[0]), int(d0.split('-')[1]), int(d0.split('-')[2]))

    delta = d1 - d0
    date_list = [d0 + timedelta(days=x) for x in range(0, delta.days, delta.days // 6)]
    for date in date_list[1:]:
        newdate = date.replace(day=1)
        date_list[date_list.index(date)] = newdate

    fig = plt.figure(figsize=(8, 6))
    fig.subplots_adjust(bottom=0.2)
    ax = fig.add_subplot(111)
    for state in states:
        df = get_comment_timeseries(state, rolling=True)
        df = df[df['day'] >= d0]
        ax.plot(df['day'], df['rolling_freq'], c = 'blue', alpha = 0.4, lw=1.2, label=state)
        # i += 1

    ax.xaxis.set_major_formatter(years_fmt)
    # ax.legend(loc='upper left', ncol=3, fontsize=10, frameon=False)
    ax.set_xticks(date_list)
    plt.grid()
    plt.title('Comment Frequency on State Subreddits')
    plt.savefig('../figures/states_rolling.png')
    # plt.show()
    plt.close()

def cities_timeseries(cities):

    rc('font', **{'family': 'serif', 'serif': ['Computer Modern'], 'size': 18})
    rc('text', usetex=True)
    years_fmt = mdates.DateFormatter('%b\n%Y')
    colors = plt.cm.tab20(np.linspace(0,1,len(cities)))
    i = 0

    d0 = '2019-12-30'
    d1 = '2020-04-19'
    d1 = datetime.date(int(d1.split('-')[0]), int(d1.split('-')[1]), int(d1.split('-')[2]))
    d0 = datetime.date(int(d0.split('-')[0]), int(d0.split('-')[1]), int(d0.split('-')[2]))

    delta = d1 - d0
    date_list = [d0 + timedelta(days=x) for x in range(0, delta.days, delta.days // 6)]
    for date in date_list[1:]:
        newdate = date.replace(day=1)
        date_list[date_list.index(date)] = newdate

    fig = plt.figure(figsize=(8, 6))
    fig.subplots_adjust(bottom=0.2)
    ax = fig.add_subplot(111)
    for city in cities:
        df = get_comment_timeseries(city, rolling=True)
        df = df[df['day'] >= d0]
        ax.plot(df['day'], df['rolling_freq'], c = colors[i], alpha = 0.7, lw=1.2, label=city)
        i += 1

    ax.xaxis.set_major_formatter(years_fmt)
    ax.set_xticks(date_list)
    ax.legend(loc='upper left', ncol=2, fontsize=14, frameon=False)
    plt.grid()
    plt.title('Comment Frequency on City Subreddits')
    plt.savefig('../figures/cities_rolling.png')
    # plt.show()
    plt.close()

def main():
    cities = reddit_utils.get_list_of_cities()
    states = reddit_utils.get_list_of_states()
    top5 = reddit_utils.get_top5_cities()
    states1 = states[:18]
    states2 = states[18:36]
    states3 = states[36:]

    word = "coronavirus"

    # States
    # states_word_freq(states, word)
    # states_word_freq_tiled(states1, '1', word)
    # states_word_freq_tiled(states2, '2', word)
    # states_word_freq_tiled(states3, '3', word)
    # states_timeseries(states)

    # Cities
    # cities_word_freq(cities, word)
    # cities_word_freq_tiled(cities, word)
    # cities_timeseries(cities)

    # Top 5 Cities
    cities_word_freq(top5, word, 'top5')
    cities_word_freq_tiled(top5, word, 'top5')


if __name__ == "__main__":
    main()