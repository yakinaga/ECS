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

## 7章

