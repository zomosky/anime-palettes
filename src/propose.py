# -*- coding: utf-8 -*-
"""给自己喜欢的角色加一套配色：输入 6 个原始色，输出 5 个调色方案供挑选。

    python src/propose.py --slug my-char --zh 角色名 --en Name \
        --tone-zh 霜蓝 --tone-en Frost --family 蓝 --source 出处 \
        --colors "#4FA8DE,#9CD2F0,#2A6BA5,#1F2430,#B9C4D0,#EAF2F8"

五个方案的差别在 tune 的目标函数取向，不在色相 —— 角色的辨识度色相始终锁着。
挑好之后 `--apply B` 写回 data.py 与 tuned.py，再跑 `make all && make skill`。

零依赖，只用 stdlib 和同目录的 colorlib / tune。
"""
import argparse
import itertools
import os
import sys
import unicodedata
from collections import namedtuple

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 只依赖 colorlib，刻意不 import derive —— derive 的模块级有指纹校验，
# 仓库处于「改了 data.py 还没 tune」时会 SystemExit，而那正是最需要 propose 的时候。
from colorlib import (delta_e00, hex2lab, lch, simulate_cvd, hex2rgb,   # noqa: E402
                      grade, safe_set)
import tune as tunemod                                                  # noqa: E402

Candidate = namedtuple("Candidate",
                       "key label colors min_de cvd_de grade safe_n gray_gap drift")


def _min_pairwise(hexes, transform=lambda c: c):
    labs = [hex2lab(transform(c)) for c in hexes]
    return min(delta_e00(labs[i], labs[j])
               for i, j in itertools.combinations(range(len(hexes)), 2))


def _gray_gap(hexes):
    """排序后相邻明度间隔的最小值 —— 灰度打印能不能分开就看它。"""
    Ls = sorted(lch(c)[0] for c in hexes)
    return min(b - a for a, b in zip(Ls, Ls[1:]))


def _cvd_de(hexes):
    """红/绿色盲模拟下的最小两两 ΔE00，取两种色盲里更差的那个。"""
    return min(_min_pairwise(hexes, lambda c: simulate_cvd(c, 'protan')),
               _min_pairwise(hexes, lambda c: simulate_cvd(c, 'deutan')))


def build(colors, mono=False):
    """跑 5 个 profile，返回按 A-E 排好的候选列表。"""
    out = []
    for key in ("A", "B", "C", "D", "E"):
        pf = tunemod.PROFILES[key]
        hexes, _, _ = tunemod.tune(colors, mono=mono, profile=pf)
        cvd = _cvd_de(hexes)
        drift = sum(delta_e00(hex2lab(a), hex2lab(b))
                    for a, b in zip(colors, hexes)) / len(colors)
        out.append(Candidate(
            key=key, label=pf.label, colors=hexes,
            min_de=round(_min_pairwise(hexes), 1),
            cvd_de=round(cvd, 1),
            grade=grade(hexes),
            safe_n=len(safe_set(hexes)),
            gray_gap=round(_gray_gap(hexes), 1),
            drift=round(drift, 1),
        ))
    return out


def ansi_row(colors):
    """一行 24 位真彩色块。终端不支持真彩时会退化成近似色，不影响判断。

    hex2rgb 返回的是 0–1 的浮点，这里必须先乘回 0–255 —— 直接拿去填 %d
    会把每个通道截成 0，整行印成纯黑（预览就废了，而且测试看不出来）。
    """
    cells = ""
    for c in colors:
        r, g, b = (max(0, min(255, round(v * 255))) for v in hex2rgb(c))
        cells += "\x1b[48;2;%d;%d;%dm      " % (r, g, b)
    return cells + "\x1b[0m"


def _width(s):
    """字符串在终端里占几列。中文是双宽，f-string 的 `<12` 按字符数补空格，
    「忠于原作」和「区分度优先」会差出一列，整张表就歪了。"""
    return sum(2 if unicodedata.east_asian_width(ch) in "WF" else 1 for ch in s)


def _lpad(s, n):
    return s + " " * max(0, n - _width(s))


def _rpad(s, n):
    return " " * max(0, n - _width(s)) + s


