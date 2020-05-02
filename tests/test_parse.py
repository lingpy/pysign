from pysign.parse import parse_hamnosys, ascify
from tabulate import tabulate

strings = ["   ", "   ", 
        "   ", "   ",
        "   ",
        ]

for string in strings:
    data = parse_hamnosys(string, ascify_text=False)
    table = [
            [
            'handshape', 
            'dominant', 
            'shape', 
            data['handshape']['dominant']['shape'],
            ascify(data['handshape']['dominant']['shape'])],
            [
            'handshape', 
            'dominant', 
            'change', 
            data['handshape']['dominant']['change'],
            ascify(data['handshape']['dominant']['change'])],
            [
            'handshape', 
            'nonnondominant', 
            'shape', 
            data['handshape']['nondominant']['shape'],
            ascify(data['handshape']['nondominant']['shape'])],
            [
            'handshape', 
            'nondominant', 
            'change', 
            data['handshape']['nondominant']['change'],
            ascify(data['handshape']['nondominant']['change'])],
            ['errors', '', '', data['errors'][:2], ''],
            ['rest', '', '', data['rest'], ascify(data['rest'])[:30]]
            ]
    print(tabulate(table, tablefmt='pipe'))
    input()
