# -*- coding: utf-8 -*-
"""色库自检。`python -m pytest tests/ -q`，或直接 `python tests/test_palettes.py`。

覆盖：数据完整性、四种排序的合法性、四种色标的色彩学性质
（明度单调 / 环形闭合 / 感知均匀）、色盲评级自洽、公开 API 行为。
"""
import itertools
import math
import os
import sys

import pytest

_ROOT = os.path.join(os.path.dirname(__file__), "..")
sys.path.insert(0, _ROOT)
sys.path.insert(0, os.path.join(_ROOT, "src"))
import anime_palettes as ap        # noqa: E402
from colorlib import delta_e00, hex2lab   # 生成链路用的同一份实现，下面单独验证它  # noqa: E402


def _de00(a, b):
    return delta_e00(hex2lab(a), hex2lab(b))


# Sharma et al. (2005) CIEDE2000 参考数据，先验证 ΔE00 实现本身是对的
CIEDE2000_REF = [
    ((50.0000, 2.6772, -79.7751), (50.0000, 0.0000, -82.7485), 2.0425),
    ((50.0000, 3.1571, -77.2803), (50.0000, 0.0000, -82.7485), 2.8615),
    ((50.0000, 2.8361, -74.0200), (50.0000, 0.0000, -82.7485), 3.4412),
    ((50.0000, -1.3802, -84.2814), (50.0000, 0.0000, -82.7485), 1.0000),
    ((50.0000, 2.5000, 0.0000), (50.0000, 0.0000, -2.5000), 4.3065),
    ((50.0000, 2.5000, 0.0000), (73.0000, 25.0000, -18.0000), 27.1492),
    ((50.0000, 2.5000, 0.0000), (50.0000, 3.1736, 0.5854), 1.0000),
    ((60.2574, -34.0099, 36.2677), (60.4626, -34.1751, 39.4387), 1.2644),
    ((22.7233, 20.0904, -46.6940), (23.0331, 14.9730, -42.5619), 2.0373),
    ((2.0776, 0.0795, -1.1350), (0.9033, -0.0636, -0.5514), 0.9082),
]


def test_delta_e00_implementation():
    for lab1, lab2, expect in CIEDE2000_REF:
        assert abs(delta_e00(lab1, lab2) - expect) < 1e-3, (lab1, lab2)

ALL = list(ap.PALETTES)


# ------------------------------------------------------------ 色彩学小工具
def _lab(h):
    def s2l(c):
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = [s2l(int(h[1:][i:i + 2], 16) / 255) for i in (0, 2, 4)]
    X = .4124564 * r + .3575761 * g + .1804375 * b
    Y = .2126729 * r + .7151522 * g + .0721750 * b
    Z = .0193339 * r + .1191920 * g + .9503041 * b

    def f(t):
        return t ** (1 / 3) if t > 216 / 24389 else (841 / 108) * t + 4 / 29
    fx, fy, fz = f(X / .95047), f(Y), f(Z / 1.08883)
    return (116 * fy - 16, 500 * (fx - fy), 200 * (fy - fz))


def _hue(h):
    L, A, B = _lab(h)
    return math.degrees(math.atan2(B, A)) % 360


# ------------------------------------------------------------ 数据完整性
def test_palette_count():
    assert len(ALL) == 36
    assert len({ap.PALETTES[s]["name_zh"] for s in ALL}) == 36


@pytest.mark.parametrize("slug", ALL)
def test_structure(slug):
    e = ap.PALETTES[slug]
    for key in ("colors", "dark", "light"):
        assert len(e[key]) == 6
        assert len(set(e[key])) == 6
    for key in ("bg", "bg2", "muted", "ink", "signature" if "signature" in e else "bg"):
        assert isinstance(e[key], str)
    for c in e["colors"] + e["dark"] + e["light"] + [e["bg"], e["bg2"], e["muted"], e["ink"]]:
        assert len(c) == 7 and c[0] == "#"
        int(c[1:], 16)


@pytest.mark.parametrize("slug", ALL)
def test_orders_are_permutations(slug):
    e = ap.PALETTES[slug]
    for name in ap.ORDERS:
        idx = e["orders"][name]
        assert sorted(idx) == list(range(6)), f"{slug}/{name} 不是合法置换"
        assert {e["colors"][i] for i in idx} == set(e["colors"])
    assert e["orders"]["smooth"] == list(range(6))


@pytest.mark.parametrize("slug", ALL)
def test_smooth_is_optimal_anchored_path(slug):
    """平滑序必须是「以主色为起点」的全部路径中相邻色差之和最小者。"""
    cs = ap.PALETTES[slug]["colors"]
    D = [[_de00(a, b) for b in cs] for a in cs]
    best = min(sum(D[p[i]][p[i + 1]] for i in range(5))
               for tail in itertools.permutations(range(1, 6))
               for p in [(0,) + tail])
    cur = sum(D[i][i + 1] for i in range(5))
    assert cur <= best + 1e-6


@pytest.mark.parametrize("slug", ALL)
def test_hue_and_light_orders(slug):
    e = ap.PALETTES[slug]
    Ls = [_lab(e["colors"][i])[0] for i in e["orders"]["light"]]
    assert all(Ls[i] >= Ls[i + 1] - 1e-6 for i in range(5)), "明度序应由浅到深"


# ------------------------------------------------------------ 色标性质
@pytest.mark.parametrize("slug", ALL)
def test_ramps_present(slug):
    e = ap.PALETTES[slug]
    for r in ap.RAMPS:
        assert len(e[r]) >= 17
        for c in e[r]:
            assert len(c) == 7 and c[0] == "#"


