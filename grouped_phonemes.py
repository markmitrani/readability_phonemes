import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
from collections import Counter

import seaborn as sns
from pandas import read_csv

import phonemes_IPA
from phonemes_IPA import text_to_phonemes, visualize_counter, visualize_counter_fancy

def merge_columns(df, column_list, result_column):
    # Display the first row before the operation
    print("Before operation:")
    print(df.loc[0])

    # Create a new column that is the sum of the columns in column_list
    df[result_column] = df[column_list].apply(lambda row: row.sum(), axis=1)

    # Drop the original columns
    df.drop(columns=column_list, inplace=True)

    # Display the first row after the operation
    print("\nAfter operation:")
    print(df.loc[0])

    return df

year_grouping = ['year_2', 'year_3', 'year_4', 'year_5', 'year_6']
year_2 = ['B', 'D', 'HH', 'M', 'N', 'P', 'W']
year_3 = ['F', 'G', 'K', 'NG', 'T', 'Y']
year_4 = ['CH', 'JH', 'L', 'S', 'SH', 'V', 'Z']
year_5 = ['DH', 'R', 'ZH']
year_6 = ['TH']

def group_by_age(df):
    merge_columns(df, year_2, 'year_2')
    merge_columns(df, year_3, 'year_3')
    merge_columns(df, year_4, 'year_4')
    merge_columns(df, year_5, 'year_5')
    merge_columns(df, year_6, 'year_6')
    df.to_csv('all_levels_grouped_by_age.csv')

class_grouping = ['plosives', 'nasals', 'fricatives', 'glides', 'liquids', 'affricates', 'back', 'mid', 'front']
plosives = ['B', 'P', 'T', 'D', 'K', 'G']
nasals = ['M', 'N', 'NG']
fricatives = ['DH', 'F', 'S', 'SH', 'ZH', 'V', 'Z', 'TH']
glides = ['W', 'Y']
liquids = ['L', 'R']
affricates = ['CH', 'JH']
back = ['AA','AO','OW','UH','UW']
mid = ['AH', 'ER']
front = ['AE', 'EH', 'EY', 'IH', 'IY']

def group_by_class(df):
    merge_columns(df, plosives, 'plosives')
    merge_columns(df, nasals, 'nasals')
    merge_columns(df, fricatives, 'fricatives')
    merge_columns(df, glides, 'glides')
    merge_columns(df, liquids, 'liquids')
    merge_columns(df, affricates, 'affricates')
    merge_columns(df, back, 'back')
    merge_columns(df, mid, 'mid')
    merge_columns(df, front, 'front')
    df.to_csv('all_levels_grouped_by_class.csv')

def main():
    df = read_csv('all_levels_full_one_hot.csv')
    group_by_age(df)

if __name__ == '__main__':
    main()