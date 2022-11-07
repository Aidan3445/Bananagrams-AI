'''
A convenient, self-contained, 515 KB Scrabble dictionary module, ideal
for use in word games.

Functionality:

- Check if a word is in the dictionary.
- Enumerate all words in the dictionary.
- Determine what letters may appear after a given prefix.
- Determine what words can be formed by anagramming a set of letters.

Sample usage:

>>> import twlsimple
>>> twl.check('dog')
True
>>> twl.check('dgo')
False
>>> words = set(twl.iterator())
>>> len(words)
178691
>>> twl.children('dude')
['$', 'd', 'e', 's']
>>> list(twl.anagram('top'))
['op', 'opt', 'pot', 'to', 'top']

Provides a simple API using the TWL06 (official Scrabble tournament)
dictionary. Contains American English words that are between 2 and 15
characters long, inclusive. The dictionary contains 178691 words.

Implemented using a DAWG (Directed Acyclic Word Graph) packed in a
binary lookup table for a very small memory footprint, not only on
disk but also once loaded into RAM. In fact, this is the primary
benefit of this method over others - it is optimized for low memory
usage (not speed).

The data is stored in the Python module as a base-64 encoded,
zlib-compressed string.

Each record of the DAWG table is packed into a 32-bit integer.

MLLLLLLL IIIIIIII IIIIIIII IIIIIIII

M - More Flag
L - ASCII Letter (lowercase or '$')
I - Index (Pointer)

The helper method _get_record(index) will extract these three elements
into a Python tuple such as (True, 'a', 26).

All searches start at index 0 in the lookup table. Records are scanned
sequentially as long as the More flag is set. These records represent all
of the children of the current node in the DAWG. For example, the first
26 records are:

0 (True, 'a', 26)
1 (True, 'b', 25784)
2 (True, 'c', 11666)
3 (True, 'd', 39216)
4 (True, 'e', 33704)
5 (True, 'f', 50988)
6 (True, 'g', 46575)
7 (True, 'h', 60884)
8 (True, 'i', 56044)
9 (True, 'j', 67454)
10 (True, 'k', 65987)
11 (True, 'l', 76093)
12 (True, 'm', 68502)
13 (True, 'n', 83951)
14 (True, 'o', 79807)
15 (True, 'p', 89048)
16 (True, 'q', 88465)
17 (True, 'r', 113967)
18 (True, 's', 100429)
19 (True, 't', 125171)
20 (True, 'u', 119997)
21 (True, 'v', 134127)
22 (True, 'w', 131549)
23 (True, 'x', 136449)
24 (True, 'y', 136058)
25 (False, 'z', 136584)

The root node contains 26 children because there are words that start
with all 26 letters. Other nodes will have fewer children. For example,
if we jump to the node for the prefix 'b', we see:

25784 (True, 'a', 25795)
25785 (True, 'd', 28639)
25786 (True, 'e', 27322)
25787 (True, 'h', 29858)
25788 (True, 'i', 28641)
25789 (True, 'l', 29876)
25790 (True, 'o', 30623)
25791 (True, 'r', 31730)
25792 (True, 'u', 32759)
25793 (True, 'w', 33653)
25794 (False, 'y', 33654)

So the prefix 'b' may be followed only by these letters:

a, d, e, h, i, l, o, r, u, w, y

The helper method _get_child(index, letter) will return a new index
(or None if not found) when traversing an edge to a new node. For
example, _get_child(0, 'b') returns 25784.

The search is performed iteratively until the sentinel value, $, is
found. If this value is found, the string is a word in the dictionary.
If at any point during the search the appropriate child is not found,
the search fails - the string is not a word.

See also:

http://code.activestate.com/recipes/577835-self-contained-twl06-dictionary-module-500-kb/
http://en.wikipedia.org/wiki/Official_Tournament_and_Club_Word_List
http://www.isc.ro/lists/twl06.zip
'''

import base64
import collections
import itertools
import struct
import zlib


def check(word):
    '''
    Returns True if `word` exists in the TWL06 dictionary.
    Returns False otherwise.

    >>> twl.check('word')
    True
    >>> twl.check('asdf')
    False
    '''
    return word in _DAWG


