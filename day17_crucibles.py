import heapq

grid = []
for line in open("day17_input.txt"):
    line = line.rstrip()
    row = []
    for c in line:
        row.append(int(c))
    grid.append(row)
height = len(grid)
width = len(grid[0])

NORTH = 0
EAST = 1
SOUTH = 2
WEST = 3

NEXT_DIRS = {
    NORTH: (WEST, EAST),
    EAST: (NORTH, SOUTH),
    SOUTH: (EAST, WEST),
    WEST: (SOUTH, NORTH)
}

def dijkstra(min_consecutive, max_consecutive):
    queue = []
    for dir in (SOUTH, EAST):
        # (total heat loss, row, col, direction)
        heapq.heappush(queue, (0, 0, 0, dir))
    visited = set()
    while queue:
        heat_loss, i, j, dir = heapq.heappop(queue)

        # Are we done?
        if (i, j) == (height-1, width-1):
            return heat_loss

        # Have we seen this state before?
        if (i, j, dir) in visited:
            continue
        visited.add((i, j, dir))

        for k in range(min_consecutive, max_consecutive + 1):
            i2, j2 = i, j
            if dir == NORTH:
                i2 = i - k
                if i2 < 0:
                    continue
                added_heat_loss = sum([grid[i3][j] for i3 in range(i2, i)])
            elif dir == SOUTH:
                i2 = i + k
                if i2 >= height:
                    continue
                added_heat_loss = sum([grid[i3][j] for i3 in range(i+1, i2+1)])
            elif dir == EAST:
                j2 = j + k
                if j2 >= width:
                    continue
                added_heat_loss = sum([grid[i][j3] for j3 in range(j+1, j2+1)])
            else:
                j2 = j - k
                if j2 < 0:
                    continue
                added_heat_loss = sum([grid[i][j3] for j3 in range(j2, j)])
            for next_dir in NEXT_DIRS[dir]:
                heapq.heappush(queue, (heat_loss + added_heat_loss, i2, j2, next_dir))

print("Part 1:", dijkstra(1, 3))
print("Part 2:", dijkstra(4, 10))
