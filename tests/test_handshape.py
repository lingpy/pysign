# -*- coding: utf-8 -*-
"""
Two alternatives for matching handshape symbols.
"""
import re
from pysign.parse import translate

def find_handshape(string, handshape_base="", handshape_diacritic=""):
    """
    Alternative version without re.
    """
    in_handshape = False
    handshapes = []
    rest = ''
    for char in string:
        if char in handshape_base:
            if in_handshape:
                handshapes[-1] += char # append to existing handshape
            else:
                in_handshape = True # switch on environment of handshape
                handshapes += [char] # append a new segment to the list
        elif char in handshape_diacritic: 
            if in_handshape:
                handshapes[-1] += char
        else:
            in_handshape = False
            rest += char
    return {'handshape': handshapes, "rest": rest}

# all handshapes in string
regex = r"[][]*"

# only dominant and non-dominant handshapes at start of sign
dom_nondom = r"(?<!)([][]*)"

# any handshape changes in sign
handshape_change = r"(?<=)([][]*)"

# see test_sign.py for target results
test_example_1 = "   "
test_example_2 = "    "
test_example_3 = "                 "
test_example_4 = "   " 

matches_1 = re.finditer(regex, test_example_1)

for matchNum, match in enumerate(matches_1, start=1):
    
    print ("Match {matchNum} was found at {start}-{end}: {match}".format(
        matchNum = matchNum, start = match.start(), end = match.end(), 
        match = match.group()))

for example in [test_example_1, test_example_2, test_example_3,
        test_example_4]:
    res = find_handshape(example)
    print('Found handshape at {0} / {1}'.format(
        res['handshape'],
        translate(res['handshape'])))


