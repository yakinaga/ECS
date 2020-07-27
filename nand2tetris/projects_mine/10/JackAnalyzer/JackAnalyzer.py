import os
import sys
import re
import glob
import argparse
import collections

#
# Token container
#
Token = collections.namedtuple("Token", ["type", "value"])

#
# Jack token specification
#
T_COMMENT1   = "COMMENT1"
T_COMMENT2   = "COMMENT2"
T_COMMENT3   = "COMMENT3"
T_SKIP       = "SKIP"
T_STR_CONST  = "stringConstant"
T_INT_CONST  = "integerConstant"
T_SYMBOL     = "symbol"
T_KEYWORD    = "keyword"
T_IDENTIFIER = "identifier"
T_MISMATCH   = "MISMATCH"

token_spcification = [
    (T_COMMENT1, r"//.*"), # comments: //...
    (T_COMMENT2, r"/\*[\s\S]*?\*/"), # comments: /* ... */
    (T_COMMENT3, r"/\*\*[\s\S]*?\*/"), # comments: /** ... */
    (T_STR_CONST, r"\".*?\""),  # string constants (double quotations are involved)
    (T_SKIP, r"\s+|\n+"), # spaces, tabs, new lines
    (T_SYMBOL, r"[{}\(\)\[\],.;\+\-\*/&\|<>=~]"), # symbols
    (T_KEYWORD, r"class|constructor|function|method|field|static|var|int|char|boolean|void|true|false|null|this|let|do|if|else|while|return"),  # keywords
    (T_IDENTIFIER, r"\b[a-zA-Z_][a-zA-Z0-9_]*\b"), # identifiers
    (T_INT_CONST, r"\b\d+\b"), # integer constants
    (T_MISMATCH, r"."), # any other characters
]

Jack_operators = ["+", "-", "*", "/", "&", "|", "<", ">", "="]
Jack_unary_ops = ["~", "-"]
Jack_kw_constants = ["true", "false", "null", "this"]

#
# Function definitions
#
def punch_tokens_to_xml(tokenizer):
    #
    # トークンをxml形式で出力する；JackTokenizerのテスト専用
    #
    with open(tokenizer.source_file.replace(".jack", "T.xml"), "w") as fout:
        fout.write("<tokens>\n")
        while tokenizer.hasMoreTokens():
            tokenizer.advance()
            if tokenizer.tokenType() == T_KEYWORD:
                fout.write("<keyword> " + tokenizer.keyWord() + " </keyword>\n")
            elif tokenizer.tokenType() == T_SYMBOL:
                if tokenizer.symbol() == "<":
                    value = "&lt;"
                elif tokenizer.symbol() == ">":
                    value = "&gt;"
                elif tokenizer.symbol() == "&":
                    value = "&amp;"
                else:
                    value = tokenizer.symbol()
                fout.write("<symbol> " + value + " </symbol>\n")
            elif tokenizer.tokenType() == T_IDENTIFIER:
                fout.write("<identifier> " + tokenizer.identifier() + " </identifier>\n")
            elif tokenizer.tokenType() == T_INT_CONST:
                fout.write("<integerConstant> " + tokenizer.intVal() + " </integerConstant>\n")
            elif tokenizer.tokenType() == T_STR_CONST:
                fout.write("<stringConstant> " + tokenizer.stringVal() + " </stringConstant>\n")
            else:
                raise ValueError("Invalid token type.")
        fout.write("</tokens>\n")

#
# Class definitions
#
class JackAnalyzer():
    def __init__(self, source):
        if os.path.isdir(source):
            self.src_files = sorted(glob.glob(os.path.join(source, "*.jack")))
        elif os.path.isfile(source):
            if not source.endswith(".jack"):
                raise ValueError("Input file "+source+" may not be a jack source file?")
            self.src_files = [source]
        else:
            raise FileNotFoundError("Jack source file(s) not found !")

    def run(self):
        for src_file in self.src_files:
            #
            print("Compiling "+src_file)
            #
            # Tokenizer instance
            tknzr = JackTokenizer(src_file)
            #
            # Punch out tokens
            # *** For testing JackTokenizer class only
            # *** Note: Calling punch_tokens_to_xml() consumes tokens,
            # ***       which means CompilationEngine produces nothing
#            punch_tokens_to_xml(tknzr)
            #
            # CompilationEngine instance
            ce = CompilationEngine(tknzr)
            # Start compilation
            ce.compileClass()
            # End of compilation
            ce.finalize()
        print("Compilation ended successfully.")


