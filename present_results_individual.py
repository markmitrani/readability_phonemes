import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

import phonemes_IPA


# for individual phonemes: correlation per level (based on one-hot encoding)
#
# accepts a .csv as input, and runs pairwise correlation analysis between the column 'level' and every other column that has a name.
# saves the correlation matrix as the name of the file + _corr
#
def run_correlation_analysis(file):
    df = pd.read_csv(file)

    # Exclude 'level' column
    df = df.drop(columns='level')
    df = df.drop(columns='Unnamed: 0.1')
    df = df.drop(columns='Unnamed: 0')

    # Compute the full correlation matrix
    correlation_matrix = df.corr()

    # Filter the correlation matrix to keep only rows for the levels and columns for the phonemes
    level_cols = [col for col in df.columns if 'LEVEL_' in col]
    phoneme_cols = [col for col in df.columns if 'LEVEL_' not in col]

    correlation_matrix = correlation_matrix.loc[level_cols, phoneme_cols]

    # Set up the figure and axis with a wider width
    fig, ax = plt.subplots(figsize=(25, 5))

    # Create the heatmap
    heatmap = sns.heatmap(correlation_matrix, cmap='RdBu', annot=True, fmt='.2f', cbar_kws={"shrink": 0.5}, ax=ax, square=True)

    # Update the x-axis labels with their values from the dictionary
  #  heatmap.set_xticklabels([phonemes_IPA.ARPAbet_to_IPA.get(label, label) for label in columns_for_corr])

    # Add a title to the plot
    plt.title('Correlation Matrix')
    # Display the plot
    plt.savefig(file[:-4] + '_corr.png', dpi=150)
    print("Correlation analysis saved as", file[:-4] + '_corr.png')
    #plt.show()


# 1. make correlation matrix for individual phonemes
def plot_average_phoneme_frequencies(file):
    df = pd.read_csv(file)
    df = df.drop('Unnamed: 0', axis=1)
    df = df.drop('Unnamed: 0.1', axis=1)

    # Group by 'level' column and compute mean
    mean_df = df.groupby('level').mean()

    # Exclude 'LEVEL_' columns and other non-phoneme columns as needed
    non_phoneme_cols = [col for col in df.columns if 'LEVEL_' in col] + ['level']

    # Get phoneme columns by subtracting non_phoneme_cols from df.columns
    phoneme_cols = [col for col in df.columns if col not in non_phoneme_cols]

    # Set up the figure and axis with a wider width
    fig, ax = plt.subplots(figsize=(20, 6))

    # Create the heatmap
    heatmap = sns.heatmap(mean_df[phoneme_cols], cmap='crest', annot=True, square=True, fmt='.2f', cbar_kws={"shrink": 0.5}, linewidths=.5, ax=ax)

    # Adjust the vertical alignment of the correlation values
    for text in heatmap.texts:
        text.set_rotation(45)
        text.set_verticalalignment('center')

    # Add a title to the plot
    plt.title('Average Phoneme Frequencies by Level')

    # Save the plot
    plt.savefig(file[:-4] + '_avg_freq.png', dpi=300)
    print("Average phoneme frequency analysis saved as", file[:-4] + '_avg_freq.png')
    plt.show()

def plot_phoneme_variance(file):
    df = pd.read_csv(file)
    df = df.drop('Unnamed: 0', axis=1)
    df = df.drop('Unnamed: 0.1', axis=1)

    # Group by 'level' column and compute variance
    var_df = df.groupby('level').var()

    # Exclude 'LEVEL_' columns and other non-phoneme columns as needed
    non_phoneme_cols = [col for col in df.columns if 'LEVEL_' in col] + ['level', 'Unnamed: 0', 'Unnamed: 0.1']

    # Get phoneme columns by subtracting non_phoneme_cols from df.columns
    phoneme_cols = [col for col in df.columns if col not in non_phoneme_cols]

    # Set up the figure and axis with a wider width
    fig, ax = plt.subplots(figsize=(20, 6))

    # Create the heatmap
    heatmap = sns.heatmap(var_df[phoneme_cols], cmap='crest', square=True, fmt='.6f', cbar_kws={"shrink": 0.5}, linewidths=.5, ax=ax)

    # Adjust the vertical alignment of the correlation values
    for text in heatmap.texts:
        text.set_rotation(45)
        text.set_verticalalignment('center')

    # Add a title to the plot
    plt.title('Phoneme Variance by Level')

    # Save the plot
    plt.savefig(file[:-4] + '_var.png', dpi=300)
    print("Phoneme variance analysis saved as", file[:-4] + '_var.png')
    plt.show()

def main():

    #run_correlation_analysis('all_levels_full_one_hot.csv')
    plot_average_phoneme_frequencies('all_levels_full_one_hot.csv')
    plot_phoneme_variance('all_levels_full_one_hot.csv')

if __name__ == '__main__':
    main()

"""
def plot_normalized_phoneme_frequencies(file):
    df = pd.read_csv(file)

    # Group by 'level' column and compute sum
    summed_df = df.groupby('level').sum()

    # Exclude 'LEVEL_' columns and other non-phoneme columns as needed
    non_phoneme_cols = [col for col in df.columns if 'LEVEL_' in col] + ['level', 'Unnamed: 0', 'Unnamed: 0.1']

    # Get phoneme columns by subtracting non_phoneme_cols from df.columns
    phoneme_cols = phonemes_IPA.ARPAbet

    # Normalize the phoneme columns
#    summed_df[phoneme_cols] = summed_df[phoneme_cols].div(summed_df[phoneme_cols].sum(axis=1), axis=0)

    # Set up the figure and axis with a wider width
    fig, ax = plt.subplots(figsize=(20, 6))

    # Create the heatmap
    heatmap = sns.heatmap(summed_df[phoneme_cols], cmap='crest', annot=True, square=True, fmt='.2f', cbar_kws={"shrink": 0.5}, linewidths=.5, ax=ax)

    # Adjust the vertical alignment of the correlation values
    for text in heatmap.texts:
        text.set_rotation(45)
        text.set_verticalalignment('center')

    # Add a title to the plot
    plt.title('Normalized Phoneme Frequencies by Level')

    # Save the plot
    plt.savefig(file[:-4] + '_norm_freq.png', dpi=300)
    print("Normalized phoneme frequency analysis saved as", file[:-4] + '_norm_freq.png')
    plt.show()
"""