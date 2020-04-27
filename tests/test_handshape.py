# -*- coding: utf-8 -*-
"""
Regex for matching handshape symbols.
"""
import re

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
