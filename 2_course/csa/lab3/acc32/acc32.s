.data
.org 0x100

input_num: .word 0
count: .word 0
i: .word 31
one: .word 1
thirty_two: .word 32

.text
.org 0x200

_start:
    load_addr 0x80
    store_addr input_num
    beqz is_zero

    jmp loop

is_zero:
    load_addr thirty_two
    store_addr 0x84
    jmp end

loop:
    load_addr i
    ble end

    load_addr input_num
    shiftr i
    and one
    bnez found_one

    load_addr count
    add one
    store_addr count

    load_addr i
    sub one
    store_addr i

    jmp loop

found_one:
    load_addr count
    store_addr 0x84

end:
    halt
