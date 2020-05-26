import io
import math

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

def build_table(features, vocab):
    pos = 0
    neg = 0
    for record in features:
        if record[-1] == '1':
            pos += 1
        else:
            neg += 1
    ppos = pos / len(features)
    pneg = neg / len(features)
    c = -1
    ptable = []
    for word in vocab:
        pentry = []
        tt = 0
        tf = 0
        ft = 0
        ff = 0
        c += 1
        for record in features:
            if record[c]:
                if record[-1] == '1':
                    tt += 1
                else:
                    tf += 1
            else:
                if record[-1] == '1':
                    ft += 1
                else:
                    ff += 1
        pentry.append((tt+1)/(pos+2))
        pentry.append((tf+1)/(neg+2))
        pentry.append((ft+1)/(pos+2))
        pentry.append((ff+1)/(neg+2))
        ptable.append(pentry)
    return ptable

def find_proportions(features):
    l = []
    pos = 0
    neg = 0
    for record in features:
        if record[-1] == '1':
            pos += 1
        else:
            neg += 1
    ppos = pos / len(features)
    pneg = neg / len(features)
    l.append(ppos)
    l.append(pneg)
    return l

def classify(sentence, vocab, p_table, props):
    l = []

    ppos = math.log(props[0])
    pneg = math.log(props[1])
    length = len(sentence)
    for i in range(length):
        if i == len(vocab):
            break
        if sentence[i]:
            ppos += math.log(p_table[i][0])
            pneg += math.log(p_table[i][1])

    l.append(ppos)
    l.append(pneg)

    return l

def test_model(data, vocab, p_table, props):
    ## list of outcomes
    predict = []

    m = 0
    f = 1;
    for feature in data:

        ## tuple of (score, predicted score)
        l = []

        probabilities = classify(feature, vocab, p_table, props)

        l.append(feature[-1])

        if probabilities[0] > probabilities[1]:
            l.append(1)
        else:
            l.append(0)

        if probabilities[0] > m or probabilities[1] > m :
            m = max(probabilities[0],probabilities[1])

        if probabilities[0] < f or probabilities[1] < f :
            f = min(probabilities[0],probabilities[1])


        predict.append(l)
    print(m, f)

    c = 0
    for prediction in predict:
        if prediction[0] == str(prediction[1]):
            c+=1
    ## Accuracy
    print(c/len(data))


def main():

    ## pre processing
    t_tuples = sanitize('data/trainingSet.txt')
    f_tuples = sanitize('data/testSet.txt')
    f_vocab = build_vocab(f_tuples)
    t_vocab = build_vocab(t_tuples)

    ## featurize sentences based on vocab, note using training vocab
    # when making test set skips un-learned words which greatly impacts accuracy
    train = featurize(t_tuples, t_vocab)
    test = featurize(f_tuples, t_vocab)
    write_data(train, t_vocab)

    ## list of conditional probability tables for each word.
    # eg. < P( good | good = v, class = v), ... >
    p_table = build_table(train, t_vocab)
    props = find_proportions(train)

    test_model(test, t_vocab, p_table, props)


main()
