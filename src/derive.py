# -*- coding: utf-8 -*-
"""把调过的 6 主色扩展成完整的一套：深/浅变体、背景/墨色、连续与发散 colormap，
并给出色盲友好度评级与安全子集长度。"""
import itertools
import math
from colorlib import (hex2lab, lab2hex, delta_e00, simulate_cvd, contrast,
                      sequential, diverging, lch, lab2rgb, hex2rgb,
                      flow, cyclic, uniformize, ramp_stats)
from data import (PALETTES, MONO, DIVERGING_OVERRIDE, SIGNATURE_OVERRIDE,
                  source_fingerprint)
from tuned import TUNED, SOURCE

# 下面所有产物都由 TUNED 派生，data.py 里的 colors 只作为原始记录留档。
# 所以改了色值却没重跑 tune 的话，产物一字不变 —— 在这里拦住，别让它静默通过。
if SOURCE != source_fingerprint():
    raise SystemExit(
        "src/tuned.py 与 src/data.py 不同步：data.py 的色值改过，但调优结果还是旧的。\n"
        "直接派生的话所有产物都不会变化（测试也照样全绿）。先跑 `make tune`（约 40s）。"
    )


def _shift(h, dL, cf=1.0):
    L, a, b = hex2lab(h)
    return lab2hex((max(0, min(100, L + dL)), a * cf, b * cf))


def cvd_min(hexes, kinds=('protan', 'deutan', 'tritan')):
    out = {}
    for k in kinds:
        labs = [hex2lab(simulate_cvd(c, k)) for c in hexes]
        out[k] = min(delta_e00(labs[i], labs[j])
                     for i, j in itertools.combinations(range(len(hexes)), 2))
    return out


def safe_set(hexes, thr=12.0):
    """按顺序贪心挑出在红/绿色盲下仍两两可分的最大子集（返回索引）。"""
    keep = [0]
    for i in range(1, len(hexes)):
        sub = [hexes[k] for k in keep] + [hexes[i]]
        if min(cvd_min(sub, ('protan', 'deutan')).values()) >= thr:
            keep.append(i)
    return keep


def grade(hexes):
    m = min(cvd_min(hexes, ('protan', 'deutan')).values())
    if m >= 13:
        return 'A'
    if m >= 9:
        return 'B'
    return 'C'


def order_smooth(cs, sig_i=0):
    """以签名色为起点，穷举 6! 条路径取相邻 ΔE00 之和最小者 —— 过渡最顺滑的排列。
    锚定起点比完全自由的路径平均只贵约 9%，但保证 colors[0] 始终是角色主色。"""
    n = len(cs)
    labs = [hex2lab(c) for c in cs]
    D = [[delta_e00(labs[i], labs[j]) for j in range(n)] for i in range(n)]
    rest = [i for i in range(n) if i != sig_i]
    best, bestcost = None, 1e18
    for tail in itertools.permutations(rest):
        p = (sig_i,) + tail
        cost = sum(D[p[k]][p[k + 1]] for k in range(n - 1))
        if cost < bestcost:
            best, bestcost = p, cost
    return list(best)


def order_hue(cs):
    """色相环顺序（红→橙→黄→绿→青→蓝→紫）；近中性色按明度排在末尾。"""
    info = [(i, *lch(c)) for i, c in enumerate(cs)]
    chrom = [t for t in info if t[2] >= 12]
    neut = [t for t in info if t[2] < 12]
    chrom.sort(key=lambda t: t[3])
    neut.sort(key=lambda t: -t[1])
    return [t[0] for t in chrom + neut]


def order_light(cs):
    """明度由浅到深。"""
    return [i for i, _ in sorted(enumerate(cs), key=lambda t: -lch(t[1])[0])]


def pick_diverging(cs, slug):
    """自动选发散色标两端：彩度足够 & 色相相距最远的一对。
    若整套配色色相跨度过小（单色系），则把签名色相旋转 165° 派生出另一端。"""
    if slug in DIVERGING_OVERRIDE:
        i, j = DIVERGING_OVERRIDE[slug]
        return i, j, 'manual'
    info = [lch(c) for c in cs]           # (L, C, h)
    def cool(h):
        return 130 <= h <= 310
    best = None
    for i, j in itertools.combinations(range(len(cs)), 2):
        Ci, Cj = info[i][1], info[j][1]
        if Ci < 16 or Cj < 16:
            continue
        dh = abs((info[i][2] - info[j][2] + 180) % 360 - 180)
        w = dh + 0.30 * min(Ci, Cj) + (25 if cool(info[i][2]) != cool(info[j][2]) else 0)
        if best is None or w > best[0]:
            best = (w, dh, i, j)
    if best and best[1] >= 80:
        _, _, i, j = best
        # 惯例：冷色在低值端，暖色在高值端
        if cool(info[j][2]) and not cool(info[i][2]):
            i, j = j, i
        return i, j, 'auto'
    # 单色系：派生对端
    k = max(range(len(cs)), key=lambda t: info[t][1])
    L, C, h = info[k]
    other = lab2hex((max(38.0, min(62.0, L)),
                     max(C, 18) * math.cos(math.radians(h + 165)),
                     max(C, 18) * math.sin(math.radians(h + 165))))
    return k, other, 'derived'


