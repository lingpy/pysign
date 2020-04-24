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
>>> from pysign.parse import translate
>>> print(translate( "    "))                                                                            
symmpar finger2 <> chest moveo
```


