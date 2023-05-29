import re
import phonemizer
from phonemizer import separator
from collections import Counter
import matplotlib.pyplot as plt

def visualize_counter(counter):
    # Extract key-value pairs from the counter
    items = counter.most_common()
    keys, values = zip(*items)

    # Plot the bar chart
    plt.bar(keys, values)
    plt.xlabel('Phoneme')
    plt.ylabel('Counts')
    plt.title('Phonemes in Input')

    # Display the plot
    plt.show()


def make_phonemes(text):
    # convert string into phonemes separated by |
    phonemes = phonemizer.phonemize(text, separator=separator.Separator(phone="|"))

    # remove spaces by replacing with empty string
    phonemes = re.sub(r"\s+", '', phonemes)
    print(phonemes)
    return phonemes

def make_phoneme_counter(phonemes):
    phonemes_list = phonemes.split('|')
    phonemes_counter = Counter(phonemes_list)
    return phonemes_counter

def main():
    with open('Text/small.txt') as f:
        lines = f.readlines()
       # print(lines)

        #print(make_phonemes())
        text = "That quick beige fox jumped in the air over each thin dog. Look out, I shout, for he's foiled you again, creating chaos."
        text += "Are those shy Eurasian footwear, cowboy chaps, or jolly earthmoving headgear?"
        text += "The hungry purple dinosaur ate the kind, zingy fox, the jabbering crab, and the mad whale and started vending and quacking."
        phonemes_counter = make_phoneme_counter((make_phonemes(text)))
        print(phonemes_counter)
        print(len(phonemes_counter))
        #visualize_counter(phonemes_counter)


if __name__ == "__main__":
    main()