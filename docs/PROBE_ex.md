# 名前探索(改造版の追加機能)

名前がアーカイブから取り除かれた吉里吉里 Z のゲーム(`Hxv4` など。GARbro で名前が化ける)から、
復号済み・元の名前つきでファイルを書き出すための追加機能です。

## 仕組み

エンジンは名前でファイルを開き、その時点で復号します。DLL が名前の候補を順に開けば、
実在する名前だけが復号されて、名前つきで出ます。アーカイブの添字で開く方法は、暗号化されたままです。

## 使い方

1. 上流の README のとおり、`KrkrDump.dll` / `KrkrDump.json` / `KrkrDumpLoader.exe` を同じフォルダに置き、
   ゲームの exe を Loader にドラッグして起動します。
2. ゲームを少し遊び、ログ(`KrkrDump-日付.log`、`loglevel: 2`)で、ゲームが開く名前の形を調べます。
   `Included "..."` / `Excluded "..."` が、開かれた名前です。
3. 名前の規則を設定します(下記)。
4. ゲームのタイトル画面で `hotkey`(既定は F9)を **1 回**押し、メニューを開くなど何か操作します。
   探索はエンジンのスレッドで走るので、終わるまでゲームが固まって見えます。

## 設定

[`examples/voice_probe.json`](../examples/voice_probe.json) を参照してください。
JSON の `\` は `\\` と書きます(1 本だと読み込みに失敗し、設定がすべて無効になります)。
起動時にログへ `Config ... rules=N out=...` が出るので、読めたかを確認できます。

| キー | 説明 |
| --- | --- |
| `hotkey` | 探索を始めるキー(`F1`〜`F12`、または英数字 1 文字)。既定 `F9`。 |
| `voiceProbe.prefixes` | 名前の先頭(キャラ名など)の一覧。 |
| `voiceProbe.exts` | 試す拡張子。 |
| `voiceProbe.separator` | 区切り文字。既定 `_`。 |
| `voiceProbe.sceneDigits` / `numberDigits` | 場面・連番の桁数(0 埋め)。既定 3 / 4。 |
| `voiceProbe.sceneMax` | 場面番号の上限。既定 999。 |
| `voiceProbe.numberHead` | 先頭から何個を試して、その場面が存在するか決めるか。既定 4。 |
| `voiceProbe.numberMax` | 連番の上限。既定 10000。 |
| `voiceProbe.missLimit` | 連番がこの回数続けて外れたら、その場面を打ち切る。既定 30。 |
| `voiceProbe.subdir` | 出力フォルダ(`outputDirectory` の下)。 |
| `voiceProbe.groupByPrefix` | `true` なら `subdir\プレフィックス\名前` に分ける。 |
| `nameList` | 名前の候補を 1 行 1 件で書いた UTF-8 ファイル。 |
| `nameListPrefix` | 候補の前に付けるパス。既定 `arc://./`(ログで確認)。 |
| `nameListSubdir` | `nameList` の出力フォルダ。 |

形の決まった名前(`<プレフィックス>_<場面>_<連番>`)は `voiceProbe`、
それ以外(`noa_loop_101` など)は `nameList` で探します。`nameList` の候補は
[`tools/make_names.py`](../tools/make_names.py) で作れます。

```
python tools/make_names.py names_loop.txt --prefixes noa,ama --pattern "{p}_loop_{n:03d}" --count 1000 --exts .ogg,.ogg.sli
```

## 名前の手がかりの探し方

- 暗号化テキスト(`FE FE ...` で始まる)は、`decryptSimpleCrypt: true` で復号して出せます。
  ゲーム内のボイス表(このゲームでは `charvoice.csv`)に、命名規則が書かれていることがあります。
- シナリオ(`.ks.scn`、PSB)にも、ボイス名が平文で入っています。名前で開いて復号したものを grep します。
- `arc://./名前` で名前を指定すれば、シナリオも名前の候補から探せます。

## 注意

- ゲームの exe の位置が x86 / x64 のどちらかに合わせてビルドします(`Release|x86` / `Release|x64`)。
- ゲームのフォルダには何も書き込みません。書き込むのは `outputDirectory` だけです。
- 設定の新しいキーを省くと、既定値(上の表)で動きます。
