@256
D=A
@SP
M=D
// push constant 0
@0
D=A
@SP
A=M
M=D
@SP
M=M+1
// pop local 0
@LCL
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
// label loop_start
(null$loop_start)
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
// push local 0
@LCL
D=M
@0
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
// pop local 0
@LCL
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
// if-goto loop_start
@SP
A=M-1
D=M
@SP
M=M-1
@null$loop_start
D;JNE
// push local 0
@LCL
D=M
@0
AD=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1
