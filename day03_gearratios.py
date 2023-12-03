

def part1():
    f = open("day03_input.txt", "r")
    input = []
    for line in f:
        input.append(line)
    allparts = set()
    for i in range(1, len(input) - 1):
        for j, c in enumerate(input[i]):
            if is_symbol(c):
                parts = process_symbol(input, i, j)
                allparts.update(parts)
    print(sum([part_number for part_number,_,_ in allparts]))


def part2():
    f = open("day03_input.txt", "r")
    input = []
    for line in f:
        input.append(line)
    total = 0
    for i in range(1, len(input) - 1):
        for j, c in enumerate(input[i]):
            if is_symbol(c):
                parts = process_symbol(input, i, j)
                if len(parts) == 2:
                    total += parts[0][0] * parts[1][0]
    print(total)

def is_symbol(c):
    if c.isdigit():
        return False
    if c == ".":
        return False
    if c == "\n":
        return False
    return True

def find_part_number(line, index):
    left = index
    while left > 0 and line[left-1].isdigit():
        left -= 1
    right = index
    while right < len(line) and line[right+1].isdigit():
        right += 1
    part_number = int(line[left:right+1])
    return part_number, right

OFFSETS = ((-1,-1), (-1,0), (-1,1),
            (0,-1), (0,1),
            (1,-1), (1, 0), (1,1))


def process_symbol(input, i, j):
    parts = set()
    for di, dj in OFFSETS:
        i2 = i+di
        j2 = j+dj
        if i2 < 0 or j2 < 0 or i2 == len(input) or j2 == len(input[0]):
            continue
        if input[i2][j2].isdigit():
            part_number, right = find_part_number(input[i2], j2)
            parts.add((part_number, i, right))
    return list(parts)

part1()
part2()
