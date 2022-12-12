from collections import deque
from dataclasses import dataclass
import math
from string import ascii_lowercase
from typing import Sequence, Tuple


@dataclass(frozen=True)
class Position:
    row: int
    column: int


@dataclass(frozen=True)
class Map:
    start: Position
    end: Position
    heightmap: Sequence[Sequence[int]]

    def adjecent_positions(self, position: Position) -> Sequence[Position]:
        positions = []
        if position.row > 0:
            positions.append(Position(position.row - 1, position.column))

        if position.row + 1 < len(self.heightmap):
            positions.append(Position(position.row + 1, position.column))

        if position.column > 0:
            positions.append(Position(position.row, position.column - 1))

        if position.column + 1 < len(self.heightmap[0]):
            positions.append(Position(position.row, position.column + 1))

        return positions

    def height_at(self, position: Position):
        return self.heightmap[position.row][position.column]

    @classmethod
    def from_file(cls: "Map", input: str):
        heightmap = []

        with open("input") as a_file:
            for row, line in enumerate(a_file.readlines()):
                line = line.strip()
                heights = []

                for column, elem in enumerate(line):
                    if elem == "E":
                        end = Position(row, column)
                        heights.append(ascii_lowercase.index("z"))
                    elif elem == "S":
                        start = Position(row, column)
                        heights.append(ascii_lowercase.index("a"))
                    else:
                        heights.append(ascii_lowercase.index(elem))

                heightmap.append(heights)

        return Map(start, end, heightmap)


@dataclass(frozen=True)
class Cursor:
    position: Position
    steps: int = 0


def solve(map: Map, visited: Sequence[Sequence[int]]):
    cursors = deque([Cursor(map.start)])
    while cursor := cursors.pop() if cursors else None:
        # TODO: Valid steps are only those that go down
        if visited[cursor.position.row][cursor.position.column] < cursor.steps:
            continue

        visited[cursor.position.row][cursor.position.column] = cursor.steps

        if cursor.position == map.end:
            continue

        next_positions = [
            position
            for position in map.adjecent_positions(cursor.position)
            if visited[position.row][position.column] > cursor.steps + 1
            and map.height_at(position) <= map.height_at(cursor.position) + 1
        ]

        for position in next_positions:
            cursors.append(Cursor(position, steps=cursor.steps + 1))


map = Map.from_file("input")
visited = [
    [math.inf for _ in range(len(map.heightmap[0]))] for _ in range(len(map.heightmap))
]
solve(map, visited)

print(visited[map.end.row][map.end.column])
