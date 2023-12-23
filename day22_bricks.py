import re
import collections

brick_start = {}
brick_end = {}
brick_num = 0
for line in open("day22_input.txt"):
    x1, y1, z1, x2, y2, z2 = [int(x) for x in re.findall("\d+", line)]
    brick_start[brick_num] = (x1, y1, z1)
    brick_end[brick_num] = (x2, y2, z2)
    brick_num += 1

grid = {}
for i in brick_start:
    x1, y1, z1 = brick_start[i]
    x2, y2, z2 = brick_end[i]
    for x in range(x1, x2 + 1):
        for y in range(y1, y2 + 1):
            for z in range(z1, z2 + 1):
                grid[(x, y, z)] = i

# Sort the bricks by z coordinate in ascending order (literally).
bottoms_up = [(coord[2], i) for i, coord in brick_start.items()]
bottoms_up.sort()
blockers = collections.defaultdict(set)
blocking = collections.defaultdict(set)
for _, i in bottoms_up:
    # Figure out how far the brick can fall, and which bricks are preventing
    # it from falling further.
    x1, y1, z1 = brick_start[i]
    x2, y2, z2 = brick_end[i]
    final_decrement = z1 - 1
    for decrement in range(1, z1):
        occupied = False
        for x in range(x1, x2 + 1):
            for y in range(y1, y2 + 1):
                for z in range(z1, z2 + 1):
                    if (x, y, z - decrement) not in grid:
                        continue
                    j = grid[(x, y, z - decrement)]
                    if i == j:
                        # A brick cannot be blocked by itself.
                        continue
                    occupied = True
                    final_decrement = decrement - 1
                    blockers[i].add(j)
                    blocking[j].add(i)
        if occupied:
            break

    # Move the brick to its new position before processing the next brick.
    for x in range(x1, x2 + 1):
        for y in range(y1, y2 + 1):
            for z in range(z1, z2 + 1):
                del grid[(x, y, z)]
                grid[(x, y, z - final_decrement)] = i
    brick_start[i] = (x1, y1, z1 - final_decrement)
    brick_end[i] = (x2, y2, z2 - final_decrement)

# A brick can be disintegrated if it is not the only brick blocking another
# brick from falling.
disintegrate_count = 0
for i in brick_start:
    ok = True
    for j in blocking[i]:
        if len(blockers[j]) == 1:
            ok = False
    if ok:
        disintegrate_count += 1
print("Part 1:", disintegrate_count)

# If we disintegrate a brick, any bricks for which it was the sole blocker will
# fall one level. Then the bricks on the next level will fall if they no longer
# have any blockers, and so on.
fallen_count = 0
for i in brick_start:
    fallen = set([i])
    falling = collections.deque()
    falling.extend(blocking[i])
    while falling:
        j = falling.popleft()
        if fallen.issuperset(blockers[j]):
            fallen.add(j)
            falling.extend(blocking[j])
    fallen_count += len(fallen) - 1
print("Part 2:", fallen_count)