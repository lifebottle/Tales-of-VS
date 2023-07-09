.open "D:/Tales/tales_vs/PSP_GAME/SYSDIR/ULJS00209.BIN","D:/Tales/tales_vs/PSP_GAME/SYSDIR/EBOOT.BIN",0x8803FAC
.psp

; for standard print
TEXT_WIDTH equ 0x7
DOUBLE_TEXT_WIDTH equ 0xC

; for vwf
SPACE_WIDTH equ 0x5
MIN_WIDTH equ 0x1
.definelabel sceFontGetCharInfo, 0x08a2e828

;Tales of Vs eboot
.org 0x088C1008
    li v1, TEXT_WIDTH

.org 0x088C121C
    li a0, TEXT_WIDTH

; weird cutscene thing that breaks shit
.org 0x088C251C
    nop

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

.org 0x088C2214
    li a1, TEXT_WIDTH

.close