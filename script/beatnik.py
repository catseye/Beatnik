#!/usr/bin/env python

import sys
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

ACTION = {
    5: 'PUSH',
    6: 'DISCARD',
    7: 'ADD',
    8: 'INPUT',
    9: 'OUTPUT',
    10: 'SUBTRACT',
    11: 'SWAP',
    12: 'DUP',
    13: 'SKIP_AHEAD_ZERO',
    14: 'SKIP_AHEAD_NONZERO',
    15: 'SKIP_BACK_ZERO',
    16: 'SKIP_BACK_NONZERO',
    17: 'STOP',
}

def scrabble(word):
    acc = 0
    for c in word.upper():
        acc += SCRABBLE[c]
    return acc

DEBUG = False

def debug(s, *args):
    if not DEBUG:
        return
    sys.stderr.write(s % args)
    sys.stderr.write("\n")


class Stack(object):
    def __init__(self):
        self._stack = []

    def push(self, value):
        self._stack.append(value % 256)

    def append(self, value):
        """for backwards compatibility"""
        self.push(value)

    def pop(self):
        return self._stack.pop()


def main(args):
    global DEBUG
    tokenize = False
    text = None

    while args and args[0].startswith('--'):
        switch = args.pop(0)
        if switch == '--debug':
            DEBUG = True
        elif switch == '--tokenize':
            tokenize = True
        elif switch == '--eval':
            text = args.pop(0)
        else:
            raise KeyError("Unknown command-line option '%s'" % switch)

    words = []
    if text is not None:
        for word in re.findall(r'[a-zA-Z]+', text):
            words.append(word)
    else:
        with open(args[0]) as f:
            for line in f:
                for word in re.findall(r'[a-zA-Z]+', line):
                    words.append(word)

    if tokenize:
        # A better version of this would not try to assign an ACTION
        # to constants (words that follow PUSH or SKIP instructions)
        for word in words:
            value = scrabble(word)
            print ("[%s:%s/%s]" % (value, ACTION.get(value, 'NOP'), word))
        sys.exit(0)

    words.append('FOXY')  # stop if you get to the end

    stack = Stack()
    pc = 0
    done = False

    while not done:
        value = scrabble(words[pc])
        debug("* '%s' = %s (%s)", words[pc], value, ACTION.get(value, '(none)'))
        if value == 5:
            pc += 1
            a = scrabble(words[pc])
            stack.append(a)
        elif value == 6:
            stack.pop()
        elif value == 7:
            a = stack.pop()
            b = stack.pop()
            debug("...ADD %s %s", a, b)
            stack.append(a + b)
        elif value == 8:
            c = sys.stdin.read(1)
            stack.append(ord(c))
        elif value == 9:
            c = stack.pop()
            debug("...WRITE %s", c)
            sys.stdout.write(chr(c))
        elif value == 10:
            a = stack.pop()
            b = stack.pop()
            stack.append(b - a)
        elif value == 11:
            a = stack.pop()
            b = stack.pop()
            stack.append(a)
            stack.append(b)
        elif value == 12:
            a = stack.pop()
            stack.append(a)
            stack.append(a)
        elif value == 13:
            a = stack.pop()
            pc += 1
            dist = scrabble(words[pc])
            if a == 0:
                pc += dist
        elif value == 14:
            a = stack.pop()
            pc += 1
            dist = scrabble(words[pc])
            if a != 0:
                pc += dist
        elif value == 15:
            a = stack.pop()
            dist = scrabble(words[pc + 1])
            if a == 0:
                pc -= dist
        elif value == 16:
            a = stack.pop()
            dist = scrabble(words[pc + 1])
            if a != 0:
                pc -= dist
        elif value == 17:
            done = True
        pc += 1


if __name__ == '__main__':
    main(sys.argv[1:])
