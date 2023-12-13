def make_splits(puzzle, split, horizontal):
    length = len(puzzle) if horizontal else len(puzzle[0])
    fanout = min(split, length - split)
    if horizontal:
        top = puzzle[split - fanout:split][::-1]
        bottom = puzzle[split:split + fanout]
        return top, bottom
    left = [[puzzle[j][i] for j in range(len(puzzle))] for i in range(split - fanout, split)][::-1]
    right = [[puzzle[j][i] for j in range(len(puzzle))] for i in range(split, split + fanout)]
    return left, right

def compare(region1, region2, max=1):
    total_differences = 0
    for i in range(len(region1)):
        for j in range(len(region1[i])):
            if region1[i][j] != region2[i][j]:
                total_differences += 1
                if total_differences == max:
                    return total_differences
    return total_differences

def find_split(puzzle, num_expected_diffs=0):
    for split in range(1, len(puzzle)):
        top, bottom = make_splits(puzzle, split, True)
        if compare(top, bottom, num_expected_diffs + 1) == num_expected_diffs:
            return 100 * split
    for split in range(1, len(puzzle[0])):
        left, right = make_splits(puzzle, split, False)
        if compare(left, right, num_expected_diffs + 1) == num_expected_diffs:
            return split

puzzles = [puzzle.split("\n") for puzzle in open("day13_input.txt").read().split("\n\n")]
print("Part 1:", sum([find_split(puzzle) for puzzle in puzzles]))
print("Part 2:", sum([find_split(puzzle, 1) for puzzle in puzzles]))
