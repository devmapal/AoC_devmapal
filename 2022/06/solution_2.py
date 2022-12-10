with open("input") as input_file:
    input = input_file.readline()

UNIQUE_CHARS = 14

counts = {}
for index, c in enumerate(input):
    counts.setdefault(c, 0)
    counts[c] += 1

    if all((value == 1 for value in counts.values())) and sum(counts.values()) == UNIQUE_CHARS:
        print(index+1)
        break
    elif index >= UNIQUE_CHARS-1:
        start_char = input[index-(UNIQUE_CHARS-1)]
        count = counts.get(start_char)
        
        if count == 1:
            del counts[start_char]
        else:
            counts[start_char] = count - 1
