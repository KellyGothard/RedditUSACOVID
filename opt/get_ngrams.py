import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
import sys
from datetime import datetime
from collections import Counter

import argparse

import tweet_utils.src.regex as regex


def make_args(raw_args=None):
    description = "Extract labmt vectors from txt zipf files."
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('-i',
                        '--inputdir',
                        help='path to input directory of pydicts',
                        required=True,
                        type=Path)
    parser.add_argument('-o',
                        '--outdir',
                        help='path to output directory (where .txts are saved)',
                        required=True,
                        type=Path)
    parser.add_argument('-t',
                        '--type',
                        help='text type (comments or posts)',
                        required=True,
                        type=str)
    parser.add_argument('-n',
                        '--ngram',
                        help='ngram order',
                        required=False,
                        type=int)

    return parser.parse_args(raw_args)


def parse_ngrams(inputdir: Path, outdir: Path, ngram_order=1):
    """

    :param inputdir:
    :param outdir: save location
    :param ngram_order:
    :return: dataframe with count, rank, freq of ngrams
    """
    save_loc = outdir / f'{inputdir.stem}'
    save_loc.mkdir(exist_ok=True, parents=True)

    regex_loc = '/home/hereford/Projects/tweet_utils/resources/ngrams.bin'  # terrible, I know

    reddit_data = pd.read_csv(inputdir)

    reddit_data.created_utc = pd.to_datetime(reddit_data.created_utc, unit='s').dt.date

    for date in reddit_data.created_utc.unique():
        if (save_loc / f'{str(date)}.tsv').exists(): continue
        print(date, end='\r')
        temp_df = reddit_data[reddit_data.created_utc == date]
        days_counts = Counter()
        for text in temp_df.body.astype(str).values:
            days_counts += regex.get_ngrams(text, regex_loc, ngram_order)
        temp_df = pd.DataFrame([days_counts]).T
        temp_df['freq'] = (temp_df[0] / temp_df[0].sum()).round(decimals=4)
        temp_df['rank'] = temp_df[0].rank(ascending=False)
        temp_df.columns = ['count', 'freq', 'rank']
        temp_df.index.name = 'Ngram'
        temp_df.sort_values(by='rank', inplace=True)
        temp_df.to_csv(save_loc / f'{str(date)}.tsv', sep='\t')


def main(raw_args=None):
    args = make_args(raw_args)

    targets = args.inputdir.glob(f'*/*{args.type}*')

    args.outdir = args.outdir / f'{args.ngram}grams'
    args.outdir.mkdir(parents=True, exist_ok=True)

    for target in targets:
        print(target.stem)
        parse_ngrams(target, args.outdir, args.ngram)


if __name__ == "__main__":
    main()
