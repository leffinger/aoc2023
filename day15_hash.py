import re
import collections

def HASH(input):
    result = 0
    for c in input:
        result += ord(c)
        result *= 17
        result %= 256
    return result

inputs = open("day15_input.txt").read().rstrip().split(",")
print("Part 1:", sum([HASH(input) for input in inputs]))

HASHMAP = collections.defaultdict(list)
for input in inputs:
    m = re.search("(\w+)=(\d)", input)
    if m:
        label = m.group(1)
        focus_length = int(m.group(2))
        box = HASH(label)
        lenses = HASHMAP[box]
        replaced = False
        for i in range(len(lenses)):
            if lenses[i][0] == label:
                lenses[i] = (label, focus_length)
                replaced = True
                break
        if not replaced:
            lenses.append((label, focus_length))

    m = re.search("(\w+)\-", input)
    if m:
        label = m.group(1)
        box = HASH(label)
        lenses = HASHMAP[box]
        for i in range(len(lenses)):
            if lenses[i][0] == label:
                lenses.pop(i)
                break

total = 0
for box in HASHMAP:
    for i in range(len(HASHMAP[box])):
        label, focus_length = HASHMAP[box][i]
        total += (box + 1) * (i + 1) * focus_length
print("Part 2:", total)

