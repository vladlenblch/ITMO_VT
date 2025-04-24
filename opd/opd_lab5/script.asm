ORG 0x40D
LENADR2:
    WORD $LENGTH2
LENADR:
    WORD $LENGTH
ADR:
    WORD $RES
START:
    CLA
LEN:
    IN 7
    AND #0x40
    BEQ LEN
    IN 6
    ST (LENADR)
    LD (LENADR)
    ST (LENADR2)
    CLA
CHECK1:
    LD (LENADR)
    DEC
    ST (LENADR)
    BMI ENDING
    CLA
SUM1:
    IN 7
    AND #0x40
    BEQ SUM1
    IN 6
    SWAB
    ST (ADR)
CHECK2:
    LD (LENADR)
    DEC
    ST (LENADR)
    BMI ENDING
    CLA
SUM2:
    IN 7
    AND #0x40
    BEQ SUM2
    LD (ADR)
    IN 6
    ST (ADR)+
    JUMP CHECK1
ENDING:
    LD (LENADR2)
    ST (LENADR)
    CLA
    ST (LENADR2)
    HLT
ORG 0x553
LENGTH2:
    WORD 0
LENGTH:
    WORD 0
RES:
    WORD 0
