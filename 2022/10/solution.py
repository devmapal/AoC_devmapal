from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Generator


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
signal_strengths = []
with open("input") as a_file:
    while line := a_file.readline():
        command = parse_command(line)
        for _ in command.cycle(state):
            state.cycle += 1
            if (state.cycle - 20) % 40 == 0:
                signal_strengths.append(state.cycle * state.X)

print(sum(signal_strengths))
