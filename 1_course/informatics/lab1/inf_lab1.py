num = int(input())
fib_nums = [1, 1]
final = 0

for i in range(len(str(num)) - 1):
    fib_nums.append(fib_nums[-1] + fib_nums[-2])
fib_nums = fib_nums[::-1]

c = 0
for i in str(num):
    if i == '1':
        final += fib_nums[c]
    c += 1

print(final)
