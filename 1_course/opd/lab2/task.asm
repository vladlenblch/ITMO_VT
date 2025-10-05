ORG 0x000
WORD 0x0831          ; ячейка памяти для первого числа. 000
WORD 0x0012          ; ячейка памяти для второго числа. 001
WORD 0x0010          ; счетчик сдвигов. 002
WORD 0x0000          ; ячейка памяти для результата. 003

START:               ; 004
CLA                  ; 005
LD 0x001             ; 006
ROR                  ; 007
ST 0x001             ; 008
BHIS SUM             ; 009
LD 0x000             ; 00A
ASL                  ; 00B
ST 0x000             ; 00C
LOOP 0x002           ; 00D
JUMP 0x004           ; 00E
HLT                  ; 00F

SUM:                 ; 010
LD 0x003             ; 011
ADD 0x000            ; 012
ST 0x003             ; 013
LD 0x002             ; 014
BEQ SAVE_RESULT      ; 015
JUMP 0x009           ; 016
HLT                  ; 017

SAVE_RESULT:         ; 018
LD 0x003             ; 019
ST 0x777             ; 01A
HLT                  ; 01B
