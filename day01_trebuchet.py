import re

digits = {
    '0': 0,
    '1': 1,
    '2': 2,
    '3': 3,
    '4': 4,
    '5': 5,
    '6': 6,
    '7': 7,
    '8': 8,
    '9': 9,
    'zero': 0,
    'one': 1,
    'two': 2,
    'three': 3,
    'four': 4,
    'five': 5,
    'six': 6,
    'seven': 7,
    'eight': 8,
    'nine': 9,
}

f = open("day01_input.txt", "r")
total = 0
for line in f:
    # Part 1
    # x = re.findall("\d", line)
    # Part 2
    x = re.findall("(?=(zero|one|two|three|four|five|six|seven|eight|nine|\d))", line)
    if not x:
        continue
    value = digits[x[0]] * 10 + digits[x[-1]]
    total += value
print(total)

    