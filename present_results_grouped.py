import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

import grouped_phonemes


def run_correlation_analysis_with_grouping(file, grouping):
    df = pd.read_csv(file)

    # Exclude 'level' column
    df = df.drop(columns='level')
    df = df.drop(columns='Unnamed: 0.1')
    df = df.drop(columns='Unnamed: 0')

    # Compute the full correlation matrix
    correlation_matrix = df.corr()

    # Filter the correlation matrix to keep only rows for the levels and columns for the phonemes
    level_cols = [col for col in df.columns if 'LEVEL_' in col]
    phoneme_cols = grouping

    correlation_matrix = correlation_matrix.loc[level_cols, phoneme_cols]

    # Set up the figure and axis with a wider width
    fig, ax = plt.subplots(figsize=(10, 10))

    # Create the heatmap
    heatmap = sns.heatmap(correlation_matrix, cmap='RdBu', annot=True, fmt='.2f', ax=ax, square=True)

    # Update the x-axis labels with their values from the dictionary
  #  heatmap.set_xticklabels([phonemes_IPA.ARPAbet_to_IPA.get(label, label) for label in columns_for_corr])

    # Add a title to the plot
    plt.title('Correlation Matrix')
    # Display the plot
    plt.savefig(file[:-4] + '_corr.png', dpi=150)
    print("Correlation analysis saved as", file[:-4] + '_corr.png')
    #plt.show()


def create_bar_charts(df, columns_to_plot):
    # Drop unnecessary columns
    df = df.drop(columns=['Unnamed: 0.1', 'Unnamed: 0'])

    # Group by level and compute mean
    df_grouped = df.groupby('level').sum()

    # Loop over the list of columns to plot
    for column in columns_to_plot:
        # Create a new figure for each column
        plt.figure(figsize=(10, 6))

        # Create a bar chart for the current column
        plt.bar(x=df_grouped.index, height=df_grouped[column])

        # Set the title and labels
        plt.title(f'Mean Frequency of {column} by Level')
        plt.xlabel('Level')
        plt.ylabel(column)

        # Save and show the plot
        plt.savefig(f'bar_chart_{column}_by_level_discard.png', dpi=300)
        plt.show()

def main():

    # Call the function
    columns_to_plot = grouped_phonemes.year_grouping
    run_correlation_analysis_with_grouping('all_levels_grouped_by_age.csv', columns_to_plot)
    create_bar_charts(pd.read_csv('all_levels_grouped_by_age.csv'), columns_to_plot)

    columns_to_plot = grouped_phonemes.class_grouping
    run_correlation_analysis_with_grouping('all_levels_grouped_by_class.csv', columns_to_plot)
    create_bar_charts(pd.read_csv('all_levels_grouped_by_class.csv'), columns_to_plot)

if __name__ == '__main__':
    main()