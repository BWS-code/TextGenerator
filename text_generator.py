from nltk.tokenize import regexp_tokenize
from re import match
from collections import defaultdict, Counter
import random
from time import perf_counter


class RangeError(Exception):
    def __init__(self):
        self.message = "Index Error. Please input an integer that is in the range of the corpus."
        super().__init__(self.message)


class NonIntError(Exception):
    def __str__(self):
        return "Type Error. Please input an integer."


class NotInModelError(Exception):
    def __str__(self):
        return 'Key Error. The requested word is not in the model. Please input another word.'


class TextPredictor:
    def __init__(self, filename, pattern, sents, words, depth=3):
        self.filename = filename
        self.pattern = pattern
        self.tokens = None
        self.bigrams = None
        self.trigrams = None
        self.head_tails = None
        self.sents = sents
        self.words = words
        self.depth = depth

    def get_tokens(self):
        with open(self.filename, 'r', encoding="utf-8") as file:
            text = file.read()
        return regexp_tokenize(text, self.pattern)

    def get_bigrams(self):
        return [
            [self.tokens[i], self.tokens[i + 1]]
            for i in range(len(self.tokens) - 1)]

    def get_trigrams(self):
        return [
            [' '.join((self.tokens[i], self.tokens[i + 1])), self.tokens[i + 2]]
            for i in range(len(self.tokens) - 2)]

    def get_collection_stats(self, collection: list) -> 'string with # of elements in collection':
        """Get collection statistics"""
        if len(collection[0]) == 2:
            if len(collection[0].split()) == 2:
                return f'Number of trigrams: {len(collection)}' # collection is trigrams list
            return f'Number of bigrams: {len(collection)}'  # collection is bigrams list
        else:  # collection is tokens list
            total_tokens, unique_tokens = len(collection), len(set(collection))
            return f'Corpus statistics\nAll tokens: {total_tokens}\nUnique tokens: {unique_tokens}'

    def get_element_by_ind(self, ind: str, collection: list) -> 'string or list from collection':
        """Pull token or basis from collection by index"""
        if match(r'^-?\d+$', ind) is None:
            raise NonIntError
        if int(ind) > len(collection) - 1 or int(ind) < 0 and abs(int(ind)) > len(collection):
            raise RangeError
        if len(collection[0]) == 2:  # collection is basis list
            return f'Head: {collection[int(ind)][0]} Tail: {collection[int(ind)][1]}'
        else:  # collection is tokens list
            return collection[int(ind)]

    def get_head_tails(self):
        """Make dictionary with key head and value tails"""
        my_dict = defaultdict(list)
        if self.depth == 2:
            basis = self.get_bigrams()
        if self.depth == 3:
            basis = self.get_trigrams()
        for pair in basis:
            head, tail = pair[0], pair[1]
            my_dict[head].append(tail)
        return my_dict

    def get_head_stats(self):
        """Print all tails and their frequencies per head"""
        head = input()
        stats = f'Head: {head}'
        tails_freq = Counter(self.head_tails[head])
        longest_tail = max([tail for tail in tails_freq], key=len) or ''
        if not tails_freq:
            raise NotInModelError
        for tail_freq in tails_freq.most_common():
            tail, freq = tail_freq[0], tail_freq[1]
            space = ''.join(' ' for _ in range(len(longest_tail) - len(tail)))
            stats += f'\nTail: {tail}{space} Count: {freq}'
        return stats


    def get_sentences(self):
        """Make specified num of sentences with not less than specified num of words"""
        sentences = []
        starters = {el for el in self.head_tails.keys() if match(r'^[A-Z].*[^.?!]$', el.split()[0])}
        for head in [random.choice(list(starters)) for _ in range(n_sentences)]:
            sentence = [word for word in head.split()]
            while len(sentence) < self.words or sentence[-1][-1] not in '.?!':  # match(r'.+[.?!]$', sentence[-1]) is None
                tails_freq = Counter(self.head_tails[head])
                tails = [tail for tail in tails_freq]
                weights = [tails_freq[tail] for tail in tails]
                next_word = ''.join(random.choices(tails, weights))
                sentence.append(next_word)
                if self.depth == 2:
                    head = sentence[-1]
                if self.depth == 3:
                    head = ' '.join((sentence[-2], sentence[-1]))
            sentences.append(' '.join(sentence))
        return '\n'.join(sentences)

    def main(self):
        # start = perf_counter()
        self.tokens = self.get_tokens()
        self.head_tails = self.get_head_tails()
        result = self.get_sentences()
        print(result)
        # end = perf_counter()
        # print(end - start)

corpus = input()
tokenizer_pattern = r'\S+'
n_sentences, n_words = 10, 5

my_text_app = TextPredictor(corpus,
                            tokenizer_pattern,
                            n_sentences, n_words,
                            depth=3)
my_text_app.main()
