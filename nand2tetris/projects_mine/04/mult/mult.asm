// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

// ver.2 シンボル使用；R0, R1の小さい方をカウンターにして演算量減らす；テストスクリプトのrepeat回数を増やさないとエラーになる

// Initialize
@result
M=0
// Find min(R0, R1)
@0
D=M
@1
D=D-M
@R0_GE_R1
D;JGE
(R0_LT_R1) // counter: R0, base: R1
@0
D=M
@counter
M=D
@1
D=M
@base
M=D
@LOOP
0;JMP
(R0_GE_R1) // counter: R1, base: R0
@1
D=M
@counter
M=D
@0
D=M
@base
M=D

// Start
(LOOP)
// Terminate if counter = 0
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

