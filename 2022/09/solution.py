from dataclasses import dataclass
from typing import Literal, Sequence, Set

Direction = Literal["U", "D", "L", "R"]


@dataclass(frozen=True)
class Position:
    x: int
    y: int

    def distance_sq(self, other: "Position") -> int:
        return (self.x - other.x) ** 2 + (self.y - other.y) ** 2

    def up(self) -> "Position":
        return Position(self.x, self.y + 1)

    def down(self) -> "Position":
        return Position(self.x, self.y - 1)

    def left(self) -> "Position":
        return Position(self.x - 1, self.y)

    def right(self) -> "Position":
        return Position(self.x + 1, self.y)

    def move(self, direction: Direction) -> "Position":
        if direction == "U":
            return self.up()
        elif direction == "D":
            return self.down()
        elif direction == "L":
            return self.left()
        elif direction == "R":
            return self.right()


def get_tail_directions(head: Position, tail: Position) -> Sequence[Direction]:
    directions: Sequence[Direction] = []

    if head.distance_sq(tail) < 4:
        return directions

    x_difference = head.x - tail.x
    y_difference = head.y - tail.y
    if x_difference != 0 and y_difference != 0:
        DIFF = 0
    else:
        DIFF = 1
    if x_difference > DIFF:
        directions.append("R")
    elif x_difference < -DIFF:
        directions.append("L")

    if y_difference > DIFF:
        directions.append("U")
    elif y_difference < -DIFF:
        directions.append("D")

    return directions


head = Position(0, 0)
tail = Position(0, 0)

unique_tail_positions = set([tail])

with open("input") as a_file:
    while line := a_file.readline():
        direction, count_str = line.strip().split(" ")
        count = int(count_str)

        for _ in range(count):
            head = head.move(direction)
            tail_directions = get_tail_directions(head, tail)
            for tail_direction in tail_directions:
                tail = tail.move(tail_direction)

            unique_tail_positions.add(tail)
            assert 0 <= abs(head.x - tail.x) <= 1
            assert 0 <= abs(head.y - tail.y) <= 1

print(len(unique_tail_positions))
