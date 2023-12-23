from enum import Enum

class GardenPlot(Enum):
    EMPTY = 0
    ROCK = 1

class Corner(Enum):
    NW = 0
    NE = 1
    SW = 2
    SE = 3

OFFSETS = [(1, 0), (-1, 0), (0, 1), (0, -1)]

input = open("day21_input.txt").read().split()
width = len(input)
assert len(input[0]) == width
grid = {}
start = (0, 0)
for i in range(width):
    for j in range(width):
        grid[(i,j)] = GardenPlot.ROCK if input[i][j] == "#" else GardenPlot.EMPTY
        if input[i][j] == "S":
            start = (i, j)

def reachable_after_step(reachable):
    next_reachable = set()
    for i, j in reachable:
        for di, dj in OFFSETS:
            ii, jj = i + di, j + dj
            if (ii, jj) in grid and grid[(ii, jj)] == GardenPlot.EMPTY:
                next_reachable.add((ii, jj))
    return next_reachable

reachable = set()
reachable.add(start)
for _ in range(64):
    reachable = reachable_after_step(reachable)
print("Part 1:", len(reachable))

odd_reachable = set()
even_reachable = set()
odd_reachable.add(start)
for _ in range(0, width, 2):
    even_reachable = reachable_after_step(odd_reachable)
    odd_reachable = reachable_after_step(even_reachable)

def is_in_corner(i, j, corner, inclusive):
    i = i - width // 2
    j = j - width // 2
    if abs(i) + abs(j) < width // 2:
        return False
    if not inclusive and abs(i) + abs(j) == width // 2:
        return False
    match corner:
        case Corner.NW:
            return i <= 0 and j <= 0
        case Corner.NE:
            return i <= 0 and j >= 0
        case Corner.SW:
            return i >= 0 and j <= 0
        case Corner.SE:
            return i >= 0 and j >= 0

left_chunk = [(i, j) for i, j in even_reachable if not(is_in_corner(i, j, Corner.NW, False) or is_in_corner(i, j, Corner.SW, False))]
right_chunk = [(i, j) for i, j in even_reachable if not(is_in_corner(i, j, Corner.NE, False) or is_in_corner(i, j, Corner.SE, False))]
top_chunk = [(i, j) for i, j in even_reachable if not(is_in_corner(i, j, Corner.NW, False) or is_in_corner(i, j, Corner.NE, False))]
bottom_chunk = [(i, j) for i, j in even_reachable if not(is_in_corner(i, j, Corner.SW, False) or is_in_corner(i, j, Corner.SE, False))]

nw_corner = [(i, j) for i, j in odd_reachable if is_in_corner(i, j, Corner.NW, True)]
ne_corner = [(i, j) for i, j in odd_reachable if is_in_corner(i, j, Corner.NE, True)]
sw_corner = [(i, j) for i, j in odd_reachable if is_in_corner(i, j, Corner.SW, True)]
se_corner = [(i, j) for i, j in odd_reachable if is_in_corner(i, j, Corner.SE, True)]

without_nw_corner = [(i, j) for i, j in even_reachable if not is_in_corner(i, j, Corner.NW, False)]
without_ne_corner = [(i, j) for i, j in even_reachable if not is_in_corner(i, j, Corner.NE, False)]
without_sw_corner = [(i, j) for i, j in even_reachable if not is_in_corner(i, j, Corner.SW, False)]
without_se_corner = [(i, j) for i, j in even_reachable if not is_in_corner(i, j, Corner.SE, False)]

X = 26501365 // width
total = X * X * len(odd_reachable)
total += (X - 1) * (X - 1) * len(even_reachable)
total += len(left_chunk) + len(right_chunk) + len(top_chunk) + len(bottom_chunk)
total += X * (len(nw_corner) + len(ne_corner) + len(sw_corner) + len(se_corner))
total += (X - 1) * (len(without_ne_corner) + len(without_nw_corner) + len(without_se_corner) + len(without_sw_corner))
print("Part 2:", total)
