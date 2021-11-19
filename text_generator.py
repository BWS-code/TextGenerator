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


def get_corpus_stats(corp):
    total = len(corp)
    unique = len(set(corp))
    return f'Corpus statistics\nAll tokens: {total}\nUnique tokens: {unique}'


def get_token_by_ind(ind, tokens):
    if match(r'^-?\d+$', ind) is None:
        raise TypeError
    if int(ind) > len(tokens) - 1 or int(ind) < 0 and abs(int(ind)) > len(tokens):
        raise RangeError
    print(tokens[int(ind)])


def main():
    file = input()
    pattern = r'\S+'
    tokens = get_corpus(file, pattern)
    print(get_corpus_stats(tokens))
    while True:
        entry = input()
        if entry == 'exit':
            break
        try:
            get_token_by_ind(entry, tokens)
        except RangeError as err:
            print(err)
        except TypeError as err:
            print(err)

main()