def iterator():
    '''
    Returns an iterator that will yield all words stored in the
    dictionary in alphabetical order.

    Useful if you want to use this module simply as a method of
    loading words into another type of data structure. (After
    all, this Python module is significantly smaller than the
    original word list file - 500KB vs 1900KB.)

    >>> words = set(twl.iterator())
    >>> words = list(twl.iterator())
    '''
    return iter(_DAWG)


def children(prefix):
    '''
    Returns a list of letters that may appear after `prefix`.
    '''
    return _DAWG.children(prefix)


def anagram(letters):
    '''
    Yields words that can be formed with some or all of the
    given `letters`. `letters` may include '?' characters as
    a wildcard.
    '''
    for word in _DAWG.anagram(letters):
        yield word


END = '$'
WILD = '?'


class _Dawg(object):
    def __init__(self, data):
        data = base64.b64decode(data)
        data = zlib.decompress(data)
        self.data = data

    def _get_record(self, index):
        a = index * 4
        b = index * 4 + 4
        x = struct.unpack('<I', self.data[a:b])[0]
        more = bool(x & 0x80000000)
        letter = chr((x >> 24) & 0x7f)
        link = int(x & 0xffffff)
        return (more, letter, link)

    def _get_child(self, index, letter):
        while True:
            more, other, link = self._get_record(index)
            if other == letter:
                return link
            if not more:
                return None
            index += 1

    def _get_children(self, index):
        result = []
        while True:
            more, letter, link = self._get_record(index)
            result.append(letter)
            if not more:
                break
            index += 1
        return result

    def _anagram(self, bag, index=0, letters=None):
        letters = letters or []
        while True:
            more, letter, link = self._get_record(index)
            if letter == END:
                yield ''.join(letters)
            elif bag[letter]:
                bag[letter] -= 1
                letters.append(letter)
                for word in self._anagram(bag, link, letters):
                    yield word
                letters.pop(-1)
                bag[letter] += 1
            elif bag[WILD]:
                bag[WILD] -= 1
                letters.append(letter)
                for word in self._anagram(bag, link, letters):
                    yield word
                letters.pop(-1)
                bag[WILD] += 1
            if not more:
                break
            index += 1

    def __contains__(self, word):
        index = 0
        for letter in itertools.chain(word, END):
            index = self._get_child(index, letter)
            if index is None:
                return False
        return True

    def __iter__(self, index=0, letters=None):
        letters = letters or []
        while True:
            more, letter, link = self._get_record(index)
            if letter == END:
                yield ''.join(letters)
            else:
                letters.append(letter)
                for word in self.__iter__(link, letters):
                    yield word
                letters.pop(-1)
            if not more:
                break
            index += 1

    def children(self, prefix):
        index = 0
        for letter in prefix:
            index = self._get_child(index, letter)
            if index in (0, None):
                return []
        return self._get_children(index)

    def anagram(self, letters):
        bag = collections.defaultdict(int)
        for letter in letters:
            bag[letter] += 1
        for word in self._anagram(bag):
            yield word


