from collections import Counter

import nltk
import nltk.data
import matplotlib.pyplot as plt

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


def text_to_phonemes(text):
    # Download the CMU Pronouncing Dictionary if not already downloaded
 #   nltk.download('cmudict')

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

def main():
    nltk.download('cmudict')

    text = "That quick beige fox jumped in the air over each thin dog. Look out, I shout, for he's foiled you again, creating chaos."
    text += " Are those shy Eurasian footwear, cowboy chaps, or jolly earthmoving headgear?"
    text += " The hungry purple dinosaur ate the kind, zingy fox, the jabbering crab, and the mad whale and started vending and quacking."

    phonemes = text_to_phonemes(text)
    phoneme_ctr = Counter(phonemes)
    print(phoneme_ctr)
    visualize_counter(phoneme_ctr, 'Sample')


if __name__ == "__main__":
    main()