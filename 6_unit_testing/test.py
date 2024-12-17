nums = [3,3]
target = 6
output = []

for index in range(len(nums)):
    for index2 in range(len(nums)-1):
        result = nums[index] + nums[index2]
        if target == result:
            output = [index2, index]

print(output)