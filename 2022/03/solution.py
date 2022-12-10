import functools
import string

duplicates = []
with open("input") as a_file:
    for line in a_file.readlines():
        pocket_a = set(line[: len(line) // 2])
        pocket_b = set(line[len(line) // 2 :])
        duplicates.append(pocket_a.intersection(pocket_b).pop())

char_to_index = {
    **{c: index for index, c in enumerate(string.ascii_lowercase, start=1)},
    **{c: index for index, c in enumerate(string.ascii_uppercase, start=27)},
}

print(functools.reduce(lambda a, b: a + b, [char_to_index[c] for c in duplicates]))
