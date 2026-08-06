# -*- coding: utf-8 -*-
"""科研可用性微调器。

约束：每个颜色的 **色相角 h 基本锁定**（角色辨识度不丢），只允许
  · L*  在 [LMIN, LMAX] 内移动
  · C*  在原始彩度的 [0.45, 1.20] 倍内缩放
  · h   最多 ±7°（仅当同一配色内出现无法分离的同色相对时才动用）
目标：最大化「正常视觉 + 红/绿色盲模拟」下的最小两两 ΔE2000，
      同时惩罚对原色的偏离。坐标下降 + 多次随机重启。

上面这些边界和目标函数的权重都收在 `Profile` 里，默认值即 `DEFAULT`。
`PROFILES` 另给 5 个取向不同的预设，供 `propose.py` 一次跑出多个候选方案挑选。
"""
import math
import random
import itertools
from collections import namedtuple
from colorlib import (hex2lab, lab2hex, delta_e00, simulate_cvd, contrast)

LMIN, LMAX = 30.0, 78.0
MONO_LMIN, MONO_LMAX = 20.0, 86.0

Profile = namedtuple("Profile", "name label penalty_w cvd_w lmin lmax "
                                "hue_span chroma_hi chroma_lo spread_w")

# 默认：与参数化之前的写死常量逐位等价。改这里会让 tuned.py 整体变化，
# CI 的逐字节 diff 会红 —— 要动之前先想清楚。
DEFAULT = Profile("default", "默认", 0.55, 0.65, LMIN, LMAX, 7.0, 1.20, 0.45, 0.0)

PROFILES = {
    # 偏离惩罚拉高 3 倍、色相几乎焊死 —— 色值基本不动
    "A": Profile("faithful", "忠于原作", 1.60, 0.65, LMIN, LMAX, 2.0, 1.20, 0.45, 0.0),
    # 惩罚压到一半以下、明度窗口放宽 —— 换取最大的两两色差
    "B": Profile("distinct", "区分度优先", 0.25, 0.65, 26.0, 82.0, 7.0, 1.30, 0.40, 0.0),
    # 色盲项权重拉到 2.5 倍 —— 冲 grade A
    "C": Profile("cvdsafe", "色盲友好", 0.55, 1.60, LMIN, LMAX, 7.0, 1.20, 0.45, 0.0),
    # 加明度间距项 —— 灰度打印下也能靠深浅区分
    "D": Profile("grayscale", "灰度打印", 0.45, 0.40, 28.0, 80.0, 7.0, 1.20, 0.45, 1.10),
    # 压彩度上限、抬明度下限 —— 适合大面积填充与背景
    "E": Profile("soft", "柔和低饱和", 0.55, 0.65, 42.0, 84.0, 7.0, 0.85, 0.40, 0.0),
}


def lab2lch(lab):
    L, a, b = lab
    return L, math.hypot(a, b), math.degrees(math.atan2(b, a)) % 360


def lch2hex(L, C, h):
    r = math.radians(h)
    return lab2hex((L, C * math.cos(r), C * math.sin(r)))


def _min_pair(hexes, cvd_w=0.65):
    labs = [hex2lab(c) for c in hexes]
    pl = [hex2lab(simulate_cvd(c, 'protan')) for c in hexes]
    dl = [hex2lab(simulate_cvd(c, 'deutan')) for c in hexes]
    worst_n = worst_c = 1e9
    n = len(hexes)
    for i, j in itertools.combinations(range(n), 2):
        worst_n = min(worst_n, delta_e00(labs[i], labs[j]))
        worst_c = min(worst_c, delta_e00(pl[i], pl[j]), delta_e00(dl[i], dl[j]))
    return worst_n + cvd_w * worst_c, worst_n, worst_c


def _penalty(cur, orig):
    p = 0.0
    for (L, C, h), (L0, C0, h0) in zip(cur, orig):
        p += abs(L - L0) / 9.0
        p += abs(C - C0) / 16.0
        dh = abs((h - h0 + 180) % 360 - 180)
        p += dh / 2.5
    return p


