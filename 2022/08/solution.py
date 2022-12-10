def is_visible(grid, x, y):
    if x == 0 or x == len(grid[0]) - 1 or y == 0 or y == len(grid) - 1:
        return True

    return (
        is_visible_east(grid, x, y)
        or is_visible_north(grid, x, y)
        or is_visible_south(grid, x, y)
        or is_visible_west(grid, x, y)
    )


def is_visible_west(grid, x, y):
    return max(grid[y][:x], default=-1) < grid[y][x]


def is_visible_east(grid, x, y):
    return max(grid[y][x + 1 :], default=-1) < grid[y][x]


def is_visible_north(grid, x, y):
    column = [row[x] for row in grid]
    return max(column[:y]) < grid[y][x]


def is_visible_south(grid, x, y):
    column = [row[x] for row in grid]
    return max(column[y + 1 :]) < grid[y][x]


with open("input") as a_file:
    grid = [[int(elem) for elem in line.strip()] for line in a_file.readlines()]

visible_count = 0
for y, row in enumerate(grid):
    for x in range(len(row)):
        if is_visible(grid, x, y):
            visible_count += 1

print(visible_count)
