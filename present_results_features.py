import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

def feature_correlations(file):
    df = pd.read_csv(file)

    # Exclude 'level' column
    df = df.drop(columns=['level', 'Unnamed: 0'])

    # Compute the full correlation matrix
    correlation_matrix = df.corr()

    # Filter the correlation matrix to keep only rows for the levels and columns for the phonemes
    level_cols = [col for col in df.columns if 'LEVEL_' in col]
    feature_cols = ['GPC', 'phoneme diversity']

    correlation_matrix = correlation_matrix.loc[level_cols, feature_cols]

    # Set up the figure and axis with a wider width
    fig, ax = plt.subplots(figsize=(10, 10))

    # Create the heatmap
    heatmap = sns.heatmap(correlation_matrix, cmap='RdBu', annot=True, fmt='.2f', ax=ax, square=True)

    # Add a title to the plot
    plt.title('Correlation Matrix')
    # Display the plot
    plt.savefig(file[:-4] + '_corr.png', dpi=150)
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

    #plot_with_error_bars('all_levels_features.csv', 'GPC')
    #plot_with_error_bars('all_levels_features.csv', 'phoneme diversity')
    feature_correlations('all_levels_features_one_hot.csv')

if __name__ == '__main__':
    main()