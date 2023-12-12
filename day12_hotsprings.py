
memotable = {}

def memoized_num_valid_configs(conditions, contiguous, counts):
    key = conditions + "+" + str(contiguous) + "+" + ",".join([str(x) for x in counts])
    if key in memotable:
        return memotable[key]
    value = num_valid_configs(conditions, contiguous, counts)
    memotable[key] = value
    return value

# `contiguous` is the number of expected contiguous "#" symbols at the beginning of the input.
# contiguous == n > 0 means we expect n more "#"" (or "?") symbols.
# contiguous == 0 means the next symbol must be ".", "?", or end of input.
# contiguous == -1 means the next symbol can be anything.
def num_valid_configs(conditions, contiguous, counts):
    if conditions == "":
        # No more input to be processed
        if (contiguous == -1 or contiguous == 0) and counts == []:
            return 1
        return 0
    if counts == [] and contiguous == 0:
        # No more #s expected.
        match conditions[0]:
            case "#":
                return 0
            case "." | "?":
                return memoized_num_valid_configs(conditions[1:], 0, [])
    if contiguous == 0:
        # Next symbol must not be #.
        match conditions[0]:
            case "#":
                return 0
            case "." | "?":
                return memoized_num_valid_configs(conditions[1:], -1, counts)
    if contiguous == -1:
        # Next symbol can be anything. This is where we branch in the decision tree.
        match conditions[0]:
            case "#":
                if counts == []:
                    return 0
                return memoized_num_valid_configs(conditions[1:], counts[0] - 1, counts[1:])
            case ".":
                return memoized_num_valid_configs(conditions[1:], -1, counts)
            case "?":
                return (memoized_num_valid_configs(conditions[1:], counts[0] - 1, counts[1:])
                        + memoized_num_valid_configs(conditions[1:], -1, counts))
    # Next symbol must be #.
    match conditions[0]:
        case "#" | "?":
            return memoized_num_valid_configs(conditions[1:], contiguous - 1, counts)
        case ".":
            return 0
    assert(False)

part1_total = 0
part2_total = 0
for line in open("day12_input.txt"):
    conditions, counts = line.split()
    counts = [int(x) for x in counts.split(",")]
    part1_total += memoized_num_valid_configs(conditions, -1, counts)
    conditions = "?".join([conditions for x in range(5)])
    counts = counts * 5
    part2_total += memoized_num_valid_configs(conditions, -1, counts)
print("Part 1:", part1_total)
print("Part 2:", part2_total)

