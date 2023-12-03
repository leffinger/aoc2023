import re

maxcounts = {
    "red": 12,
    "green": 13,
    "blue": 14,
}

f = open("day02_input.txt")
part1_total = 0
part2_total = 0
for line in f:
    x = re.match("Game (?P<gameno>\d+):(?P<games>.*)$", line)
    gameno = int(x.group("gameno"))
    games = x.group("games").split("; ")
    possible = True
    mincounts = {color: 0 for color in ["red", "green", "blue"]}
    for game in games:
        x = re.findall("(\d+) (red|blue|green)", game)
        for count, color in x:
            count = int(count)
            # Part 1
            if count > maxcounts[color]:
                possible = False
            # Part 2
            mincounts[color] = max(count, mincounts[color])
    # Part 1
    if possible:
        part1_total += gameno
    # Part 2
    power = mincounts["red"] * mincounts["green"] * mincounts["blue"]
    part2_total += power
print("Part 1:", part1_total)
print("Part 2:", part2_total)