import heapq

calories = []
with open("input") as a_file:
    current_calories = 0
    for line in a_file.readlines():
        if not line.strip():
            calories.append(-current_calories)
            current_calories = 0
        else:
            current_calories += int(line.strip())

heapq.heapify(calories)

sum = 0
for _ in range(3):
    sum += abs(heapq.heappop(calories))

print(sum)
