import pandas as pd
import os
from collections import Counter

import phonemes_IPA
from phonemes_IPA import text_to_phonemes, visualize_counter, visualize_counter_fancy


# Method to convert a Counter to a DataFrame
def counter_to_dataframe(counter):
    df = pd.DataFrame.from_dict(counter, orient='index', columns=['Count'])
    df.index.name = 'Name'
    return df

# Method to add counts from a Counter to an existing DataFrame
def add_counts_to_dataframe(counter, dataframe):
    for name, count in counter.items():
        if name in dataframe.index:
            dataframe.loc[name, 'Count'] += count
        else:
            dataframe = dataframe.append(pd.DataFrame({'Count': [count]}, index=[name]))
    return dataframe


#
# Method to take all .txt files in a directory and return their phonemes in a single list
#
def process_text_files(directory_path):
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


def main():
    # grouping. 'phonemes' or 'vowels/consonants'
    grouping = 'vowels_consonants'

    # func: specifying directories and processing them in a loop
    directories = ['Text']
    for directory in directories:
        directory_path = os.path.join('data', directory)
        phonemes_unfiltered = process_text_files(directory_path)
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
        counter_to_dataframe(phoneme_ctr).to_csv(directory+"_"+grouping+'.csv')
        visualize_counter_fancy(phoneme_ctr, directory)

if __name__ == '__main__':
    main()