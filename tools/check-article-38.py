#!/usr/bin/env python3
"""独立再計算: article-38 ドラム式のドア開け時の奥行の表と一致するか。"""
ROWS = [
    # 製品, 外形奥行, ドア開け時の奥行（None=記載なし）
    ("Panasonic NA-LX129FL", 732, 1226),
    ("Panasonic NA-SD10UBL", 650, 1127),
    ("日立 BD-STX130M", 720, 1153),
    ("日立 BD-SX130M", 720, 1153),
    ("日立 BD-SV120M", 716, 1140),
    ("シャープ ES-X12C", 739, 1259),
    ("シャープ ES-12X2", 719, 1215),
    ("シャープ ES-10L2", 650, 1160),
    ("シャープ ES-8L2", 600, 1110),
    ("シャープ ES-7S2", 600, 973),
    ("東芝 TW-127XP5L", 720, 1175),
    ("東芝 TW-84GS5L", 633, 1111),
    ("東芝 TW-137XP6L", 720, None),
]
EXPECTED_DELTA = [494, 477, 433, 433, 424, 520, 496, 510, 510, 373, 455, 478]
# 横方向: 日立「ドア開け時の幅」− 外形幅
SIDE = [("日立 BD-STX130M", 630, 689, 59), ("日立 BD-SV120M", 638, 804, 166)]
# パナソニック: 壁面からの必要奥行 − ドア開け時の奥行
PANA_WALL = [(1236, 1226, 10), (1137, 1127, 10)]


def main():
    known = [(n, d, o) for n, d, o in ROWS if o is not None]
    deltas = [o - d for _, d, o in known]
    assert deltas == EXPECTED_DELTA, (deltas, EXPECTED_DELTA)
    opens = [o for _, _, o in known]
    depths = [d for _, d, _ in ROWS]
    assert min(opens) == 973 and max(opens) == 1259 and max(opens) - min(opens) == 286
    assert min(deltas) == 373 and max(deltas) == 520
    assert min(depths) == 600 and max(depths) == 739 and max(depths) - min(depths) == 139
    assert 1110 - 973 == 137  # ES-8L2 と ES-7S2（外形奥行600同士）
    hit = [o - d for n, d, o in known if n.startswith("日立")]
    assert min(hit) == 424 and max(hit) == 433
    for _, w, p, diff in SIDE:
        assert p - w == diff
    for wall, o, diff in PANA_WALL:
        assert wall - o == diff
    print("OK", len(known), "rows with data; open", min(opens), "-", max(opens), "; delta", min(deltas), "-", max(deltas))


if __name__ == "__main__":
    main()
