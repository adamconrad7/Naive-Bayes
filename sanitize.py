import io

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
    ppos = props[0]
    pneg = props[1]
    cnt = 0
    for feature in sentence:
        if cnt == len(vocab):
            break
        if feature:
            ppos *= p_table[cnt][0]
            pneg *= p_table[cnt][1]

        cnt+=1
    l.append(ppos)
    l.append(pneg)

    # print(ppos)
    if ppos > pneg:
        return 1
    else:
        return 0
    # return l



def main():
    tuples = sanitize('data/trainingSet.txt')
    vocab = build_vocab(tuples)
    features = featurize(tuples, vocab)
    write_data(features, vocab)
    p_table = build_table(features, vocab)
    props = find_proportions(features)
    predict = []
    for feature in features:
        l = []
        l.append(feature[-1])
        l.append(classify(feature, vocab, p_table, props))
        # predict = classify(feature, vocab, p_table, props)
        print(l)
        predict.append(l)
    c = 0
    for prediction in predict:
        if prediction[0] == str(prediction[1]):
            print(prediction)
            c+=1
    print(c/len(features))



    # print(predict[0], predict[1])





main()
