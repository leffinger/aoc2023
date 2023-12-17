import collections

grid = open("day16_input.txt").read().split()
height = len(grid)
width = len(grid[0])

EAST = 0
WEST = 1
NORTH = 2
SOUTH = 3

NEXT_DIRS = {
    (".", EAST): [EAST],
    (".", WEST): [WEST],
    (".", NORTH): [NORTH],
    (".", SOUTH): [SOUTH],
    ("/", EAST): [NORTH],
    ("/", WEST): [SOUTH],
    ("/", NORTH): [EAST],
    ("/", SOUTH): [WEST],
    ("\\", EAST): [SOUTH],
    ("\\", WEST): [NORTH],
    ("\\", NORTH): [WEST],
    ("\\", SOUTH): [EAST],
    ("-", EAST): [EAST],
    ("-", WEST): [WEST],
    ("-", NORTH): [EAST, WEST],
    ("-", SOUTH): [EAST, WEST],
    ("|", EAST): [NORTH, SOUTH],
    ("|", WEST): [NORTH, SOUTH],
    ("|", NORTH): [NORTH],
    ("|", SOUTH): [SOUTH],
}

OFFSETS = {
    EAST: (0, 1),
    WEST: (0, -1),
    NORTH: (-1, 0),
    SOUTH: (1, 0),
}

def bfs(i, j, dir):
    queue = collections.deque()
    queue.append((i, j, dir))
    visited = set()
    while queue:
        i, j, dir = queue.popleft()
        if (i, j, dir) in visited:
            continue
        if i < 0 or i >= height or j < 0 or j >= width:
            continue
        visited.add((i, j, dir))
        for next_dir in NEXT_DIRS[(grid[i][j], dir)]:
            offset = OFFSETS[next_dir]
            queue.append((i + offset[0], j + offset[1], next_dir))
    return len(set([(i, j) for i, j, _ in visited]))

print("Part 1:", bfs(0, 0, EAST))

entry_points = ([(i, 0, EAST) for i in range(height)]
                + [(i, width - 1, WEST) for i in range(height)]
                + [(0, j, SOUTH) for j in range(width)]
                + [(height - 1, j, NORTH) for j in range(width)])

print("Part 2:", max([bfs(i, j, dir) for i, j, dir in entry_points]))
