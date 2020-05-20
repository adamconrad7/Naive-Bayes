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

def featurize(tuples, vocab):
    featurized = []
    for tuple in tuples:
        sentence = sorted(set(tuple[0].split()))
        features = []
        for word in vocab:
            if word in sentence:
                features.append(1)
            else:
                features.append(0)
        features.append(tuple[1])
        featurized.append(features)
    return featurized

def write_data(features, vocab):
    f = open("preprocessed_train.txt", "w")
    for word in vocab:
        f.write(word)
        f.write(' ')
    f.write('classlabel')
    for line in features:
        f.write('\n')
        for feature in line:
            f.write(str(feature))
            f.write(' ')

def pre_proccess(filename):
    tuples = sanitize(filename)
    vocab = build_vocab(tuples)
    features = featurize(tuples, vocab)
    write_data(features, vocab)
    return features

def main():
    features = pre_proccess('data/trainingSet.txt')

main()
