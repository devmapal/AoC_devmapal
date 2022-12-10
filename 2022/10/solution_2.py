from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Generator, Literal, Sequence


@dataclass
class State:
    X: int = 1
    cycle: int = 0


class Command(ABC):
    @abstractmethod
    def cycle(self, state: State) -> Generator[None, None, None]:
        raise NotImplementedError()


class Noop(Command):
    DURATION = 1

    def cycle(self, state: State) -> Generator[None, None, None]:
        for _ in range(Noop.DURATION):
            yield


class Addx(Command):
    DURATION = 2

    def __init__(self, value: int) -> "Addx":
        self._value = value

    def cycle(self, state: State) -> Generator[None, None, None]:
        for _ in range(Addx.DURATION):
            yield

        state.X += self._value


def parse_command(line: str):
    if line.startswith("noop"):
        return Noop()
    elif line.startswith("addx"):
        value = int(line.strip().split(" ")[1])
        return Addx(value)


state = State()
with open("input") as a_file:
    line_pixels: Sequence[Literal["#", "."]] = []

    while line := a_file.readline():
        command = parse_command(line)
        for _ in command.cycle(state):
            state.cycle += 1

            position = len(line_pixels)
            if abs(state.X - position) <= 1:
                line_pixels.append("#")
            else:
                line_pixels.append(".")
            
            if len(line_pixels) == 40:
                print("".join(line_pixels))
                line_pixels = []
