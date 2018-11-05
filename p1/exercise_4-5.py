import os
import pickle
import sys
from collections import defaultdict
from itertools import permutations
from math import log

SENTENCES = [
    "Judyta dała wczoraj Stefanowi czekoladki.",
    "Babuleńka miała dwa rogate koziołki.",
    "Wczoraj wieczorem spotkałem pewną piękną kobietę",
    # Examples
    "To, że milczę, nie znaczy,",
    "że nie mam nic do powiedzenia.",
    "Na litość boską, królowo",
    "Czy ośmieliłbym się nalać damie wódki?",
    "To czysty spirytus.",
    "A jeśli pewnego dnia będę musiał odejść?",
    "- spytał Krzyś, ściskając Misiową łapkę.",
    "Wyniki wyborów samorządowych 2018",
    "to coś, na co czeka każdy wyborca.",
]


def tokenize(line):
    for c in "!?,.":
        line = line.replace(c, " %s " % c)
    return line.lower().split()


class NGrams:
    LAMBDA_N1 = 0.03
    LAMBDA_N2 = 0.11
    LAMBDA_N3 = 0.86

    def __init__(self, n3_grams_filename):
        self.n3_grams = defaultdict(int)
        self.n3_count = 0
        self.n2_grams = defaultdict(int)
        self.n2_count = 0
        self.n1_grams = defaultdict(int)
        self.n1_count = 0
        self.read_or_generate_N_grams(n3_grams_filename)

    def read_or_generate_N_grams(self, n3_grams_filename):
        pickled_ngrams_filename = n3_grams_filename + ".pickle"
        # Try to load pickled data
        if os.path.isfile(pickled_ngrams_filename):
            with open(pickled_ngrams_filename, "rb") as pickled_ngrams_file_obj:
                (
                    self.n3_grams,
                    self.n3_count,
                    self.n2_grams,
                    self.n2_count,
                    self.n1_grams,
                    self.n1_count,
                ) = pickle.load(pickled_ngrams_file_obj)
        else:
            # Generate n*_grams
            self.generate_N_grams(n3_grams_filename)
            # Pickle newly generated n*_grams
            with open(pickled_ngrams_filename, "wb") as pickled_ngrams_file_obj:
                data = (
                    self.n3_grams,
                    self.n3_count,
                    self.n2_grams,
                    self.n2_count,
                    self.n1_grams,
                    self.n1_count,
                )
                pickle.dump(data, pickled_ngrams_file_obj)

    def generate_N_grams(self, n3_grams_filename):
        with open(n3_grams_filename, "r") as n3_grams_file_obj:
            # Read the first line
            line = n3_grams_file_obj.readline()
            while line:
                try:
                    count, word1, word2, word3 = line.split()
                except ValueError:
                    word3 = None
                    count, word1, word2 = line.split()
                count = int(count)
                self.n1_grams[word1] += count
                self.n1_grams[word2] += count
                self.n2_grams[" ".join((word1, word2))] += count
                if word3:
                    self.n1_grams[word3] += count
                    self.n2_grams[" ".join((word2, word3))] += count
                    self.n3_grams[" ".join((word1, word2, word3))] += count
                # Read the next line
                line = n3_grams_file_obj.readline()
            # Update total counts
            self.n3_count = sum(self.n3_grams.values())
            self.n2_count = sum(self.n2_grams.values())
            self.n1_count = sum(self.n1_grams.values())

    def score_sentence(self, words):
        # Add 2 empty words at the beginning to count 1-gram for the first word
        words = ["", ""] + list(words)
        score = 0
        i = 2
        while i < len(words):
            word1 = words[i - 2]
            word2 = words[i - 1]
            word3 = words[i]
            word12 = "%s %s" % (word1, word2)
            word23 = "%s %s" % (word2, word3)
            word123 = "%s %s %s" % (word1, word2, word3)
            score += log(
                self.LAMBDA_N1 * self.n1_grams.get(word3, 1) / self.n1_count
                + self.LAMBDA_N2
                * (
                    self.n2_grams.get(word23, 1)
                    / self.n1_grams.get(word2, self.n1_count)
                )
                + self.LAMBDA_N3
                * (
                    self.n3_grams.get(word123, 1)
                    / self.n2_grams.get(word12, self.n2_count)
                )
            )
            i += 1

        return score

    def generate_best_sentences(self, words):
        results = []
        for perm in set(permutations(words)):
            score = self.score_sentence(perm)
            results.append((score, perm))
        results.sort()
        return results[:3], results[-3:]


if __name__ == "__main__":
    # cat poleval_3grams.txt | grep -v "^[0-1] " > poleval_3grams_K_gt_1.txt
    # cat poleval_3grams.txt | grep -v "^[0-3] " > poleval_3grams_K_gt_3.txt
    # cat poleval_3grams.txt | grep -v "^[1-9]\?[0-9] " > poleval_3grams_K_gt_99.txt
    if len(sys.argv) < 2:
        print("Usage: python exercise_4-5.py 3-grams")
        exit(0)
    n3_grams_filename = sys.argv[1]
    n_grams = NGrams(n3_grams_filename)

    def run(sentence):
        words = tokenize(sentence)
        bottom_3, top_3 = n_grams.generate_best_sentences(words)
        print("Top 3:")
        for score, sentence in top_3:
            print("\t", " ".join(sentence))
        print("Bottom 3:")
        for score, sentence in bottom_3:
            print("\t", " ".join(sentence))
        print("\n\t---\n")

    for sentence in SENTENCES:
        print('Sentence: "{sentence}"'.format(sentence=sentence))
        run(sentence)
    # Loop at the end for user's provided examples
    sentence = input("> ")
    while sentence:
        run(sentence)
        sentence = input("> ")
