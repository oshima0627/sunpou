# 記事29 スーツケース総外寸158cm以内は何リットル？（`/cabin-bag/outer-sum-158-liters/`）

公開予定 2026-09-17。カテゴリ `cabin-bag`。
docs 番号は `article-28-*` まで使用済みのため、次の空き **29** を採用（依頼文の article-24 はカーテン記事と衝突）。

データ取得日はすべて **2026-09-17**。

---

## 1. テーマの決め方

- `docs/article-23-liter-nanpaku.md` §6 の次候補「スーツケース 158cm以内 何リットル」
- 勝てる型：①メーカー横断 ②カタログに無い読み（同じ総外寸帯でもLが割れる）
- 図版なし（airline 記事と同様）

---

## 2. データ源（一次）

### 航空会社

| 出典 | URL | 使った値 | 取り方 |
|---|---|---|---|
| ANA 国内線 無料預け入れ | https://www.ana.co.jp/ja/jp/guide/boarding-procedures/baggage/domestic/free/ | 3辺合計158cm以内／キャスターと持ち手を含む | curl 200 |
| ANA 国際線 無料預け入れ | https://www.ana.co.jp/ja/jp/guide/boarding-procedures/baggage/international/baggage-free/ | 同上 | curl 200 |
| JAL 国際線 大型手荷物 | https://www.jal.co.jp/jp/ja/inter/baggage/large/ | 1個あたり3辺総和203cm以内（重量はクラス別） | WebFetch 200 |

### サイズ定義

| 出典 | URL | 使った値 |
|---|---|---|
| ace 容量・重量・サイズ表記について | https://store.ace.jp/shop/pages/help_size.aspx | 外寸サイズ＝キャスターやハンドルなど突起を含む |

### 製品（HTMLコメント除去後に grep）

| 製品 | 外寸 | 総外寸／3辺和 | 容量 | URL |
|---|---|---|---|---|
| ace. フレットボード 68L 05433 | 72×51×28 | 151 | 68 L | https://store.ace.jp/shop/g/g05433-06/ |
| ace. フレットボード 100L 05434 | 70×53×34 | 157 | 100 L | https://store.ace.jp/shop/g/g05434-01/ |
| PROTECA ストラタム 00853 | 74×53×27 | 154 | 80 L | https://store.ace.jp/shop/g/g00853-03/ |
| PROTECA エアロフレックスDX2 01524 | 76×51×31 | 158 | 100 L | https://store.ace.jp/shop/g/g01524-09/ |
| Legend Walker 5516-70 | 76×51×28 | 155 | 81 L | https://legend-walker.com/products/5516-70 |
| Legend Walker 5528-70 | 77×50×30 | 157 | 87 L | https://legend-walker.com/products/5528-70 |
| Legend Walker 5901-70 | 78×44×35 | 157 | 91 L | https://legend-walker.com/products/5901-70 |
| Legend Walker 5510-70 | 76×51×30 | 157 | 100 L | https://legend-walker.com/products/5510-70 |
| Samsonite シーライト Spinner75 | 75.0×51.0×31.0 | 157（当サイト計算） | 94 L | https://www.samsonite.co.jp/samsonite/c-lite/spinner75/black/ss-122861-1041.html |

参考取得（本文表外）:

| 製品 | 総外寸 | 容量 | 備考 |
|---|---|---|---|
| PROTECA 360G4 02424 | 157 | 100 L | https://store.ace.jp/shop/g/g02424-01/ |
| PROTECA プレスティ 02434 | 157 | 100 L | https://store.ace.jp/shop/g/g02434-02/ |
| Legend Walker 6033-66 | 157 | 100 L | 72×50×35 |
| Samsonite ネクシス Spinner70 | 145（計算） | 82 L | 帯の下限寄り |

---

## 3. 検算

| 製品 | H+W+D | 公式総外寸／3辺和 | 一致 |
|---|---|---|---|
| 05433 | 72+51+28=151 | 151 | ○ |
| 05434 | 70+53+34=157 | 157 | ○ |
| 00853 | 74+53+27=154 | 154 | ○ |
| 01524 | 76+51+31=158 | 158 | ○ |
| 5516-70 | 76+51+28=155 | 155 | ○ |
| 5528-70 | 77+50+30=157 | 157 | ○ |
| 5901-70 | 78+44+35=157 | 157 | ○ |
| 5510-70 | 76+51+30=157 | 157 | ○ |
| Spinner75 | 75+51+31=157 | （公式総外寸欄なし・計算） | ○（計算） |

157帯の容量: 87 / 91 / 94 / 100 / 100 / （158で100） → 記事の「87〜100L」と一致。

---

## 4. 未検証

- 空港ゲージ実測適合
- 拡張時総外寸が158超になる製品の網羅
- 容量測り方の社間差・内寸／シェル厚
- サムソナイト幅・奥行のキャスター込み定義
- JAL 203cmページのキャスター込み文言
- IATAを158の万能根拠にすること
- RIMOWA（403）・無印など未取得

---

## 5. 次候補メモ（1行）

- 外寸と総外寸の差／キャスター＋ハンドル分は何cm（aceは本体と外寸を併記）
- 冷蔵庫の搬入経路フィット（通路幅×本体奥行）
- 据置食洗機のドア開放奥行の一次補強（Sharp/Hitachi 未検証残り）
