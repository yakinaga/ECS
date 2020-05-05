import os
import sys
import re
import glob
import argparse

"""
バーチャルマシン(VM)プログラムをHackアセンブリに変換する（#2: 完全版）
Usage: $ python VMtranslator.py <prog_dir>
* prog_dirは.vmファイル群が置かれたディレクトリパス
* 出力：prog_dirディレクトリ下にprog_dir.asmが生成される

Parserクラス
* アトリビュート
** self.vm ... .vmファイルのデスクリプタ
** self.row ... 現在読み込んでいる行
** self.command ... 現在読み込んでいるコマンド
* __init__() ... アドリビュートを初期化
* hasMoreCommands() ... self.vmから1行読んでEOFならFalse. コメント削除&strip()してブランクにならなければTrue.
                         ブランクなら次の行を読み込んで繰り返し。Trueの時は読み込んだ行をself.rowに格納
* advance() ... self.rowかのコメントを除去しstrip()　→self.commandに格納
* commandType(str) ... コマンド(str)の種類を返す
* arg1() ... コマンドの第1引数を返す。C_ARITHMETICの場合はコマンド自身を返す
* arg2() ... コマンドの第2引数を返す

CodeWriterクラス
* アトリビュート
** self.asm ... 出力ファイルのデスクリプタ
** self.vm ... 現在読み込まれている.vmファイル名
** self.label_id ... .asmのL_COMMANDに使うラベルの通し番号。開始は1
** self.func_name ... 現在の関数名（初期値は"null"）
** self.ln ... ROMアドレス（コメントと擬コードを除いた行番号；0開始）。※デバッグ用途のみ
* __init__() ... アトリビュートの初期化
* _getLabel() ... self.label_idからユニークなラベル文字列を生成して返す。self.label_idをインクリメントする
* _outCommand(str) ... str型の引数にROMアドレスself.lnと改行コードをつけて返し、ROMアドレスをインクリメント
* setFileName(str) ... self.vmを設定
* writeInit() ... ブートストラップコードを書き込む。SP=256に初期化し、Sys.initをcall（writeCall("Sys.init", 0)を実行）
* writeArithmetic(str) ... 9種類のarithmeticコマンドをHackアセンブリに変換して出力ファイルに書き込む
* writePushPop(str1, str2, int) ... push, popコマンドをHackアセンブリに変換して出力ファイルに書き込む
* writeLabel(str) ... labelコマンドを変換して出力ファイルに書き込む
* writeGoto(str) ... gotoコマンドを変換して出力ファイルに書き込む
* writeIf(str) ... if-gotoコマンドを変換して出力ファイルに書き込む
* writeCall(str, int) ... callコマンドを変換して出力ファイルに書き込む
* writeReturn() ... returnコマンドを変換して出力ファイルに書き込む
* writeFunction(str, int) ... functionコマンドを変換して出力ファイルに書き込む
** R[13]-R[15]の領域は汎用レジスタとしてpopコマンドの変換で使用
* close() ... 出力ファイルをクローズ
"""

#
# Constants
#
C_ARITHMETIC = 0
C_PUSH = 1
C_POP = 2
C_LABEL = 3
C_GOTO = 4
C_IF = 5
C_FUNCTION = 6
C_RETURN = 7
C_CALL = 8

#
# Class definitions
#
class Parser():
    def __init__(self, infile):
        self.vm = open(infile, "r")
        self.row = ""
        self.command = ""
        print("Open VM file", infile)

    def hasMoreCommands(self):
        while True:
            line = self.vm.readline()
            if not line:
                return False
            else:
                tmp = re.sub(r'//.*', "", line).strip()
                if tmp != "":
                    self.row = line
                    return True
                else:
                    continue

    def advance(self):
        self.command = re.sub(r'//.*', "", self.row).strip()

    def commandType(self):
        token = self.command.split()
        if len(token) > 0:
            cmd = self.command.split()[0].lower()
        else:
            cmd = self.command.lower()
        if cmd in ["add", "sub", "neg", "eq", "gt", "lt", "and", "or", "not"]:
            return C_ARITHMETIC
        elif cmd == "push":
            return C_PUSH
        elif cmd == "pop":
            return C_POP
        elif cmd == "label":
            return C_LABEL
        elif cmd == "goto":
            return C_GOTO
        elif cmd == "if-goto":
            return C_IF
        elif cmd == "function":
            return C_FUNCTION
        elif cmd == "call":
            return C_CALL
        elif cmd == "return":
            return C_RETURN

    def arg1(self):
        args = self.command.split()
        if self.commandType() == C_ARITHMETIC:
            return args[0]
        else:
            return args[1]

    def arg2(self):
        return int(self.command.split()[2])


