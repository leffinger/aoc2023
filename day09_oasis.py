def recursive_derivative(nums):
    if all([num == 0 for num in nums]):
        return 0
    return nums[-1] + recursive_derivative([nums[i] - nums[i-1] for i in range(1, len(nums))])

part1_total = 0
part2_total = 0
for line in open("day09_input.txt"):
    part1_nums = [int(num) for num in line.split()]
    part2_nums = list(reversed(part1_nums))
    part1_total += recursive_derivative(part1_nums)
    part2_total += recursive_derivative(part2_nums)
print("Part 1:", part1_total)
print("Part 2:", part2_total)
