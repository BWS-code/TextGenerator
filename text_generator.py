from nltk.tokenize import regexp_tokenize
from re import match


class RangeError(Exception):
    def __init__(self):
        self.message = "Index Error. Please input an integer that is in the range of the corpus."
        super().__init__(self.message)


class TypeError(Exception):
    def __str__(self):
        return "Type Error. Please input an integer."


def get_corpus(filename, pattern):
    with open(filename, 'r', encoding="utf-8") as file:
        text = file.read()
    return regexp_tokenize(text, pattern)


def get_bigrams(tokens):
    return [[tokens[i], tokens[i + 1]] for i in range(len(tokens) - 1)]


def get_bigrams_stats(bigrams):
    return f'Number of bigrams: {len(bigrams)}'


def get_corpus_stats(corp):
    total = len(corp)
    unique = len(set(corp))
    return f'Corpus statistics\nAll tokens: {total}\nUnique tokens: {unique}'


def get_element_by_ind(ind, what):
    if match(r'^-?\d+$', ind) is None:
        raise TypeError
    if int(ind) > len(what) - 1 or int(ind) < 0 and abs(int(ind)) > len(what):
        raise RangeError
    if len(what[0]) == 1:  # element is tokens list
        print(what[int(ind)])
    if len(what[0]) == 2:  # element is bigram list
        print(f'Head: {what[int(ind)][0]} Tail: {what[int(ind)][1]}')


def main():
    file = input()
    pattern = r'\S+'
    tokens = get_corpus(file, pattern)
    bigrams = get_bigrams(tokens)
    print(get_bigrams_stats(bigrams))
    while True:
        entry = input()
        if entry == 'exit':
            break
        try:
            get_element_by_ind(entry, bigrams)
        except RangeError as err:
            print(err)
        except TypeError as err:
            print(err)


main()
