import sys
import random
from collections import defaultdict


def read_ngrams(file_obj):
    line = file_obj.readline()
    beginnings = []
    n_grams = defaultdict(list)
    while line:
        count, rest = line.strip().split(None, 1)
        count = int(count)
        prefix, _ = rest.rsplit(None, 1)
        _, suffix = rest.split(None, 1)
        if prefix.startswith("<BOS>"):
            beginnings.append(prefix)
        n_grams[prefix].append((count, suffix))
        line = file_obj.readline()
    return beginnings, n_grams


class Exercise2:
    def choice(self, suffixes):
        [(count, suffix)] = random.choices(suffixes)
        return suffix

    def print_random_sentence(self, n_grams, prefix):
        def aux(prefix, acc=[]):
            suffixes = n_grams.get(prefix)
            if not suffixes:
                # No more suffixes, ending
                return acc
            suffix = self.choice(suffixes)
            suffix_without_first_if_more = suffix.split(None, 1)[-1]
            acc.append(suffix_without_first_if_more)
            if suffix.endswith("<EOS>"):
                # Randomly picked the "End of the sentence" n-gram, ending
                return acc
            return aux(suffix, acc)

        sentence_list = aux(prefix, acc=[prefix])
        print(" ".join(sentence_list))


if __name__ == "__main__":
    # cat poleval_2grams.txt | grep -v "^[123456789]\?[0-9] " > poleval_2grams_K_gt_99.txt
    # cat poleval_2grams.txt | grep -v "^[1]\?[0-9] " > poleval_2grams_K_gt_19.txt
    # cat poleval_2grams.txt | grep -v "^[1234]\?[0-9] " > poleval_3grams_K_gt_49.txt
    # cat poleval_3grams.txt | grep -v "^[1]\?[0-9] " > poleval_3grams_K_gt_19.txt
    if len(sys.argv) < 2:
        print("Usage: python exercise_2.py N-grams")
    with open(sys.argv[1], "r") as n_grams_file:
        beginnings, n_grams = read_ngrams(n_grams_file)
        exercise2 = Exercise2()
        exercise2.print_random_sentence(n_grams, random.choice(beginnings))
        exercise2.print_random_sentence(n_grams, random.choice(beginnings))
        exercise2.print_random_sentence(n_grams, random.choice(beginnings))
        exercise2.print_random_sentence(n_grams, random.choice(beginnings))