def build_one(p):
    src = TUNED[p['slug']]                      # 调优后的原始顺序 = 区分度优先
    mono = p['slug'] in MONO
    sig_i0 = SIGNATURE_OVERRIDE.get(p['slug'], 0)

    # --- 规范顺序 = 平滑排列（默认）；其它排序以规范顺序的下标表示 ---
    perm = order_smooth(src, sig_i0)            # canonical[k] = src[perm[k]]
    cs = [src[i] for i in perm]
    raw_ordered = [p['colors'][i] for i in perm]
    back = {old: new for new, old in enumerate(perm)}     # src 下标 -> canonical 下标
    orders = {
        'smooth': list(range(6)),
        'distinct': [back[i] for i in range(6)],
        'hue': order_hue(cs),
        'light': order_light(cs),
    }
    sig_i = back[sig_i0]
    safe_src = safe_set(src)                    # 在“区分度优先”序上贪心，再映射回来
    safe_idx = sorted(back[i] for i in safe_src)

    sig = cs[sig_i]
    di, dj, div_note = pick_diverging(cs, p['slug'])

    dark = [_shift(c, -15, 1.02) for c in cs]
    light = [_shift(c, +16, 0.78) for c in cs]
    # 背景纸色 / 墨色：取签名色的色相做极浅 / 极深
    L, a, b = hex2lab(sig)
    C = math.hypot(a, b) or 1e-6
    hu = math.atan2(b, a)
    bg = lab2hex((96.5, C * 0.06 * math.cos(hu), C * 0.06 * math.sin(hu)))
    bg2 = lab2hex((91.0, C * 0.13 * math.cos(hu), C * 0.13 * math.sin(hu)))
    ink = lab2hex((21.0, C * 0.35 * math.cos(hu), C * 0.35 * math.sin(hu)))
    muted = lab2hex((55.0, C * 0.16 * math.cos(hu), C * 0.16 * math.sin(hu)))

    lo_hex = cs[di] if isinstance(di, int) else di
    hi_hex = cs[dj] if isinstance(dj, int) else dj
    seq = uniformize(sequential(sig, 256))
    div = diverging(lo_hex, hi_hex, 256)
    flw = flow(cs, 256)
    cyc = cyclic(cs, 256)

    labs = [hex2lab(c) for c in cs]
    min_de = min(delta_e00(labs[i], labs[j])
                 for i, j in itertools.combinations(range(6), 2))
    cvd = cvd_min(cs)
    grey_ok = min(abs(lch(cs[i])[0] - lch(cs[j])[0])
                  for i, j in itertools.combinations(range(6), 2))

    return dict(
        slug=p['slug'], zh=p['zh'], en=p['en'], tone_zh=p['tone_zh'], tone_en=p['tone_en'],
        family=p['family'], source=p['source'], kind='mono' if mono else 'cat',
        name_zh=f"{p['zh']} · {p['tone_zh']}", name_en=f"{p['en']} · {p['tone_en']}",
        colors=cs, raw=raw_ordered, dark=dark, light=light, orders=orders,
        bg=bg, bg2=bg2, ink=ink, muted=muted,
        seq=seq, div=div, flow=flw, cyclic=cyc,
        div_pair=[lo_hex, hi_hex], div_note=div_note, signature=sig,
        ramp_stats={k: ramp_stats(v) for k, v in
                    (('seq', seq), ('div', div), ('flow', flw), ('cyclic', cyc))},
        wheel=[dict(i=i, L=round(lch(c)[0], 1), C=round(lch(c)[1], 1),
                    h=round(lch(c)[2], 1)) for i, c in enumerate(cs)],
        min_de=round(min_de, 1),
        cvd={k: round(v, 1) for k, v in cvd.items()},
        cvd_grade=grade(cs), safe_set=safe_idx,
        grey_gap=round(grey_ok, 1),
        contrast_white=[round(contrast(c, '#FFFFFF'), 2) for c in cs],
        L=[round(lch(c)[0], 1) for c in cs],
    )


def build_all():
    return [build_one(p) for p in PALETTES]


if __name__ == '__main__':
    import json
    lib = build_all()
    print(f"{'slug':<28}{'级':<4}{'安全前N':<8}{'minΔE':<8}{'protan':<8}{'deutan':<8}")
    for e in lib:
        print(f"{e['slug']:<28}{e['cvd_grade']:<4}{str(e['safe_set']):<20}{e['min_de']:<8}"
              f"{e['cvd']['protan']:<8}{e['cvd']['deutan']:<8}")
    json.dump(lib, open('library.json', 'w'), ensure_ascii=False, indent=1)
    print('\nwrote library.json  |  %d palettes' % len(lib))
