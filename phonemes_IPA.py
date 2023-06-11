from collections import Counter

import nltk
import nltk.data
import matplotlib.pyplot as plt
import numpy as np

ARPAbet = ["AA", "AE", 'AH', 'AO', 'AW', 'AY', 'EH', 'ER', 'EY', 'IH', 'IY', 'OW', 'OY', 'UH', 'UW', 'B', 'CH', 'D', 'DH', 'F', 'G', 'HH', 'JH', 'K', 'L', 'M', 'N', 'NG', 'P', 'R', 'S', 'SH', 'T', 'TH', 'V', 'W', 'Y', 'Z', 'ZH']
ARPAbet_to_IPA = {'AA': 'ɑ',
'AE': 'æ',
'AH': 'ʌ',
'AO': 'ɔ',
'AW': 'aʊ',
'AY': 'aɪ',
'EH': 'ɛ',
'ER': 'ɝ',
'EY': 'eɪ',
'IH': 'ɪ',
'IY': 'i',
'OW': 'oʊ',
'OY': 'ɔɪ',
'UH': 'ʊ',
'UW': 'u',
'B': 'b',
'CH': 'tʃ',
'D': 'd',
'DH': 'ð',
'F': 'f',
'G': 'g',
'HH': 'h',
'JH': 'dʒ',
'K': 'k',
'L': 'l',
'M': 'm',
'N': 'n',
'NG': 'ŋ',
'P': 'p',
'R': 'ɹ',
'S': 's',
'SH': 'ʃ',
'T': 't',
'TH': 'θ',
'V': 'v',
'W': 'w',
'Y': 'j',
'Z': 'z',
'ZH': 'ʒ'
}
ARPAbet_vowels = ["AA", "AE", 'AH', 'AO', 'AW', 'AY', 'EH', 'ER', 'EY', 'IH', 'IY', 'OW', 'OY', 'UH', 'UW']
ARPAbet_consonants = ['B', 'CH', 'D', 'DH', 'F', 'G', 'HH', 'JH', 'K', 'L', 'M', 'N', 'NG', 'P', 'R', 'S', 'SH', 'T', 'TH', 'V', 'W', 'Y', 'Z', 'ZH']

ARPAbet_diphthongs = ["AW", "AI"]
def visualize_counter(counter, title):
    # Extract key-value pairs from the counter
    items = counter.most_common()
    keys, values = zip(*items)

    # Plot the bar chart
    plt.bar(keys, values)
    plt.xlabel('Phoneme')
    plt.ylabel('Counts')
    plt.title('Phonemes in '+title)

    # Display the plot
    plt.show()

def visualize_counter_fancy(counter, title, save=False):
    # Extract key-value pairs from the counter
    items = counter.most_common()
    keys, values = zip(*items)

    # Set up the figure and axes
    fig, ax = plt.subplots(figsize=(10, 6))

    # Customize the colors
    #bar_color = '#13818F'  # Deep pastel blue color
    text_color = '#333333'  # Dark gray color

    # Plot the bar chart
    ax.bar(keys, values)

    # Customize the title and axis labels
    ax.set_title('Phonemes in '+title, fontsize=18, fontweight='bold', color=text_color)
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

    if not save:
        # Display the plot
        plt.show()
    else:
        plt.savefig(title+".png")
        plt.close()


def text_to_phonemes(text):
    # Download the CMU Pronouncing Dictionary and punkt if not already downloaded
    #nltk.download('cmudict')
    #nltk.download('punkt')

    # Load the CMU Pronouncing Dictionary
    cmudict = nltk.corpus.cmudict.dict()

    # Tokenize the text into words
    words = nltk.word_tokenize(text.lower())

    # Convert each word to its phoneme representation
    phonemes = []
    for word in words:
        if word in cmudict:
            phoneme_list = cmudict[word][0]
            phonemes.extend([phoneme.rstrip('012') for phoneme in phoneme_list])
        else:
            # Handle words not found in CMUDict
            # phonemes.append(word)
            print("No valid pronunciation found for: "+word)

    return phonemes


def compute_GPC(text):
    # Download the CMU Pronouncing Dictionary and punkt if not already downloaded
    #nltk.download('cmudict')
    #nltk.download('punkt')

    # Load the CMU Pronouncing Dictionary
    cmudict = nltk.corpus.cmudict.dict()

    # Tokenize the text into words
    words = nltk.word_tokenize(text.lower())

    # Calculate GPC of each word
    gpc_list = []
    for word in words:
        phonemes = []
        if word in cmudict:
            phoneme_list = cmudict[word][0]
            phonemes.extend([phoneme.rstrip('012') for phoneme in phoneme_list])
            ipa_phonemes = map(lambda x: ARPAbet_to_IPA[x], phonemes)
            for pp in ipa_phonemes:
                print(pp)
            phoneme_length = len(phoneme_list)
            grapheme_length = len(word)
            GPC = phoneme_length/grapheme_length
            gpc_list.append(GPC)
        else:
            # Handle words not found in CMUDict
            # phonemes.append(word)
            print("No valid pronunciation found for: "+word)

    return np.average(gpc_list)


def main():
    text = "That quick beige fox jumped in the air over each thin dog. Look out, I shout, for he's foiled you again, creating chaos."
    text += " Are those shy Eurasian footwear, cowboy chaps, or jolly earthmoving headgear?"
    text += " The hungry purple dinosaur ate the kind, zingy fox, the jabbering crab, and the mad whale and started vending and quacking."

    print(compute_GPC(text))
#
 #   phonemes = text_to_phonemes(text)
  #  phoneme_ctr = Counter(phonemes)
   # print(phoneme_ctr)
    #visualize_counter(phoneme_ctr, 'Sample')

if __name__ == "__main__":
    main()