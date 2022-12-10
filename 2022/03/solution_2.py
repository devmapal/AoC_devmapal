import functools
import string

badges = []
with open("input") as a_file:
    lines = a_file.readlines()
    while lines:
        a, b, c = [set(line.strip()) for line in lines[:3]]
        lines = lines[3:]

        badges.append(a.intersection(b.intersection(c)).pop())

char_to_index = {
    **{c: index for index, c in enumerate(string.ascii_lowercase, start=1)},
    **{c: index for index, c in enumerate(string.ascii_uppercase, start=27)},
}

print(functools.reduce(lambda a, b: a + b, [char_to_index[c] for c in badges]))
