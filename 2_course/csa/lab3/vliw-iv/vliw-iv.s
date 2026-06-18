.data
input_addr:  .word 0x80
output_addr: .word 0x84
fnv_prime:   .word 0x01000193
hash_init:   .word 0x811C9DC5

.text
.org 0x88
_start:
    lui t0, %hi(input_addr)      / lui t1, %hi(output_addr)      / nop          / nop
    addi t0, t0, %lo(input_addr) / addi t1, t1, %lo(output_addr) / nop          / nop
    lui t2, %hi(fnv_prime)       / lui t3, %hi(hash_init)        / lw t0, 0(t0) / nop
    addi t2, t2, %lo(fnv_prime)  / addi t3, t3, %lo(hash_init)   / lw t1, 0(t1) / nop
    nop                          / nop                           / lw t2, 0(t2) / nop
    nop                          / nop                           / lw t3, 0(t3) / nop

loop:
    mul t5, t3, t2               / nop                           / lw t4, 0(t0) / nop
    nop                          / nop                           / nop          / beqz t4, end
    xor t3, t5, t4               / nop                           / nop          / j loop

end:
    nop                          / nop                           / sw t3, 0(t1) / nop
    nop                          / nop                           / nop          / halt
