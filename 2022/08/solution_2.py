def visible_score(grid, x, y):
    return (
        trees_visible_east(grid, x, y) * trees_visible_north(grid, x, y) * trees_visible_south(grid, x, y) * trees_visible_west(grid, x, y)
    )


def trees_visible_west(grid, x, y):
    score = 0
    row = grid[y][:x]
    row.reverse()
    for elem in row:
        score += 1
        if elem >= grid[y][x]:
            break
    
    return score


def trees_visible_east(grid, x, y):
    score = 0
    row = grid[y][x+1:]
    for elem in row:
        score += 1
        if elem >= grid[y][x]:
            break
    
    return score


def trees_visible_north(grid, x, y):
    score = 0
    column = [row[x] for row in grid][:y]
    column.reverse()
    for elem in column:
        score += 1
        if elem >= grid[y][x]:
            break
    
    return score


def trees_visible_south(grid, x, y):
    score = 0
    column = [row[x] for row in grid][y+1:]
    for elem in column:
        score += 1
        if elem >= grid[y][x]:
            break
    
    return score


with open("input") as a_file:
    grid = [[int(elem) for elem in line.strip()] for line in a_file.readlines()]

max_score = 0
for y, row in enumerate(grid):
    for x in range(len(row)):
        max_score = max(visible_score(grid, x, y), max_score)

print(max_score)
