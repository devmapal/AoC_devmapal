from dataclasses import dataclass
import math
from pprint import pprint
import re
from typing import Optional, Sequence, Set


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

    def rim_position(self, y: int) -> Position:
        x = self.center.x + self.radius - abs(self.center.y - y)
        return Position(x, y)

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


def get_intersecting_circle(position: Position) -> Optional[Circle]:
    global circles
    return next((circle for circle in circles if circle.intersects_with(current)), None)


for y in range(0, 4000000 + 1):
    if y % 40000 == 0:
        print(y // 40000)
    current = Position(x=0, y=y)
    while current.x <= 4000000 and (
        intersecting_circle := get_intersecting_circle(current)
    ):
        rim_position = intersecting_circle.rim_position(y)
        current = Position(rim_position.x + 1, y)

    if current.x <= 4000000 and not intersecting_circle:
        break

print(current)
print(current.x * 4000000 + current.y)
