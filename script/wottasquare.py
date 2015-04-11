#!/usr/bin/env python

import sys
import random
import re


SCRABBLE = {
    'A': 1,
    'B': 3,
    'C': 3,
    'D': 2,
    'E': 1,
    'F': 4,
    'G': 2,
    'H': 4,
    'I': 1,
    'J': 8,
    'K': 5,
    'L': 1,
    'M': 3,
    'N': 1,
    'O': 1,
    'P': 3,
    'Q': 10,
    'R': 1,
    'S': 1,
    'T': 1,
    'U': 1,
    'V': 4,
    'W': 4,
    'X': 8,
    'Y': 4,
    'Z': 10
}

def scrabble(word):
    acc = 0
    for c in word.upper():
        acc += SCRABBLE[c]
    return acc


dictionary = {
    1: ['a', 'I'],
    2: ['in', 'is', 'no', 'on', 'so', 'it']
}


def load_dictionary(filename):
    with open(filename) as f:
        for line in f:
            for word in re.findall(r'[A-Za-z]+', line):
                if len(word) <= 2 or word[0].isupper():
                    continue
                dictionary.setdefault(scrabble(word), set()).add(word)


def pick_word(num):
    return random.choice(list(dictionary[num]))


def main(args):
    find_text = None
    find_amount = 20
    dictionary_filename = '/usr/share/dict/words'
    while args and args[0].startswith('--'):
        switch = args.pop(0)
        if switch == '--dictionary':
            dictionary_filename = args.pop(0)
        elif switch == '--find':
            find_text = args.pop(0)
        elif switch == '--find-all':
            find_text = args.pop(0)
            find_amount = None
        else:
            raise KeyError("Unknown command-line option '%s'" % switch)

    load_dictionary(dictionary_filename)

    if find_text:
        value = None
        if find_text.isdigit():
            value = int(find_text)
        else:
            value = scrabble(find_text)
        print value
        if find_amount is None:
            print ' '.join(sorted(dictionary[value]))
        else:
            words = list(dictionary[value])
            random.shuffle(words)
            print ' '.join(words[:find_amount])
        sys.exit(0)
            
    with open(args[0]) as f:
        for line in f:
            for num in re.findall(r'\[(\d+)\:?.*?\]', line):
                print pick_word(int(num))


if __name__ == '__main__':
    main(sys.argv[1:])
