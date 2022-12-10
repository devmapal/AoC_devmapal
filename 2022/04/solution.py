from dataclasses import dataclass


@dataclass
class Range:
    start: int
    end: int

    def contains(self, other: "Range"):
        return other.start >= self.start and other.end <= self.end
        
result = 0
with open("input") as a_file:
    for line in a_file.readlines():
        a, b = line.split(",")
        a = Range(*[int(x) for x in a.split("-")])
        b = Range(*[int(x) for x in b.split("-")])

        if a.contains(b) or b.contains(a):
            result += 1

print(result)