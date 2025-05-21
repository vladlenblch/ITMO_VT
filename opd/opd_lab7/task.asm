ORG 0x0A0
result: WORD ?

status1: WORD ?
status2: WORD ?
status3: WORD ?

result1: WORD 0x3333
arg11: WORD 0x1111
arg12: WORD 0x2222

result2: WORD 0xFFFF
arg21: WORD 0xFFFE
arg22: WORD 1

result3: WORD 0x8000
arg31: WORD 2768
arg32: WORD 30000

START:
    CALL TEST1
    CALL TEST2
    CALL TEST3
    LD status1
    AND status2
    AND status3
    ST result
    HLT

TEST1:
    LD arg11
    PUSH
    LD arg12
    PUSH
    WORD 0x0F10
    POP
    CMP result1
    BEQ SUCCESS1

ERROR1:
    POP
    POP
    CLA
    CLC
    RET

SUCCESS1:
    LD #1
    ST status1
    POP
    POP
    CLC
    CLA
    RET

TEST2:
    LD arg21
    PUSH
    LD arg22
    PUSH
    WORD 0x0F10
    POP
    CMP result2
    BEQ SUCCESS2

ERROR2:
    POP
    POP
    CLA
    CLC
    RET

SUCCESS2:
    LD #1
    ST status2
    POP
    POP
    CLA
    CLC
    RET

TEST3:
    LD arg31
    PUSH
    LD arg32
    PUSH
    WORD 0x0F10
    BVC ERROR3
    POP
    CMP result3
    BEQ SUCCESS3

ERROR3:
    POP
    POP
    CLA
    CLC
    RET

SUCCESS3:
    LD #1
    ST status3
    POP
    POP
    CLA
    CLC
    RET
