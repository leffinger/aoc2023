input = open("day11_input.txt").read().split()

galaxies = []
for i, line in enumerate(input):
    for j, c in enumerate(line):
        if c == "#":
            galaxies.append((i, j))

empty_rows = set(range(len(input))).difference([g[0] for g in galaxies])
empty_cols = set(range(len(input[0]))).difference([g[1] for g in galaxies])

def distance_1d(a, b, empties, expansion_ratio):
    high = max(a,b)
    low = min(a,b)
    num_empty = len([x for x in empties if x > low and x < high])
    return high - low + (expansion_ratio - 1) * num_empty

def distance_2d(galaxy1, galaxy2, expansion_ratio):
    return (distance_1d(galaxy1[0], galaxy2[0], empty_rows, expansion_ratio)
            + distance_1d(galaxy1[1], galaxy2[1], empty_cols, expansion_ratio))

def total_distance(expansion_ratio):
    return sum([distance_2d(galaxies[i], galaxies[j], expansion_ratio)
                for i in range(len(galaxies))
                for j in range(i, len(galaxies))])

print("Part 1:", total_distance(2))
print("Part 2:", total_distance(1000000))