def _edge_penalty(hexes, lmin, lmax):
    p = 0.0
    for c in hexes:
        k = contrast(c, '#FFFFFF')
        if k < 2.0:
            p += (2.0 - k) * 14
        if k > 14.0:
            p += (k - 14.0) * 3
    return p


def _spread(cur):
    """明度间距项：6 个 L* 排序后相邻间隔的最小值。越大灰度下越好分。"""
    Ls = sorted(t[0] for t in cur)
    return min(b - a for a, b in zip(Ls, Ls[1:]))


def score(cur, orig, lmin, lmax, pf=DEFAULT):
    hexes = [lch2hex(*t) for t in cur]
    s, wn, wc = _min_pair(hexes, pf.cvd_w)
    s = s - pf.penalty_w * _penalty(cur, orig) - _edge_penalty(hexes, lmin, lmax)
    # 默认 profile 的 spread_w 是 0，这里必须整段跳过：`s + 0.0 * x` 在浮点下
    # 不保证等于 s，一旦无条件相加，58 套的调优结果就可能整体位移。
    if pf.spread_w:
        s += pf.spread_w * _spread(cur)
    return s, wn, wc


def tune(colors, mono=False, seed=7, iters=340, profile=None):
    pf = profile or DEFAULT
    rng = random.Random(seed)
    lmin, lmax = (MONO_LMIN, MONO_LMAX) if mono else (pf.lmin, pf.lmax)
    orig = [lab2lch(hex2lab(c)) for c in colors]

    def clamp(t, o):
        L, C, h = t
        L = max(lmin, min(lmax, L))
        cmax = max(o[1] * pf.chroma_hi, 6.0)
        cmin = min(o[1] * pf.chroma_lo, o[1])
        C = max(cmin, min(cmax, C))
        dh = (h - o[2] + 180) % 360 - 180
        dh = max(-pf.hue_span, min(pf.hue_span, dh))
        return (L, C, (o[2] + dh) % 360)

    best = None
    for restart in range(6):
        cur = [clamp((L + rng.uniform(-6, 6) if restart else L, C, h), o)
               for (L, C, h), o in zip(orig, orig)]
        cs = score(cur, orig, lmin, lmax, pf)[0]
        step = 6.0
        for it in range(iters):
            i = rng.randrange(len(cur))
            k = rng.random()
            L, C, h = cur[i]
            if k < 0.55:
                cand = (L + rng.gauss(0, step), C, h)
            elif k < 0.85:
                cand = (L, C + rng.gauss(0, step * 1.3), h)
            else:
                cand = (L, C, h + rng.gauss(0, 2.5))
            cand = clamp(cand, orig[i])
            trial = list(cur)
            trial[i] = cand
            ts = score(trial, orig, lmin, lmax, pf)[0]
            if ts > cs:
                cur, cs = trial, ts
            step = max(1.2, step * 0.995)
        if best is None or cs > best[1]:
            best = (cur, cs)
    cur = best[0]
    hexes = [lch2hex(*t) for t in cur]
    _, wn, wc = _min_pair(hexes)
    return hexes, wn, wc


if __name__ == '__main__':
    from data import PALETTES, MONO, source_fingerprint
    out = {}
    print('slug                          minΔE  CVDΔE')
    for p in PALETTES:
        hexes, wn, wc = tune(p['colors'], mono=p['slug'] in MONO)
        out[p['slug']] = hexes
        print(f"{p['slug']:<28} {wn:6.1f} {wc:6.1f}")
    with open('tuned.py', 'w') as f:
        f.write('# -*- coding: utf-8 -*-\n# 自动生成：科研可用性微调后的配色\n')
        f.write('# SOURCE = 生成这份结果时 data.py 的指纹，对不上就说明该重跑 `make tune` 了\n')
        f.write('SOURCE = %r\n\nTUNED = ' % source_fingerprint())
        f.write(repr(out).replace('], ', '],\n  '))
        f.write('\n')
