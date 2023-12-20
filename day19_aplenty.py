import math
import re

parts = []
workflows = {}
for line in open("day19_input.txt"):
    if line.startswith("{"):
        part = {category: int(value) for category, value in re.findall("(\w)=(\d+)", line)}
        parts.append(part)
        continue
    m = re.search("^(\w+)\{(.*)\}", line)
    if m:
        name = m.group(1)
        steps = m.group(2).split(",")
        workflow = []
        for step in steps:
            m = re.search("(\w)(>|<)(\d+):(\w+)", step)
            if m:
                category = m.group(1)
                comparator = m.group(2)
                threshold = int(m.group(3))
                result = m.group(4)
                workflow.append(((category, comparator, threshold), result))
            else:
                workflow.append((None, step))
        workflows[name] = workflow

def do_step(part, step):
    test, result = step
    if not test:
        return result
    category, comparator, threshold = test
    value = part[category]
    if comparator == ">" and value > threshold:
        return result
    if comparator == "<" and value < threshold:
        return result
    return None

def do_workflow(part, name):
    workflow = workflows[name]
    for step in workflow:
        result = do_step(part, step)
        if not result:
            continue
        if result == "A":
            return True
        if result == "R":
            return False
        return do_workflow(part, result)

total = 0
for part in parts:
    if do_workflow(part, "in"):
        total += sum(part.values())
print("Part 1:", total)

def update_bounds(bounds, test, passed):
    category, operator, threshold = test
    if operator == "<":
        update_bounds(bounds, (category, ">", threshold - 1), not passed)
        return
    low, high = bounds[category]
    if passed:
        bounds[category] = (max(threshold+1, low), high)
    else:
        bounds[category] = (low, min(threshold, high))

def combos(tests):
    bounds = {category: (1, 4000) for category in ["x", "m", "a", "s"]}
    for test, passed in tests:
        update_bounds(bounds, test, passed)
    return math.prod([max(0, high - low + 1) for low, high in bounds.values()])

def dfs(name, stepnum, tests):
    if name == "A":
        return combos(tests)
    if name == "R":
        return 0
    test, result = workflows[name][stepnum]
    if not test:
        return dfs(result, 0, tests)
    return (dfs(result, 0, tests + [(test, True)])
             + dfs(name, stepnum + 1, tests + [(test, False)]) )       

print("Part 2:", dfs("in", 0, []))