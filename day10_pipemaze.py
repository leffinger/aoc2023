import collections

WEST = (0, -1)
EAST = (0, 1)
NORTH = (-1, 0)
SOUTH = (1, 0)

DIRECTIONS = {
    "|": [NORTH, SOUTH],
    "-": [WEST, EAST],
    "L": [NORTH, EAST],
    "J": [NORTH, WEST],
    "7": [SOUTH, WEST],
    "F": [SOUTH, EAST],
}

text = open("day10_input.txt").read().split()
height = len(text)
width = len(text[0])

# Construct the maze as a map from (i, j) -> character.
maze = {}
for i in range(height):
    for j in range(width):
        maze[(i, j)] = text[i][j]
        if text[i][j] == "S":
            start = (i, j)

# Fill this in for your input.
maze[start] = "J"

# Use BFS to find all points on the loop and their shortest distance from the start.
loop = {}
queue = collections.deque()
queue.append((start, 0))
while queue:
    coord, distance = queue.popleft()
    if coord not in maze or coord in loop:
        continue
    loop[coord] = distance
    for dir in DIRECTIONS[maze[coord]]:
        queue.append(((coord[0] + dir[0], coord[1]+dir[1]), distance+1))

print("Part 1:", max(loop.values()))

# For part 2, we'll represent the loop using 3x3 blocks.
#
#  |   -   L   J   7   F
#
# .X. ... .X. .X. ... ...
# .X. XXX .XX XX. XX. .XX
# .X. ... ... ... .X. .X.

BLOCKS = {
    "|": [(0,1), (1,1), (2,1)],
    "-": [(1,0), (1,1), (1,2)],
    "L": [(1,1), (0,1), (1,2)],
    "J": [(1,1), (0,1), (1,0)],
    "7": [(1,1), (1,0), (2,1)],
    "F": [(1,1), (1,2), (2,1)],
}

# Build the maze using 3x3 patches. Only the blocks in the loop are included
# in the maze.
bigmaze = {}
for i in range(3 * height):
    for j in range(3 * width):
        bigmaze[(i, j)] = False
for i in range(height):
    for j in range(width):
        if (i, j) in loop:
            for ii, jj in BLOCKS[maze[(i, j)]]:
                bigmaze[(3*i + ii, 3*j + jj)] = True

# Use BFS again to find the set of all coords "outside" in the big maze.
outside = set()
queue = collections.deque()
queue.append((0,0))
while queue:
    i, j = queue.popleft()
    if (i, j) not in bigmaze or bigmaze[(i, j)] or (i, j) in outside:
        continue
    outside.add((i, j))
    queue.extend([(i + dir[0], j + dir[1]) for dir in [NORTH, SOUTH, EAST, WEST]])

# Find all squares in the small maze that aren't "outside" in the big maze.
inside = set()
for i in range(height):
    for j in range(width):
        if (i, j) in loop:
            continue
        if any([(3*i + ii, 3*j + jj) in outside for ii in range(3) for jj in range(3)]):
            continue
        inside.add((i, j))

# Print because it's pretty.
for i in range(height):
    row = []
    for j in range(width):
        if (i, j) in loop:
            row.append(maze[(i, j)])
        elif (i, j) in inside:
            row.append("I")
        else:
            row.append(".")
    print("".join(row))

print("Part 2:", len(inside))