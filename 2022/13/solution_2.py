from functools import cmp_to_key
import json
import math
from numbers import Number
from typing import List, Sequence, Union

Packet = List[Union[int, "Packet"]]


def has_right_order(
    first: Packet, second: Packet, debug: bool = False, indent=0
) -> int:
    if debug:
        print(f"{'':{indent+1}}Got {first} and {second}")
    for first_elem, second_elem in zip(first, second):
        first_is_number = isinstance(first_elem, Number)
        second_is_number = isinstance(second_elem, Number)
        if first_is_number and second_is_number:
            if debug:
                print(f"{'':{indent+1}}Comparing {first_elem} and {second_elem}")
            if first_elem < second_elem:
                return -1
            elif first_elem > second_elem:
                return 1
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
            if result == 1:
                return 1
            elif result == -1:
                return -1

    if len(first) < len(second):
        return -1
    elif len(first) > len(second):
        return 1
    else:
        return 0


with open("input") as a_file:
    lines = a_file.readlines()

packets: Sequence[Packet] = []
for index in range(0, len(lines), 3):
    first = json.loads(lines[index])
    second = json.loads(lines[index + 1])

    packets.extend([first, second])

first_divider = [[2]]
second_divider = [[6]]
packets.append(first_divider)
packets.append(second_divider)


packets.sort(key=cmp_to_key(has_right_order))

print(
    math.prod(
        (
            index + 1
            for index in (packets.index(first_divider), packets.index(second_divider))
        )
    )
)
