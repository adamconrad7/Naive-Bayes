import io
import re

def sanitize(filename):
    punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
    with open(filename, "r") as a_file:
        list = []
        for line in a_file:
            line = line.strip()
            no_punct = ""
            for char in line:
               if char not in punctuations:
                   no_punct = no_punct + char
            line = no_punct
            val = line[-1]
            line = line.replace(val, '')
            line = re.sub('\s+',' ',line)
            line = line.strip()
            tup = (line, val)
            list.append(tup)
    return list

def main():
    tuples = sanitize('data/testSet.txt')


main()
