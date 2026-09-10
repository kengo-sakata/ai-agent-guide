#!/usr/bin/env python
"""maintain-guide の実行結果を機械的に採点する。

使い方: python grade.py <repo-path> [--sync-script <check_svg_sync.py>]
テスト用リポジトリは base コミット1つだけの状態から実行される前提。
"""
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

TARGET = "docs/02_Claudeの機能一覧.md"
OUT_OF_SCOPE = ("docs/00_", "docs/01_", "docs/04_", "docs/index.md",
                "docs/todo.md", "docs/xx_", "README.md")
SEC = "2-10"


def git(repo, *a):
    # core.quotepath=false: 日本語ファイル名を ã... にエスケープさせない
    r = subprocess.run(["git", "-C", str(repo), "-c", "core.quotepath=false", *a],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    return r.stdout


def section(text, num):
    """指定節の本文を切り出す。"""
    lines = text.splitlines()
    start = next((i for i, l in enumerate(lines) if l.startswith(f"## {num}.")), None)
    if start is None:
        return ""
    end = next((i for i in range(start + 1, len(lines)) if lines[i].startswith("## ")), len(lines))
    return "\n".join(lines[start:end])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("repo")
    ap.add_argument("--sync-script", default=None)
    ap.add_argument("--structure-script", default=None)
    a = ap.parse_args()
    repo = Path(a.repo)
    res = {}

    changed = [l for l in git(repo, "diff", "--name-only", "HEAD").splitlines() if l.strip()]
    untracked = [l[3:] for l in git(repo, "status", "--porcelain").splitlines()
                 if l.startswith("??")]
    res["_changed"] = changed
    res["_untracked"] = untracked

    # 対象外ファイルに触れていないか
    bad = [c for c in changed + untracked if any(c.startswith(p) for p in OUT_OF_SCOPE)]
    res["scope-outfiles"] = (not bad, f"対象外の変更: {bad}" if bad else "対象外ファイルの変更なし")

    # 変更範囲が本文+図解に限られているか
    allowed = [c for c in changed if c == TARGET or c.startswith("docs/images/")]
    stray = [c for c in changed if c not in allowed]
    res["scope-onefile"] = (not stray and TARGET in changed,
                            f"変更={changed} / 範囲外={stray}")

    # コミットしていないか
    n = git(repo, "rev-list", "--count", "HEAD").strip()
    res["no-commit"] = (n == "1", f"コミット数={n} (期待:1=baseのみ)")

    old = git(repo, "show", f"HEAD:{TARGET}")
    new = (repo / TARGET).read_text(encoding="utf-8")

    # 見出しの不変
    ho = [l for l in old.splitlines() if l.startswith("## ")]
    hn = [l for l in new.splitlines() if l.startswith("## ")]
    # 改訂履歴の新設は許容する
    hn_cmp = [l for l in hn if "改訂履歴" not in l]
    res["headings-intact"] = (ho == hn_cmp,
                              "見出し同一(改訂履歴の新設のみ許容)" if ho == hn_cmp
                              else f"差分: 追加={set(hn_cmp)-set(ho)} 削除={set(ho)-set(hn_cmp)}")

    # 改訂履歴
    has_sec = "改訂履歴" in new
    has_line = bool(re.search(r"^- 2026-09-10[:：]", new, re.M))
    res["revision-history"] = (has_sec and has_line,
                               f"セクション={has_sec} / 2026-09-10行={has_line}")

    # 出典URL:追加行のうちURLを含む割合
    diff = git(repo, "diff", "-U0", "HEAD", "--", TARGET)
    added = [l[1:] for l in diff.splitlines()
             if l.startswith("+") and not l.startswith("+++")]
    subst = [l for l in added if len(l.strip()) > 15 and not l.strip().startswith("- 2026-")]
    withurl = [l for l in subst if "http" in l]
    res["citations"] = (len(subst) == 0 or len(withurl) > 0,
                        f"実質的な追加行={len(subst)} / URLを含む行={len(withurl)}")

    # 古い iam リンクの修正
    s_old, s_new = section(old, SEC), section(new, SEC)
    had = "docs/en/iam" in s_old
    still = "docs/en/iam" in s_new
    res["stale-iam-link"] = (had and not still,
                             f"変更前に存在={had} / 変更後も残存={still}")

    # PNG等の混入
    junk = [c for c in changed + untracked
            if re.search(r"\.(png|jpg|jpeg|webp|bak|tmp)$", c, re.I)]
    res["no-png-committed"] = (not junk, f"混入={junk}" if junk else "中間生成物の混入なし")

    # 節の分量変化(過剰な書き足しの検出)
    lo, ln = len(s_old.splitlines()), len(s_new.splitlines())
    growth = (ln / lo) if lo else 0
    res["proportionality"] = (growth <= 1.6,
                              f"§{SEC} の行数 {lo} -> {ln} ({growth:.2f}倍)。"
                              f"1.6倍超は書き足し過剰の疑い")

    # 節の体裁(要素順)
    if a.structure_script:
        r = subprocess.run([sys.executable, a.structure_script, str(repo / TARGET),
                            "--section", SEC],
                           capture_output=True, text=True, encoding="utf-8",
                           errors="replace")
        res["structure"] = (r.returncode == 0, r.stdout.strip()[:400])
    else:
        res["structure"] = (None, "未検査(スクリプト未指定)")

    # 図解の整合
    svgs = [c for c in changed if c.endswith(".svg")]
    if not svgs:
        res["svg-in-sync"] = (True, "図解の変更なし(該当せず)")
    elif a.sync_script:
        r = subprocess.run([sys.executable, a.sync_script, *[str(repo / s) for s in svgs]],
                           capture_output=True, text=True, encoding="utf-8", errors="replace")
        res["svg-in-sync"] = (r.returncode == 0, r.stdout.strip()[:400])
    else:
        res["svg-in-sync"] = (None, f"未検査(スクリプト未指定): {svgs}")

    print(json.dumps(res, ensure_ascii=False, indent=2))
    checks = {k: v for k, v in res.items() if not k.startswith("_")}
    passed = sum(1 for v in checks.values() if v[0] is True)
    print(f"\n機械採点: {passed}/{len(checks)} 通過", file=sys.stderr)
    for k, v in checks.items():
        mark = {True: "PASS", False: "FAIL", None: "SKIP"}[v[0]]
        print(f"  [{mark}] {k}: {v[1]}", file=sys.stderr)


if __name__ == "__main__":
    main()
