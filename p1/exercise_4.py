import sys
from pprint import pprint
import os
import pickle
from collections import defaultdict


SENTENCES = [
    "Judyta dała wczoraj Stefanowi czekoladki.",
    "Babuleńka miała dwa rogate koziołki.",
    "Wczoraj wieczorem spotkałem pewną piękną kobietę",
    "To, że milczę, nie znaczy, że nie mam nic do powiedzenia.",
    "Na litość boską, królowo",  # – zachrypiał –
    "Czy ośmieliłbym się nalać damie wódki?",
    "To czysty spirytus.",
    # "A jeśli pewnego dnia będę musiał odejść? - spytał Krzyś, ściskając Misiową łapkę.",
    # "Wyniki wyborów samorządowych 2018 to coś, na co czeka każdy wyborca.",
]


def tokenize(line):
    for c in "!?,.":
        line = line.replace(c, " %s " % c)
    return line.lower().split()


class NGrams:
    def __init__(self, n3_grams_filename):
        self.n3_grams = defaultdict(int)
        self.n3_count = 0
        self.n2_grams = defaultdict(int)
        self.n2_count = 0
        self.n1_grams = defaultdict(int)
        self.n1_count = 0

            get_filtered_N_grams(n3_grams_file_obj)
            N3 = sum(n3_grams.values())
            N2 = sum(n2_grams.values())
            N1 = sum(n1_grams.values())

    def read_or_generate_N_grams(self, n3_grams_filename, sentences=SENTENCES):
        pickled_ngrams_filename = "filtered_n_grams.pickle"
        words = set(token for sentence in sentences for token in tokenize(sentence))
        words.add("<EOS>")
        words.add("<BOS>")
        # # Try to load pickled data
        # if os.path.isfile(pickled_ngrams_filename):
        #     with open(pickled_ngrams_filename, "rb") as pickled_ngrams_file_obj:
        #         n3_grams, n2_grams, n1_grams, filter_words = pickle.load(
        #             pickled_ngrams_file_obj
        #         )
        #     # Make sure we didn't change the set of the "words"
        #     if filter_words == words:
        #         import pprint

        #         pprint.pprint(n3_grams)
        #         return n3_grams, n2_grams, n1_grams
        # Read and filter n*_grams
        generate_N_grams(n3_grams_filename, words)
        with open(pickled_ngrams_filename, "wb") as pickled_ngrams_file_obj:
            data = self.n3_grams, self.n2_grams, self.n1_grams, words
            pickle.dump(data, pickled_ngrams_file_obj)
        return n3_grams, n2_grams, n1_grams

    def generate_N_grams(self, n3_grams_filename, words):
        with open(n3_grams_filename, "rb") as n3_grams_file_obj:
            # Read the first line
            line = n3_grams_file_obj.readline()
            while line:
                try:
                    count, word1, word2, word3 = line.split()
                except ValueError:
                    word3 = None
                    count, word1, word2 = line.split()
                self.n1_grams[word1] += 1
                self.n1_grams[word2] += 1
                self.n2_grams[" ".join((word1, word2))] += 1
                if word3:
                    self.n1_grams[word3] += 2
                    self.n2_grams[" ".join((word2, word3))] += 1
                    self.n3_grams[" ".join((word1, word2, word3))] += 1
                # Read the next line
                line = n3_grams_file_obj.readline()
            # Update total counts
            self.n3_count = sum(self.n3_grams.values())
            self.n2_count = sum(self.n2_grams.values())
            self.n1_count = sum(self.n1_grams.values())

    def generate_filtered_N_grams(self, n3_grams_filename, words):
        with open(n3_grams_filename, "rb") as n3_grams_file_obj:
            # Read the first line
            line = n3_grams_file_obj.readline()
            while line:
                try:
                    count, word1, word2, word3 = line.split()
                except ValueError:
                    word3 = ""
                    count, word1, word2 = line.split()
                word1_in = word1 in words
                word2_in = word2 in words
                word3_in = word3 in words
                if word1_in:
                    self.n1_grams[word1] += 1
                    if word2_in:
                        self.n2_grams[" ".join((word1, word2))] += 1
                if word2_in:
                    self.n1_grams[word2] += 1
                    if word3_in:
                        self.n2_grams[" ".join((word2, word3))] += 1
                if word3_in:
                    self.n1_grams[word3] += 2
                    if word1_in and word2_in:
                        self.n3_grams[" ".join((word1, word2, word3))] += 1
                # Read the next line
                line = n3_grams_file_obj.readline()
            # Update total counts
            self.n3_count = sum(self.n3_grams.values())
            self.n2_count = sum(self.n2_grams.values())
            self.n1_count = sum(self.n1_grams.values())

    def generate_best_sentences(self, words):
        pass


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python exercise_4.py 3-grams")
        exit(0)
    n3_grams_filename = sys.argv[1]
    n_grams = NGrams(n3_grams_filename)
    for sentence in SENTENCES:
        print('Sentence: "{sentence}"'.format(sentence=sentence))
        words = tokenize(sentence)
        n_grams.generate_best_sentences(words)
