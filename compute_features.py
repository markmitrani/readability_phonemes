import matplotlib.pyplot as plt
import nltk
import numpy as np
import pandas as pd
import os
from collections import Counter

import seaborn as sns
from pandas import read_csv

import phonemes_IPA
from phonemes_IPA import text_to_phonemes, visualize_counter, visualize_counter_fancy


def add_features_to_dataframe(df, filename, features):
    df.loc[filename] = pd.Series(features, index=df.columns)

#
# Method to take all .txt files in a directory and the features of each as entries in a dataframe
# Returns a dataframe object
#
def process_text_files(directory_path):
    features_df = pd.DataFrame(text_to_features('test test test'), index=['yikes.txt'])
    for filename in os.listdir(directory_path):
        if filename.endswith(".txt"):
            file_path = os.path.join(directory_path, filename)
            with open(file_path, "r", encoding="latin-1") as file:
                print("Processing file " + filename + " in " + directory_path + "...")
                text = file.read()
                add_features_to_dataframe(features_df, filename, text_to_features(text))

    return features_df


def compute_features():
    # func: specifying directories and processing them in a loop
    directories = [#'7-8_processed_sample', '8-9_processed_sample', '9-10_processed_sample',
                   #'11-14_processed_sample',
        '14-16_processed_sample']

    for directory in directories:
        if '7-8' in directory:
            level = 1
            print(level, " is the level")
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

        # Print the dataframe
        print(result_df)
        result_df.to_csv(directory + '_features.csv')


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
    fig, ax = plt.subplots(figsize=(10,10))

    # Create the heatmap
    heatmap = sns.heatmap(correlation_matrix, cmap='coolwarm', annot=True, fmt='.2f', linewidths=.5, ax=ax)

    # Add a title to the plot
    plt.title('Correlation Matrix')
    # Display the plot
    plt.savefig(file[:-4] + '_corr.png', dpi=300)
    print("Correlation analysis saved as", file[:-4] + '_corr.png')
    plt.show()


def text_to_features(text):
    feats = dict()
    # Download the CMU Pronouncing Dictionary and punkt if not already downloaded
    # nltk.download('cmudict')
    # nltk.download('punkt')

    # Load the CMU Pronouncing Dictionary
    cmudict = nltk.corpus.cmudict.dict()

    # Tokenize the text into words
    words = nltk.word_tokenize(text.lower())

    total_phonemes = []
    # Calculate GPC of each word
    gpc_list = []
    # Calculate vowel consonant ratio of each word
    vc_list = []

    dipthong_count = 0

    for word in words:
        vcount = 0
        ccount = 0
        phonemes = []
        if word in cmudict:
            phoneme_list = cmudict[word][0]
            phonemes.extend([phoneme.rstrip('012') for phoneme in phoneme_list])
            total_phonemes += phonemes

            # GPC CALC 1/2
            phoneme_length = len(phoneme_list)
            grapheme_length = len(word)
            GPC = phoneme_length / grapheme_length
            gpc_list.append(GPC)

            # V/C CALC 1/2
            vcount += sum(1 for phoneme in phonemes if phoneme in phonemes_IPA.ARPAbet_vowels)
            ccount += sum(1 for phoneme in phonemes if phoneme in phonemes_IPA.ARPAbet_consonants)
            if ccount == 0:
                vc_list.append(0)
            else:
                vc_list.append(float(vcount) / ccount)

            dipthong_count += sum(1 for phoneme in phonemes if phoneme in phonemes_IPA.ARPAbet_diphthongs)
        else:
            # Handle words not found in CMUDict
            # phonemes.append(word)
            print("No valid pronunciation found for: " + word)

    # GPC CALC 2/2
    feats['GPC'] = np.average(gpc_list)

    # V/C CALC 2/2
    feats['vowel/consonant ratio'] = np.average(vc_list)

    if len(total_phonemes) == 0:
        feats['phoneme diversity'] = 0
        feats['dipthong frequency in phonemes'] = 0
        feats['dipthong frequency in vowels'] = 0
        return feats

    # phonemic diversity calc
    feats['phoneme diversity'] = len(set(total_phonemes)) / len(total_phonemes)

    feats['dipthong frequency in vowels'] = dipthong_count / sum(
        1 for phoneme in total_phonemes if phoneme in phonemes_IPA.ARPAbet_vowels)
    feats['dipthong frequency in phonemes'] = dipthong_count / len(total_phonemes)
    print(feats)
    return feats

def main():
    #compute_features()
    join_dataframe_rows(['7-8_processed_sample_features.csv', '8-9_processed_sample_features.csv', '9-10_processed_sample_features.csv',
                   '11-14_processed_sample_features.csv', '14-16_processed_sample_features.csv'], 'all_levels_features.csv')
    run_correlation_analysis('all_levels_features.csv')

if __name__ == '__main__':
    main()
