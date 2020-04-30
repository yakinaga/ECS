import os
import sys
import glob
import argparse

"""
バーチャルマシン(VM)プログラムをHackアセンブリに変換する
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
* __init__() ... アトリビュートの初期化
* _getLabel() ... self.label_idからユニークなラベル文字列を生成して返す。self.label_idをインクリメントする
* setFileName(str) ... self.vmを設定
* writeArithmetic(str) ... 9種類のarithmeticコマンドをHackアセンブリに変換して出力ファイルに書き込む
* writePushPop(str1, str2, int) ... push, popコマンドをHackアセンブリに変換して出力ファイルに書き込む
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
                tmp = line.replace(r'//.*', "").strip()
                if tmp != "":
                    self.row = line
                    return True
                else:
                    continue

    def advance(self):
        self.command = self.row.replace(r'//.*', "").strip().lower()

    def commandType(self):
        cmd = self.command.split()[0]
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
        self.vm = ""
        self.label_id = 0

    def _getLabel(self):
        self.label_id += 1
        return "label_"+str(self.label_id)

    def setFileName(self, filename):
        self.vm = filename

    def writeArithmetic(self, command):
        out = ""
        if command in ["add", "sub", "and", "or"]: # 2 operands
            # M[M[SP]-1]（yの値）をDレジスタに保存
            out += "@SP\n"
            out += "A=M-1\n" # M[SP]-1
            out +="D=M\n"  # D = value of y
            # M[SP]-2（xのアドレス）をAレジスタに保存
            out += "A=A-1\n" # A = address of x
            # 演算を実行し、結果をM[M[SP]-2]（xのアドレス）に保存
            if command == "add":
                out += "M=D+M\n"
            elif command == "sub":
                out += "M=M-D\n"
            elif command == "and":
                out += "M=D&M\n"
            elif command == "or":
                out += "M=D|M\n"
            # スタックポインタを1減らす
            out += "@SP\n"
            out += "M=M-1\n" # Update stack pointer
        elif command in ["eq", "gt", "lt"]: # 2 operands and boolian return value
            # M[M[SP]-1]（yの値）をDレジスタに保存
            out += "@SP\n"
            out += "A=M-1\n"  # M[SP]-1
            out += "D=M\n"  # D = value of y
            # M[SP]-2（xのアドレス）をAレジスタに保存
            out += "A=A-1\n"  # A = address of x
            # x-yをDレジスタに保存
            out += "D=M-D\n"
            # 条件成立時のジャンプ先のユニークラベルを作成
            label1 = self._getLabel()
            out += "@"+label1+"\n"
            if command == "eq":
                out += "D;JEQ\n"
            elif command == "gt":
                out += "D;JGT\n"
            elif command == "lt":
                out += "D;JLT\n"
            # xのアドレスにFalseを書き込んだあとlabel2にジャンプ
            out += "@2\n"
            out += "D=A\n"
            out += "@SP\n"
            out += "A=M-D\n" # A = address of x
            out += "M=0\n"
            label2 = self._getLabel()
            out += "@"+label2+"\n"
            out += "0;JMP\n"
            out += "("+label1+")\n"
            # xのアドレスにTrueを書き込む
            out += "@2\n"
            out += "D=A\n"
            out += "@SP\n"
            out += "A=M-D\n"  # A = address of x
            out += "M=-1\n"
            out += "("+label2+")\n"
            # スタックポインタを1減らす
            out += "@SP\n"
            out += "M=M-1\n"
        else: # 1 operand (neg or not)
            # オペランドのアドレスをAレジスタに保存
            out += "@SP\n"
            out += "A=M-1\n"  # A = address of y
            # 演算結果をオペランドのアドレスに書き込む
            if command == "neg":
                out += "M=-M\n"
            elif command == "not":
                out += "M=!M\n"
        self.asm.write(out)

    def writePushPop(self, command, segment, index):
        out = ""
        if segment == "constant":
            # indexをDレジスタに読み込む
            out += "@"+str(index)+"\n"
            out += "D=A\n" # D = index
            # スタックポインタの位置にDレジスタの値を書き込む
            out += "@SP\n"
            out += "A=M\n" # A is stack pointer
            out += "M=D\n" # push index
            # スタックポインタを1増やす
            out += "@SP\n"
            out += "M=M+1\n"
        else:
            # NYI
            pass
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

for vm in glob.glob(os.path.join(prog_dir, "*.vm")):
    psr = Parser(vm)
    while psr.hasMoreCommands():
        psr.advance()
        cmd_type = psr.commandType()
        if cmd_type == C_ARITHMETIC:
            writer.writeArithmetic(psr.arg1())
        elif cmd_type == C_PUSH:
            writer.writePushPop("push", psr.arg1(), psr.arg2())
        elif cmd_type == C_POP:
            # NYI
            pass
        else:
            # NYI
            pass

writer.close()