class CodeWriter():
    def __init__(self, outfile):
        self.asm = open(outfile, "w")
        self.vm_name = ""
        self.label_id = 0
        self.func_name = "null"
        self.ln = 0

    def _outCommand(self, cmd):
        # cmd文字列にアドレスと改行を付け加えて返す
        cmd_line = cmd + " // " + str(self.ln) + "\n"
        self.ln += 1
        return cmd_line

    def _genLabel(self):
        # 汎用のユニークラベルを返す
        self.label_id += 1
        return "label_uniq_"+str(self.label_id)

    def setFileName(self, filename):
        # .vmファイル名を設定
        self.vm_name = os.path.basename(filename).replace(".vm", "")

    def writeInit(self):
        # スタックポインタ初期化; SP=256
        out = self._outCommand("@256")
        out += self._outCommand("D=A")
        out += self._outCommand("@SP")
        out += self._outCommand("M=D")
        self.asm.write(out)
        # call Sys.init
        self.vm_name = "Sys.vm"
        self.writeCall("Sys.init", 0)

    def writeArithmetic(self, command):
        out = "// "+command+"\n"
        if command in ["add", "sub", "and", "or"]: # 2 operands
            # M[M[SP]-1]（yの値）をDレジスタに保存
            out += self._outCommand("@SP")
            out += self._outCommand("A=M-1") # M[SP]-1
            out += self._outCommand("D=M")  # D = value of y
            # M[SP]-2（xのアドレス）をAレジスタに保存
            out += self._outCommand("A=A-1") # A = address of x
            # 演算を実行し、結果をM[M[SP]-2]（xのアドレス）に保存
            if command == "add":
                out += self._outCommand("M=D+M")
            elif command == "sub":
                out += self._outCommand("M=M-D")
            elif command == "and":
                out += self._outCommand("M=D&M")
            elif command == "or":
                out += self._outCommand("M=D|M")
            # スタックポインタを1減らす
            out += self._outCommand("@SP")
            out += self._outCommand("M=M-1") # Update stack pointer
        elif command in ["eq", "gt", "lt"]: # 2 operands and boolian return value
            # M[M[SP]-1]（yの値）をDレジスタに保存
            out += self._outCommand("@SP")
            out += self._outCommand("A=M-1")  # M[SP]-1
            out += self._outCommand("D=M")  # D = value of y
            # M[SP]-2（xのアドレス）をAレジスタに保存
            out += self._outCommand("A=A-1")  # A = address of x
            # x-yをDレジスタに保存
            out += self._outCommand("D=M-D")
            # 条件成立時のジャンプ先のユニークラベルを作成
            label1 = self._genLabel()
            out += self._outCommand("@"+label1)
            if command == "eq":
                out += self._outCommand("D;JEQ")
            elif command == "gt":
                out += self._outCommand("D;JGT")
            elif command == "lt":
                out += self._outCommand("D;JLT")
            # xのアドレスにFalseを書き込んだあとlabel2にジャンプ
            out += self._outCommand("@2")
            out += self._outCommand("D=A")
            out += self._outCommand("@SP")
            out += self._outCommand("A=M-D") # A = address of x
            out += self._outCommand("M=0")
            label2 = self._genLabel()
            out += self._outCommand("@"+label2)
            out += self._outCommand("0;JMP")
            out += "("+label1+")\n"
            # xのアドレスにTrueを書き込む
            out += self._outCommand("@2")
            out += self._outCommand("D=A")
            out += self._outCommand("@SP")
            out += self._outCommand("A=M-D")  # A = address of x
            out += self._outCommand("M=-1")
            out += "("+label2+")\n"
            # スタックポインタを1減らす
            out += self._outCommand("@SP")
            out += self._outCommand("M=M-1")
        else: # 1 operand (neg or not)
            # オペランドのアドレスをAレジスタに保存
            out += self._outCommand("@SP")
            out += self._outCommand("A=M-1")  # A = address of y
            # 演算結果をオペランドのアドレスに書き込む
            if command == "neg":
                out += self._outCommand("M=-M")
            elif command == "not":
                out += self._outCommand("M=!M")
        self.asm.write(out)

    def writePushPop(self, command, segment, index):
        out = "// "+command+" "+segment+" "+str(index)+"\n"
        if segment == "constant":
            # indexをDレジスタに読み込む
            out += self._outCommand("@"+str(index))
            out += self._outCommand("D=A") # D = index
            # スタックポインタの位置にDレジスタの値を書き込む。pushのみ（pop constantは存在しない）
            out += self._outCommand("@SP")
            out += self._outCommand("A=M") # A is stack pointer
            out += self._outCommand("M=D") # push index
            # スタックポインタを1増やす
            out += self._outCommand("@SP")
            out += self._outCommand("M=M+1")
        elif segment in ["local", "argument", "this", "that", "pointer", "temp", "static"]:
            # アドレス解決; 読み込みまたは書き込み先のRAMアドレスをAレジスタに格納
            ## 該当するベースポインタの値をDに読み込む
            if segment == "local":
                out += self._outCommand("@LCL")
                out += self._outCommand("D=M")
            elif segment == "argument":
                out += self._outCommand("@ARG")
                out += self._outCommand("D=M")
            elif segment == "this":
                out += self._outCommand("@THIS")
                out += self._outCommand("D=M")
            elif segment == "that":
                out += self._outCommand("@THAT")
                out += self._outCommand("D=M")
            elif segment == "pointer":
                out += self._outCommand("@3")
                out += self._outCommand("D=A")
            elif segment == "temp":
                out += self._outCommand("@5")
                out += self._outCommand("D=A")
            elif segment == "static":
                # static segemntの場合は標準マッピングに従ってXxx.indexシンボルを使用
                out += self._outCommand("@"+self.vm_name+"."+str(index))
