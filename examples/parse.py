from pysign.parse import parse_hamnosys, ascify, Sign
from tabulate import tabulate
from itertools import combinations

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

for string1, string2 in combinations(strings, r=2):
    sign1 = Sign.from_text(string1)
    sign2 = Sign.from_text(string2)
    
    sign1.pprint()
    sign2.pprint()
    print(sign1.dominant.distance(sign1.dominant))
    print(sign1.dominant.distance(sign2.dominant))
    input()
