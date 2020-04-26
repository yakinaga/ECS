"""
Hackアセンブラ（symbolフリー）
    Parserクラス
    アトリビュート
        self.asm...アセンブリファイルのデスクリプタ
        self.row...アセンブリファイルから読み取った現在の行
        self.command...現在のコマンド
    メソッド
        __init__(str)...アトリビュートの初期化
        hasMoreCommands()...アセンブリファイルから行を読み込んでself.rowに格納。EOFに達していればFalse
                            EOFではない場合、空白・コメントを除去してブランクにならなければTrue
                            ブランクなら次の行を読み込んでself.rowを更新し、上記処理を繰り返す
        advance()...self.rowから空白とコメントを除去してコマンドを読み込み、self.commandに格納
        commandType()...self.coommandのタイプ（A, c, L）を返す
        symbol()...A命令, L命令のシンボル（文字列）またはアドレス（10進数）を返す
        dest()...C命令のdestニーモニックを返す
        comp()...C命令のcompニーモニックを返す
        jump()...C命令のjumpニーモニックを返す

    Codeクラス
    メソッド
        __init__()...dest, comp, jumpのニーモニックと機械語を対応付ける辞書を作成
        dest(str)...destニーモニックの機械語を返す
        comp(str)...compニーモニックの機械語を返す
        jump(str)...jumpニーモニックの機械語を返す

    SymbolTableクラス
    アトリビュート
        self.symbols...シンボル（文字列）とアドレス（10進数）を関連付ける辞書
    メソッド
        __ini__()...self.symbolsを初期化する。定義済みシンボルを設定
        addEntry(str, int)...新たなsymbolとアドレスを登録
        contains(str)...symbolが登録済みならTrue
        getAddress(str)...symbolのアドレスを返す

    メイン
    ・実行ディレクトリを取得しcwdに格納
    ・引数で入力の.asmファイル名を取得。存在確認できなければcwdからの相対パスで探索。見つからなければエラー
    ・出力ファイルは拡張子が.hackになる。cwd下に作成
    ・Parserインスタンス作成
    ・parser.hasMoreCommands()がFalseになるまでループ
    ・・コマンドをデコードして出力ファイルに書き出す
"""
import re
import sys
import argparse

#
# Class definition
#
class Parser():
    def __init__(self, asmFile):
        # current row
        self.row = ""
        # current command
        self.command = ""
        # Open .asm file
        self.asm = open(asmFile, "r")

    def hasMoreCommands(self):
        while True:
            # Read one  line
            line = self.asm.readline()
            self.row = line
            # Return False if EOF appears
            if not self.row:
                return False
            # Remove spaces and comments
            line = line.replace(" ", "")
            line = re.sub(r'//.*', "", line)
            # Return True if line is not blank
            if line != "\n":
                return True
            else:
                continue #If blank, go to next line

    def advance(self):
        # Remove spaces and comments
        line = self.row.replace(" ", "").replace("\n", "")
        line = re.sub(r'//.*', "", line)
        #
        self.command = line

    def commandType(self):
        if self.command.startswith("@"):
            return A_COMMAND
        elif self.command.startswith("("):
            return L_COMMAND
        else:
            return C_COMMAND

    def symbol(self):
        if self.command.startswith("@"):
            return self.command.replace("@", "")
        elif self.command.startswith("("):
            return self.command.replace("(", "").replace(")", "")
        else:
            raise ValueError("Invalid command type")

    def dest(self):
        if "=" in self.command:
            return self.command.split("=")[0]
        else:
            return "null"

    def comp(self):
        if "=" in self.command:
            if ";" in self.command:
                return self.command.split("=")[1].split(";")[0]
            else:
                return self.command.split("=")[1]
        else:
            if ";" in self.command:
                return self.command.split(";")[0]
            else:
                return self.command

    def jump(self):
        if ";" in self.command:
            return self.command.split(";")[1]
        else:
            return "null"


class Code():
    def __init__(self):
        self.dest_dict = {"null": "000", "M": "001", "D": "010", "MD": "011",
                          "A": "100", "AM": "101", "AD": "110", "AMD": "111"}
        self.comp_dict = {"0": "0101010", "1": "0111111", "-1": "0111010",
                          "D": "0001100", "A": "0110000", "!D": "0001101",
                          "!A": "0110001", "-D": "0001111", "-A": "0110011",
                          "D+1": "0011111", "A+1": "0110111", "D-1": "0001110",
                          "A-1": "0110010", "D+A": "0000010", "D-A": "0010011",
                          "A-D": "0000111", "D&A": "0000000", "D|A": "0010101",
                          "M": "1110000", "!M": "1110001", "-M": "1110011",
                          "M+1": "1110111", "M-1": "1110010", "D+M": "1000010",
                          "D-M": "1010011", "M-D": "1000111", "D&M": "1000000",
                          "D|M": "1010101"}
        self.jump_dict = {"null": "000", "JGT": "001", "JEQ": "010",
                          "JGE": "011", "JLT": "100", "JNE": "101",
                          "JLE": "110", "JMP": "111"}

    def dest(self, mnemonic):
        return self.dest_dict[mnemonic]

    def comp(self, mnemonic):
        return self.comp_dict[mnemonic]

    def jump(self, mnemonic):
        return self.jump_dict[mnemonic]


################
# Main program #
################
A_COMMAND = 0
C_COMMAND = 1
L_COMMAND = 2

#
# Corrent directory
#
##cwd = os.getcwd()

#
# Command argument
#
parser = argparse.ArgumentParser(description="Hack Assembler")
parser.add_argument("asm", type=str, help="Input asm file")
args = parser.parse_args()
asmFile = args.asm

#
# Convert .asm to .hack
#
parser = Parser(asmFile)
code = Code()
binFile = asmFile.replace(".asm", ".hack")

with open(binFile, "w") as hack:
    while parser.hasMoreCommands():
        # Read next command
        parser.advance()
        # Convert to 16-bit binary instruction
        if parser.commandType() == A_COMMAND:
            address = parser.symbol()
            instruction = format(int(address), "b").zfill(16)
        elif parser.commandType() == C_COMMAND:
            instruction = "111"+code.comp(parser.comp())+code.dest(parser.dest())+code.jump(parser.jump())
        
        hack.write(instruction+"\n")


