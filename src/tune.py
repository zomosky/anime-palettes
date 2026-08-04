# -*- coding: utf-8 -*-
"""科研可用性微调器。

约束：每个颜色的 **色相角 h 基本锁定**（角色辨识度不丢），只允许
  · L*  在 [LMIN, LMAX] 内移动
  · C*  在原始彩度的 [0.45, 1.20] 倍内缩放
  · h   最多 ±7°（仅当同一配色内出现无法分离的同色相对时才动用）
目标：最大化「正常视觉 + 红/绿色盲模拟」下的最小两两 ΔE2000，
      同时惩罚对原色的偏离。坐标下降 + 多次随机重启。
"""
import math
import random
import itertools
from colorlib import (hex2lab, lab2hex, delta_e00, simulate_cvd, contrast)

LMIN, LMAX = 30.0, 78.0
MONO_LMIN, MONO_LMAX = 20.0, 86.0


def lab2lch(lab):
    L, a, b = lab
    return L, math.hypot(a, b), math.degrees(math.atan2(b, a)) % 360


def lch2hex(L, C, h):
    r = math.radians(h)
    return lab2hex((L, C * math.cos(r), C * math.sin(r)))


def _min_pair(hexes, weight_cvd=0.65):
    labs = [hex2lab(c) for c in hexes]
    pl = [hex2lab(simulate_cvd(c, 'protan')) for c in hexes]
    dl = [hex2lab(simulate_cvd(c, 'deutan')) for c in hexes]
    worst_n = worst_c = 1e9
    n = len(hexes)
    for i, j in itertools.combinations(range(n), 2):
        worst_n = min(worst_n, delta_e00(labs[i], labs[j]))
        worst_c = min(worst_c, delta_e00(pl[i], pl[j]), delta_e00(dl[i], dl[j]))
    return worst_n + weight_cvd * worst_c, worst_n, worst_c


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


def score(cur, orig, lmin, lmax):
    hexes = [lch2hex(*t) for t in cur]
    s, wn, wc = _min_pair(hexes)
    return s - 0.55 * _penalty(cur, orig) - _edge_penalty(hexes, lmin, lmax), wn, wc


def tune(colors, mono=False, seed=7, iters=340):
    rng = random.Random(seed)
    lmin, lmax = (MONO_LMIN, MONO_LMAX) if mono else (LMIN, LMAX)
    orig = [lab2lch(hex2lab(c)) for c in colors]

    def clamp(t, o):
        L, C, h = t
        L = max(lmin, min(lmax, L))
        cmax = max(o[1] * 1.20, 6.0)
        cmin = min(o[1] * 0.45, o[1])
        C = max(cmin, min(cmax, C))
        dh = (h - o[2] + 180) % 360 - 180
        dh = max(-7.0, min(7.0, dh))
        return (L, C, (o[2] + dh) % 360)

    best = None
    for restart in range(6):
        cur = [clamp((L + rng.uniform(-6, 6) if restart else L, C, h), o)
               for (L, C, h), o in zip(orig, orig)]
        cs = score(cur, orig, lmin, lmax)[0]
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
            ts = score(trial, orig, lmin, lmax)[0]
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
    from data import PALETTES
    MONO = {'noface-ink-gray', '2b-achromatic'}
    out = {}
    print('slug                          minΔE  CVDΔE')
    for p in PALETTES:
        hexes, wn, wc = tune(p['colors'], mono=p['slug'] in MONO)
        out[p['slug']] = hexes
        print(f"{p['slug']:<28} {wn:6.1f} {wc:6.1f}")
    with open('tuned.py', 'w') as f:
        f.write('# -*- coding: utf-8 -*-\n# 自动生成：科研可用性微调后的配色\nTUNED = ')
        f.write(repr(out).replace('], ', '],\n  '))
        f.write('\n')
