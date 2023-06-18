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

# for grouped phonemes: join some columns into categories and then correlation again

# 1. make correlation matrix for individual phonemes

def plot_normalized_phoneme_frequencies(file):
    df = pd.read_csv(file)

    # Group by 'level' column and compute sum
    summed_df = df.groupby('level').sum()

    # Exclude 'LEVEL_' columns and other non-phoneme columns as needed
    non_phoneme_cols = [col for col in df.columns if 'LEVEL_' in col] + ['level', 'Unnamed: 0', 'Unnamed: 0.1']

    # Get phoneme columns by subtracting non_phoneme_cols from df.columns
    phoneme_cols = list(set(df.columns) - set(non_phoneme_cols))

    # Normalize the phoneme columns
    summed_df[phoneme_cols] = summed_df[phoneme_cols].div(summed_df[phoneme_cols].sum(axis=1), axis=0)

    # Set up the figure and axis with a wider width
    fig, ax = plt.subplots(figsize=(20, 6))

    # Create the heatmap
    heatmap = sns.heatmap(summed_df[phoneme_cols], cmap='crest', annot=True, square=True, fmt='.2f', linewidths=.5, ax=ax)

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

def feature_correlations(file):
    df = pd.read_csv(file)
    columns_for_corr = df.columns[1:-1]
    correlation_matrix = df[columns_for_corr].corrwith(df['level']).to_frame().T

    # Set up the figure and axis with a wider width
    fig, ax = plt.subplots(figsize=(10,10))

    # Create the heatmap
    heatmap = sns.heatmap(correlation_matrix, cmap='RdBu', annot=True, fmt='.2f', linewidths=.5, ax=ax)

    # Add a title to the plot
    plt.title('Correlation Matrix')
    # Display the plot
    plt.savefig(file[:-4] + '_corr.png', dpi=300)
    print("Correlation analysis saved as", file[:-4] + '_corr.png')
    plt.show()

def trends_for_each_feature(file):
    df = pd.read_csv(file)
    avg_df = df.groupby('level').mean()

def plot_with_error_bars(filename, feature):
    df = pd.read_csv(filename)

    # Group the dataframe by the readability level and calculate mean, min and max
    grouped = df.groupby('level')[feature].agg(['mean', 'min', 'max']).reset_index()

    # Calculate the lower and upper error values
    grouped['lower_error'] = grouped['mean'] - grouped['min']
    grouped['upper_error'] = grouped['max'] - grouped['mean']

    # Create a figure and axis
    fig, ax = plt.subplots()

    # Create an error bar plot
    ax.bar(grouped['level'], grouped['mean'], yerr=[grouped['lower_error'], grouped['upper_error']],
           align='center', alpha=0.5, ecolor='black', capsize=10)

    # Set labels and title
    ax.set_ylabel(feature)
    ax.set_xlabel('Readability Level')
    ax.set_title('Mean ' + feature + ' by Readability Level')

    # Save and show the plot
    plt.savefig(filename[:-4] + '_' + feature + '_plot.png', dpi=300)
    print(feature + " analysis saved as", filename[:-4] + '_' + feature + '_plot.png')
    plt.show()

def main():
    #print(pd.read_csv('all_levels_full_one_hot.csv').columns)
    #run_correlation_analysis('all_levels_full_one_hot.csv')
    #plot_normalized_phoneme_frequencies('all_levels_full_one_hot.csv')
    plot_with_error_bars('all_levels_features.csv', 'GPC')

if __name__ == '__main__':
    main()