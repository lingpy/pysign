from pysign.parse import parse_hamnosys, ascify, Sign
from tabulate import tabulate

strings = [
        "   ", # simple, one hand
        "   ", # two hands, no symmetry
        "   ", # two hands, simultaneous movement with complex bracketing
        "    ", # one hand, beginning and ending locations with contact
        "   ", # contact and repetition 
        "   ", # one hand, simultaneous movement
        "    " # detailed initial position, two contacts
          ]

for string in strings:
    sign = Sign.from_text(string)
    sign.pprint()
    input()
