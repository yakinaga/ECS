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
    - __init__() ... アトリビュートの初期化
    - _getLabel() ... self.label_idからユニークなラベル文字列を生成して返す。self.label_idをインクリメントする
    - setFileName(str) ... self.vmを設定
    - writeArithmetic(str) ... 9種類のarithmeticコマンドをHackアセンブリに変換して出力ファイルに書き込む
    - writePushPop(str1, str2, int) ... push, popコマンドをHackアセンブリに変換して出力ファイルに書き込む
    - R[13]-R[15]の領域は汎用レジスタとしてpopコマンドの変換で使用
    - close() ... 出力ファイルをクローズ
  * main
    1. コマンド引数処理、エラーチェック
    2. CodeWriterインスタンス生成
    3. 入力ディレクトリ下の.vmファイルに対して順次処理
      1. Parserインスタンス生成
      2. コマンドタイプごとにVMコマンドをHackアセンブリに変換し.asmファイルに出力
      
## 9章