def _report(cands, colors):
    print("原始色  ", ansi_row(colors))
    print()
    print(_lpad("", 4) + _lpad("方案", 12) + _rpad("minΔE", 7) + _rpad("色盲ΔE", 8)
          + _rpad("级", 3) + _rpad("安全", 6) + _rpad("灰度间隔", 9) + _rpad("偏移", 7))
    for c in cands:
        print(_lpad(c.key, 4) + _lpad(c.label, 12)
              + f"{c.min_de:7.1f}{c.cvd_de:8.1f}{c.grade:>3}"
              + f"{c.safe_n:>4}/6{c.gray_gap:9.1f}{c.drift:7.1f}")
    print()
    for c in cands:
        print(f"{c.key} {c.label}")
        print(f"   正常   {ansi_row(c.colors)}")
        print(f"   红色盲 {ansi_row([simulate_cvd(x, 'protan') for x in c.colors])}")
        print(f"   灰度   {ansi_row([_gray(x) for x in c.colors])}")
        print("   " + " ".join(c.colors))
        print()
    print("偏移 = 相对原始色的平均 ΔE00，越小越忠于原作。")
    print("挑好之后用 --apply <方案字母> 写回 data.py 与 tuned.py（该选项尚未实现）。")


def _gray(hexcode):
    from colorlib import lab2hex
    L = lch(hexcode)[0]
    return lab2hex((L, 0.0, 0.0))


def _ramps(cs):
    """四条色标，直接用 colorlib 现算，不读 library.json ——
    这样全新 clone 上没跑过 make derive 也能用这个预览页。"""
    from colorlib import sequential, flow, diverging, cyclic, uniformize, lch as _lch
    sig = cs[0]
    warm = [c for c in cs if _lch(c)[1] >= 16]
    lo, hi = (warm[-1], warm[0]) if len(warm) >= 2 else (cs[-1], cs[0])
    return [("seq", uniformize(sequential(sig, 64))),
            ("flow", flow(cs, 64)),
            ("div", diverging(lo, hi, 64)),
            ("cyclic", cyclic(cs, 64))]


def _grad(seq):
    n = len(seq)
    stops = ",".join(f"{c} {i * 100 / (n - 1):.1f}%" for i, c in enumerate(seq))
    return f"linear-gradient(90deg,{stops})"


def render_html(cands, colors, meta):
    """5 个方案并排 + 每个的 4 条色标。单文件，不引任何外部资源。"""
    head = (
        "<!DOCTYPE html>\n<html lang=\"zh-CN\"><head><meta charset=\"utf-8\">"
        "<meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">"
        f"<title>{meta['zh']} · {meta['tone_zh']} —— 5 个调色方案</title><style>"
        "body{font:14px/1.6 system-ui,-apple-system,'PingFang SC',sans-serif;"
        "background:#f6f6f4;color:#1d1d21;margin:0;padding:26px}"
        "h1{font-size:19px;margin:0 0 4px}.meta{color:#6c6c76;font-size:12.5px;margin-bottom:20px}"
        ".card{background:#fff;border:1px solid #e4e4e0;border-radius:10px;padding:15px;margin-bottom:14px}"
        ".hd{display:flex;justify-content:space-between;align-items:baseline;gap:12px;margin-bottom:10px}"
        ".hd b{font-size:15px}.stat{color:#6c6c76;font-size:12px;font-variant-numeric:tabular-nums}"
        ".sw{display:flex;border-radius:6px;overflow:hidden;margin-bottom:9px}"
        ".sw div{flex:1;height:52px;display:flex;align-items:flex-end;justify-content:center;"
        "font-size:10px;padding-bottom:4px;font-family:ui-monospace,monospace}"
        ".rl{display:flex;gap:8px;font-size:11px;color:#6c6c76;margin-bottom:3px}"
        ".rl span{flex:1}.rs{display:flex;gap:8px}.rs i{flex:1;height:13px;border-radius:3px}"
        "</style></head><body>")
    ink = lambda c: "#111" if lch(c)[0] > 58 else "#fff"
    parts = [head,
             f"<h1>{meta['zh']} · {meta['tone_zh']}</h1>",
             f"<div class=\"meta\">{meta['en']} · {meta['tone_en']} &nbsp;|&nbsp; "
             f"{meta['source']} &nbsp;|&nbsp; 色系 {meta['family']} &nbsp;|&nbsp; "
             f"slug <code>{meta['slug']}</code></div>",
             "<div class=\"card\"><div class=\"hd\"><b>原始取色</b>"
             "<span class=\"stat\">未调优</span></div><div class=\"sw\">",
             "".join(f"<div style=\"background:{c};color:{ink(c)}\">{c[1:]}</div>" for c in colors),
             "</div></div>"]
    for c in cands:
        parts.append(
            f"<div class=\"card\"><div class=\"hd\"><b>{c.key} · {c.label}</b>"
            f"<span class=\"stat\">minΔE₀₀ {c.min_de} · 色盲ΔE {c.cvd_de} · "
            f"{c.grade} 级 · 安全 {c.safe_n}/6 · 灰度间隔 {c.gray_gap} · 偏移 {c.drift}</span></div>"
            "<div class=\"sw\">"
            + "".join(f"<div style=\"background:{x};color:{ink(x)}\">{x[1:]}</div>" for x in c.colors)
            + "</div><div class=\"rl\">"
            + "".join(f"<span>{k}</span>" for k, _ in _ramps(c.colors))
            + "</div><div class=\"rs\">"
            + "".join(f"<i style=\"background:{_grad(v)}\"></i>" for _, v in _ramps(c.colors))
            + "</div></div>")
    parts.append("</body></html>")
    return "".join(parts)


