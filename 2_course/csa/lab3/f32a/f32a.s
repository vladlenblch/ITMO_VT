.data
.org 0x00
buf: .byte '________________________________'

.text
.org 0x100
_start:
    lit 0x84                \ 0x84 -> dataStack
    b!                      \ dataStack -> B

    lit buf                 \ 0x00 -> dataStack
    a!                      \ dataStack -> A

read_loop:
    @p 0x80                 \ i_char -> dataStack

    dup                     \ i_char -> dataStack
    lit 10                  \ 10 -> dataStack ('\n' = 10)
    x_minus_c               \ i_char - 10 -> dataStack
    if success              \ if dataStack == 0: success

    a                       \ A -> dataStack
    lit 31                  \ 31 -> dataStack
    x_minus_c               \ A - 31 -> dataStack
    if overflow             \ if dataStack == 0 && not success: overflow

    dup                     \ char -> dataStack
    lit 97                  \ 97 ('a') -> dataStack
    x_minus_c               \ char - 97 -> dataStack
    -if check               \ jump to check if char >= 'a'

    store_buf ;             \ otherwise jump to store_buf

check:
    dup                     \ char -> dataStack
    lit 122                 \ 122 ('z') -> dataStack
    c_minus_x               \ 122 - char -> dataStack
    -if make_upper          \ jump to make_upper if char <= 'z'

    store_buf ;             \ otherwise jump to store_buf

make_upper:
    lit -32                 \ -32 -> dataStack
    +                       \ lowercase to uppercase -> dataStack

store_buf:
    !+                      \ char -> mem[A], A += 1
    read_loop ;             \ jump to read_loop

success:
    drop                    \ remove x_minus_c from dataStack
    lit 0                   \ 0x00 -> dataStack
    !+                      \ null-terminator -> mem[A], A += 1

    fill_tail_check         \ call fill_tail_check

    lit buf                 \ 0x00 -> dataStack
    a!                      \ dataStack -> A

output_loop:
    @                       \ mem[A] -> dataStack
    lit 255                 \ 255 -> dataStack
    and                     \ keep low byte of mem[A] -> dataStack

    dup                     \ keep low byte of mem[A] -> dataStack
    if output_done          \ if low byte of mem[A] == 0: end of string

    !b                      \ dataStack -> mem[B]
    a                       \ A -> dataStack
    lit 1                   \ 1 -> dataStack
    +                       \ A + 1 -> dataStack
    a!                      \ dataStack -> A
    output_loop ;           \ jump to output_loop

output_done:
    drop                    \ remove duplicated zero byte
    end ;                   \ jump to halt

overflow:
    drop                    \ remove overflowing char from dataStack
    lit buf                 \ 0x00 -> dataStack 
    a!                      \ dataStack -> A
    fill_tail_check         \ call fill_tail_check: restore buf with '_'
    lit -858993460          \ 0xCCCCCCCC -> dataStack
    !b                      \ dataStack -> mem[B]
    end ;                   \ jump to halt

end:
    halt                    \ stop

fill_tail_check:
    a                       \ A -> dataStack
    lit 31                  \ 31 -> dataStack
    c_minus_x               \ 31 - A -> dataStack
    -if fill_tail_step      \ if A <= 31: continue filling with '_'
    ;                       \ return to caller

fill_tail_step:
    lit 0x5f5f5f5f          \ 0x5f5f5f5f -> dataStack
    !                       \ 4 '_' at mem[A]
    a                       \ A -> dataStack
    lit 4                   \ 4 -> dataStack
    +                       \ A + 4 -> dataStack
    a!                      \ dataStack -> A
    fill_tail_check ;       \ jump to fill_tail_check

x_minus_c:                  \ dataStack: x c -> dataStack: x - c
    inv lit 1 + + ;

c_minus_x:                  \ dataStack: x c -> dataStack: c - x
    over inv lit 1 + + ;
