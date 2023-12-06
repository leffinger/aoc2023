import re
import collections

category_order = {}
category_ranges = collections.defaultdict(list)
for line in open("day05_input.txt"):
    if line.startswith("seeds:"):
        # this is always the first line, I'm just lazy
        seeds = [int(x) for x in re.findall("\d+", line)]
        seed_ranges = []
        for i in range(0, len(seeds), 2):
            seed_ranges.append((seeds[i], seeds[i]+seeds[i+1]))
        continue
    m = re.match("(?P<src>\w+)\-to\-(?P<dst>\w+) map:", line)
    if m:
        current_src = m.group("src")
        category_order[current_src] = m.group("dst")
        continue
    m = re.match("(?P<dst_start>\d+) (?P<src_start>\d+) (?P<length>\d+)", line)
    if m:
        src_start = int(m.group("src_start"))
        dst_start = int(m.group("dst_start"))
        length = int(m.group("length"))
        # store ranges as start, end, and offset (amount to be added to matching values)
        category_ranges[current_src].append((src_start, src_start + length, dst_start - src_start))

# Puts a single seed value through all of the transformations.
def process_seed(seed):
    src_category = "seed"
    src_value = seed
    while src_category != "location":
        dst_value = src_value
        for dst_start, dst_end, offset in category_ranges[src_category]:
            if src_value >= dst_start and src_value < dst_end:
                dst_value = src_value + offset
                break
        next_category = category_order[src_category]
        src_category = next_category
        src_value = dst_value
    return dst_value

# Part 1: process each seed and find the lowest final value.
lowest_location = None
for seed in seeds:
    dst_value = process_seed(seed)
    if lowest_location:
        lowest_location = min(lowest_location, dst_value)
    else:
        lowest_location = dst_value
print("Part 1:", lowest_location)

# Part 2, step 1: Given two sets of ranges, split the first set such that
# any range in the first set is either entirely contained by a single destination
# range, or does not intersect with any destination ranges.
def split_ranges(src_ranges, dst_ranges_with_offsets):
    result = []
    while src_ranges:
        src_start, src_end = src_ranges.pop(0)
        intersected = False
        for dst_start, dst_end, _ in dst_ranges_with_offsets:
            if src_start >= dst_end or src_end <= dst_start:
                continue
            intersected = True
            if src_start >= dst_start and src_start < dst_end:
                # src range starts in dst range
                if src_end <= dst_end:
                    # entirely contained in the dst range
                    result.append((src_start, src_end))
                else:
                    # split into two ranges around dst_end
                    result.append((src_start, dst_end))
                    src_ranges.append((dst_end, src_end))
            else:
                # src range starts before dst_range
                if src_end <= dst_end:
                    # split into two ranges around dst_start
                    src_ranges.append((src_start, dst_start))
                    result.append((dst_start, src_end))
                else:
                    # split into three ranges
                    src_ranges.append((src_start, dst_start))
                    result.append((dst_start, dst_end))
                    src_ranges.append((dst_end, src_end))
            break
        if not intersected:
            result.append((src_start, src_end))
    return result

# Part 2, step 2: transform all src ranges through one step.
def map_ranges(src_ranges, dst_ranges_with_offsets):
    result = []
    for src_start, src_end in src_ranges:
        found = False
        for dst_start, dst_end, offset in dst_ranges_with_offsets:
            if src_start >= dst_start and src_end <= dst_end:
                found = True
                result.append((src_start+offset, src_end+offset))
                break
        if not found:
            result.append((src_start, src_end))
    return result

# Part 2, combined: repeatedly split, map, split, map until you're done.
src_category = "seed"
src_ranges = seed_ranges.copy()
while src_category != "location":
    dst_ranges_with_offsets = category_ranges[src_category]
    src_ranges = split_ranges(src_ranges, dst_ranges_with_offsets)
    src_ranges = map_ranges(src_ranges, dst_ranges_with_offsets)
    src_category = category_order[src_category]
lowest_location = min([src_start for src_start, _ in src_ranges])
print("Part 2:", lowest_location)