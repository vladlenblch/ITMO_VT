ORG 0x0
V0: WORD $default, 0x180
V1: WORD $INT1, 0x180
V2: WORD $INT2, 0x180
V3: WORD $default, 0x180
V4: WORD $default, 0x180
V5: WORD $default, 0x180
V6: WORD $default, 0x180
V7: WORD $default, 0x180

ORG 0x24
X: WORD ?
max: WORD 0x0018
min: WORD 0xFFE6
default: IRET

START:
    DI
    CLA
    OUT 0x1
    OUT 0x7
    OUT 0xB
    OUT 0xD
    OUT 0x11
    OUT 0x15
    OUT 0x19
    OUT 0x1D

    LD #9
    OUT 3
    LD #0xA
    OUT 5

PROG:
    DI
    LD X
    NOP
    SUB #3
    CALL CHECK
    NOP
    ST X
    EI
    JUMP PROG

INT1:
    LD X
    NOP
    ASL
    ASL
    ADD X
    ADD #3
    OUT 2
    NOP
    IRET

TEMP: WORD ?
XOR_X: WORD ?
XOR_NOT_X: WORD ?
TEMP_IN: WORD ?

INT2:
    LD X
    NOP
    ST XOR_X
    NOT
    ST XOR_NOT_X

    IN 4
    SXTB
    ST TEMP_IN
    AND XOR_NOT_X
    ST TEMP

    LD TEMP_IN
    NOT
    AND XOR_X
    OR TEMP
    CALL CHECK
    ST X
    NOP
    IRET

CHECK:
CHECK_min:
    CMP min
    BPL CHECK_max
    JUMP LD_max
CHECK_max:
    CMP max
    BMI RETURN
LD_max:
    LD max
RETURN:
    RET
