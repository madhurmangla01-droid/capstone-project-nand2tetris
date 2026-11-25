// Box.asm
// Name: Madhur Mangla
// Roll No: 2501350087
// K = 87
//
// Draws a black box starting at row 87 (address 19168),
// 20 rows high and 64 pixels (4 words) wide while any key is pressed.
// Clears the box when the key is released.

(MAIN)
    @KBD
    D=M             // Read keyboard memory map (RAM[24576])
    @PRESSED
    D;JNE           // If any key is pressed (D != 0), jump to PRESSED

    @color
    M=0             // No key pressed -> set color to white (0)
    @DRAW
    0;JMP

(PRESSED)
    @color
    M=-1            // Key pressed -> set color to black (-1, all 16 bits 1)

(DRAW)
    @19168          // First screen address: 16384 + (32 * 87) = 19168
    D=A
    @addr
    M=D             // addr = 19168

    @20
    D=A
    @rows
    M=D             // rows = 20 (box height)

(ROWLOOP)
    @4
    D=A
    @cols
    M=D             // cols = 4 words (64 pixels wide)

    @addr
    D=M
    @ptr
    M=D             // ptr = start address of current row

(COLLOOP)
    @color
    D=M             // D = current color (-1 or 0)
    @ptr
    A=M             // Point A register to the screen memory address stored in ptr
    M=D             // Write color to screen RAM[ptr]

    @ptr
    M=M+1           // Move to next 16-bit word in the row

    @cols
    M=M-1           // Decrement word counter
    D=M
    @COLLOOP
    D;JGT           // Repeat until all 4 words in the row are drawn

    @32
    D=A
    @addr
    M=M+D           // Move addr down by 1 row (+32 words)

    @rows
    M=M-1           // Decrement row counter
    D=M
    @ROWLOOP
    D;JGT           // Repeat until all 20 rows are drawn

    @MAIN
    0;JMP           // Loop back to check keyboard state
