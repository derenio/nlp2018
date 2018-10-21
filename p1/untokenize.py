import sys


def untokenize(file_obj):
    for line in file_obj.readlines():
        print(line.replace(" ", "").lower(), end="")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        with open(sys.argv[1], mode="r") as f:
            untokenize(f)
    else:
        untokenize(sys.stdin)
