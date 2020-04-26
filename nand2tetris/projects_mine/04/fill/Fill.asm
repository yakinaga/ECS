// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.


(LOOP)
@KBD
D=M
@CLEAR
D;JEQ // If 0, jump to CLEAR
@FILL
0;JMP // If not 0, jump to FILL

// Clear screen
(CLEAR)
@8191
D=A
(LOOP1)
@SCREEN
A=D+A
M=0  // Set all bits 0
D=D-1
@LOOP1
D;JGE
@CONTINUE
0;JMP

// Fill screen
(FILL)
@8191
D=A
(LOOP2)
@SCREEN
A=D+A
M=-1  // Set all bits 1
D=D-1
@LOOP2
D;JGE

(CONTINUE)
@LOOP
0;JMP
(END)
