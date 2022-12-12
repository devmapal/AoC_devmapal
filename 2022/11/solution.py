from dataclasses import dataclass
import math
import re
from typing import Callable, Deque, Literal, Sequence


@dataclass(frozen=True)
class Item:
    stress_level: int

    def releive(self) -> "Item":
        return Item(self.stress_level // 3)


@dataclass
class Monkey:
    items: Deque[Item]
    operation: Callable[[Item], Item]
    test: Callable[[Item], int]
    inspected_items: int = 0

    def getNextItem(self):
        self.inspected_items += 1
        item = self.items.pop()
        return self.operation(item).releive()

    def getNextMonketIndex(self, item: Item):
        return self.test(item)

    def addItem(self, item: Item):
        self.items.insert(0, item)


def parse_items(line: str) -> Sequence[Item]:
    # I.e. "  Starting items: 65, 78\n"
    raw_items = line.split(":")[1].strip().split(", ")
    return [Item(int(item)) for item in raw_items]


def parse_operation_fn(
    operation: Literal["+", "-", "*", "/"]
) -> Callable[[int, int], int]:
    if operation == "+":
        return lambda x, y: x + y
    elif operation == "-":
        return lambda x, y: x - y
    elif operation == "*":
        return lambda x, y: x * y
    elif operation == "/":
        return lambda x, y: x / y


def parse_operand(item: Item, operand: str) -> int:
    if operand == "old":
        return item.stress_level
    else:
        return int(operand)


def parse_operation(line: str) -> Callable[[Item], Item]:
    pattern = r"Operation: new = (?P<operand1>old|\d+) (?P<operation_fn>[+\-\*/]) (?P<operand2>old|\d+)"
    match = re.search(pattern, line)
    operand1 = match.group("operand1")
    operand2 = match.group("operand2")
    operation_fn = parse_operation_fn(match.group("operation_fn"))

    def operation(item: Item) -> Item:
        op1 = parse_operand(item, operand1)
        op2 = parse_operand(item, operand2)

        return Item(operation_fn(op1, op2))

    return operation


def parse_test(line: str, test_true: str, test_false: str) -> Callable[[Item], Item]:
    divisor = int(line.strip().split(" ")[-1])
    true_monkey_index = int(test_true.split(" ")[-1])
    false_monkey_index = int(test_false.split(" ")[-1])

    def test_fn(item: Item):
        if item.stress_level % divisor == 0:
            return true_monkey_index
        else:
            return false_monkey_index

    return test_fn


def parse_monkeys(lines: Sequence[str]):
    monkeys: Sequence[Monkey] = []
    for start_index in range(0, len(lines), 7):
        items = parse_items(lines[start_index + 1])
        operation = parse_operation(lines[start_index + 2])
        test = parse_test(
            lines[start_index + 3], lines[start_index + 4], lines[start_index + 5]
        )

        monkeys.append(Monkey(items, operation, test))

    return monkeys


with open("input") as a_file:
    monkeys = parse_monkeys(a_file.readlines())

for _ in range(20):
    for monkey in monkeys:
        while monkey.items:
            item = monkey.getNextItem()
            target_monkey_index = monkey.test(item)
            monkeys[target_monkey_index].addItem(item)

print(
    math.prod(sorted([monkey.inspected_items for monkey in monkeys], reverse=True)[:2])
)
