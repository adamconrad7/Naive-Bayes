import io
import re

def sanitize(filename):

    punctuations = '''!()[]{};:'"\,<>?@#$%^&*_~'''
    with open(filename, "r") as a_file:
        list = []
        for line in a_file:

            #removes newlines
            line = line.strip()

            #removes punctuation and concatenates
            no_punct = ""
            for char in line:
               if char not in punctuations:
                   no_punct = no_punct + char
            line = no_punct

            #replaces punctuation with space
            line = line.replace('-', ' ')
            line = line.replace('/', ' ')
            line = line.replace('.', ' ')

            #removes value
            val = line[-1]
            line = line.replace(val, '')

            #converts to lowercase
            if not line.islower():
                line = line.lower()

            # stores sentence with its value
            tup = (line, val)
            list.append(tup)

    return list

def build_vocab(tuples):
    words = ''
    for sentence in tuples:
        words += sentence[0] + ' '
    unique_words = sorted(set(words.split()))
    return unique_words

def main():
    tuples = sanitize('data/trainingSet.txt')
    vocab = build_vocab(tuples)
    



main()
