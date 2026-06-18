.data
input_addr:   .word 0x80
output_addr:  .word 0x84
remaining:    .word 0
input_left:   .word 0
word_count:   .word 0
out_buf:      .word 0, 0, 0, 0, 0, 0, 0, 0
out_buf_tail: .word 0, 0, 0, 0, 0, 0, 0, 0

.text
.org 0x100

_start:
    movea.l 0x1000, A7
    movea.l input_addr, A5
    movea.l (A5), A0
    movea.l output_addr, A5
    movea.l (A5), A1
    movea.l out_buf, A3

    move.l (A0), D0
    cmp.l 0, D0
    blt error
    beq empty_input

    move.l D0, D1
    add.l 3, D1
    div.l 4, D1
    movea.l input_left, A4
    move.l D1, (A4)

    move.l D0, D1
    and.l 1, D1
    cmp.l 0, D1
    bne drain_error

    movea.l remaining, A4
    move.l D0, (A4)
    movea.l word_count, A4
    move.l 0, (A4)

    move.l 4, D2
    move.l 0, D5
    move.l 0, D6
    move.l 0, D7

decode_loop:
    movea.l remaining, A4
    move.l (A4), D0
    cmp.l 0, D0
    beq finish_decode
    sub.l 2, D0
    move.l D0, (A4)

    jsr read_byte
    move.l D0, D3
    cmp.l 0, D3
    beq drain_error

    jsr read_byte
    move.l D0, D4

emit_run:
    move.l D4, D0
    and.l 0xff, D0
    cmp.l 0, D7
    beq emit_shift_24
    cmp.l 1, D7
    beq emit_shift_16
    cmp.l 2, D7
    beq emit_shift_8
    jmp emit_or

emit_shift_24:
    lsl.l 24, D0
    jmp emit_or

emit_shift_16:
    lsl.l 16, D0
    jmp emit_or

emit_shift_8:
    lsl.l 8, D0

emit_or:
    or.l D0, D6
    add.l 1, D5
    add.l 1, D7
    cmp.l 4, D7
    bne emit_next

    move.l D6, (A3)+
    movea.l word_count, A4
    move.l (A4), D0
    add.l 1, D0
    move.l D0, (A4)
    move.l 0, D6
    move.l 0, D7

emit_next:
    sub.l 1, D3
    cmp.l 0, D3
    bne emit_run
    jmp decode_loop

finish_decode:
    cmp.l 0, D7
    beq write_result
    move.l D6, (A3)+
    movea.l word_count, A4
    move.l (A4), D0
    add.l 1, D0
    move.l D0, (A4)

write_result:
    move.l D5, (A1)
    movea.l out_buf, A3
    movea.l word_count, A4
    move.l (A4), D3

write_words:
    cmp.l 0, D3
    beq end
    move.l (A3)+, D0
    move.l D0, (A1)
    sub.l 1, D3
    jmp write_words

empty_input:
    move.l 0, (A1)
    jmp end

drain_error:
    movea.l input_left, A4

drain_loop:
    move.l (A4), D0
    cmp.l 0, D0
    beq error
    move.l (A0), D1
    sub.l 1, D0
    move.l D0, (A4)
    jmp drain_loop

error:
    move.l -1, (A1)
    jmp end

read_byte:
    jsr load_word_if_needed
    move.l D1, D0
    cmp.l 0, D2
    beq read_shift_24
    cmp.l 1, D2
    beq read_shift_16
    cmp.l 2, D2
    beq read_shift_8
    jmp read_mask

read_shift_24:
    lsr.l 24, D0
    jmp read_mask

read_shift_16:
    lsr.l 16, D0
    jmp read_mask

read_shift_8:
    lsr.l 8, D0

read_mask:
    and.l 0xff, D0
    add.l 1, D2
    rts

load_word_if_needed:
    move.l D0, -(A7)
    cmp.l 4, D2
    bne load_word_done
    move.l (A0), D1
    movea.l input_left, A4
    move.l (A4), D0
    sub.l 1, D0
    move.l D0, (A4)
    move.l 0, D2

load_word_done:
    move.l (A7)+, D0
    rts

end:
    halt
