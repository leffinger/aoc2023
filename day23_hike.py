import collections

OFFSETS = {
    "v": (1, 0),
    "<": (-1, 0),
    ">": (0, 1), 
    "^": (0, -1)
}

# file = "day23_sample.txt"
file = "day23_input.txt"

input = open(file).read().split()
height = len(input)
width = len(input[0])
end = (height - 1, width - 2)

grid = {}
for i in range(height):
    for j in range(width):
        grid[(i, j)] = input[i][j]

def part1():
    # Use iterative DFS to identify all paths through the grid.
    stack = []
    stack.append((0, 1, set()))
    longest_path_length = 0
    while stack:
        i, j, prev = stack.pop()
        if (i, j) == end:
            longest_path_length = max(len(prev), longest_path_length)
        for di, dj in OFFSETS.values():
            ii, jj = i + di, j + dj
            if (ii, jj) not in grid:
                continue
            if grid[(ii, jj)] == "#":
                continue
            if (ii, jj) in prev:
                continue
            copy = set()
            copy.update(prev)
            copy.add((i, j))
            if grid[(ii, jj)] == ".":
                stack.append((ii, jj, copy))
                continue
            di, dj = OFFSETS[grid[(ii, jj)]]
            iii, jjj = ii + di, jj + dj
            if (iii, jjj) in copy:
                continue
            copy.add((ii, jj))
            stack.append((iii, jjj, copy))

    return longest_path_length

def build_adjacency_list():
    adjacency_list = {}
    queue = collections.deque()
    queue.append((0,1))
    while queue:
        i, j = queue.popleft()
        if (i, j) in adjacency_list:
            continue
        adjacency_list[(i, j)] = {}
        for di, dj in OFFSETS.values():
            ii, jj = i + di, j + dj
            if (ii, jj) not in grid or grid[(ii, jj)] == "#":
                continue
            adjacency_list[(i, j)][(ii, jj)] = 1
            queue.append((ii, jj))

    # Prune the adjacency list by identifying nodes who have exactly two
    # neighbors, and connecting the two neighbors directly. This assumes the
    # graph is undirected (therefore can't be used for Part 1).
    while True:
        coord2 = next(
            (coord for coord in adjacency_list
             if len(adjacency_list[coord]) == 2),
            None
        )
        if not coord2:
            break

        coord1, coord3 = adjacency_list[coord2].keys()
        distance12 = adjacency_list[coord1][coord2]
        distance21 = adjacency_list[coord2][coord1]
        assert distance12 == distance21
        distance23 = adjacency_list[coord2][coord3]
        distance32 = adjacency_list[coord3][coord2]
        assert distance23 == distance32
        adjacency_list[coord1][coord3] = distance12 + distance23
        adjacency_list[coord3][coord1] = distance12 + distance23
        del adjacency_list[coord1][coord2]
        del adjacency_list[coord3][coord2]
        del adjacency_list[coord2]

    return adjacency_list

class PathNode:
    def __init__(self, i, j, prev=None, distance=0):
        self.i = i
        self.j = j
        self.prev = prev
        self.path_length = distance
        if self.prev:
            self.path_length += self.prev.path_length
    
    def contains(self, i, j):
        if i == self.i and j == self.j:
            return True
        if not self.prev:
            return False
        return self.prev.contains(i, j)
    
    def length(self):
        return self.path_length
    
    def most_recent(self):
        return self.i, self.j

def find_longest_path_length(adjacency_list):
    stack = []
    stack.append(PathNode(0, 1))
    longest_path_length = 0
    while stack:
        path = stack.pop()
        i, j = path.most_recent()
        if (i, j) == end:
            longest_path_length = max(path.length(), longest_path_length)
        for ii, jj in adjacency_list[(i, j)]:
            if path.contains(ii, jj):
                continue
            stack.append(PathNode(ii, jj, path, adjacency_list[(i, j)][(ii, jj)]))
    return longest_path_length

print("Part 1:", part1())

adjacency_list = build_adjacency_list()
print("Part 2:", find_longest_path_length(adjacency_list))
