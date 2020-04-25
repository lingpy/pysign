#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re

regex = r"[][]*"

test_str = ""

matches = re.finditer(regex, test_str)

for matchNum, match in enumerate(matches, start=1):
    
    print ("Match {matchNum} was found at {start}-{end}: {match}".format(
        matchNum = matchNum, start = match.start(), end = match.end(), 
        match = match.group()))
    
