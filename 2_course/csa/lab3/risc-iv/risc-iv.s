.data
input_addr:    .word 0x80
output_addr:   .word 0x84

.text
.org 0x100
_start:
    lui t0, %hi(input_addr)
    addi t0, t0, %lo(input_addr)
    lw t2, 0(t0)
    lw t2, 0(t2)

    addi t4, zero, 10

    ble t2, zero, neg
    j loop

neg:
    sub t2, zero, t2
    
loop:
    beqz t2, end
    rem t3, t2, t4
    div t2, t2, t4
    add t5, t5, t3
    j loop

end:
    lui t1, %hi(output_addr)
    addi t1, t1, %lo(output_addr)
    lw t1, 0(t1)
    sw t5, 0(t1)
    halt

; t0 = адрес инпут порта
; t1 = адрес оутпут порт
; t2 = число с которым работаем
; t3 = остаток
; t4 = 10
; t5 = сумма
