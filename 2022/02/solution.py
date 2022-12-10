from typing import Literal

class Shape():
    def __init__(self, points):
        self.points = points

class Rock(Shape):
    beats = "Scissor"

    def __init__(self):
        super().__init__(1)

class Paper(Shape):
    beats = "Rock"

    def __init__(self):
        super().__init__(2)

class Scissor(Shape):
    beats = "Paper"

    def __init__(self):
        super().__init__(3)

def from_char(c: Literal["A", "B", "C", "X", "Y", "Z"]) -> Shape:
    if c in ["A", "X"]:
        return Rock();
    elif c in ["B", "Y"]:
        return Paper()
    else:
        return Scissor()

total_points = 0
with open("input") as a_file:
    for line in a_file.readlines():
        opponent, you = [from_char(c) for c in line.split()]

        total_points += you.points
        if opponent.__class__ == you.__class__:
            total_points += 3
        elif opponent.__class__.__name__ == you.beats:
            total_points += 6

print(total_points)