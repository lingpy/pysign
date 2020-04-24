"""
Module for parsing segmented HamNoSys transcriptions.
"""
from pysign.data import HAMNOSYS

def translate(text, sep='.'):
    return '.'.join(
            HAMNOSYS.get(char, {"Name": '<'+char+'>'})["Name"] for char in
            text).replace('.asciispace.', ' ')


class Word(object):
    
    def __init__(self, text, delimiter=' + '):
        self.signs = [Sign(sign) for sign in text.split(delimiter)]


class Sign(object):

    def __init__(self, text, delimiter=None):
        
        segments = text.split(delimiter)
        data = {}
        for i, segment in enumerate(segments):
            pass


