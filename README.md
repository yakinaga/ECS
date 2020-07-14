# ECS
The elements of Computer Systems（邦題：「コンピュータシステムの理論と実装 --モダンなコンピュータの作り方」）

## 1~5章
* .hdlは全テストクリア

## 6章
* 使用言語：Python3.7.4（以降のプロジェクトも同じの予定）
* binary形式の実行モジュールはpyinstallで作成。pyinstallはpipでinstall可能。実行モジュール作成は$ pyinstall XXX.py --onefile
* binary形式の実行方法
  * $ Assembler <.asm file>
  *  カレントディレクトリに.hackファイルが作成される
* Assembler.py設計
  * Parserクラス
    - self.asm ... .asmファイルのデスクリプタ
    - self.row ... 現在の行
    - self.command ... 現在のコマンド
    - __init__() ... アトリビュート初期化
    - hasMoreCommand() ... アセンブリファイルから行を読み込んでself.rowに格納。EOFに達していればFalse。EOFではない場合、空白・コメントを除去してブランクにならなければTrue。ブランクなら次の行を読み込んでself.rowを更新し、上記処理を繰り返す
    - advance() ... self.rowから空白とコメントを除去してコマンドを読み込み、self.commandに格納
    - commandType() ... self.coommandのタイプ（A, c, L）を返す
    - symbol() ... A命令, L命令のシンボル（文字列）またはアドレス（10進数）を返す
    - dest() ... C命令のdestニーモニックを返す
    - comp() ... C命令のcompニーモニックを返す
    - jump() ... C命令のjumpニーモニックを返す
  * Codeクラス
    * dest(str), comp(str), jump(str) ... 受け取ったニーモニックの機械語を返す
  * SymbolTableクラス
    * self.table ... シンボルとアドレスを対応付ける辞書
    * __init__() ... self.tableを初期化。定義済みシンボルの登録
    * addEntry(str, int) ... self.tableにエントリーを追加
    * contains(str) ... self.tableに含まれているかどうか
    * getAddress(str) ... strをキーとするself.tableの値を返す
  * main
    1. 1st pass: 入力ファイルを1行ずつ読み込んで処理
      * C or A命令ならaddressに1追加
      * L命令ならラベルを登録
    2. 2nd pass: 入力ファイルを再度先頭から1行ずつ処理
      * A命令：アドレスを取得。アドレスがシンボルの場合、SymbolTableに登録済みなら置き換え。未登録なら新規登録して置き換え
      * C命令：仕様に沿ってデコード
      * L命令：何もしない
      * A or C命令なら出力ファイルにinstructionを書き込む

## 7-8章
* ベースポインタの初期化：
  - SP ... ブートストラップで256に初期化される
  - LCL, ARG ... Sys.initのcall文が初期化になる（ARG=SP-5, LCL=SP）
  - THIS, THAT ... ?
* 使用言語：Python3.7.4
* binary形式の実行モジュールはpyinstallで作成。pyinstallはpipでinstall可能。実行モジュール作成は$ pyinstall XXX.py --onefile
* binary形式の実行方法
  * $ VMtranslator <prog_dir>
  * prog_dirは.vimファイル群が置かれているディレクトリ名
  * prog_dir/下に.asmファイルが作成される
