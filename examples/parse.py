from pysign.parse import parse_hamnosys, ascify, Sign
from tabulate import tabulate

strings = ["   ", "   ", 
        "   ", "    ",
        "    "
        ]

for string in strings:
    sign = Sign.from_text(string)
    sign.pprint()
    input()
