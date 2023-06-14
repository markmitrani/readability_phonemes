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
def process_text_files(directory_path, include_stopwords = True):
    phonemes_df = phoneme_count_dataframe()
    for filename in os.listdir(directory_path):
        if filename.endswith(".txt"):
            file_path = os.path.join(directory_path, filename)
            with open(file_path, "r", encoding="latin-1") as file:
                print("Processing file " + filename + " in " + directory_path + "...")
                text = file.read()
                add_counter_to_dataframe(phonemes_df, filename, Counter(text_to_phonemes(text, include_stopwords)))

    return phonemes_df

def compute_frequencies(include_stopwords = True):
    # func: specifying directories and processing them in a loop
    directories = ['7-8_processed', '8-9_processed', '9-10_processed',
                    '11-14_processed', '14-16_processed']

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
        result_df = process_text_files(directory_path, include_stopwords)
        result_df['level'] = level

        # Normalize the dataframe
        #normalized_df = result_df.iloc[:, 1:].div(result_df.iloc[:, 1:].sum(axis=1), axis=0)

        # Print the normalized dataframe
        print(result_df)
        if not include_stopwords:
            result_df.to_csv(directory + '_per_entry_no_stopwords.csv')
        else:
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
    plt.savefig(file[:-4] + '_corr.png', dpi=300)
    print("Correlation analysis saved as", file[:-4] + '_corr.png')
    plt.show()

def visualize_dataframe(filename):
    df = pd.read_csv(filename)
    # Join the rows by summing them per column and calculate the average
    sum_cols = df.columns[1:-1]
    num_rows = len(df[sum_cols])

    #print("final df sums up to: "+df[sum_cols].sum().to_frame().T.divide(num_rows).sum(axis=1))

    final_df = df[sum_cols].sum().to_frame().T.divide(num_rows)
    columns = final_df.columns
    values = final_df.values[0]

    # Create key-value pairs with values as keys and columns as values
    pairs = dict(zip(values, columns))

    # Option: sort the columns in descending order
    sorted_pairs = dict(sorted(pairs.items(), reverse=True))
    columns = sorted_pairs.values()
    values = sorted_pairs.keys()

    # Option: change phonemes to IPA
    columns = [phonemes_IPA.ARPAbet_to_IPA.get(label) for label in columns]

    # Set up the figure and axes
    fig, ax = plt.subplots(figsize=(10, 6))

    # Customize the colors
    # bar_color = '#13818F'  # Deep pastel blue color
    text_color = '#333333'  # Dark gray color

    # Plot the bar chart
    ax.bar(columns, values)

    # Customize the title and axis labels
    ax.set_title('Phonemes in ' + filename[:-4], fontsize=18, fontweight='bold', color=text_color)
    ax.set_xlabel('Phoneme', fontsize=12, color=text_color)
    ax.set_ylabel('Counts', fontsize=12, color=text_color)

    # Customize the tick labels
    ax.tick_params(axis='x', rotation=45, labelsize=10, colors=text_color)
    ax.tick_params(axis='y', labelsize=10, colors=text_color)

    # Set the background color
    ax.set_facecolor('#FFFFFF')  # White color

    # Remove spines
    for spine in ax.spines.values():
        spine.set_color('lightgray')

    # Add a grid
    ax.set_axisbelow(True)
    ax.grid(color='lightgray', linestyle='-', linewidth=0.5)

    plt.savefig(filename[:-4]+'.png')

def main():
    #compute_frequencies(include_stopwords=False)
 #   join_dataframe_rows(['7-8_processed_per_entry_no_stopwords.csv'   , '8-9_processed_per_entry_no_stopwords.csv', '9-10_processed_per_entry_no_stopwords.csv',
  #                 '11-14_processed_per_entry_no_stopwords.csv', '14-16_processed_per_entry_no_stopwords.csv'], 'all_levels_full_no_stopwords.csv')
#    run_correlation_analysis('all_levels_full_no_stopwords.csv')
    #visualize_dataframe('7-8_processed_per_entry.csv')
    list1 = ['7-8_processed_per_entry.csv', '8-9_processed_per_entry.csv',
     '9-10_processed_per_entry.csv', '11-14_processed_per_entry.csv',
     '14-16_processed_per_entry.csv']
    for item in list1:
        visualize_dataframe(item)

if __name__ == '__main__':
    main()