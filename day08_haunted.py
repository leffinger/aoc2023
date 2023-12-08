import re
import math

f = open("day08_input.txt", "r")
directions = f.readline().rstrip()
f.readline()

network = {}
for line in f:
    m = re.search("(?P<src>\w+) = \((?P<left>\w+), (?P<right>\w+)\)", line)
    network[m.group("src")] = (m.group("left"), m.group("right"))

def steps(start, end_nodes):
    node = start
    i = 0
    while not node in end_nodes:
        if directions[i % len(directions)] == "L":
            node = network[node][0]
        else:
            node = network[node][1]
        i += 1
    return i

print("Part 1:", steps("AAA", ["ZZZ"]))

start_nodes = [node for node in network if node[-1] == "A"]
end_nodes = set([node for node in network if node[-1] == "Z"])
all_steps = [steps(start, end_nodes) for start in start_nodes]
print("Part 2:", math.lcm(*all_steps))
