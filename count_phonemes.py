import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
from collections import Counter

import seaborn as sns
from pandas import read_csv

import phonemes_IPA
from phonemes_IPA import text_to_phonemes, visualize_counter, visualize_counter_fancy


def phoneme_count_dataframe():
    index = phonemes_IPA.ARPAbet_to_IPA.keys()
    df = pd.DataFrame(columns=index)
    return df

def add_counter_to_dataframe(df, filename, phoneme_ctr):
    total_count = sum(phoneme_ctr.values())
    normalized_counts = {k: v/total_count for k, v in phoneme_ctr.items()}
    df.loc[filename] = normalized_counts
    df.loc[filename] = df.loc[filename].fillna(0)

#
# Method to take all .txt files in a directory and the phonemes of each as entries in a dataframe
# Returns a dataframe object
#
def process_text_files(directory_path):
    phonemes_df = phoneme_count_dataframe()
    for filename in os.listdir(directory_path):
        if filename.endswith(".txt"):
            file_path = os.path.join(directory_path, filename)
            with open(file_path, "r", encoding="latin-1") as file:
                print("Processing file " + filename + " in " + directory_path + "...")
                text = file.read()
                add_counter_to_dataframe(phonemes_df, filename, Counter(text_to_phonemes(text)))

    return phonemes_df

def compute_frequencies():
    # func: specifying directories and processing them in a loop
    directories = [ #'7-8_processed', '8-9_processed', '9-10_processed',
                   # '11-14_processed', '14-16_processed']
                   '14-16_processed']
    for directory in directories:
        if '7-8' in directory:
            level = 1
            print(level," is the level")
        elif '8-9' in directory:
            level = 2
        elif '9-10' in directory:
            level = 3
        elif '11-14' in directory:
            level = 4
        elif '14-16' in directory:
            level = 5
        directory_path = os.path.join('data', directory)
        result_df = process_text_files(directory_path)
        result_df['level'] = level

        # Normalize the dataframe
        #normalized_df = result_df.iloc[:, 1:].div(result_df.iloc[:, 1:].sum(axis=1), axis=0)

        # Print the normalized dataframe
        print(result_df)
        result_df.to_csv(directory + '_per_entry.csv')

#
# gets a list of filenames for csv's as an input, and reads them as dataframes.
# assuming they all have the same columns, it joins the rows of all dataframes.
#
def join_dataframe_rows(files, output_file):
    dataframes = []
    for file in files:
        dataframes.append(pd.read_csv(file))

    joined_df = pd.concat(dataframes, ignore_index=True)

    joined_df.to_csv(output_file, index=False)  # Save joined DataFrame to a CSV file without index

    print("Joined DataFrame saved to", output_file)

#
# accepts a .csv as input, and runs pairwise correlation analysis between the column 'level' and every other column that has a name.
# saves the correlation matrix as the name of the file + _corr
#
def run_correlation_analysis(file):
    df = pd.read_csv(file)
    columns_for_corr = df.columns[1:-1]
    correlation_matrix = df[columns_for_corr].corrwith(df['level']).to_frame().T

    # Set up the figure and axis with a wider width
    fig, ax = plt.subplots(figsize=(16, 6))

    # Create the heatmap
    heatmap = sns.heatmap(correlation_matrix, cmap='coolwarm', annot=True, fmt='.2f', linewidths=.5, ax=ax)

    # Rotate the x-axis labels vertically
    plt.xticks(rotation='vertical')

    # Update the x-axis labels with their values from the dictionary
    heatmap.set_xticklabels([phonemes_IPA.ARPAbet_to_IPA.get(label, label) for label in columns_for_corr])

    # Adjust the vertical alignment of the correlation values
    for text in heatmap.texts:
        text.set_rotation(90)
        text.set_verticalalignment('center')

    # Add a title to the plot
    plt.title('Correlation Matrix')
    # Display the plot
    plt.show()
    plt.savefig(file[:-4] + '_corr.png')
    print("Correlation analysis saved as", file[:-4] + '_corr.png')


def main():
    compute_frequencies()
    join_dataframe_rows(['7-8_processed_per_entry.csv'   , '8-9_processed_per_entry.csv', '9-10_processed_per_entry.csv',
                   '11-14_processed_per_entry.csv', '14-16_processed_per_entry.csv'], 'all_levels_full.csv')
    run_correlation_analysis('all_levels_full.csv')

if __name__ == '__main__':
    main()