* VMtranslator.py設計
  * Parserクラス
    - self.vm ... .vmファイルのデスクリプタ
    - self.row ... 現在読み込んでいる行
    - self.command ... 現在読み込んでいるコマンド
    - __init__() ... アドリビュートを初期化
    - hasMoreCommands() ... self.vmから1行読んでEOFならFalse. コメント削除&strip()してブランクにならなければTrue. ブランクなら次の行を読み込んで繰り返し。Trueの時は読み込んだ行をself.rowに格納
     - advance() ... self.rowかのコメントを除去しstrip()　→self.commandに格納
     - commandType(str) ... コマンド(str)の種類を返す
     - arg1() ... コマンドの第1引数を返す。C_ARITHMETICの場合はコマンド自身を返す
     - arg2() ... コマンドの第2引数を返す  
  * CodeWriterクラス
    - self.asm ... 出力ファイルのデスクリプタ
    - self.vm ... 現在読み込まれている.vmファイル名
    - self.label_id ... .asmのL_COMMANDに使うラベルの通し番号。開始は1
    - self.func_name ... 現在の関数名（初期値は"null"）
    - self.ln ... ROMアドレス（コメントと擬コードを除いた行番号；0開始）。※デバッグ用途のみ
    - __init__() ... アトリビュートの初期化
    - _getLabel() ... self.label_idからユニークなラベル文字列を生成して返す。self.label_idをインクリメントする
    - _outCommand(str) ... str型の引数にROMアドレスself.lnと改行コードをつけて返し、ROMアドレスをインクリメント
    - setFileName(str) ... self.vmを設定
    - writeInit() ... ブートストラップコードを書き込む。SP=256に初期化し、Sys.initをcall（writeCall("Sys.init", 0)を実行）
    - writeArithmetic(str) ... 9種類のarithmeticコマンドをHackアセンブリに変換して出力ファイルに書き込む
    - writePushPop(str1, str2, int) ... push, popコマンドをHackアセンブリに変換して出力ファイルに書き込む
      - staticセグメントのアドレス（A命令のシンボル）を本書の記述通りにすると「ベースポインタ + index」というルールに合致しない。しかしシンボルのユニーク性を担保するには、こちら（本書に記述）の方が確実
    - writeLabel(str) ... labelコマンドを変換して出力ファイルに書き込む
    - writeGoto(str) ... gotoコマンドを変換して出力ファイルに書き込む
    - writeIf(str) ... if-gotoコマンドを変換して出力ファイルに書き込む
    - writeCall(str, int) ... callコマンドを変換して出力ファイルに書き込む
    - writeReturn() ... returnコマンドを変換して出力ファイルに書き込む
    - writeFunction(str, int) ... functionコマンドを変換して出力ファイルに書き込む
    - R[13]-R[15]の領域は汎用レジスタとしてpopコマンドの変換で使用
    - close() ... 出力ファイルをクローズ
  * main
    1. コマンド引数処理、エラーチェック
    2. CodeWriterインスタンス生成、ブートストラップコード書き込み
    3. 入力ディレクトリ下の.vmファイルに対して順次処理
      1. Parserインスタンス生成
      2. コマンドタイプごとにVMコマンドをHackアセンブリに変換し.asmファイルに出力
      
## 9章

## 10章
* コンパイラ作成#1
* 使用言語：Python3.7.4
* 作成モジュール：JackAnalyzer.py
* 実装クラス
  * JackAnalyzer()
  * JackTokenizer()
  * CompilationEngine()
* クラス設計
  * JackAnalyzer()
    - __init__() ... インスタンス初期化
    - run(source) ...
      - Input: sourceはディレクトリまたはJackソースファイル名
      1. インプットからソースファイルを展開
      2. ソースファイルでループ
        1. JackTokenizer()インスタンス初期化。入力はソースファイル
        2. （JackTokenizerクラスのテスト用） トークンとそのタイプを取得し、.xmlファイルに出力する
        3. CompilationEngine()を初期化（以下ce）
        4. ce.compileClass()
  * JackTokenizer()
    - __init__(srcfile) ... 入力はソースファイル名。self.token_listにトークンを格納。読み取ったトークンはリストから削除され、最終的に空のリストになる
      1. ファイルを開いて内容を一括読み込み
      2. 読み込んだテキストデータの改行とコメントを空白で置き換える
      3. symbolの両側に空白を挿入する（split()で分割できるようにするため）
      4. split()で分解し、リストに格納→self.token_list
      5. self.current_token = None; self.next_token = self.token_list[0]
    - hasMoreTokens() ... self.token_listの長さが0ならFalse
    - advance() ...
      1. self.current_token = self.token_list[0]
      2. self.token_listの第0要素を削除
      3. self.next_token = self.token_list[0]
      4. return self.current_token
    - 他の関数は自明
  * CompilationEngine()
    - __init__(tknzr) ... JackTokenizerインスタンスを入力で受け取り、selfのアトリビュートとして格納。テキストの仕様に無いが、これがないとCompilationEngineの中でトークンを取得できない
    - compile***()関数群ではself.tokenizerのadvance()およびcurrent_token, next_tokenを使ってトークンを取得
      - トークンの先読みが必要な場合はtknzr.next_tokenを参照する
      
