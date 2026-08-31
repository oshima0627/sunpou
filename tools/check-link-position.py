# -*- coding: utf-8 -*-
"""最初のアフィリエイトリンクが、記事本文のどこに出るかを測る。

なぜ測るか：Amazonアソシエイトのクッキーは24時間で、カート投入なら89日。
読者が離脱する前にリンクへ到達させたいので、**本文の20%以内**を目安にしている。

測り方：
  ビルド後の `site/dist/**/index.html` の `<article>` を読み、
  目次・カテゴリ名・日付・PR表記・図版キャプションを外したうえで、
  タグを落とした文字数に対する `class="buy"` の初出位置を出す。
  （目次を含めたまま測ると位置が数ポイント大きく出る）

使い方: node site/build.mjs && python tools/check-link-position.py
"""
import io
import os
import re
import glob
import sys

LIMIT = 20.0  # %


def strip_chrome(art):
    # class は "toc" 単独とは限らない（2026-08-31 に "toc toc--inline" になった）。
    # 完全一致で書いていたせいで目次が除外されなくなり、割合が数ポイント水増しされていた。
    art = re.sub(r'(?is)<nav class="toc[^"]*".*?</nav>', '', art)
    art = re.sub(r'(?is)<p class="(cat-label|dates|pr-notice)">.*?</p>', '', art)
    art = re.sub(r'(?is)<figcaption>.*?</figcaption>', '', art)
    return art


def plain(html):
    return re.sub(r'\s+', '', re.sub(r'(?s)<[^>]+>', '', html))


def main():
    root = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'site', 'dist')
    if not os.path.isdir(root):
        print('site/dist がありません。先に node site/build.mjs を実行してください')
        return 2
    rows = []
    for f in sorted(glob.glob(os.path.join(root, '**', 'index.html'), recursive=True)):
        slug = os.path.dirname(f).replace(os.sep, '/').replace(root.replace(os.sep, '/'), '') or '/'
        m = re.search(r'(?is)<article[^>]*>(.*?)</article>', io.open(f, encoding='utf-8').read())
        if not m:
            continue
        art = strip_chrome(m.group(1))
        total = len(plain(art))
        i = art.find('class="buy"')
        if i < 0 or not total:
            continue
        rows.append((slug, total, len(plain(art[:i])) / total * 100.0))
    rows.sort(key=lambda r: -r[2])
    print('%-40s %7s %9s' % ('page', 'chars', '1st buy%'))
    over = []
    for slug, total, pos in rows:
        mark = '  <-- %.0f%% 超' % LIMIT if pos > LIMIT else ''
        print('%-40s %7d %8.1f%s' % (slug, total, pos, mark))
        if pos > LIMIT:
            over.append((slug, pos))
    print()
    print('%d 本中 %d 本が %.0f%% を超えています' % (len(rows), len(over), LIMIT))
    for slug, pos in over:
        print('  - %s  %.1f%%' % (slug, pos))
    return 1 if over else 0


if __name__ == '__main__':
    sys.exit(main())
