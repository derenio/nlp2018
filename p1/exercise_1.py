import sys
import pygtrie
from collections import defaultdict


def count_words(file_obj):
    d = defaultdict(int)
    for line in file_obj.readlines():
        for word in line.split():
            word = word.lower()
            d[word] += 1
    return d


def words_trie(file_obj):
    trie = pygtrie.CharTrie()
    line = file_obj.readline()
    while line:
        for word in line.split():
            word = word.lower()
            if word in trie:
                trie[word] += 1
            else:
                trie[word] = 1
        line = file_obj.readline()
    return trie


def max_match(untokenized_corpus, trie):
    def max_match_prefix(start, end, line):
        if end > len(line):
            return None
        word = line[start:end]
        test = trie.has_node(word)
        if test & pygtrie.Trie.HAS_SUBTRIE:
            # Trying to generate a longer prefix
            new_end = max_match_prefix(start, end + 1, line)
            if new_end is not None:
                return new_end
        if test & pygtrie.Trie.HAS_VALUE:
            # This prefix is a valid word, return its end index
            return end
        else:
            # Dead-end, couldn't find a valid prefix
            return None

    line = untokenized_corpus.readline()
    while line:
        line = line.strip()
        start = 0
        end = 1
        acc = []
        while end <= len(line):
            new_end = max_match_prefix(start, end, line)
            if new_end is None:
                # Prefix not present in the trie.
                # Assume the single character is a valid word
                new_end = end
            word = line[start:new_end]
            acc.append(word)
            start = new_end
            end = start + 1
        yield " ".join(acc)
        line = untokenized_corpus.readline()


def similarity(base_lines, lines):
    base_total = 0
    common = 0
    for base_line, line in zip(base_lines, lines):
        base_line_set = set(base_line.lower().split())
        line_set = set(line.lower().split())
        base_line_set_len = len(base_line_set)
        common_len = len(base_line_set & line_set)
        if base_line_set_len != common_len:
            print("Different line:")
            print("\t%s" % base_line.strip())
            print("\t%s" % line)
        base_total += base_line_set_len
        common += common_len
    return (common, base_total, common / base_total)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python exercise_1.py corpus untokenized_corpus")
        exit(0)
    with open(sys.argv[1], "r") as corpus, open(sys.argv[2], "r") as untokenized_corpus:
        trie = words_trie(corpus)
        retokenized = list(max_match(untokenized_corpus, trie))
        corpus.seek(0)
        print(similarity(corpus.readlines(), retokenized))
