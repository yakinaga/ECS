@256
D=A
@SP
M=D
// push argument 1
@ARG
D=M
@1
AD=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1
// pop pointer 1
@3
D=A
@1
AD=D+A
@R13
M=D
@SP
A=M-1
D=M
@R13
A=M
M=D
@SP
M=M-1
// push constant 0
@0
D=A
@SP
A=M
M=D
@SP
M=M+1
// pop that 0
@THAT
D=M
@0
AD=D+A
@R13
M=D
@SP
A=M-1
D=M
@R13
A=M
M=D
@SP
M=M-1
// push constant 1
@1
D=A
@SP
A=M
M=D
@SP
M=M+1
// pop that 1
@THAT
D=M
@1
AD=D+A
@R13
M=D
@SP
A=M-1
D=M
@R13
A=M
M=D
@SP
M=M-1
// push argument 0
@ARG
D=M
@0
AD=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1
// push constant 2
@2
D=A
@SP
A=M
M=D
@SP
M=M+1
// sub
@SP
A=M-1
D=M
A=A-1
M=M-D
@SP
M=M-1
// pop argument 0
@ARG
D=M
@0
AD=D+A
@R13
M=D
@SP
A=M-1
D=M
@R13
A=M
M=D
@SP
M=M-1
// label main_loop_start
(null$main_loop_start)
// push argument 0
@ARG
D=M
@0
AD=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1
// if-goto compute_element
@SP
A=M-1
D=M
@SP
M=M-1
@null$compute_element
D;JNE
// goto end_program
@null$end_program
0;JMP
// label compute_element
(null$compute_element)
// push that 0
@THAT
D=M
@0
AD=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1
// push that 1
@THAT
D=M
@1
AD=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1
// add
@SP
A=M-1
D=M
A=A-1
M=D+M
@SP
M=M-1
// pop that 2
@THAT
D=M
@2
AD=D+A
@R13
M=D
@SP
A=M-1
D=M
@R13
A=M
M=D
@SP
M=M-1
// push pointer 1
@3
D=A
@1
AD=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1
// push constant 1
@1
D=A
@SP
A=M
M=D
@SP
M=M+1
// add
@SP
A=M-1
D=M
A=A-1
M=D+M
@SP
M=M-1
// pop pointer 1
@3
D=A
@1
AD=D+A
@R13
M=D
@SP
A=M-1
D=M
@R13
A=M
M=D
@SP
M=M-1
// push argument 0
@ARG
D=M
@0
AD=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1
// push constant 1
@1
D=A
@SP
A=M
M=D
@SP
M=M+1
// sub
@SP
A=M-1
D=M
A=A-1
M=M-D
@SP
M=M-1
// pop argument 0
@ARG
D=M
@0
AD=D+A
@R13
M=D
@SP
A=M-1
D=M
@R13
A=M
M=D
@SP
M=M-1
// goto main_loop_start
@null$main_loop_start
0;JMP
// label end_program
(null$end_program)
