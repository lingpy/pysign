# -*- coding: utf-8 -*-
"""
Two alternatives for matching handshape symbols.
"""
import re
#from pysign.parse import translate

def find_handshape(string, handshape_base="", 
                   handshape_diacritic="",
                   dom_nondom=""):
    """
    function for identifying handshape symbols
    """
    in_handshape = False
    handshapes = []
    nondominant = []
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
        elif char in dom_nondom: # to catch the nondominant handshapes
            if in_handshape:
                in_handshape = False # nondominant handshape should be new item in handshapes list
                nondominant += char
        else:
            in_handshape = False
            rest += char

    handshape_change = ''
    nondominant_hand = ''
    if "" in nondominant: # if true, we know that the second item is nondominant
        dominant_hand = handshapes[0]
        nondominant_hand = handshapes[1]
        handshape_change = handshapes[2:] # there may be multiple changes; typically 1 or 2 per morpheme
    elif len(handshapes) > 1:
        dominant_hand = handshapes[0]
        handshape_change = handshapes[1:]      
    else:
        dominant_hand = handshapes[0]
    
    return {'handshapes' : handshapes,
            'dominant hand' : dominant_hand,
            'non-dominant hand' : nondominant_hand,
            'handshape change(s)' : handshape_change,
            "rest" : rest}

### Tests: see test_sign.py
# Example (1) most simple full sign transcription: 
# one dominant hand, one orientation (must have two symbols), one location,
# one movement

{
"   ": # segmented into types
    {
    "symmetry": "",
    "dominant_hand": "", # hamfinger2, '\ue002'
    "nondominant_hand": "",
    "handshape_change": "",
    "dominant_orientation": "", # hamextfingeru,hampalmu
    "nondominant_orientation": "",
    "dominant_location": "", # hamchest
    "nondominant_location": "",
    "dominant_movement": "", # hammoveo
    "nondominant_movement": ""
    }
}

#1
find_handshape("   ")

#1 returns
{'handshapes': ['\ue002'],
 'dominant hand': '\ue002',
 'non-dominant hand': '',
 'handshape change(s)': '',
 'rest': ' \ue020\ue038 \ue052 \ue089'}


# Example (3) two-handed sign completely asymmetrical: 
# one dominant hand, one nondominant hand; orientations, locations,  
# and movements for each hand

{
 "               ":
     {
      "symmetry": "",
      "dominant_hand": "", # hamfinger2, \ue002
      "nondominant_hand": "", # hamflathand, \ue001
      "handshape_change": "",
      "dominant_orientation": "", # hamextfingeru,hampalml
      "nondominant_orientation": "", # hamextfingero,hampalmd
      "dominant_location": "", # hamshoulders,hamlrat (sequence matters!)
      "nondominant_location": "", # hamlrat,hamchest (sequence matters!)
      "dominant_movement": "", # hammovedo
      "nondominant_movement": "" # hamnomotion
      }
 }

#3
find_handshape("               ")

#3 returns
{'handshapes': ['\ue002', '\ue001'],
 'dominant hand': '\ue002',
 'non-dominant hand': '\ue001',
 'handshape change(s)': [],
 'rest': '\ue0e2  \ue0e3 \ue0e2 \ue020\ue03e  \ue029\ue03c \ue0e3\ue0e2 \ue051\ue059  \ue059\ue052 \ue0e3\ue0e2 \ue090  \ue0af \ue0e3'}

# Example (4) one-handed sign with handshape change: 
# one dominant hand and handshape change; no orientation provided,
# two locations, and movement as handshape change

{
 "   ":
    {"symmetry": "",
      "dominant_hand": "", # \ue002\ue00d
      "nondominant_hand": "",
      "handshape_change": "", # \ue002\ue010\ue00d
      "dominant_orientation": "",
      "nondominant_orientation": "",
      "dominant_location": ["", ""], # beginning and ending locations
      "nondominant_location": "",
      "dominant_movement": "",
      "nondominant_movement": ""
    }
}

#4
find_handshape("   ")

#4 returns
{'handshapes': ['\ue002\ue00d', '\ue002\ue010\ue00d'],
 'dominant hand': '\ue002\ue00d',
 'non-dominant hand': '',
 'handshape change(s)': ['\ue002\ue010\ue00d'],
 'rest': ' \ue04a\ue0d0\ue067 \ue0aa \ue0d6\ue04a\ue0d1\ue067'}

# Example (5) two-handed sign with handshape change: 
# one dominant hand, one nondominant, and handshape change; no orientation provided,
# two locations, and movement as handshape change

{
 "   ":
    {"symmetry": "",
      "dominant_hand": "", # \ue002\ue00d
      "nondominant_hand": "", # \ue005\ue00c
      "handshape_change": "", # \ue002\ue010\ue00d
      "dominant_orientation": "",
      "nondominant_orientation": "",
      "dominant_location": ["", ""], # beginning and ending locations
      "nondominant_location": "",
      "dominant_movement": "",
      "nondominant_movement": ""
    }
}

#5
find_handshape("   ")

#5 returns
{'handshapes': ['\ue002\ue00d', '\ue005\ue00c', '\ue002\ue010\ue00d'],
 'dominant hand': '\ue002\ue00d',
 'non-dominant hand': '\ue005\ue00c',
 'handshape change(s)': ['\ue002\ue010\ue00d'],
 'rest': ' \ue04a\ue0d0\ue067 \ue0aa \ue0d6\ue04a\ue0d1\ue067'}


def find_handshape_old(string, handshape_base="", handshape_diacritic=""): # updated function above
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


