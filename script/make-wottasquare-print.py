#!/usr/bin/env python

import sys
import random


def main(args):
    words = []
    s = args[0]
    for c in s:
        v = ord(c)
        first = True
        while v > 0:
            t = min(random.randint(5, 17), v)
            v -= t
            print "[5:PUSH]"
            print "[%s]" % t
            if not first:
                print "[7:ADD]"
            first = False
        print "[9:OUTPUT]"
        print


if __name__ == '__main__':
    main(sys.argv[1:])