#                out += "@16\n"
                out += self._outCommand("AD=A")
            if segment != "static":
                ## indexをAに読み込んでベースポインタとの和を求め、A, Dレジスタに保存。Aはpush用、Dはpop用
                out += self._outCommand("@"+str(index))
                out += self._outCommand("AD=D+A")
            # push or pop
            if command == "push":
                # pushする値を取得
                out += self._outCommand("D=M")
                # スタックトップに書き込む
                out += self._outCommand("@SP")
                out += self._outCommand("A=M")
                out += self._outCommand("M=D")
                # スタックポインタを更新
                out += self._outCommand("@SP")
                out += self._outCommand("M=M+1")
            elif command == "pop":
                # 書き込み先アドレスを汎用レジスタ(R13)に保存
                out += self._outCommand("@R13")
                out += self._outCommand("M=D")
                # スタックからデータをDレジスタに取得
                out += self._outCommand("@SP")
                out += self._outCommand("A=M-1")
                out += self._outCommand("D=M")
                # Dレジスタの値をメモリに書き込む
                out += self._outCommand("@R13")
                out += self._outCommand("A=M")
                out += self._outCommand("M=D")
                # スタックポインタを更新
                out += self._outCommand("@SP")
                out += self._outCommand("M=M-1")
        else:
            raise ValueError("Invalid memory segment.")
        self.asm.write(out)

    def writeLabel(self, label):
        out = "// label " + label + "\n"
        uniq_label = self.func_name + "$" + label
        out += "("+uniq_label+")\n"
        self.asm.write(out)

    def writeGoto(self, label):
        out = "// goto " + label + "\n"
        uniq_label = self.func_name + "$" + label
        out += self._outCommand("@"+uniq_label)
        out += self._outCommand("0;JMP")
        self.asm.write(out)

    def writeIf(self, label):
        out = "// if-goto " + label + "\n"
        uniq_label = self.func_name + "$" + label
        # Dレジスタにpop
        out += self._outCommand("@SP")
        out += self._outCommand("A=M-1")
        out += self._outCommand("D=M")
        out += self._outCommand("@SP")
        out += self._outCommand("M=M-1")
        # 条件ジャンプ
        out += self._outCommand("@"+uniq_label)
        out += self._outCommand("D;JNE")
        self.asm.write(out)

    def writeCall(self, func, narg):
        out = "// call " + func + " " + str(narg) + "\n"
        # call処理
        ## return address格納用のシンボルを作る
        rt = self._genLabel()
        ## return address, LCL, ARG, THIS, THATをpushする
        for label in [rt, "LCL", "ARG", "THIS", "THAT"]:
            out += "//+++ push "+label+"\n"
            out += self._outCommand("@"+label)
            if label == rt: # return addressはシンボルの値
                out += self._outCommand("D=A")
            else: # segmentベースポインタはシンボルの値による参照
                out += self._outCommand("D=M")
            out += self._outCommand("@SP")
            out += self._outCommand("A=M")
            out += self._outCommand("M=D")
            out += self._outCommand("@SP")
            out += self._outCommand("M=M+1")
        # ARGをcallする関数の位置に移動 (ARG = SP-narg-5)
        out += "//+++ ARG = SP-"+str(narg)+"-5\n"
        out += self._outCommand("@5")
        out += self._outCommand("D=A") #D=5
        out += self._outCommand("@"+str(narg))
        out += self._outCommand("D=D+A") #D=5+narg
        out += self._outCommand("@SP")
        out += self._outCommand("D=M-D")
        out += self._outCommand("@ARG")
        out += self._outCommand("M=D")
        # LCLをSPに設定 (LCL =SP)
        out += "//+++ LCL=SP\n"
        out += self._outCommand("@SP")
        out += self._outCommand("D=M")
        out += self._outCommand("@LCL")
        out += self._outCommand("M=D")
        # callする関数に制御を移す
        out += "//+++ goto "+func+"\n"
        out += self._outCommand("@"+func)
        out += self._outCommand("0;JMP")
        # return addressラベル
        out += "//+++ (return address)\n"
        out += "("+rt+")\n"
        #
        self.asm.write(out)

    def writeReturn(self):
        out = "// return\n"
        # return処理
        ## FRAME=LCL
        out += self._outCommand("@LCL")
        out += self._outCommand("D=M")
        out += self._outCommand("@FRAME")
        out += self._outCommand("M=D")
        ## RET = *(FRAME-5)
        out += self._outCommand("@5")
        out += self._outCommand("D=A") #D=5
        out += self._outCommand("@FRAME")
        out += self._outCommand("A=M-D") #A=FRAME-5
        out += self._outCommand("D=M") #D=*(FRAME-5)
        out += self._outCommand("@RET")
        out += self._outCommand("M=D") #RET=*(FRAME-5)
        ## *ARG = pop()
        out += self._outCommand("@SP")
        out += self._outCommand("A=M-1")
        out += self._outCommand("D=M") # pop() -> D register
        out += self._outCommand("@ARG")
        out += self._outCommand("A=M") #A=ARG
        out += self._outCommand("M=D") #*ARG=pop()
        ## SP = ARG + 1
        out += self._outCommand("@ARG")
        out += self._outCommand("D=M+1") #D=ARG+1
        out += self._outCommand("@SP")
        out += self._outCommand("M=D") #SP=ARG+1
        ## Retrieve caller segment base pointers
        for cnt, label in enumerate(["THAT", "THIS", "ARG", "LCL"]):
            out += self._outCommand("@FRAME")
            out += self._outCommand("AM=M-1")
            out += self._outCommand("D=M")
            out += self._outCommand("@"+label)
            out += self._outCommand("M=D")
        ## goto RET
        out += self._outCommand("@RET")
        out += self._outCommand("A=M")
        out += self._outCommand("0;JMP")
        self.asm.write(out)

    def writeFunction(self, func, nloc):
        out = "// function " + func +" " + str(nloc) + "\n"
        out += "("+func+")\n"
        # 関数名を登録
        self.func_name = func
        # push 0 (repeat nloc times)
        for _ in range(nloc):
            out += self._outCommand("@SP")
            out += self._outCommand("A=M")
            out += self._outCommand("M=0")
            out += self._outCommand("@SP")
            out += self._outCommand("M=M+1")
        self.asm.write(out)

    def close(self):
        self.asm.close()

