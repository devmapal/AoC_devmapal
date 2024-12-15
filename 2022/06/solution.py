with open("input") as input_file:
    input = input_file.readline()

counts = {}
for index, c in enumerate(input):
    counts.setdefault(c, 0)
    counts[c] += 1

    if all((value == 1 for value in counts.values())) and sum(counts.values()) == 4:
        print(index + 1)
        break
    elif index >= 3:
        count = counts.get(input[index - 3])

        if count == 1:
            del counts[input[index - 3]]
        else:
            counts[input[index - 3]] = count - 1
