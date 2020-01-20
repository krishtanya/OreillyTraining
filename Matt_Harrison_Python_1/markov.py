'''
This is a docstring for the module.

>>> m = Markov('ab')
>>> m.predict('a')
b
### http://setosa.io/ev/markov-chains/
# https://www.gutenberg.org/files/1342/1342-0.txt
'''
import argparse
import random
import sys
import urllib.request as req


def fetch_url(url, fname):
    fin = req.urlopen(url)
    data = fin.read()
    with open(fname, mode='wb') as fout:
        fout.write(data)


def from_file(fname, size):
    with open(fname, encoding='utf8') as fin:
        txt = fin.read()
    return Markov(txt, size)


class Markov:
    def __init__(self, data, size=1):
        self.tables = []
        self.size = size
        for i in range(size):
            self.tables.append(get_table(data, size=i+1))


    def predict(self, txt):
        table = self.tables[len(txt) - 1]
        options = table.get(txt, {})
        if not options:
            raise KeyError(f'{txt} not found')
        possibles = []
        for key in options:
            count = options[key]
            for i in range(count):
                possibles.append(key)
        return random.choice(possibles)

    def lazy_predict(self, num_chars, start):
        res = [start]
        for i in range(num_chars):
            letter = self.predict(start)
            res.append(letter)
            start = ''.join(res[-self.size:])
        return ''.join(res)

    def repl(self):
        print("Welcome to REPL")
        print("Ctrl-C to exit")
        while True:
            try:
                txt = input('>')
            except KeyboardInterrupt:
                print('Goodbye!')
                break
            try:
                res = self.predict(txt)
            except KeyError:
                print('Data not found in training data')
            except IndexError:
                print("Too long. Try again!")
            else:
                print(res)


def get_table(txt, size=1):
    '''
    >>> get_table('ab')
    >>> {'a':{'b':1}}
    '''
    results = {}
    for i in range(len(txt)):
        chars = txt[i:i+size]
        try:
            out = txt[i+size]
        except IndexError:
            break

        char_dict = results.get(chars, {})
        char_dict.setdefault(out, 0)
        char_dict[out] += 1
        results[chars] = char_dict
    return results

def main(args):
    p = argparse.ArgumentParser()
    p.add_argument('-f', '--file', help='Input file')
    p.add_argument('-s', '--size', help='Markov size(default 1)',
                     default=1, type=int)
    opts = p.parse_args(args)
    if opts.file:
        m = from_file(opts.file, size=opts.size)
        m.repl()

if __name__ == '__main__':
    main(sys.argv[1:])
#Below code will output results to REPL
#    m = from_file('pp.txt', size=4)
#    m.repl()
#    m.lazy_predict(100, '')