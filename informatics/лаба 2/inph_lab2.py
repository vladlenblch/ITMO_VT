file = open("result.txt", "w")


def output():   #основная функция, выводит ответ
    nums = [int(i) for i in message]
    s1 = nums[0] ^ nums[2] ^ nums[4] ^ nums[6]
    s2 = nums[1] ^ nums[2] ^ nums[5] ^ nums[6]
    s3 = nums[3] ^ nums[4] ^ nums[5] ^ nums[6]
    s_overall = s3 * 4 + s2 * 2 + s1
    bit = s_overall - 1
    bits = {0: 'r1', 1: 'r2', 2: 'i1', 3: 'r3', 4: 'i2', 5: 'i3', 6: 'i4'}
    if s_overall == 0:
        print("Переданное сообщение не содержит ошибок!")
        file.write("correct")
    else:
        nums[bit] = (nums[bit] + 1) % 2
        print("Ошибка в бите: " + bits[bit])
        print("Верное сообщение: " + str(nums[2]) + str(nums[4]) + str(nums[5]) + str(nums[6]))
        file.write(str(bits[bit]))


def correct_input():    #рекурсивная функция, проверяющая корректность ввода
    message = input()
    condition = len(message) == 7 and all(i in '01' for i in message)
    if not condition:
        print("Некорректный ввод. Попробуйте снова.")
        return correct_input()
    else:
        return message


message = correct_input()
output()
