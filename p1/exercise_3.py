import sys
import random

from exercise_2 import Exercise2, read_ngrams


class Exercise3(Exercise2):
    def choice(self, suffixes_with_counts):
        counts, suffixes = zip(*suffixes_with_counts)
        [suffix] = random.choices(suffixes, weights=counts)
        return suffix


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python exercise_3.py N-grams")
    with open(sys.argv[1], "r") as n_grams_file:
        beginnings, n_grams = read_ngrams(n_grams_file)
        exercise3 = Exercise3()
        exercise3.print_random_sentence(n_grams, random.choice(beginnings))
        exercise3.print_random_sentence(n_grams, random.choice(beginnings))
        exercise3.print_random_sentence(n_grams, random.choice(beginnings))
        exercise3.print_random_sentence(n_grams, random.choice(beginnings))
