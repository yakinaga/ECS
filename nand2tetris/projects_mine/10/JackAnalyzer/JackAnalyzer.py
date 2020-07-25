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
T_STR_CONST  = "STRING_CONST"
T_INT_CONST  = "INT_CONST"
T_SYMBOL     = "SYMBOL"
T_KEYWORD    = "KEYWORD"
T_IDENTIFIER = "IDENTIFIER"
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

#
# Function definitions
#
def punch_tokens_to_xml(tokenizer):
    # Punch out tokens in xml format
    with open(tokenizer.source_file.replace(".jack", "T.xml"), "w") as fout:
        fout.write("<tokens>\n")
        while tokenizer.hasMoreTokens():
            token = tokenizer.advance()
            if token.type == T_KEYWORD:
                fout.write("<keyword> " + token.value + " </keyword>\n")
            elif token.type == T_SYMBOL:
                if token.value == "<":
                    value = "&lt;"
                elif token.value == ">":
                    value = "&gt;"
                elif token.value == "&":
                    value = "&amp;"
                else:
                    value = token.value
                fout.write("<symbol> " + value + " </symbol>\n")
            elif token.type == T_IDENTIFIER:
                fout.write("<identifier> " + token.value + " </identifier>\n")
            elif token.type == T_INT_CONST:
                fout.write("<integerConstant> " + token.value + " </integerConstant>\n")
            elif token.type == T_STR_CONST:
                fout.write("<stringConstant> " + token.value + " </stringConstant>\n")
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
            # Tokenizer instance
            tknzr = JackTokenizer(src_file)
            #
            # Punch out tokens
            # *** For testing JackTokenizer class only
            # *** Note: Calling punch_tokens_to_xml() consumes tokens,
            # ***       which means CompilationEngine produces nothing
            punch_tokens_to_xml(tknzr)
            #
            # CompilationEngine instance
#            ce = CompilatoinEngine(tknzr)
            # Start compilation
#            ce.CompileClass()


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
        return self.current_token

    def tokenType(self):
        return self.current_token.kind

    def keyword(self):
        return self.current_token.value

    def symbol(self):
        return self.current_token.value

    def identifier(self):
        return self.current_token.value

    def intVal(self):
        return int(self.current_token.value)

    def stringVal(self):
        return self.current_token.value

#
# Main program
#
parser = argparse.ArgumentParser()
parser.add_argument("--source", required=True, help="Source file or directory")
args = parser.parse_args()
source = args.source

analyzer = JackAnalyzer(source)
analyzer.run()
