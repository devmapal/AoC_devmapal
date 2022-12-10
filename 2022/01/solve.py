max_calories = 0
with open("input") as a_file:
    current_calories = 0
    for line in a_file.readlines():
        if not line.strip():
            max_calories = max(current_calories, max_calories)
            current_calories = 0
        else:
            current_calories += int(line.strip())

print(max_calories)
