import math
import re
from functools import reduce

f = open("day06_input.txt", "r")
lines = f.read().split("\n")

times = [int(x) for x in re.findall("\d+", lines[0])]
record_distances = [int(x) for x in re.findall("\d+", lines[1])]

wins = []
for i, total_time in enumerate(times):
    distances = []
    for hold_time in range(total_time + 1):
        distances.append(hold_time * (total_time - hold_time))
    wins.append(len([x for x in distances if x > record_distances[i]]))
print("Part 1:", math.prod(wins))

part2_time = int(reduce(lambda x, y: x + str(y), times, ''))
part2_record = int(reduce(lambda x, y: x + str(y), record_distances, ''))

# We can use the quadratic formula to solve this.
#
# record = hold_time * (total_time - hold_time)
# i.e. r = x * (t - x)
#      r = tx - x^2
#      x^2 - tx + r = 0
# Subbing into the quadratic formula:
#   a = 1
#   b = -t
#   c = r
# So the zeroes of the equation are:
#   (t +/- sqrt(t^2 - 4r))/2
sqrt = math.sqrt(part2_time * part2_time - 4 * part2_record)
low_x = (part2_time - sqrt) / 2
high_x = (part2_time + sqrt) / 2
# The total number of wins is the number of whole numbers between low and high.
print("Part 2:", int(high_x - low_x))