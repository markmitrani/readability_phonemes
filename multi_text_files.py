import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
from collections import Counter

import phonemes_IPA
from phonemes_IPA import text_to_phonemes, visualize_counter, visualize_counter_fancy



#
# Method to take all .txt files in a directory and return their phonemes in a single list
#
def process_text_files_old(directory_path):
    result = []

    for filename in os.listdir(directory_path):
        if filename.endswith(".txt"):
            file_path = os.path.join(directory_path, filename)
            with open(file_path, "r", encoding="latin-1") as file:
                print("Processing file "+filename+" in "+directory_path+"...")
                text = file.read()
                current_items = text_to_phonemes(text)
                for item in current_items:
                    result.append(item)

    return result

#
# Method to take all .txt files in a directory and return their GPC average
#
def process_text_files_GPC(directory_path):
    result = []

    for filename in os.listdir(directory_path):
        if filename.endswith(".txt"):
            file_path = os.path.join(directory_path, filename)
            with open(file_path, "r", encoding="latin-1") as file:
                print("Processing file "+filename+" in "+directory_path+"...")
                text = file.read()
                item = phonemes_IPA.compute_GPC(text)
                result.append(item)

    return np.average(result)

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
                print("Processing file "+filename+" in "+directory_path+"...")
                text = file.read()
                add_counter_to_dataframe(phonemes_df, filename, Counter(text_to_phonemes(text)))

    return phonemes_df


def phoneme_count_dataframe():
    index = phonemes_IPA.ARPAbet_to_IPA.keys()
    df = pd.DataFrame(columns=index)
    return df

def add_counter_to_dataframe(df, filename, phoneme_ctr):
    df.loc[filename] = phoneme_ctr
    df.loc[filename] = df.loc[filename].fillna(0)


def frequency_analysis():
    # grouping: 'phonemes' or 'vowels/consonants'
    grouping = 'phonemes'

    # func: specifying directories and processing them in a loop
    directories = ['7-8_processed_sample', '8-9_processed_sample', '9-10_processed_sample', '11-14_processed_sample', '14-16_processed_sample']
    for directory in directories:
        directory_path = os.path.join('data', directory)
        phonemes_unfiltered = process_text_files_old(directory_path)
        phonemes = []

        # post-processing of the result set
        for item in phonemes_unfiltered:
            print(item)
            # filter items not in ARPAbet
            if item in phonemes_IPA.ARPAbet:
                phonemes.append(item)

        phoneme_ctr = Counter(phonemes)
        if grouping == 'vowels_consonants':
            grouped_ctr = Counter({'Vowels': 0, 'Consonants': 0})
            for phon in phonemes_IPA.ARPAbet_vowels:
                if phon in phoneme_ctr:
                    grouped_ctr['Vowels'] += phoneme_ctr[phon]
            for phon in phonemes_IPA.ARPAbet_consonants:
                if phon in phoneme_ctr:
                    grouped_ctr['Consonants'] += phoneme_ctr[phon]
            phoneme_ctr = grouped_ctr

        print(phoneme_ctr)
        # convert counter to dataframe then export to csv
        counter_to_dataframe_old(phoneme_ctr).to_csv(directory + "_" + grouping + '.csv')
        visualize_counter_fancy(phoneme_ctr, directory, True)

def main():

    #frequency_analysis()
    counter_to_dataframe("example.txt", Counter({"AA": 5}))


def GPC_analysis():
    result = []
    # func: specifying directories and processing them in a loop
    directories = ['7-8', '8-9', '9-10', '11-14']
    #directories = ['sample1', 'sample2', 'sample3', 'sample4']
    for directory in directories:
        directory_path = os.path.join('data', directory)
        GPC = process_text_files_GPC(directory_path)
        item = (directory, GPC)
        result.append(item)

    # Extract x and y values from tuples
    x = [item[0] for item in result]
    y = [item[1] for item in result]

    # Plot the data
    plt.bar(x, y)
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    plt.title('Plotting Data for GPC')
    plt.savefig('GPC_trend.png')
    plt.close()


if __name__ == '__main__':
    main()

# Method to convert a Counter to a DataFrame
def counter_to_dataframe_old(counter):
    # Create a new dictionary with the same keys but with all values set to 0:
    new_dict = {key: 0 for key in phonemes_IPA.ARPAbet_to_IPA.keys()}

    df = pd.DataFrame(list(new_dict.items()), columns=['Name', 'Count'])
    add_counts_to_dataframe_old(counter, df)
    return df

# Method to add counts from a Counter to an existing DataFrame
def add_counts_to_dataframe_old(counter, dataframe):
    for name, count in counter.items():
        if name in dataframe.rows:
            dataframe.loc[name, 'Count'] += count
        else:
            #dataframe = dataframe.append(pd.DataFrame({'Count': [count]}, index=[name]))
            print("couldn't insert "+name+" with count "+str(count))
    return dataframe
