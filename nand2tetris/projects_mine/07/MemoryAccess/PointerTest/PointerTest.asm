// push constant 3030
@3030
D=A
@SP
A=M
M=D
@SP
M=M+1
// pop pointer 0
@3
D=A
@0
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
// push constant 3040
@3040
D=A
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
// push constant 32
@32
D=A
@SP
A=M
M=D
@SP
M=M+1
// pop this 2
@THIS
D=M
@2
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
// push constant 46
@46
D=A
@SP
A=M
M=D
@SP
M=M+1
// pop that 6
@THAT
D=M
@6
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
// push pointer 0
@3
D=A
@0
AD=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1
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
// add/n@SP
A=M-1
D=M
A=A-1
M=D+M
@SP
M=M-1
// push this 2
@THIS
D=M
@2
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
// push that 6
@THAT
D=M
@6
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