// push constant 111
@111
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 333
@333
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 888
@888
D=A
@SP
A=M
M=D
@SP
M=M+1
// pop static 8
@16
D=A
@8
AD=D+A
@13
M=D
@SP
A=M-1
D=M
@13
A=M
M=D
@SP
M=M-1
// pop static 3
@16
D=A
@3
AD=D+A
@13
M=D
@SP
A=M-1
D=M
@13
A=M
M=D
@SP
M=M-1
// pop static 1
@16
D=A
@1
AD=D+A
@13
M=D
@SP
A=M-1
D=M
@13
A=M
M=D
@SP
M=M-1
// push static 3
@16
D=A
@3
AD=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1
// push static 1
@16
D=A
@1
AD=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1
// sub/n@SP
A=M-1
D=M
A=A-1
M=M-D
@SP
M=M-1
// push static 8
@16
D=A
@8
AD=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1
// add/n@SP
A=M-1
D=M
A=A-1
M=D+M
@SP
M=M-1
