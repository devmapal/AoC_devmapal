from dataclasses import dataclass


@dataclass
class Range:
    start: int
    end: int

    def overlaps_with(self, other: "Range"):
        return (
            other.start <= self.start <= other.end
            or other.start <= self.end <= other.end
            or self.start <= other.start <= self.end
            or self.start <= other.end <= self.end
        )


result = 0
with open("input") as a_file:
    for line in a_file.readlines():
        a, b = line.split(",")
        a = Range(*[int(x) for x in a.split("-")])
        b = Range(*[int(x) for x in b.split("-")])

        if a.overlaps_with(b):
            result += 1

print(result)
