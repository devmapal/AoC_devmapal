from dataclasses import dataclass
from pprint import pprint
from typing import Literal, Mapping, Sequence


@dataclass
class Position:
    row: int
    column: int


Path = Sequence[Position]


@dataclass
class Map:
    map: Sequence[Mapping[int, Literal[".", "#", "+", "o"]]]
    crack: Position
    floor: int

    @classmethod
    def from_paths(cls, paths: Sequence[Path], crack: Position) -> "Map":
        floor = max((position.row for path in paths for position in path)) + 2
        columns = [position.column for path in paths for position in path]
        min_column = min(columns)
        max_column = max(columns)

        map = [
            {
                column: "."
                for column in range(min_column - floor, max_column + 1 + floor)
            }
            for _ in range(floor + 1)
        ]

        for path in paths:
            for first, second in zip(path[:-1], path[1:]):
                if first.row == second.row:
                    column_min = min(first.column, second.column)
                    column_max = max(first.column, second.column)
                    for column in range(column_min, column_max + 1):
                        map[first.row][column] = "#"
                else:
                    row_min = min(first.row, second.row)
                    row_max = max(first.row, second.row)
                    for row in range(row_min, row_max + 1):
                        map[row][first.column] = "#"

        map[crack.row][crack.column] = "+"
        floor_row = map[floor]
        for column in floor_row:
            floor_row[column] = "#"

        return cls(map, crack, floor)

    def is_air(self, position: Position) -> bool:
        return self.get_value_at(position) == "."

    def is_solid(self, position: Position) -> bool:
        return not self.is_air(position)

    def get_value_at(self, position: Position) -> Literal["#", ".", "+", "o"]:
        if not self.within_map(position):
            return "."
        else:
            return self.map[position.row][position.column]

    def within_map(self, position) -> bool:
        return (
            0 <= position.row < len(self.map)
            and position.column in self.map[position.row]
        )

    def update_map(self, position: Position, value: Literal["#", ".", "+", "o"]):
        assert self.within_map(position)
        self.map[position.row][position.column] = value

    def __str__(self) -> str:
        return "\n".join(("".join(row.values()) for row in self.map))


def parse_path(line: str) -> Path:
    raw_positions = (
        position.split(",")
        for position in line.strip().split(" -> ")
        if line.strip() != ""
    )
    return [Position(row=int(row), column=int(column)) for column, row in raw_positions]


@dataclass
class Simulation:
    map: Map

    def _get_next_position(self, current: Position):
        down = Position(current.row + 1, current.column)
        down_left = Position(current.row + 1, current.column - 1)
        down_right = Position(current.row + 1, current.column + 1)

        if self.map.is_air(down):
            return down
        elif self.map.is_air(down_left):
            return down_left
        elif self.map.is_air(down_right):
            return down_right

    def simulate_sand(self, start: Position):
        current_position = start
        while next_position := self._get_next_position(current_position):
            current_position = next_position
            assert self.map.within_map(current_position)

        return current_position

    def run_simulation(self, start: Position) -> int:
        simulated_pieces = 0
        while sand := self.simulate_sand(start):
            simulated_pieces += 1
            if sand == self.map.crack:
                break

            self.map.update_map(sand, "o")

        return simulated_pieces


paths: Sequence[Path] = []

with open("input") as a_file:
    for line in a_file:
        paths.append(parse_path(line))

simulation = Simulation(Map.from_paths(paths, Position(row=0, column=500)))

print(simulation.run_simulation(Position(row=0, column=500)))
print(simulation.map)
