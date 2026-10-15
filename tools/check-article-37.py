#!/usr/bin/env python3
"""独立再計算: article-37 縦型フタ開け時高さの表と一致するか。"""
ROWS = [
    ("Panasonic NA-FA12V6", 1086, 1479, 1349),
    ("Panasonic NA-FA10K6", 1071, 1430, 1267),
    ("日立 BW-X120M", 1077, 1379, 1286),
    ("日立 BW-V100M", 1000, 1297, 1200),
    ("日立 BW-G70M", 980, 1223, 1086),
    ("シャープ ES-SW11L", 1055, 1320, 1264),
    ("シャープ ES-GV10L", 1009, 1287, 1231),
    ("シャープ ES-GV8L", 1018, 1262, 1113),
    ("シャープ ES-GE7K", 898, 1158, 1025),
    ("シャープ ES-GE5K", 890, 1132, 993),
    ("東芝 AW-12DPB6", 1098, 1529, 1334),
    ("東芝 AW-10DPB6", 1033, 1464, 1269),
    ("東芝 AW-9DPB6", 1033, 1434, 1268),
    ("東芝 AW-7DH6", 998, 1259, 1150),
    ("東芝 AW-10GM3", 1052, 1345, None),
]
EXPECTED_DELTA = [393, 359, 302, 297, 243, 265, 278, 244, 260, 242, 431, 431, 401, 261, 293]
EXPECTED_FOLD_DELTA = [130, 163, 93, 97, 137, 56, 56, 149, 133, 139, 195, 195, 166, 109]

def main():
    deltas = [f - c for _, c, f, _ in ROWS]
    assert deltas == EXPECTED_DELTA, (deltas, EXPECTED_DELTA)
    fulls = [f for _, _, f, _ in ROWS]
    closeds = [c for _, c, _, _ in ROWS]
    assert min(fulls) == 1132 and max(fulls) == 1529
    assert max(fulls) - min(fulls) == 397
    assert min(deltas) == 242 and max(deltas) == 431
    assert min(closeds) == 890 and max(closeds) == 1098
    fold_deltas = [f - fold for _, _, f, fold in ROWS if fold is not None]
    assert fold_deltas == EXPECTED_FOLD_DELTA, (fold_deltas, EXPECTED_FOLD_DELTA)
    print("OK", len(ROWS), "rows; full", min(fulls), "-", max(fulls), "; delta", min(deltas), "-", max(deltas))

if __name__ == "__main__":
    main()
