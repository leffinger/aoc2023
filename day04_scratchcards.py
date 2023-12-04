import re

f = open("day04_input.txt", "r")
part1_total = 0
upcoming_copies = []
part2_total = 0
for line in f:
    m = re.search(":(?P<winners>.*)\|(?P<mine>.*)$", line)
    winners = set(m.group("winners").rsplit())
    winners.intersection_update(m.group("mine").rsplit())
    if winners:
        part1_total += pow(2, len(winners) - 1)
    copies = upcoming_copies.pop(0) if upcoming_copies else 1
    part2_total += copies
    for i in range(len(winners)):
        if i < len(upcoming_copies):
            upcoming_copies[i] += copies
        else:
            upcoming_copies.append(copies + 1)
print("Part 1:", part1_total)
print("Part 2:", part2_total)
