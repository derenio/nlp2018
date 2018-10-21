import sys
import pygtrie

from exercise_1 import similarity


def reversed_words_trie(file_obj):
    reversed_trie = pygtrie.CharTrie()
    line = file_obj.readline()
    while line:
        for word in line.split():
            word = word.lower()[::-1]
            if word in reversed_trie:
                reversed_trie[word] += 1
            else:
                reversed_trie[word] = 1
        line = file_obj.readline()
    return reversed_trie


def reversed_max_match(untokenized_corpus, reversed_trie):
    def max_match_sufix(start, end, line):
        if start < 0:
            return None
        word = line[start:end]
        test = reversed_trie.has_node(word[::-1])
        if test & pygtrie.Trie.HAS_SUBTRIE:
            # Trying to generate a longer sufix
            new_start = max_match_sufix(start - 1, end, line)
            if new_start is not None:
                return new_start
        if test & pygtrie.Trie.HAS_VALUE:
            # This sufix is a valid word, return its start index
            return start
        else:
            # Dead-end, couldn't find a valid sufix
            return None

    line = untokenized_corpus.readline()
    while line:
        line = line.strip()
        end = len(line)
        start = end - 1
        acc = []
        while start >= 0:
            new_start = max_match_sufix(start, end, line)
            if new_start is None:
                # Sufix not present in the trie.
                # Assume the single character is a valid word
                new_start = start
            word = line[new_start:end]
            acc.append(word)
            end = new_start
            start = end - 1
        yield " ".join(acc[::-1])
        line = untokenized_corpus.readline()


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python exercise_1.py corpus untokenized_corpus")
    with open(sys.argv[1], "r") as corpus, open(sys.argv[2], "r") as untokenized_corpus:
        reversed_trie = reversed_words_trie(corpus)
        retokenized = list(reversed_max_match(untokenized_corpus, reversed_trie))
        corpus.seek(0)
        print(similarity(corpus.readlines(), retokenized))
