import copy

grid = []
for line in open("day14_input.txt"):
    grid.append(list(line.rstrip()))
height = len(grid)
width = len(grid[0])

def tilt_north():
    for j in range(width):
        stopping_point = 0
        for i in range(height):
            if grid[i][j] == "O":
                grid[i][j] = grid[stopping_point][j]
                grid[stopping_point][j] = "O"
                stopping_point += 1
            elif grid[i][j] == "#":
                stopping_point = i + 1

def tilt_south():
    for j in range(width):
        stopping_point = height - 1
        for i in range(height - 1, -1, -1):
            if grid[i][j] == "O":
                grid[i][j] = grid[stopping_point][j]
                grid[stopping_point][j] = "O"
                stopping_point -= 1
            elif grid[i][j] == "#":
                stopping_point = i - 1

def tilt_west():
    for i in range(height):
        stopping_point = 0
        for j in range(width):
            if grid[i][j] == "O":
                grid[i][j] = grid[i][stopping_point]
                grid[i][stopping_point] = "O"
                stopping_point += 1
            elif grid[i][j] == "#":
                stopping_point = j + 1

def tilt_east():
    for i in range(height):
        stopping_point = width - 1
        for j in range(width - 1, -1, -1):
            if grid[i][j] == "O":
                grid[i][j] = grid[i][stopping_point]
                grid[i][stopping_point] = "O"
                stopping_point -= 1
            elif grid[i][j] == "#":
                stopping_point = j - 1

def score_grid():
    total = 0
    for i in range(height):
        for j in range(width):
            if grid[i][j] == "O":
                total += height - i
    return total

memo_table = {}
def score_grid_memoized(cycle):
    key = "".join(["".join(row) for row in grid])
    if key in memo_table:
        return memo_table[key]
    score = score_grid()
    memo_table[key] = (score, cycle)
    return memo_table[key], -1

grid_copy = copy.deepcopy(grid)
tilt_north()
print("Part 1 score:", score_grid())
grid = grid_copy

total_cycles = 1000000000
cycle = 0
skipped_ahead = False
while cycle < total_cycles:
    tilt_north()
    tilt_west()
    tilt_south()
    tilt_east()
    if not skipped_ahead:
        score, previous = score_grid_memoized(cycle)
        if previous != -1:
            cycle_lenth = cycle - previous
            cycle += ((total_cycles - cycle) // cycle_lenth) * cycle_lenth
            skipped_ahead = True
    cycle += 1

print("Part 2 score:", score_grid())
