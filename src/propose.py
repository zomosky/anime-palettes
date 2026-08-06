# -*- coding: utf-8 -*-
"""给自己喜欢的角色加一套配色：输入 6 个原始色，输出 5 个调色方案供挑选。

    python src/propose.py --slug my-char --zh 角色名 --en Name \
        --tone-zh 霜蓝 --tone-en "Frost Blue" --family 蓝 --source 出处 \
        --colors "#4FA8DE,#7BC6E8,#2A6BA5,#C86A7A,#D8B25C,#5E6B7A"

6 个色都要落在 L* ∈ [30, 78]（--mono 放宽到 [20, 86]），越界的会被拽进窗口，
上面这组示例就是照这个窗口挑的。取色的坑见 skills/anime-palettes/references/add-palette.md。

五个方案的差别在 tune 的目标函数取向，不在色相 —— 角色的辨识度色相始终锁着。
挑好之后 `--apply B` 写回 data.py 与 tuned.py，再跑 `make all && make skill`。

零依赖，只用 stdlib 和同目录的 colorlib / tune。
"""
import argparse
import html as html_escape
import itertools
import os
import sys
import unicodedata
from collections import namedtuple

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)

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
    print("挑好之后用 --apply <方案字母> 写回 data.py 与 tuned.py。")


def _gray(hexcode):
    from colorlib import lab2hex
    L = lch(hexcode)[0]
    return lab2hex((L, 0.0, 0.0))


def _ramps(cs):
    """四条色标，直接用 colorlib 现算，不读 library.json ——
    这样全新 clone 上没跑过 make derive 也能用这个预览页。

    div 的两端用 colorlib.pick_diverging_pair 选（跟 derive.py 生成正式
    产物时用的是同一份算法：彩度足够 & 色相相距最远的一对，色相跨度不够
    时派生对端）——不能自己简化一套，简化版曾经选出两个同冷暖的颜色，
    夹出来的不是发散色标。"""
    from colorlib import sequential, flow, diverging, cyclic, uniformize, pick_diverging_pair
    sig = cs[0]
    di, dj, _mode = pick_diverging_pair(cs)
    lo = cs[di] if isinstance(di, int) else di
    hi = cs[dj] if isinstance(dj, int) else dj
    return [("seq", uniformize(sequential(sig, 64))),
            ("flow", flow(cs, 64)),
            ("div", diverging(lo, hi, 64)),
            ("cyclic", cyclic(cs, 64))]


def _grad(seq):
    n = len(seq)
    stops = ",".join(f"{c} {i * 100 / (n - 1):.1f}%" for i, c in enumerate(seq))
    return f"linear-gradient(90deg,{stops})"


def render_html(cands, colors, meta):
    """5 个方案并排 + 每个的 4 条色标。单文件，不引任何外部资源。

    meta 里的字段（zh/en/tone_zh/tone_en/family/source/slug）全部来自用户
    在命令行敲的 --zh / --source 之类的参数，直接 f-string 拼进 HTML 之前
    要先转义 —— 角色名或出处里带 &、<、" 之类的字符会产出畸形 HTML。"""
    meta = {k: html_escape.escape(str(v)) for k, v in meta.items()}
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


def render_record(meta, colors):
    """一条 data.py 记录的源码文本，缩进与现有记录一致（4 空格 + 续行 9 空格）。"""
    cols = ", ".join(f'"{c}"' for c in colors)
    return (
        f'    dict(slug="{meta["slug"]}", zh="{meta["zh"]}", en="{meta["en"]}", '
        f'tone_zh="{meta["tone_zh"]}", tone_en="{meta["tone_en"]}",\n'
        f'         family="{meta["family"]}", source="{meta["source"]}",\n'
        f'         colors=[{cols}]),'
    )


def apply(meta, raw_colors, tuned_colors):
    """把新配色写回 data.py 与 tuned.py。

    tune() 逐套独立，别的 slug 的调优结果不受影响，所以这里只并入新条目
    再重算指纹 —— 单套不到 1s，不用重跑几十秒的全库。
    """
    # render_record 是拿双引号拼字符串字面量的，元数据里再带一个双引号就会把
    # data.py 写成语法错误。这个校验必须在任何写操作之前 —— 写坏之后才 SyntaxError
    # 虽然响亮，但用户得先 `git checkout src/data.py` 才能继续。
    bad = sorted(k for k, v in meta.items() if '"' in str(v))
    if bad:
        raise SystemExit(f"字段 {bad} 里含英文双引号，会写坏 data.py。"
                         "请改用中文引号“”或去掉。")

    data_path = os.path.join(_HERE, "data.py")
    with open(data_path, encoding="utf-8") as f:
        text = f.read()
    anchor = "\n]\n\n# 每套配色的“签名色”"
    if anchor not in text:
        raise SystemExit("data.py 的结构变了，找不到 PALETTES 列表的结尾，请手动添加记录")
    text = text.replace(anchor, "\n" + render_record(meta, raw_colors) + anchor, 1)
    with open(data_path, "w", encoding="utf-8") as f:
        f.write(text)

    # 指纹必须用「刚写完的」data.py 重算，所以这里要把已经 import 过的旧模块
    # 踢掉重新 import —— 少了这几行，SOURCE 还是旧值，derive.py 会直接报错退出。
    for m in ("data", "tuned"):
        sys.modules.pop(m, None)
    import data as _data
    import tuned as _tuned

    merged = dict(_tuned.TUNED)
    merged[meta["slug"]] = list(tuned_colors)
    tuned_path = os.path.join(_HERE, "tuned.py")
    with open(tuned_path, "w", encoding="utf-8") as f:
        f.write("# -*- coding: utf-8 -*-\n# 自动生成：科研可用性微调后的配色\n")
        f.write("# SOURCE = 生成这份结果时 data.py 的指纹，对不上就说明该重跑 `make tune` 了\n")
        f.write("SOURCE = %r\n\nTUNED = " % _data.source_fingerprint())
        f.write(repr(merged).replace("], ", "],\n  "))
        f.write("\n")

    print(f"已写入 src/data.py 与 src/tuned.py（{meta['slug']}）")
    print("接下来跑：make all && make skill")
    print("对结果不满意的话：git checkout src/data.py src/tuned.py")


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
    if a.apply:
        key = a.apply.upper()
        chosen = next(c for c in cands if c.key == key)
        meta = dict(slug=a.slug, zh=a.zh, en=a.en, tone_zh=a.tone_zh,
                    tone_en=a.tone_en, family=a.family, source=a.source)
        apply(meta, a.colors, list(chosen.colors))
    if a.html:
        # build 目录锚在 src/ 上而不是 cwd 上：propose.py 的用法是从仓库根
        # `python src/propose.py`，用相对路径的话页面会掉进根目录的 build/，
        # 而下面那行提示又写着 src/build/ —— 用户按提示去开会扑空。
        outdir = os.path.join(_HERE, "build")
        os.makedirs(outdir, exist_ok=True)
        meta = dict(slug=a.slug, zh=a.zh, en=a.en, tone_zh=a.tone_zh,
                    tone_en=a.tone_en, family=a.family, source=a.source)
        path = os.path.join(outdir, f"propose-{a.slug}.html")
        with open(path, "w", encoding="utf-8") as f:
            f.write(render_html(cands, a.colors, meta))
        print(f"预览页：{os.path.relpath(path, os.getcwd())}")
    return cands, a


if __name__ == "__main__":
    main()
