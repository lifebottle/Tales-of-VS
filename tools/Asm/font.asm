.open "../../0_data/USRDIR/FONT/tcretab_14.pgf","../../3_patched/USRDIR/FONT/tcretab_14.pgf", 0x00
.psp

; Change the height of the tilde
.org 0x01BD6C
    .byte 0x30


.close