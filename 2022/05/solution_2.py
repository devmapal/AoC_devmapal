import re
from typing import Dict, List


def parse_stacks(lines: List[str]) -> Dict[int, List[str]]:
    stacks: Dict[int, List[str]] = {}

    for line in lines:
        if line.startswith(" 1"):
            break

        for stack_num, index in enumerate(range(1, len(line), 4)):
            elem = line[index]
            if elem == " ":
                continue

            stack = stacks.setdefault(stack_num + 1, [])
            stack.insert(0, elem)

    return stacks


regex = re.compile(r"move (?P<count>\d+) from (?P<from>\d+) to (?P<to>\d+)")


def parse_move(line: str):
    match = re.match(regex, line)
    return (
        int(x) for x in (match.group("count"), match.group("from"), match.group("to"))
    )


with open("input") as a_file:
    lines = a_file.readlines()

stacks = parse_stacks(lines)

for line in lines:
    if not line.startswith("move"):
        continue

    count, start, end = parse_move(line)
    intermediate_stack: List[str] = []
    for _ in range(count):
        elem = stacks[start].pop()
        intermediate_stack.append(elem)
    
    while intermediate_stack:
        elem = intermediate_stack.pop()
        stacks[end].append(elem)

print("".join([stacks[index].pop() for index in range(1, len(stacks)+1)]))
