from dataclasses import dataclass
import math
from pprint import pprint
import re
from typing import Sequence, Set


@dataclass(frozen=True)
class Position:
    x: int
    y: int

    def manhatten_distance(self, other: "Position") -> int:
        return abs(self.x - other.x) + abs(self.y - other.y)


class Circle:
    def __init__(self, center: Position, rim_point: Position):
        self.center = center
        self.radius = center.manhatten_distance(rim_point)

    def intersects_with(self, position: Position) -> bool:
        return self.center.manhatten_distance(position) <= self.radius

    def __repr__(self):
        return f"Circle(center={str(self.center)}, radius={self.radius}"


sensors: Set[Position] = set()
beacons: Set[Position] = set()
circles: Sequence[Circle] = []
min_x = math.inf
max_x = -math.inf
with open("input") as a_file:
    input_line_pattern = re.compile(
        r"x=(?P<sensor_x>-?\d+).*y=(?P<sensor_y>-?\d+).+x=(?P<beacon_x>-?\d+).*y=(?P<beacon_y>-?\d+)"
    )
    while line := a_file.readline():
        if line.strip() == "":
            continue

        match = re.search(input_line_pattern, line)
        sensor = Position(int(match.group("sensor_x")), int(match.group("sensor_y")))
        beacon = Position(int(match.group("beacon_x")), int(match.group("beacon_y")))

        sensors.add(sensor)
        beacons.add(beacon)

        circle = Circle(center=sensor, rim_point=beacon)
        circles.append(circle)

        min_x = min(min_x, circle.center.x - circle.radius)
        max_x = max(max_x, circle.center.x + circle.radius)

possible_positions = (Position(x=x, y=2000000) for x in range(min_x, max_x + 1))
intersections = (
    possible_position not in sensors
    and possible_position not in beacons
    and any((circle.intersects_with(possible_position) for circle in circles))
    for possible_position in possible_positions
)

print(sum((int(intersection) for intersection in intersections)))
