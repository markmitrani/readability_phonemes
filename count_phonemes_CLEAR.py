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

def add_counter_to_dataframe(df, phoneme_ctr):
    total_count = sum(phoneme_ctr.values())
    normalized_counts = {k: v/total_count for k, v in phoneme_ctr.items()}
    df = normalized_counts
    df = df.fillna(0)

#
# Method to take all .txt files in a directory and the phonemes of each as entries in a dataframe
# Returns a dataframe object
#
def process_excel_file(directory_path):
    phonemes_df = phoneme_count_dataframe()
    for filename in os.listdir(directory_path):
        if filename.endswith(".txt"):
            file_path = os.path.join(directory_path, filename)
            with open(file_path, "r", encoding="latin-1") as file:
                print("Processing file " + filename + " in " + directory_path + "...")
                text = file.read()
                add_counter_to_dataframe(phonemes_df, filename, Counter(text_to_phonemes(text)))

    return phonemes_df


def extract_columns_from_xlsx(filename):
    filename = 'CLEAR_corpus_final.xlsx'
    file_path = os.path.join('data', filename)

    # Load the XLSX file
    data = pd.read_excel(file_path)

    # Extract the columns based on first row values
    excerpt_col = None
    bt_easiness_col = None
    for col in data.columns:
        print(col)
        print(data[col].iloc[0])
        if col == 'Excerpt':
            excerpt_col = col
        elif col == 'BT_easiness':
            bt_easiness_col = col

    # Check if the required columns were found
    if excerpt_col is None or bt_easiness_col is None:
        raise ValueError("Required columns not found in the XLSX file")

    # Create a DataFrame with the extracted columns
    df = pd.DataFrame({
        'Excerpt': data[excerpt_col],
        'BT_easiness': data[bt_easiness_col]
    })

    print(df)

    return df

def compute_frequencies(df, include_stopwords = True):
    for index, row in df.iterrows():
        print('Processing row',index)
        phonemes = Counter(text_to_phonemes(row['Excerpt'], include_stopwords))
        total_count = sum(phonemes.values())
        normalized_counts = {k: v / total_count for k, v in phonemes.items()}

        # Iterate over the columns
        for column_name, value in row.items():
            if column_name in normalized_counts:
                df.at[index, column_name] = normalized_counts[column_name]
    if include_stopwords:
        df.to_csv('CLEAR_phonemes.csv')
    else:
        df.to_csv('CLEAR_phonemes_no_stopwords.csv')

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
    print(df)
    columns_for_corr = df.columns[3:]
    correlation_matrix = df[columns_for_corr].corrwith(df['BT_easiness']).to_frame().T

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


def fix_read_metric(file):
    df = pd.read_csv(file)
    max_value = df['BT_easiness'].max()
    min_value = df['BT_easiness'].min()
    print(max_value, 'is max')
    print(min_value, 'is min')

    print("before", df['BT_easiness'])
    df['BT_easiness'] = max_value - df['BT_easiness']
    print("after", df['BT_easiness'])

    max_value = df['BT_easiness'].max()
    min_value = df['BT_easiness'].min()
    print(max_value, 'is max')
    print(min_value, 'is min')
    df.drop(df.columns[0], axis=1, inplace=True)
    df.to_csv(file[:-4]+'_fixed.csv')



def main():
  #  df = extract_columns_from_xlsx('CLEAR_corpus_final.xlsx')
  #  # Concatenate the two DataFrames
  #  df = pd.concat([df, phoneme_count_dataframe()], axis=1).fillna(0)
  #  compute_frequencies(df, include_stopwords=False)
  #  fix_read_metric('CLEAR_phonemes_no_stopwords.csv')
    run_correlation_analysis('CLEAR_phonemes_no_stopwords_fixed.csv')

    #compute_frequencies()
    #join_dataframe_rows(['7-8_processed_per_entry.csv'   , '8-9_processed_per_entry.csv', '9-10_processed_per_entry.csv',
    #               '11-14_processed_per_entry.csv', '14-16_processed_per_entry.csv'], 'all_levels_full.csv')
    #run_correlation_analysis('all_levels_full.csv')

if __name__ == '__main__':
    main()