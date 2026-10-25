# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 目的

`crskycode/KrkrDump`(Kirikiri Z 用のフック型ダンパー)の改造版。ゲーム「天使☆騒々 RE-BOOT!」(`N:\game\tenshi_sz`, 32bit `tenshi_sz.exe`)の `voice.xp3`(51,246 ファイル)を、**復号済み・元の名前つきで、ゲームを遊ばずに短時間で**書き出すこと。

改造の方針:
1. 名前の正規表現で `AV_` 系のボイスだけに絞る(設定 JSON の regex)。
2. ゲームを再生する代わりに、DLL がアーカイブの全エントリを順に開いて読み、エンジンに復号させて書き出す。
3. 復号後の ogg に名前を付ける(下記「名前の復元」)。

## 構成

- 上流 `KrkrDump` のクローン。サブモジュール `Detours` / `cJSON` / `zlib` は取得済み。
- `KrkrDump/dllmain.cpp`(約 2,000 行)が本体。`KrkrDumpLoader` が exe に DLL を差し込む。`KrkrPlugin/tp_stub.*` は Kirikiri プラグイン API。`Common/` は共通ヘルパー。
- 使い方(上流 README): `KrkrDump.dll` + `KrkrDump.json` + `KrkrDumpLoader.exe` を同じフォルダに置き、ゲーム exe を Loader にドラッグ。JSON は DLL と同名。
- ビルド: `KrkrDump.sln`。**x86 でビルドする**(ゲームが 32bit)。ビルド環境は Visual Studio 2022 Build Tools(MSVC 14.44、`C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools`)。`cl`/`msbuild` は PATH にないので、開発者コマンドプロンプトの環境を読み込んでから使う。

## これまでの調査結果(重要)

- GARbro-Mod で `voice.xp3` を開くと名前が化けるのは文字コードのせいではない。アーカイブの名前は `Hxv4` 形式で取り除かれ、並び順を表す連番(`0x5000 + 番号` の UTF-16 文字)に置き換わっている。
- GARbro で展開しても**中身が暗号化されたまま**。復号済みの `krkrz_dump/e04h.ks.scn` と比べると、ほぼ全バイトが `0xA2` との XOR だが、先頭約 160 バイトと数か所が一致しない(ファイルごとの鍵が入っている)。よって GARbro 展開では ogg として使えない可能性が高い。ゲームに復号させる方式が必要。
- 名前の復元(未検証の仮説): アーカイブの並び順は元ファイル名の名前順らしい。`krkrz_dump` の `AV_504_0001`〜`0009.ogg` が、アーカイブ内の連番 `0x5407`〜`0x540F` に連続して当たることを、サイズ + adler32 の照合で確認済み。シナリオ(復号済み PSB `.ks.scn`)の中に `AV_504_0001` のようなボイス名が平文で入っている。全シナリオからボイス名を集めて名前順に並べ、アーカイブ順に当てはめる計画。ただし全シナリオ(`scn.xp3`)は復号済みの形では未取得。
- `voice.xp3.index` などゲームフォルダの `*.index` は、`KrkrzExtract` が作った表のコピーで、名前の対応表ではない。
- `N:\game\tenshi_sz\krkrz_dump` には過去に `KrkrzExtract` で書き出した 1,266 ファイル(復号済み)がある。ボイスは 20 件ほどしかない。

## 注意

- ゲームのファイルは読み取り専用の扱いにする。書き込むのは出力先フォルダだけ。
- 不確かな点: KrkrDump がこのゲームの `Hxv4` に対応しているか。全エントリを自動で読む処理はエンジン内部のアドレス探しが必要で、失敗したら人の操作で読ませる形に落とす。