#
# Main program
#
parser = argparse.ArgumentParser(description="VM translator")
parser.add_argument("prog", help="program directory")

args = parser.parse_args()
prog_dir = args.prog

if not os.path.exists(prog_dir):
    print("Error: "+prog_dir+" does not exist.")
    sys.exit(1)

#
# Start code generation
#
## output file name
asmfile = os.path.join(os.path.basename(prog_dir), ".asm").replace(os.sep, "")
## CodeWriter instance
writer = CodeWriter(os.path.join(prog_dir, asmfile))

## Bootstrap
writer.writeInit()

## Process .vm files
for vm in glob.glob(os.path.join(prog_dir, "*.vm")):
    psr = Parser(vm)
    writer.setFileName(vm)
    while psr.hasMoreCommands():
        psr.advance()
        cmd_type = psr.commandType()
        if cmd_type == C_ARITHMETIC:
            writer.writeArithmetic(psr.arg1())
        elif cmd_type == C_PUSH:
            writer.writePushPop("push", psr.arg1(), psr.arg2())
        elif cmd_type == C_POP:
            writer.writePushPop("pop", psr.arg1(), psr.arg2())
        elif cmd_type == C_LABEL:
            writer.writeLabel(psr.arg1())
        elif cmd_type == C_GOTO:
            writer.writeGoto(psr.arg1())
        elif cmd_type == C_IF:
            writer.writeIf(psr.arg1())
        elif cmd_type == C_CALL:
            writer.writeCall(psr.arg1(), psr.arg2())
        elif cmd_type == C_RETURN:
            writer.writeReturn()
        elif cmd_type == C_FUNCTION:
            writer.writeFunction(psr.arg1(), psr.arg2())
        else:
            raise ValueError("Invalid type of command: "+psr.command)

writer.close()
