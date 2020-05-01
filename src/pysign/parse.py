"""
Module for parsing segmented HamNoSys transcriptions.
"""
from pysign.data import HAMNOSYS

def ascify(text, sep='.'):
    return '.'.join(
            HAMNOSYS.get(char, {"Name": '<'+char+'>'})["Name"] for char in
            text).replace('.asciispace.', ' ')


def parse_hamnosys(
        text,
        handshape_base="",
        handshape_diacritic="",
        nondominant="",
        ascify_text=False
        ):
    # handshapes
    in_handshape, handshapes = False, []
    # unparsable parts
    unparsable, rest = [], ''
    for i, char in enumerate(text):
        if char in handshape_base:
            if in_handshape:
                handshapes[-1] += char
            else:
                in_handshape = True
                handshapes += [char]
        elif char in handshape_diacritic:
            if in_handshape:
                handshapes[-1] += char
            else:
                unparsable += [(i, char, 'not in handshape')]
                rest += char
        elif char == nondominant:
            # handshape starts anew now
            in_handshape = False
            handshapes += [char]
        else:
            in_handshape = False
            rest += char

    # determine dominant hands
    if nondominant in handshapes:
        dominant_hand = handshapes[0]
        nondominant_hand = ''.join(handshapes[2])
        handshape_change = ''.join(handshapes[3:])
    # only one hand
    else:
        dominant_hand = handshapes[0]
        nondominant_hand = ''
        handshape_change = ''.join(handshapes[1:])
    
    if not ascify_text:
        data = {
                'handshape': {
                    'dominant': {
                        'shape': dominant_hand,
                        'change': handshape_change
                        },
                    'nondominant': {
                        'shape': nondominant_hand,
                        'change': '' # is this never annotated?
                        }
                    },
                'errors': unparsable,
                'rest': rest
               }
    else:
        data = {
                'handshape': {
                    'dominant': {
                        'shape': ascify(dominant_hand),
                        'change': ascify(handshape_change)
                        },
                    'nondominant': {
                        'shape': ascify(nondominant_hand),
                        'change': '' # is this never annotated?
                        }
                    },
                'errors': unparsable,
                'rest': ascify(rest)
               }
    return data

class Word(object):
    
    def __init__(self, text, delimiter=' + '):
        self.signs = [Sign(sign) for sign in text.split(delimiter)]


class Sign(object):

    def __init__(self, text, delimiter=None):
        
        segments = text.split(delimiter)
        data = {}
        for i, segment in enumerate(segments):
            pass


