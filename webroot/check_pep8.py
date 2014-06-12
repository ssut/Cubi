#!/usr/bin/env python
import os
import sys

import pep8

class Writer:
    def __init__(self, exclude=[], stdout=None):
        self.content = []
        self.exclude = exclude
        self.stdout = stdout

    def write(self, text):
        text = text.replace("\n", "")
        if text == '':
            return
        for ex in self.exclude:
            if ex in text:
                return

        self.content.append(text)

exclude = [
    'E226',
    'E302',
    'E41',
    'registration/',
]

stdout = sys.stdout
sys.stdout = Writer(exclude=exclude, stdout=stdout)

guide = pep8.StyleGuide()

search_dir = [
    os.path.dirname(os.path.realpath(__file__))
]
guide.check_files(search_dir)

print >> stdout, "-" * 57
print >> stdout, "<<%20s PEP8 REPORT %20s>>" % ("", "", )
print >> stdout, "-" * 57
print >> stdout, " TOTAL ERROR COUNT: {0}".format(
    len(sys.stdout.content))
print >> stdout, "-" * 57

for c in sys.stdout.content:
    c = c.replace(search_dir[0], "")
    print >> stdout, c