def parse_args(argv):
    ap = argparse.ArgumentParser(
        prog="propose.py", description="给新角色生成 5 个调色方案")
    ap.add_argument("--slug", required=True, help="小写连字符，如 my-char")
    ap.add_argument("--zh", required=True, help="中文角色名")
    ap.add_argument("--en", required=True, help="英文角色名")
    ap.add_argument("--tone-zh", required=True, help="中文色调标签，如 霜蓝")
    ap.add_argument("--tone-en", required=True, help="英文色调标签，如 Frost Blue")
    ap.add_argument("--family", required=True, help="色系标签")
    ap.add_argument("--source", required=True, help="出处作品")
    ap.add_argument("--colors", required=True, help="6 个 HEX，逗号分隔")
    ap.add_argument("--mono", action="store_true", help="单色相配色，放宽明度范围")
    ap.add_argument("--html", action="store_true", help="额外生成对比预览页")
    ap.add_argument("--apply", metavar="ABCDE", help="选定方案并写回 data.py / tuned.py")
    a = ap.parse_args(argv)

    import data
    if a.family not in data.FAMILY_ORDER:
        ap.error(f"--family 只能是 {data.FAMILY_ORDER} 之一，收到 {a.family!r}")
    if a.slug in {p["slug"] for p in data.PALETTES}:
        ap.error(f"slug {a.slug!r} 已存在")

    cs = [c.strip().upper() for c in a.colors.split(",") if c.strip()]
    if len(cs) != 6:
        ap.error(f"--colors 需要正好 6 个 HEX，收到 {len(cs)} 个")
    for c in cs:
        if len(c) != 7 or c[0] != "#":
            ap.error(f"{c!r} 不是 #RRGGBB 形式")
        try:
            int(c[1:], 16)
        except ValueError:
            ap.error(f"{c!r} 不是合法的 HEX")
    if len(set(cs)) != 6:
        ap.error("6 个色里有重复")
    if a.apply and a.apply.upper() not in "ABCDE":
        ap.error("--apply 只能是 A / B / C / D / E")
    a.colors = cs
    return a


def main(argv=None):
    a = parse_args(argv if argv is not None else sys.argv[1:])
    for c in a.colors:
        L = lch(c)[0]
        lo, hi = (20, 86) if a.mono else (30, 78)
        if not lo <= L <= hi:
            print(f"提示：{c} 的 L*={L:.0f} 在可用窗口 [{lo}, {hi}] 之外，"
                  f"tune 会把它拽回来，保真度会下降。", file=sys.stderr)
    cands = build(a.colors, mono=a.mono)
    _report(cands, a.colors)
    # 静默无操作比报错更糟：用户跑 --apply 看到退出码 0 加一份完整报告，
    # 很容易以为已经写回去了。--apply 落地时把这段换成真实逻辑即可。
    if a.apply:
        print("提示：--apply 尚未实现，本次没有写入任何文件。",
              file=sys.stderr)
    if a.html:
        os.makedirs("build", exist_ok=True)
        meta = dict(slug=a.slug, zh=a.zh, en=a.en, tone_zh=a.tone_zh,
                    tone_en=a.tone_en, family=a.family, source=a.source)
        path = os.path.join("build", f"propose-{a.slug}.html")
        with open(path, "w", encoding="utf-8") as f:
            f.write(render_html(cands, a.colors, meta))
        print(f"预览页：src/{path}")
    return cands, a


if __name__ == "__main__":
    main()
