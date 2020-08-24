# pysl: Python library for the manipulation of sign language data

## Installation

```
$ git clone https://github.com/lingpy/pysign.git
$ cd pysign
$ pip install -e ./
```

## First test
Unknown symbols (according to potentially missing information) are shown in `<SYMBOL>`.

```python
>>> from pysign.parse import parse_hamnosys
>>> print(parse_hamnosys( "    "))                                                                            
{'symmetry': ['\ue0e8'], 'initial position': [], 'dominant': {'shape': ['\ue002', ''], 'orientation': ['\ue020\ue038', ''], 'location': ['\ue052', ''], 'contact': ['', ''], 'movement': ['\ue089', ''], 'repetition': [''], 'is_dominant': True}, 'nondominant': {'shape': ['', ''], 'orientation': ['', ''], 'location': ['', ''], 'contact': [], 'movement': ['', ''], 'is_dominant': False}, 'meta': {'handshape': [], 'orientation': [], 'contact': [], 'location': [], 'movement': [], 'rest': '    '}}
```


