"""
Module for parsing segmented HamNoSys transcriptions.
"""
from pysign.data import HAMNOSYS

def translate(text):
    return ' '.join(
            HAMNOSYS.get(char, {"Name": '<'+char+'>'})["Name"] for char in
            text.split())


class Word(object):
    
    def __init__(self, text, delimiter=' + '):
        self.signs = [Sign(sign) for sign in text.split(delimiter)]


class Sign(object):

    def __init__(self, text, delimiter=None):
        
        segments = text.split(delimiter)
        data = {}
        for i, segment in enumerate(segments):
            pass


