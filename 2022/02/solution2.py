from enum import Enum
from typing import Literal

class Shape():
    def __init__(self, points):
        self.points = points

class Rock(Shape):
    def __init__(self):
        super().__init__(1)

class Paper(Shape):
    def __init__(self):
        super().__init__(2)

class Scissor(Shape):
    def __init__(self):
        super().__init__(3)

class Result(Enum):
    WINS_AGAINST = 1
    LOOSES_AGAINST = 2

relations = {
    Rock: {
        Result.WINS_AGAINST: Scissor,
        Result.LOOSES_AGAINST: Paper,
    },
    Paper: {
        Result.WINS_AGAINST: Rock,
        Result.LOOSES_AGAINST: Scissor,
    },
    Scissor: {
        Result.WINS_AGAINST: Paper,
        Result.LOOSES_AGAINST: Rock,
    },
}

def opponent_from_char(c: Literal["A", "B", "C"]) -> Shape:
    if c  == "A":
        return Rock();
    elif c  == "B":
        return Paper()
    else:
        return Scissor()

def you_from_char(c: Literal["X", "Y", "Z"], opponent: Shape) -> Shape:
    if c == "X":
        return relations[opponent.__class__][Result.WINS_AGAINST]()
    elif c == "Y":
        return opponent.__class__()
    else:
        return relations[opponent.__class__][Result.LOOSES_AGAINST]()

total_points = 0
with open("input") as a_file:
    for line in a_file.readlines():
        o, y = line.split()
        opponent = opponent_from_char(o)
        you = you_from_char(y, opponent)

        total_points += you.points
        if opponent.__class__ == you.__class__:
            total_points += 3
        elif relations[you.__class__][Result.WINS_AGAINST] == opponent.__class__:
            total_points += 6

print(total_points)