class JackTokenizer():
    def __init__(self, source_file):
        self.source_file = source_file
        # Read source file
        with open(source_file, "r") as fin:
            source_text = fin.read()
        # Tokenize
        tmp_list = []
        tok_regex = "|".join("(?P<%s>%s)" % pair for pair in token_spcification)
        for mo in re.finditer(tok_regex, source_text):
            type = mo.lastgroup
            value = mo.group()
            if type in [T_COMMENT1, T_COMMENT2, T_COMMENT3, T_SKIP]:
                continue
            elif type in [T_SYMBOL, T_KEYWORD, T_STR_CONST, T_INT_CONST, T_IDENTIFIER]:
                value = value.replace('"', '')
                tmp_list.append(Token(type, value))
            else:
                raise RuntimeError(f"{value!r} unexpected.")
        #
        self.token_list = tmp_list
        self.next_token = self.token_list[0]
        self.current_token = None

    def hasMoreTokens(self):
        if self.token_list:
            return True
        else:
            return False

    def advance(self):
        self.current_token = self.token_list[0]
        del self.token_list[0]
        if self.token_list: # token_list is not empty yet
            self.next_token = self.token_list[0]
        else:               # token_list has been consumed
            self.next_token = None

    def tokenType(self):
        return self.current_token.type

    def keyword(self):
        return self.current_token.value

    def symbol(self):
        return self.current_token.value

    def identifier(self):
        return self.current_token.value

    def intVal(self):
        return self.current_token.value

    def stringVal(self):
        return self.current_token.value


