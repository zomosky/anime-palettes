# -*- coding: utf-8 -*-
"""科研可用性体检：类内区分度 / 白底可读性 / 色盲区分度 / 明度分布。"""
import itertools
from colorlib import de_hex, contrast, lch, simulate_cvd, hex2lab, delta_e00
from data import PALETTES

MIN_DE = 12.0        # 同一配色内任意两色的最小 dE00（前 4 色更严格）
MIN_DE_CORE = 15.0
MIN_CONTRAST = 1.9   # 白底上作为线条/柱体的最低对比度
MIN_CVD_DE = 9.0     # 色盲模拟后前 4 色的最小 dE00

def report():
    bad = 0
    for p in PALETTES:
        msgs = []
        cs = p["colors"]
        for i, j in itertools.combinations(range(6), 2):
            d = de_hex(cs[i], cs[j])
            lim = MIN_DE_CORE if (i < 4 and j < 4) else MIN_DE
            if d < lim:
                msgs.append(f"  dE {i}-{j} = {d:5.1f} ({cs[i]} vs {cs[j]}) < {lim}")
        for i, c in enumerate(cs):
            k = contrast(c, "#FFFFFF")
            if k < MIN_CONTRAST and i < 5:
                msgs.append(f"  白底对比 #{i} = {k:4.2f} ({c}) 偏浅")
            if k > 15.0 and i < 5:
                msgs.append(f"  白底对比 #{i} = {k:4.2f} ({c}) 过深")
        for kind in ("protan", "deutan"):
            sim = [simulate_cvd(c, kind) for c in cs]
            for i, j in itertools.combinations(range(4), 2):
                d = delta_e00(hex2lab(sim[i]), hex2lab(sim[j]))
                if d < MIN_CVD_DE:
                    msgs.append(f"  {kind} dE {i}-{j} = {d:5.1f}")
        Ls = sorted(round(lch(c)[0]) for c in cs)
        if msgs:
            bad += 1
            print(f"[{p['slug']}] {p['zh']}·{p['tone_zh']}  L*={Ls}")
            for m in msgs:
                print(m)
    print(f"\n{bad}/{len(PALETTES)} 套配色有待调整")

if __name__ == "__main__":
    report()