_DAWG = _Dawg(
    "eJxlnFGu4zqSpld07yDvDhpTaKBrUNMPVeh+NGSLlpWWRF2JtFP5NNuY7c1K5v"
    "/+oHyyUDiH8YdoiiIpMhgMBtV1127p89Ig9d11nMZydNcpdddci8hL3JY7/bSn5ZYMit"
    "/zVEs6cTrgtmt3rXvqbl2f5vHW3W4kFV1PSr7i9l107OPXwOmLU2a3W57n3HdlVOG4WLvFsVs/LsOlZPjq24HLPW9i69aVdKJzcWkeY3qdMPuZY9"
    "/dnkt+T6kfUndRHisF+7OOm2DLlE/J4ull5G4oWQppoFvhiWVzVUql+FCl6PWnmvbCfnQOJ07iLr72bbqoa1Aq1Kc"
    "/K8VvSE7f666M5nGLdoBLUEVmHlEnkVfHWwnojaUbiFBN62ZmK0HHPX0YN0S7UJOKHZ0Nae73Ts"
    "+835MawZSn39XGfXffOjXevaTNZMn8Iubdbf3eDd24mOwuw6ACDeo0B1QxA/WmNYfciU8mLshDjybjcebJ43Yje"
    "+GaN7rGNpsoO4DiTrf8yFMDdbWJbCdFTCOppvw2oV9M02Ubh0d0rGnOKtukvg4ZTHb1OzFV962P7prKieT7K8"
    "/9tKhgz91EI0CWzl3kiyVdeeQ6PIR5SOVBynd37N3v8+/d3P1MJj2U2szX6CHztU5"
    "+nTNlm93DTekgM50Z0kO5TV3qUJxh3HXjSFsufbcMeuAyqE8vwzaqOAKRkWZcnkQvKua2d8QuesCNqOyLQ/kDfsBCzzYlk"
    "+yKLPsbWsbfILdxpdcuP8akYSHIdW/ALfxfcw"
    "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"
    "/R/05Wit5mQzOn13T1HbAG7nrk"
    "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"
    "+m7pB9tuhdzSZHHd1zcTCji9yoB99eq5HVe/yp1"
    "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"
    "+S36hFVjPvxVNn"
    "+SCiesIL0ojqday5n4ZlXmwX9aIUVELwXnJ0ixTeVe0CUT5GA2U9gUJTlhQr7Ze7NCpZKMMImaw8VPK2EN3vdjwBHA1qkPygNpwQelZ40HddOCF"
    "jPm1JoPktXzMVYJDbnFkwQTwpPZgsCH4XZEIgcXCWpFKPYEGGuES/mF5XtvkzsSoF"
    "+mJx5CxCKzx5lPkjUg1oLBPj67V1tjzEoBjhx8ZgdHl6FdcMeibLfdqsduV4OolBRJhRpqxPhD"
    "/+44ggfEnUZ4cH5nf4649zbQs9jJN9H70ctRUKM/D3+NDKIXj8Vgx2tq93bw3jaFhUohMb/Th9iOPHbs2yLKYu4kUmc6CDtL+5yfJtRm1rt"
    "+BNUt7D7si3LIe+5Wf8xsCqofhchd+lBW"
    "/1Ig8l74FNieJY3xEsfupOLtbQ707L5zLq8FbPW7PdreAJ5seCuw8DEzsmeGt9tDss1o5WDB03PPoLUECTY6JOoCfUfdcHc/y+pBzQJ7s"
    "/n1YZK2Zcc+urP237Hhmaiwa"
    "/sAUzB1bYd4GiCkz1M9ZhDfDVtckjRekZqQyGCaTKgSXlb7yjsTUXLmfVGVZpToDYpk4Mjtvk5EiTgbWnTl60qiebGFU0Rh05hYWRoEjdKjJOys"
    "e9LOsudnHDWCahxyZDUONxZNhLYvm3C6sZyOqY07ApHapTmlBlPXE9uPDv46XzHxkA+mthjfU+K0EzrUHmokUB0rYV06HnlYTzAT7i/hZTUdRtM"
    "JMoskOI2I4kPfgIrCNYIDEgUY7TYdWOPXA6ebuwk3Mtws6QpNQ8dmV10vtNjDUuLPuiibi3bqFMFvScs/hh7oo97LkBqQaawLwyFx4NqF3hDU6O"
    "eDuqS/jRpUHQfNkmeikwZ1NuPTeqpHadkaXU1SUG7NTpX9K84URzieVSu5dUBU8blAmr5qQQtVkkojaO2vHA6lqN6QEoRS3hgseb+wypoLu7rt"
    "9YZtyKCaBCDKPhypVamqNq19zzk/KLHsLgWlTvU86/nFkUhLPRHatQG9Rqt0gvu1kA9UgZRj3nEU0BtiQ1+3zrzxuvyd0xGKtEV9M4bXgli6Tv"
    "VmUgPu814S9r3dhpCdw0o0yMaWrACL2gf7xrgeJ+ebYtJrGD9/2J3POxxfFN2nep0DqAmoaTAaHfGt1v0ttc+EHN7ofW9vSgvU8d90LnzYTJxk"
    "nAlz48EL9uH9HTF0OFMP2jdfKFn2Y74qxYEP7IOvujb22Bljs9s9CB+snPwhALwB7BzA6DWDKDHDdFiarwqgBwW2S3971z4rpZueOFKoowl1ua"
    "K6DjxnV4QeXrof+h+LDyHfHiYc3LMrzYBYKHiOfzP9o8Qno/ioFd8cmoKRWDTjjxRyltc7Hz7U64UbjpelabTx7UlrGecHZSSKPt+WKXFYNg7M"
    "3o521o9Yn0zFWYDFD/ptwwMhyPE/HPgJT5Pd9HLYsb9ESPY32HySeTPZcYwhEDfHziJO7QqZw5/JiW1GgeE4qN7Bw6YuA+unwre/mGc910KeJq"
    "H3mz3j1QInXrq9sd7Qh1PDSpnsIZIeQOzOn2gOPccMCXA79/ruRIrVrqEAa7MvLFjKetMSlJwDXUrEqdaM/jVyMrgmPsXBUtZ90pzj63z9x0O6"
    "QU+s3TGffOayPyjt6I6IXC+hUTE5+ON0BPd629sVr2RrtMfYjASlHQQQUjqOGZdcMg/K6TRoFk3oqfhDq/pt9ucnCxvh6oSS3BXq5"
    "/PlpSKFTMMVeGgeKmyn6Ta+mWyXo5IlXYtrzoE2jlOqf2V/r6Bw5B2ieA3BfPAFowR5Fo7lQCgmgFz9MMr9i524DZHsac4kblp2ie5"
    "/Rs2PZjCnnUxkvOyxRRyshOy/MmfStfjATtCJrHn5m523yCBh3VPnwFcMghrObPlkLsTE4aG++WMPwO5JuPK72narVEhvXURNqmHjrx2W"
    "+KBPqdf0D2kkvLGq1sdcwad9+A7hEiLt/EKlGdzvzCArjBHvrLawa5ix1DfXbqjrP"
    "/6r6P1ohAEvvrAaa0kzR3lLWSy4Wb95oxD1r3dmS1fBdQxQfQ6P94tKHKf++3bVDkNXTUY4KOFhd6Ji5uuGu261obguX5+fr+c3Fivf5KvLL9"
    "+Hq1+fAavL10etsCBtJnGUyqy/L2vOCuMXx9dAuHgzcwUnSS0mf9Xg5Hjnv9Tkw6n8C8ebg"
    "/rK7iBU8Yt1fDuXWX3WSTD6COnyOauBb7aqysSAOwnBDI/zJ8BTw7HobnyoK37Qb92DX5OoVLSgPAWPWFG8P+k+zdWqLucec/3FPF/j9IB"
    "+/dKYOD1DjARPXdTM3Qlk/g4f7w+juLWuKj7OBpgpyhfxV1dWf8+aDmsdfES3QToEld5x7ZaqOZagsu14rPm/v3wz"
    "/cO0MI4o3G5fLgYVJnk93AWM4r262JXhnED"
    "/wjFEUVOloiCW8Ve3jS0NLqKm5QD0AIHYvbzSEKL2lR7jLT6vUcPUOsYX0ej3fObgNXYvLLgzNHPdJ3z13i81jxY7rzHbBhBYGqikmpGiyOpBO/P"
    "+9Zz+ocUkbxxJmF751vHNeeXOpzGx6s7+XtFbD3h3GpgiDvTop6KmJ0GtD/icJUiLTxNB47qL/r+waNb/TCgPqNNtfHFmcQ77g+A5DKbFIXACyX1"
    "/+K6dMkmXM4lfGhO7by7gC1vKO2nEPQmoBG8fxBNVR2IkEuKBcQzv/m4f4XyHf"
    "/w7XfWPiePNl4KW4b9xIURoSgF9EjTggEkRnJvzyTxJOfyV0EwJFw"
    "+htzQYgqTFW80ixYfAq35zpk9kIbSILcwA3W6IOBdI3eRhr18R3GaA4iuV0UfZInUmLs8KfKfleGNZGrFmi6oFxrsup55AlAoao"
    "+wz2BrjRhs1BrG4mv4BzW9Rm/rePmn0ju94v71P/5ZugIuYgg/U+tNDW/f2ObelHZkVOG9s9"
    "+/sPmKqkffOuSeoQaQQvPPW42VJINHm7ibwa8rbxK+MMOAwiQQ75wexBAKkVEkw3r19XvTbOzYD3pqGCZj83qgUbz7TYOJZMDh"
    "/Gcnf2INGUjTfNyvQdyxDD0mZo3svR+oefF3o8HcbjrQffuvqM4cEQK76XwaRjbAf4Tl3t0L8M235p7Sj/w/wYqdc "
)