class CompilationEngine():
    def __init__(self, tokenizer):
        #
        # 初期化
        #
        self.tokenizer = tokenizer
        self.fout = open(tokenizer.source_file.replace(".jack", ".xml"), "w")
        self.indent = "  "
        self.indent_level = 0

    def finalize(self):
        #
        # 終了処理
        #
        self.fout.close()

    def _to_xml(self, tag, val):
        #
        # 終端記号をxml形式で出力: <tag> val </tag>
        #
        self.fout.write(self.indent_level * self.indent + "<" + tag + ">")
        if val == "<":
            val = "&lt;"
        elif val == ">":
            val = "&gt;"
        elif val == "&":
            val = "&amp;"
        self.fout.write(" " + val +" ")
        self.fout.write("</" + tag + ">\n")

    def _open_tag(self, tag):
        #
        # 非終端記号の開タグを出力
        #
        self.fout.write(self.indent_level * self.indent + "<"+tag+">\n")
        self.indent_level += 1

    def _close_tag(self, tag):
        #
        # 非終端記号の閉タグを出力
        #
        self.indent_level -= 1
        self.fout.write(self.indent_level * self.indent + "</"+tag+">\n")

    def _expect(self, type=None, values=None):
        #
        # トークンを一つ読み進んで出力する
        # type ... 期待されるトークンタイプ。異なっていた場合エラー停止
        # values ... 取りうる値のリスト(optional)。これ以外のvalueであった場合はエラー停止
        #
        tk = self.tokenizer
        if tk.hasMoreTokens():
            tk.advance()
        else:
            raise RuntimeError("Unexpected end of tokens.")
        if tk.tokenType() == type:
            if values:
                if tk.current_token.value in values:
                    self._to_xml(type, tk.current_token.value)
                else:
                    raise RuntimeError("Expected token value(s): " + str(values) + ", but got " + tk.current_token.value)
            else:
                self._to_xml(type, tk.current_token.value)
        else:
            raise RuntimeError("Expected token type: " + type + ", but got " + tk.tokenType())

    def compileClass(self):
        tk = self.tokenizer
        self._open_tag("class")
        self._expect(type=T_KEYWORD, values=["class"])
        # class name
        self._expect(type=T_IDENTIFIER)
        # open brace
        self._expect(type=T_SYMBOL, values=["{"])
        # class variable decleration
        while tk.next_token.value in ["static", "field"]:
            self.compileClassVarDec()
        # subroutines
        while tk.next_token.value in ["constructor", "function", "method"]:
            self.compileSubroutine()
        # close brace
        self._expect(type=T_SYMBOL, values=["}"])
        self._close_tag("class")

    def compileClassVarDec(self):
        self._open_tag("classVarDec")
        tk = self.tokenizer
        # static or field
        self._expect(type=T_KEYWORD, values=["static", "field"])
        # type
        if tk.next_token.type == T_KEYWORD: ## built-in type
            self._expect(type=T_KEYWORD, values=["int", "char", "boolean"])
        else: ## class
            self._expect(type=T_IDENTIFIER)
        # first varName
        self._expect(type=T_IDENTIFIER)
        # other varNames
        while tk.next_token.value != ";":
            self._expect(type=T_SYMBOL, values=[","])
            self._expect(type=T_IDENTIFIER)
        # end of classVar declaretion
        self._expect(type=T_SYMBOL, values=[";"])
        self._close_tag("classVarDec")

    def compileSubroutine(self):
        tk = self.tokenizer
        self._open_tag(tag="subroutineDec")
        # subroutine type
        self._expect(type=T_KEYWORD, values=["constructor", "function", "method"])
        # return value type
        if tk.next_token.type == T_KEYWORD:
            self._expect(type=T_KEYWORD, values=["void", "int", "char", "boolean"])
        else:
            self._expect(type=T_IDENTIFIER)
        # subroutine name
        self._expect(type=T_IDENTIFIER)
        # arguments
        self._expect(type=T_SYMBOL, values=["("])
        self.compileParameterList()
        self._expect(type=T_SYMBOL, values=[")"])
        # subroutine body
        self._open_tag(tag="subroutineBody")
        self._expect(type=T_SYMBOL, values=["{"])
        ## varDec
        while tk.next_token.value == "var":
            self.compileVarDec()
        ## statements
        self.compileStatements()
        self._expect(type=T_SYMBOL, values=["}"])
        self._close_tag(tag="subroutineBody")
        self._close_tag(tag="subroutineDec")

    def compileParameterList(self):
        #
        # 次のトークンが")"記号であればリストの終わりとみなす
        #
        tk = self.tokenizer
        self._open_tag(tag="parameterList")
        if tk.next_token.value == ")":
            pass
        else:
            first = True
            while tk.next_token.value != ")":
                if not first: self._expect(type=T_SYMBOL, values=[","])
                if tk.next_token.type == T_KEYWORD:
                    self._expect(type=T_KEYWORD, values=["int", "char", "boolean"])
                else:
                    self._expect(type=T_IDENTIFIER)
                self._expect(type=T_IDENTIFIER)
                first = False
        self._close_tag(tag="parameterList")

    def compileVarDec(self):
        tk = self.tokenizer
        self._open_tag(tag="varDec")
        self._expect(type=T_KEYWORD, values=["var"])
        if tk.next_token.type == T_KEYWORD:
            self._expect(type=T_KEYWORD, values=["int", "char", "boolean"])
        else:
            self._expect(type=T_IDENTIFIER)
        first = True
        while tk.next_token.value != ";":
            if not first: self._expect(type=T_SYMBOL, values=[","])
            self._expect(type=T_IDENTIFIER)
            first = False
        self._expect(type=T_SYMBOL, values=[";"])
        self._close_tag(tag="varDec")

    def compileStatements(self):
        tk = self.tokenizer
        self._open_tag(tag="statements")
        while tk.next_token.value in ["let", "if", "while", "do", "return"]:
            next_val = tk.next_token.value
            if next_val == "let":
                self.compileLet()
            elif next_val == "if":
                self.compileIf()
            elif next_val == "while":
                self.compileWhile()
            elif next_val == "do":
                self.compileDo()
            elif next_val == "return":
                self.compileReturn()
        self._close_tag(tag="statements")

    def compileDo(self):
        tk = self.tokenizer
        self._open_tag(tag="doStatement")
        self._expect(type=T_KEYWORD, values=["do"])
        # subroutineCall
        self._expect(type=T_IDENTIFIER) # subroutineName or (className|varName)
        if tk.next_token.value == "(":
            self._expect(type=T_SYMBOL, values=["("])
            self.compileExpressionList()
            self._expect(type=T_SYMBOL, values=[")"])
        elif tk.next_token.value == ".":
            self._expect(type=T_SYMBOL, values=["."])
            self._expect(type=T_IDENTIFIER)
            self._expect(type=T_SYMBOL, values=["("])
            self.compileExpressionList()
            self._expect(type=T_SYMBOL, values=[")"])
        self._expect(type=T_SYMBOL, values=[";"])
        self._close_tag(tag="doStatement")

    def compileLet(self):
        tk = self.tokenizer
        self._open_tag(tag="letStatement")
        self._expect(type=T_KEYWORD, values=["let"])
        self._expect(type=T_IDENTIFIER)  # varName
        if tk.next_token.value == "[":
            self._expect(type=T_SYMBOL, values=["["])
            self.compileExpression()
            self._expect(type=T_SYMBOL, values=["]"])
        self._expect(type=T_SYMBOL, values=["="])
        self.compileExpression()
        self._expect(type=T_SYMBOL, values=[";"])
        self._close_tag(tag="letStatement")

    def compileWhile(self):
        tk = self.tokenizer
        self._open_tag(tag="whileStatement")
        self._expect(type=T_KEYWORD, values=["while"])
        self._expect(type=T_SYMBOL, values=["("])
        self.compileExpression()
        self._expect(type=T_SYMBOL, values=[")"])
        self._expect(type=T_SYMBOL, values=["{"])
        self.compileStatements()
        self._expect(type=T_SYMBOL, values=["}"])
        self._close_tag(tag="whileStatement")

    def compileReturn(self):
        tk = self.tokenizer
        self._open_tag(tag="returnStatement")
        self._expect(type=T_KEYWORD, values=["return"])
        if tk.next_token.value != ";":
            self.compileExpression()
        self._expect(type=T_SYMBOL, values=[";"])
        self._close_tag(tag="returnStatement")

    def compileIf(self):
        tk = self.tokenizer
        self._open_tag(tag="ifStatement")
        self._expect(type=T_KEYWORD, values=["if"])
        self._expect(type=T_SYMBOL, values=["("])
        self.compileExpression()
        self._expect(type=T_SYMBOL, values=[")"])
        self._expect(type=T_SYMBOL, values=["{"])
        self.compileStatements()
        self._expect(type=T_SYMBOL, values=["}"])
        if tk.next_token.value == "else":
            self._expect(type=T_KEYWORD, values=["else"])
            self._expect(type=T_SYMBOL, values=["{"])
            self.compileStatements()
            self._expect(type=T_SYMBOL, values=["}"])
        self._close_tag(tag="ifStatement")

    def compileExpression(self):
        tk = self.tokenizer
        self._open_tag(tag="expression")
        self.compileTerm()
        while tk.next_token.value in Jack_operators:
            self._expect(type=T_SYMBOL, values=Jack_operators)
            self.compileTerm()
        self._close_tag(tag="expression")

    def compileTerm(self):
        tk = self.tokenizer
        self._open_tag(tag="term")
        next_type = tk.next_token.type
        next_value = tk.next_token.value
        if next_type == T_INT_CONST:   # integerConstant
            self._expect(type=T_INT_CONST)
        elif next_type == T_STR_CONST:   # stringConstant
            self._expect(type=T_STR_CONST)
        elif next_value in Jack_kw_constants:   # KeywordConstant
            self._expect(type=T_KEYWORD, values=Jack_kw_constants)
        elif next_value == "(":  # (expression)
            self._expect(type=T_SYMBOL, values=["("])
            self.compileExpression()
            self._expect(type=T_SYMBOL, values=[")"])
        elif next_value in Jack_unary_ops:   # unaryOp term
            self._expect(type=T_SYMBOL, values=Jack_unary_ops)
            self.compileTerm()
        elif next_type == T_IDENTIFIER:   # varName | varName[expression] | subroutineCall
            self._expect(type=T_IDENTIFIER)
            if tk.next_token.value == "[":   # varName[expression]
                self._expect(type=T_SYMBOL, values=["["])
                self.compileExpression()
                self._expect(type=T_SYMBOL, values=["]"])
            elif tk.next_token.value in ["(", "."]:   # subroutineCall
                if tk.next_token.value == "(":
                    self._expect(type=T_SYMBOL, values=["("])
                    self.compileExpressionList()
                    self._expect(type=T_SYMBOL, values=[")"])
                elif tk.next_token.value == ".":
                    self._expect(type=T_SYMBOL, values=["."])
                    self._expect(type=T_IDENTIFIER)
                    self._expect(type=T_SYMBOL, values=["("])
                    self.compileExpressionList()
                    self._expect(type=T_SYMBOL, values=[")"])
            else:   # varName
                pass
        self._close_tag(tag="term")

    def compileExpressionList(self):
        #
        # 次のトークンが")"記号であればリストの終わりとみなす
        #
        tk = self.tokenizer
        self._open_tag(tag="expressionList")
        if tk.next_token.value == ")":
            pass
        else:
            first = True
            while tk.next_token.value != ")":
                if not first:
                    self._expect(type=T_SYMBOL, values=[","])
                first = False
                self.compileExpression()
        self._close_tag(tag="expressionList")

#
# Main program
#
parser = argparse.ArgumentParser()
parser.add_argument("--source", required=True, help="Source file or directory")
args = parser.parse_args()
source = args.source

analyzer = JackAnalyzer(source)
analyzer.run()
