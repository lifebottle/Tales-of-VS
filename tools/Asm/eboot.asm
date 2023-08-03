.open "../../0_data/SYSDIR/EBOOT.BIN","../../3_patched/SYSDIR/EBOOT.BIN",0x8803FAC
.psp

; for standard print
; change this back to 0x7 for HW fix that breaks JP text
TEXT_WIDTH equ 0xE
DOUBLE_TEXT_WIDTH equ 0xC
ESCAPE_CHAR equ 0x24

; for vwf
SPACE_WIDTH equ 0x5
MIN_WIDTH equ 0x1
.definelabel sceFontGetCharInfo, 0x08a2e828

;Tales of Vs eboot
; change control character from % to $
.org 0x088BFE90
    li v1, ESCAPE_CHAR
.org 0x088BFF0C
    li v1, ESCAPE_CHAR
.org 0x088c3708
    li v1, ESCAPE_CHAR
.org 0x088c116c
    li v1, ESCAPE_CHAR

; fix menu item spacing
; divide strlen by 2
.org 0x088c03f4
    sra s0, v0, 0x1

; Name Keyboard Settings
.org 0x089CDA30
    sw zero, 0x10(v0)

; Default Name to Player - utf16 ascii
.org 0x08A32598
    .byte 0x50, 00, 0x6c, 00, 0x61, 00, 0x79, 00, 0x65, 00, 0x72, 0x00

; Text Spacing
.org 0x088C1008
    li v1, TEXT_WIDTH

.org 0x088C121C
    li a0, TEXT_WIDTH

.org 0x088C2214
    li a1, TEXT_WIDTH

; VWF ROUTINE
.org 0x088c2644
    addiu sp, sp, -0x20
    sw ra, 0x1c(sp)
    sw a0, 0x18(sp)
    sw a1, 0x14(sp)
    sw a0, 0x10(sp)
    sw s0, 0xc(sp)
    sw s1, 0x8(sp)
    sw s2, 0x4(sp)
    
    lw s0, 0x8(a1)
    move s1, a2

    ; need to get v0+2 bitmapleft first
    ; need to check for 0???
    lh a1, 0x2(v0)
    move a0, s0
    jal sceFontGetCharInfo
    lui a2, 0x9f7

    lui v0, 0x9f7
    lw s2, 0x8(v0)

    li v0, 0x20
    beq v0, s1, @@end
    li v0, SPACE_WIDTH

    move a0, s0
    move a1, s1
    jal sceFontGetCharInfo
    lui a2, 0x9f7
     ;v0 has width
    lui a2, 0x9f7
    lw v0, 0x0(a2)
    lw a2, 0x8(a2)
    addu v0, v0, a2
@@end:
    subu v0, v0, s2 ; subtract left?
    
    ;li a1, MIN_WIDTH
    ;blel v0, a1, @@real_end
    ;li v0, MIN_WIDTH

@@real_end:
    ; put v0 in f0 floating point shit
    mtc1 v0, f0
    cvt.s.w f0, f0
    lw ra, 0x1c(sp)
    lw s0, 0xc(sp)
    lw s1, 0x8(sp)
    lw s2, 0x4(sp)
    lw a0, 0x18(sp)
    lw a1, 0x14(sp)
    lw a0, 0x10(sp)
    jr ra
    addiu sp, sp, 0x20

; Standard smaller fixed width
; if switching to vwf comment these out
.org 0x088C26C8
    ;li v0, TEXT_WIDTH
    ;li v0, DOUBLE_TEXT_WIDTH

.close