@pytest.mark.parametrize("slug", ALL)
def test_sequential_ramps_are_monotonic(slug):
    """seq / flow 必须明度单调 —— 这是「颜色表达多少」的前提。"""
    e = ap.PALETTES[slug]
    for r in ("seq", "flow"):
        assert e["ramp_stats"][r]["monotonic"], f"{slug}/{r} 明度不单调"
        assert e["ramp_stats"][r]["L_range"] >= 60, f"{slug}/{r} 明度跨度不足"
        Ls = [_lab(c)[0] for c in e[r]]
        assert all(Ls[i] >= Ls[i + 1] - 1.0 for i in range(len(Ls) - 1))


@pytest.mark.parametrize("slug", ALL)
def test_cyclic_is_a_closed_monotone_loop(slug):
    """环形色标必须首尾闭合、色相单向走满一圈（曾经这里出过反向折回的 bug）。"""
    e = ap.PALETTES[slug]
    assert _de00(e["cyclic"][0], e["cyclic"][-1]) < 6
    hs = [_hue(c) for c in e["cyclic"]]
    unwrapped = [hs[0]]
    for h in hs[1:]:
        unwrapped.append(unwrapped[-1] + (h - unwrapped[-1]) % 360)
    assert all(unwrapped[i + 1] >= unwrapped[i] - 1e-9 for i in range(len(unwrapped) - 1)), \
        f"{slug} 环形色标色相方向反转"
    assert 300 <= unwrapped[-1] - unwrapped[0] <= 375


@pytest.mark.parametrize("slug", ALL)
def test_ramp_uniformity(slug):
    """相邻步长的色差不能太不均匀，否则色标上会出现视觉断层。
    单色系配色（龙猫、2B）天然偏低，阈值按全库实测下限留出余量。"""
    for r in ("seq", "flow", "div", "cyclic"):
        u = ap.PALETTES[slug]["ramp_stats"][r]["uniformity"]
        assert u >= 0.35, f"{slug}/{r} 均匀度 {u} 过低"
    assert ap.PALETTES[slug]["ramp_stats"]["flow"]["uniformity"] >= 0.50


# ------------------------------------------------------------ 色盲
@pytest.mark.parametrize("slug", ALL)
def test_cvd_grade_consistent(slug):
    e = ap.PALETTES[slug]
    assert e["cvd_grade"] in "ABC"
    m = min(e["cvd"]["protan"], e["cvd"]["deutan"])
    assert e["cvd_grade"] == ("A" if m >= 13 else "B" if m >= 9 else "C")
    assert 1 <= len(e["safe_set"]) <= 6
    assert e["safe_set"] == sorted(set(e["safe_set"]))


def test_grade_distribution():
    from collections import Counter
    c = Counter(ap.PALETTES[s]["cvd_grade"] for s in ALL)
    assert c["A"] >= 15, "A 级配色太少，可用性回退了"


# ------------------------------------------------------------ 公开 API
def test_name_resolution():
    for alias in ("miku", "初音未来", "miku-aqua", "青碧", "Miku", "MIKU"):
        assert ap.colors(alias) == ap.colors("miku-aqua")
    with pytest.raises(KeyError):
        ap.colors("不存在的角色")


def test_colors_variants_and_orders():
    for slug in ALL:
        for order in ap.ORDERS:
            for variant in ("main", "dark", "light"):
                cs = ap.colors(slug, variant=variant, order=order)
                assert len(cs) == 6 and len(set(cs)) == 6
        assert len(ap.colors(slug, n=13)) == 13          # 循环取色
        assert ap.colors(slug)[0] == ap.PALETTES[slug]["colors"][0]


def test_helpers():
    for slug in ALL:
        assert set(ap.neutrals(slug)) == {"bg", "bg2", "muted", "ink"}
        assert 1 <= len(ap.safe(slug)) <= 6
        assert len(ap.to_hex_block(slug).splitlines()) == 6
        assert ap.ramp_info(slug, "flow")["monotonic"] is True
    assert len(ap.find("原神")) == 6
    assert set(ap.find("鬼灭之刃")) == {"giyu-pine", "nezuko-crimson-pink",
                                        "tanjiro-ink-ember", "zenitsu-lightning"}


def test_matplotlib_integration():
    mpl = pytest.importorskip("matplotlib")
    mpl.use("Agg")
    import matplotlib.pyplot as plt

    for w in ("seq", "flow", "div", "cyclic", "seq_r", "flow_r", "div_r", "cyclic_r"):
        cm = ap.cmap("miku", w)
        assert cm.N == 256
    assert ap.cmap("miku", "flow")(0.0) != ap.cmap("miku", "flow_r")(0.0)
    assert ap.cmap("miku", "flow", crop=(.2, .8))(0.0) != ap.cmap("miku", "flow")(0.0)
    assert len(ap.register("miku")) == 8
    assert len(ap.listed("miku", 6).colors) == 6

    ap.use("hutao", order="distinct")
    assert plt.rcParams["axes.prop_cycle"].by_key()["color"] == \
        ap.colors("hutao", order="distinct")

    before = plt.rcParams["axes.prop_cycle"]
    with ap.using("miku"):
        pass
    assert plt.rcParams["axes.prop_cycle"] == before


def test_plot_helpers_run():
    pytest.importorskip("matplotlib")
    pytest.importorskip("numpy")
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    ap.preview("eva01")
    ap.wheel("eva01")
    ap.scatter_guide("eva01")
    plt.close("all")


if __name__ == "__main__":
    sys.exit(pytest.main([__file__, "-q"]))
