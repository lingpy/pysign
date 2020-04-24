from pathlib import Path
from csvw.dsv import UnicodeDictReader

def data_path(*path):
    return Path(__file__).parent.joinpath('data', *path)

with UnicodeDictReader(data_path('hamnosys.tsv'), delimiter="\t") as reader:
    HAMNOSYS = {}
    for row in reader:
        HAMNOSYS[eval(r'"\u'+row['Unicode']+'"')] = row

