Beatnik
=======

This is Cat's Eye Technologies' distribution of tools for Cliff L. Biffle's
**[Beatnik][]** programming language.  This includes an interpreter for Beatnik,
some example Beatnik programs, a compiler from a [wimpmode][] dialect called
**Wottasquare**, and various small utilities which can (for example) search a
dictionary file for all words with a given Scrabble score.

All tools are written in Python and located in the `scripts` directory.
You may wish to `cd` to this directory to run them, or put this directory
on your executable search path.

beatnik.py
----------

Basic usage:

    beatnik.py (filename.beatnik|--eval 'Beatnik program source')

Interprets the Beatnik program in the given source file, or, if the `--eval`
flag is given, the Beatnik program in the command line.

It considers the program to be written in Beatnik at face value.  That is to
say, it interprets the Beatnik specification as containing no errors, even
though the author claims there is an error in it and won't divulge where.
Don't expect this interpreter to work on the example programs supplied with
the specification.

There are two bugs/shortcomings that should really be fixed someday:

*   Integers on the stack can be any value supported by Python, rather
    than limited to the range 0-255.
*   The instructions that skip back, probably skip back the wrong amount.

Other than those two things, this interpreter seems to have the same behaviour
as Catatonic Porpoise's interpreter.  Could use some test cases, though.

`beatnik.py` also takes a `--debug` flag, which dumps some internal state
to standard error as the program is run.

`beatnik.py` also takes a `--tokenize` flag, which prevents the program
from being run, and instead dumps a representation of the program in
Wottasquare to standard output.  (It is essentially a Beatnik-to-Wottasquare
compiler.)

The following idiom can be used to find out what Scrabble score, and thus what
Beatnik instruction, a particular word has.

    $ beatnik.py --tokenize --eval 'Twenty'
    [12:DUP/Twenty]

wottasquare.py
--------------

Basic usage:

    wottasquare.py [--dictionary filename] filename.wottasquare

Reads the Wottasquare program from the given file and compiles it to an
equivalent Beatnik program on standard output.

The Wottasquare language has the same semantics as the Beatnik language,
but each token has the form `[n:comment]` where `n` is the Scrabble score,
given in decimal, and `comment` is optional, purely descriptive, and ignored
by translation tools such as this one.

Thus, the Wottasquare token `[5]` could be translated to any word which has
a Scrabble score of 5, such as `slug`, for use in Beatnik.

By default, `wottasquare.py` looks in `/usr/share/dict/words` for
words to use when translating Wottasquare to Beatnik.  A different dictionary
file can be specified with the `--dictionary` command-line argument.  Note
that the dictionary file is parsed like a Beatnik source file would be;
punctuation is ignored (and treated as word seperator), etc.

There are two flags which trigger special behaviour:

    wottasquare.py --find 'number-or-word'

Shows the Scrabble score of the given word (or treats the given argument as
a Scrabble score, if it is numeric,) then dumps, to standard output, 20 words
chosen from the dictionary file which have the same Scrabble score as the given
word.  Examples:

    $ wottasquare.py --find chase
    10
    cubits badger gourmet pointers militant acumen engorges rehab fulled bibles bonny wantons motored blasters colossus warder howl colonial mainline frailer

    $ wottasquare.py --find 5
    5
    nip rode sitar lisle stilt uteri slug stain stool earls terns cot liter stout lob lab trots lotus altos boo

The flag `--find-all` works similarly, but dumps _all_ words from the dictionary
with the given Scrabble score to standard output.

make-wottasquare-print.py
-------------------------

Takes a string on the command line and writes, to standard output, a
Wottasquare program which, when run, prints that string.  It does not produce
the most efficient such program.

This tool was used to generate `eg/hello-world.wottasquare`, which was then
translated to Beatnik by `wottasquare.py`, which was then manually formatted
and punctuated, with some (maybe 3%) words "adjusted" to make it flow better.

License
-------

The contents of this repository are in the public domain.  See the file
UNLICENSE in this directory for more information.

[Beatnik]: http://esolangs.org/wiki/Beatnik
[wimpmode]: http://esolangs.org/wiki/Wimpmode
