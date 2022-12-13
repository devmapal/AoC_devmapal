import json
from numbers import Number
from typing import List, Tuple, Union

Packet = List[Union[int, "Packet"]]
pairs: List[Tuple[Packet, Packet]] = []


def has_right_order(
    first: Packet, second: Packet, debug: bool = False, indent=0
) -> bool:
    if debug:
        print(f"{'':{indent+1}}Got {first} and {second}")
    for first_elem, second_elem in zip(first, second):
        first_is_number = isinstance(first_elem, Number)
        second_is_number = isinstance(second_elem, Number)
        if first_is_number and second_is_number:
            if debug:
                print(f"{'':{indent+1}}Comparing {first_elem} and {second_elem}")
            if first_elem < second_elem:
                return True
            elif first_elem > second_elem:
                return False
        else:
            first_elem_list = [first_elem] if first_is_number else first_elem
            second_elem_list = [second_elem] if second_is_number else second_elem
            if debug:
                print(
                    f"{'':{indent+1}}has_right_order({first_elem_list}, {second_elem_list})"
                )
            result = has_right_order(
                first_elem_list, second_elem_list, debug, indent=indent + 2
            )
            if result is True:
                return True
            elif result is False:
                return False

    if len(first) < len(second):
        return True
    elif len(first) > len(second):
        return False


with open("input") as a_file:
    lines = a_file.readlines()

for index in range(0, len(lines), 3):
    first = json.loads(lines[index])
    second = json.loads(lines[index + 1])

    pairs.append((first, second))


right_order: List[int] = []
for index, (first, second) in enumerate(pairs):
    if has_right_order(first, second):
        right_order.append(index + 1)

print(sum(right_order))
