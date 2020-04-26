// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

// ver.1 using symbols
// Initialize
@result
M=0
// Set counter
@1
D=M
@counter
M=D
// Set base
@0
D=M
@base
M=D
// Start
(LOOP)
// End if counter = 0
@END
@counter
MD=M-1
@END
D;JLT
// result += base
@base
D=M
@result
M=M+D
@LOOP
0;JMP
(END)
// copy result to RAM[2]
@result
D=M
@2
M=D
(FIN)
@FIN
0;JMP

