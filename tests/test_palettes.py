# -*- coding: utf-8 -*-
"""色库自检。`python -m pytest tests/ -q`，或直接 `python tests/test_palettes.py`。

覆盖：数据完整性、四种排序的合法性、四种色标的色彩学性质
（明度单调 / 环形闭合 / 感知均匀）、色盲评级自洽、公开 API 行为。
"""
import itertools
import math
import os
import re
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
    assert len(ALL) == 58
    assert len({ap.PALETTES[s]["name_zh"] for s in ALL}) == 58


# 新增配色的验收线：不能有 C 级，且最小色差要够画多系列图
NEW_ANIME = {
    "eren-survey-olive": "B", "haku-river": "B", "muichiro-mist": "B",
    "rem-peacock": "A", "violet-evergarden": "B", "nyanko-fortune": "A",
    "rx78-trikolor": "A",
}


@pytest.mark.parametrize("slug,expect", sorted(NEW_ANIME.items()))
def test_new_anime_palettes_meet_the_bar(slug, expect):
    e = ap.PALETTES[slug]
    assert e["cvd_grade"] == expect, f"{slug} 评级是 {e['cvd_grade']}，预期 {expect}"
    assert e["min_de"] >= 10.0, f"{slug} 最小 ΔE00 只有 {e['min_de']}"


NEW_GAME_1 = {
    "ichika-leoneed": "A", "minori-emerald": "B", "inkling-splat": "A",
    "joker-phantom": "B", "tarnished-gilded": "A", "nekomata-neon": "A",
    "acheron-magenta": "B", "dusk-inkvermilion": "A",
}


@pytest.mark.parametrize("slug,expect", sorted(NEW_GAME_1.items()))
def test_new_game_palettes_1_meet_the_bar(slug, expect):
    e = ap.PALETTES[slug]
    assert e["cvd_grade"] == expect, f"{slug} 评级是 {e['cvd_grade']}，预期 {expect}"
    assert e["min_de"] >= 10.0, f"{slug} 最小 ΔE00 只有 {e['min_de']}"


NEW_GAME_2 = {
    "yinlin-violetgold": "A", "jiyan-windteal": "B", "amiya-originium": "A",
    "texas-inkgray": "B", "robin-goldfeather": "A", "saber-knightblue": "A",
    "hollowknight-pale": "B",
}


@pytest.mark.parametrize("slug,expect", sorted(NEW_GAME_2.items()))
def test_new_game_palettes_2_meet_the_bar(slug, expect):
    e = ap.PALETTES[slug]
    assert e["cvd_grade"] == expect, f"{slug} 评级是 {e['cvd_grade']}，预期 {expect}"
    assert e["min_de"] >= 10.0, f"{slug} 最小 ΔE00 只有 {e['min_de']}"


def test_hue_coverage_has_no_big_hole():
    """58 套签名色沿色相环铺开后，最大空洞不得超过 25°。

    增补前最大空洞是 h 188->239 的 51°（miku 的青碧之后直接跳到 rei 的粉蓝），
    多系列图想在青蓝区找主色时无处可选。增补后实测 19°。
    """
    from colorlib import lch
    hs = sorted(lch(ap.PALETTES[s]["colors"][0])[2] for s in ALL)
    gaps = [b - a for a, b in zip(hs, hs[1:])] + [hs[0] + 360 - hs[-1]]
    assert max(gaps) <= 25.0, f"最大色相空洞 {max(gaps):.0f}°"


def test_no_c_grade_among_new_palettes():
    """新增的 22 套一个 C 级都不该有 —— C 级意味着 6 色在红/绿色盲下并团，
    只能退回安全子集。老库里有 5 套 C 是角色本身同色系，新增的没有这个包袱。"""
    new = set(NEW_ANIME) | set(NEW_GAME_1) | set(NEW_GAME_2)
    bad = {s for s in new if ap.PALETTES[s]["cvd_grade"] == "C"}
    assert not bad, f"新增配色里有 C 级：{bad}"


def test_warm_dark_signature_exists():
    """增补前 L*<35 的签名色全部挤在 h 276-291 的蓝紫带，红/橙/绿/青一个都没有。

    dusk-inkvermilion（墨朱，h≈20 L≈33）是全库第一个暖调暗色签名。
    """
    from colorlib import lch
    warm_dark = [s for s in ALL
                 if (lambda t: t[0] < 35 and (t[2] < 100 or t[2] > 330))(lch(ap.PALETTES[s]["colors"][0]))]
    assert "dusk-inkvermilion" in warm_dark, f"暖调暗色签名只有 {warm_dark}"


def test_tuned_is_in_sync_with_data():
    """改了 data.py 的色值却忘了 `make tune`，产物会一字不变地静默通过。

    生成链路里所有东西都从 tuned.py 派生，data.py 的 colors 只是留档，所以
    这种改动不会引发任何别的测试失败 —— 只有这里能抓到。
    """
    import data
    import tuned
    assert tuned.SOURCE == data.source_fingerprint(), (
        "src/tuned.py 与 src/data.py 不同步，跑 `make tune`（约 40s）重新调优"
    )


def test_family_is_valid():
    """family 是检索标签，拼错或用了没定义的标签会让 HTML 的筛选按钮筛不到东西。"""
    import data
    for p in data.PALETTES:
        assert p["family"] in data.FAMILY_ORDER, \
            f"{p['slug']} 的 family {p['family']!r} 不在 FAMILY_ORDER 里"


def test_slug_is_unique():
    import data
    slugs = [p["slug"] for p in data.PALETTES]
    dup = {s for s in slugs if slugs.count(s) > 1}
    assert not dup, f"slug 重复：{dup}"


def test_purple_family_signature_is_actually_purple():
    """「紫」这个标签的签名色必须真落在紫区（LCh 色相 285-335）。

    howl-iridescent 的 #C4548C 是 h=350 的粉红，一度被归在紫 —— 检索「紫」的人
    会拿到一套粉配色。这里守住这条线。
    """
    from colorlib import lch
    for slug in ALL:
        e = ap.PALETTES[slug]
        if e["family"] != "紫":
            continue
        h = lch(e["colors"][0])[2]
        assert 285 <= h <= 335, f"{slug} 归在紫，但签名色 {e['colors'][0]} 的 h={h:.1f}"


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
    # e["cvd"] 展示时四舍五入到 1 位小数，真实值（derive.grade() 用来定级的那个）
    # 可能比展示值低至多 0.05——卡在阈值 0.05 以内时评级可能落在相邻一档，
    # 容差按展示精度收紧，而不是拿四舍五入后的数字硬掰阈值。
    eps = 0.05
    if m >= 13 + eps:
        expect = {"A"}
    elif m >= 13 - eps:
        expect = {"A", "B"}
    elif m >= 9 + eps:
        expect = {"B"}
    elif m >= 9 - eps:
        expect = {"B", "C"}
    else:
        expect = {"C"}
    assert e["cvd_grade"] in expect, f"{slug}: min(protan,deutan)={m}, 评级={e['cvd_grade']}"
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
    assert set(ap.find("鬼灭之刃")) == {"giyu-pine", "muichiro-mist", "nezuko-crimson-pink",
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


# ------------------------------------------------------------ 命令行
def test_cli_commands(capsys):
    for argv in (["ls"], ["ls", "--family", "蓝", "--grade", "A"],
                 ["show", "胡桃"], ["show", "miku", "--order", "distinct"],
                 ["hex", "miku", "-n", "3"], ["hex", "hutao", "--safe"],
                 ["search", "原神"], ["json", "miku"]):
        assert ap.main(argv) == 0
        assert capsys.readouterr().out.strip()


def test_cli_hex_output(capsys):
    ap.main(["hex", "miku", "-n", "3", "--order", "distinct"])
    out = capsys.readouterr().out.split()
    assert out == ap.colors("miku", n=3, order="distinct")


def test_cli_json_roundtrip(capsys):
    import json
    ap.main(["json", "ganyu"])
    assert json.loads(capsys.readouterr().out)["colors"] == ap.colors("ganyu")


@pytest.mark.parametrize("lang", ["python", "python256", "r", "matlab", "origin", "css", "hex"])
@pytest.mark.parametrize("ramp", ["seq", "flow", "div", "cyclic"])
def test_code_generation(lang, ramp):
    src = ap.code("miku", ramp, lang)
    assert len(src) > 80
    assert ap.get("miku")["name_zh"] in src or "miku" in src


def test_generated_python_code_executes():
    pytest.importorskip("matplotlib")
    for ramp in ap.RAMPS:
        for lang in ("python", "python256"):
            ns = {}
            exec(ap.code("ganyu", ramp, lang), ns)
            cm = ns[f"ganyu_{ramp}"]
            assert cm(0.0) != cm(0.5) != cm(1.0)
            if ramp == "cyclic":            # 环形色标首尾必须接上
                assert max(abs(a - b) for a, b in zip(cm(0.0), cm(1.0))) < 0.02
            else:
                assert cm(0.0) != cm(1.0)


def test_code_rejects_bad_args():
    with pytest.raises(ValueError):
        ap.code("miku", "nope")
    with pytest.raises(ValueError):
        ap.code("miku", "flow", "cobol")


# ------------------------------------------------------------ 标志物
_MARK_CMDS = set("MLHVCSQTAZmlhvcsqtaz")
_MARK_NUMS = set("0123456789 ,.-eE")


def test_every_slug_has_a_mark():
    """标志物开关打开后，缺 mark 的卡片会露出空洞。键集合必须严格相等。"""
    import data
    import marks
    slugs = {p["slug"] for p in data.PALETTES}
    assert set(marks.MARKS) == slugs, (
        f"缺 mark：{sorted(slugs - set(marks.MARKS))}；"
        f"多余 mark：{sorted(set(marks.MARKS) - slugs)}"
    )


def test_mark_is_wellformed():
    """不要用 @parametrize 展开 —— 那会在收集阶段就 import marks，
    marks.py 还没建的时候整个测试模块都收集不起来。"""
    import marks
    for slug, (vb, d) in sorted(marks.MARKS.items()):
        parts = vb.split()
        assert len(parts) == 4, f"{slug} 的 viewBox 不是四段：{vb!r}"
        for x in parts:
            float(x)
        assert d.strip(), f"{slug} 的 path 是空的"
        assert d.lstrip()[0] in "Mm", f"{slug} 的 path 不是以 M/m 开头：{d[:12]!r}"
        bad = set(d) - _MARK_CMDS - _MARK_NUMS
        assert not bad, f"{slug} 的 path 含非法字符：{sorted(bad)}"


_PATH_TOKEN = re.compile(r"[MmLlHhVvCcSsQqTtAaZz]|[-+]?(?:\d*\.\d+|\d+\.?\d*)(?:[eE][-+]?\d+)?")


def _arc_points(p0, rx, ry, rot, large, sweep, p1, n):
    """SVG 圆弧的端点参数化 -> 圆心参数化（规范 F.6.5），再按角度采样。"""
    (x0, y0), (x1, y1) = p0, p1
    rx, ry = abs(rx), abs(ry)
    if rx == 0 or ry == 0 or (x0, y0) == (x1, y1):
        return [p1]
    phi = math.radians(rot)
    cs, sn = math.cos(phi), math.sin(phi)
    dx, dy = (x0 - x1) / 2.0, (y0 - y1) / 2.0
    xp, yp = cs * dx + sn * dy, -sn * dx + cs * dy
    lam = xp * xp / (rx * rx) + yp * yp / (ry * ry)
    if lam > 1:                       # 半径不够大时按规范等比放大
        rx, ry = rx * math.sqrt(lam), ry * math.sqrt(lam)
    num = rx * rx * ry * ry - rx * rx * yp * yp - ry * ry * xp * xp
    den = rx * rx * yp * yp + ry * ry * xp * xp
    co = math.sqrt(max(num, 0.0) / den) * (-1 if large == sweep else 1)
    cxp, cyp = co * rx * yp / ry, -co * ry * xp / rx
    cx = cs * cxp - sn * cyp + (x0 + x1) / 2.0
    cy = sn * cxp + cs * cyp + (y0 + y1) / 2.0
    t0 = math.atan2((yp - cyp) / ry, (xp - cxp) / rx)
    t1 = math.atan2((-yp - cyp) / ry, (-xp - cxp) / rx)
    dt = t1 - t0
    if not sweep and dt > 0:
        dt -= 2 * math.pi
    elif sweep and dt < 0:
        dt += 2 * math.pi
    steps = max(int(n * abs(dt) / (2 * math.pi)) + 4, 6)
    out = []
    for k in range(1, steps + 1):
        t = t0 + dt * k / steps
        out.append((cs * rx * math.cos(t) - sn * ry * math.sin(t) + cx,
                    sn * rx * math.cos(t) + cs * ry * math.sin(t) + cy))
    return out


def _path_points(d, n=24):
    """把一条 path 采样成点集：直线取端点，贝塞尔与圆弧各取若干点。

    纯 Python，不引第三方依赖 —— 本项目核心零依赖，测试也守这条。
    采样点都落在曲线上，所以算出来的包围盒是真实包围盒的内逼近；
    n=24 时两者差距在 1e-3 量级，远小于下面阈值留的余量。
    """
    toks = [t if t in "MmLlHhVvCcSsQqTtAaZz" else float(t)
            for t in _PATH_TOKEN.findall(d)]
    pts, cur, sub = [], (0.0, 0.0), (0.0, 0.0)
    ctrl_c = ctrl_q = None
    cmd, i = None, 0
    while i < len(toks):
        if isinstance(toks[i], str):
            cmd = toks[i]
            i += 1
            if cmd in "Zz":
                cur = sub
                pts.append(cur)
                ctrl_c = ctrl_q = None
            continue
        assert cmd, "path 不是以命令开头"
        rel, c = cmd.islower(), cmd.upper()
        x, y = cur

        def a(k):                      # 取 k 个参数
            return toks[i:i + k]

        if c in "ML":
            p = (a(2)[0] + (x if rel else 0), a(2)[1] + (y if rel else 0))
            i += 2
            if c == "M":
                sub = p
                cmd = "l" if rel else "L"
            pts.append(p)
            cur, ctrl_c, ctrl_q = p, None, None
        elif c in "HV":
            v = a(1)[0]
            i += 1
            p = ((v + (x if rel else 0), y) if c == "H" else (x, v + (y if rel else 0)))
            pts.append(p)
            cur, ctrl_c, ctrl_q = p, None, None
        elif c in "CS":
            if c == "C":
                q = a(6)
                i += 6
                p1 = (q[0] + (x if rel else 0), q[1] + (y if rel else 0))
                p2 = (q[2] + (x if rel else 0), q[3] + (y if rel else 0))
                p3 = (q[4] + (x if rel else 0), q[5] + (y if rel else 0))
            else:
                q = a(4)
                i += 4
                p1 = (2 * x - ctrl_c[0], 2 * y - ctrl_c[1]) if ctrl_c else (x, y)
                p2 = (q[0] + (x if rel else 0), q[1] + (y if rel else 0))
                p3 = (q[2] + (x if rel else 0), q[3] + (y if rel else 0))
            for k in range(1, n + 1):
                t, u = k / float(n), 1 - k / float(n)
                pts.append((u ** 3 * x + 3 * u * u * t * p1[0] + 3 * u * t * t * p2[0] + t ** 3 * p3[0],
                            u ** 3 * y + 3 * u * u * t * p1[1] + 3 * u * t * t * p2[1] + t ** 3 * p3[1]))
            cur, ctrl_c, ctrl_q = p3, p2, None
        elif c in "QT":
            if c == "Q":
                q = a(4)
                i += 4
                p1 = (q[0] + (x if rel else 0), q[1] + (y if rel else 0))
                p2 = (q[2] + (x if rel else 0), q[3] + (y if rel else 0))
            else:
                q = a(2)
                i += 2
                p1 = (2 * x - ctrl_q[0], 2 * y - ctrl_q[1]) if ctrl_q else (x, y)
                p2 = (q[0] + (x if rel else 0), q[1] + (y if rel else 0))
            for k in range(1, n + 1):
                t, u = k / float(n), 1 - k / float(n)
                pts.append((u * u * x + 2 * u * t * p1[0] + t * t * p2[0],
                            u * u * y + 2 * u * t * p1[1] + t * t * p2[1]))
            cur, ctrl_c, ctrl_q = p2, None, p1
        elif c == "A":
            q = a(7)
            i += 7
            p = (q[5] + (x if rel else 0), q[6] + (y if rel else 0))
            pts.extend(_arc_points(cur, q[0], q[1], q[2], int(q[3]), int(q[4]), p, n))
            cur, ctrl_c, ctrl_q = p, None, None
        else:
            raise AssertionError("没处理的命令 %r" % cmd)
    return pts


def test_mark_stays_inside_the_viewbox():
    """标志物不能超出 24x24，也不能贴到边上 —— 44px 渲染时要留出净空。

    同样不要 @parametrize：收集阶段就 import marks 的话，marks.py 一旦缺失
    整个测试模块都收集不起来，理由和 test_mark_is_wellformed 一样。

    阈值 [1.5, 22.5] 的来历：画法约定是「主体占 20x20、留约 2 单位边距」，但末梢
    （笔尖、柄头、垂穗）允许略微探出这条线。全库实测极值是 x ∈ [2.10, 21.90]、
    y ∈ [1.90, 22.19]：上顶到 1.90 的是 nyanko-fortune 的顶环，下探到 22.19 的是
    hollowknight-pale 的柄尾圆头，brief 给的 miku / totoro / zenitsu 三个样板也都
    正好压在 22.00。可见 2 单位是目标不是硬线，再留 0.5 单位缓冲就落到 1.5 / 22.5。
    这个值折算到 44px 渲染约 2.75px 净空，卡片里不会贴边；同时又足够紧 ——
    真把图形画飞（比如把 24 当成 20 用、或者坐标整体偏移）会立刻红。
    """
    import marks
    lo, hi = 1.5, 22.5
    for slug, (vb, d) in sorted(marks.MARKS.items()):
        x0, y0, w, h = [float(v) for v in vb.split()]
        assert (x0, y0, w, h) == (0, 0, 24, 24), "%s 的 viewBox 不是 0 0 24 24" % slug
        pts = _path_points(d)
        assert pts, "%s 采样不出任何点" % slug
        xs, ys = [p[0] for p in pts], [p[1] for p in pts]
        box = (min(xs), min(ys), max(xs), max(ys))
        assert lo <= box[0] and lo <= box[1] and box[2] <= hi and box[3] <= hi, (
            "%s 的包围盒 %s 超出 [%s, %s]，44px 下会贴边或出框"
            % (slug, tuple(round(v, 2) for v in box), lo, hi))


def test_marks_do_not_leak_into_library():
    """marks 是展示资源不是色彩数据。让它进 library.json 会破坏
    dist/anime_palettes.json 与 src/library.json 内容完全相同这条不变量。"""
    import json
    lib = json.load(open(os.path.join(_ROOT, "src", "library.json")))
    for e in lib:
        assert "mark" not in e and "path" not in e, f"{e['slug']} 的库记录里混进了标志物字段"


def test_html_ships_marks_off_by_default():
    """标志物默认关闭，且 MK 常量必须是真被替换进去的、内容对得上 marks.MARKS 的数据。

    只查子串 "const MK=" 或者挑 5 个 slug 断言在 html 里出现是不够的：前者只证明
    那 8 个字符存在，不管后面跟的是不是合法 JSON；后者恒真——slug 本来就在页面的
    DATA 数据块里，跟标志物有没有正确内嵌毫无关系。变异检验：把 gen_html.py 里
    __MARKS__ 的替换整个删掉（HTML 里留下字面量 "const MK=__MARKS__;"，页面 JS
    直接语法错误）或者把载荷换成 "const MK={};"，这两种破坏都会让上面两条旧断言
    继续全绿，必须解析出 MK 的实际 JSON 内容才挡得住。
    """
    import json
    import re
    import marks
    html = open(os.path.join(_ROOT, "dist", "anime-palettes.html"), encoding="utf-8").read()
    m = re.search(r'const MK=(\{.*?\});', html)
    assert m, "标志物数据没内嵌进 HTML（找不到形如 const MK={...}; 的赋值）"
    mk = json.loads(m.group(1))
    assert set(mk) == set(marks.MARKS), "HTML 里 MK 的 slug 集合和 marks.MARKS 对不上"
    for slug, (vb, d) in marks.MARKS.items():
        assert mk[slug] == [vb, d], f"{slug} 的标志物数据（viewBox/path）没对上"
    mb = re.search(r'<button id="mkbtn"[^>]*>', html)
    assert mb, "找不到标志物开关按钮"
    assert "class=" not in mb.group(0), f"开关默认带了类，应该是关闭态：{mb.group(0)}"


# ------------------------------------------------------------ 调优器 profile
# 抽样而不是全跑：单套调优约 1.1s，58 套要 65s，CI 三个 Python 版本就是 3 分钟。
# 全量校验放在 Task 8 的手工步骤和 CI 的 tuned.py 逐字节 diff 里，这里只挡住常见破坏。
# 这 6 套不是随手挑的，是拿变异检验选出来的：把 DEFAULT 的每个参数各推一小步
# （lmin 30→30.1、lmax 78→77.9、hue_span 7→4、chroma_hi 1.20→1.19、
#  chroma_lo 0.45→0.46、penalty_w 0.55→0.56、cvd_w 0.65→0.66），全库 58 套逐个跑，
# 记下哪些 slug 的结果会变，再选能把 7 项全覆盖的 6 套。实测两件事很反直觉：
#   · hue_span 全库只有 3 套测得出来（zenitsu-lightning / acheron-magenta / luffy-red-straw）
#     —— ±7° 的色相余量平时根本不吃满，不含这 3 套之一就等于没测色相约束
#   · cvd_w 也只有 6 套测得出来
# 括号里的数字取自 data.py 原始色，即 tune 的实际输入：
#   2b-achromatic       MONO 分支；平均彩度 7.4 全库最低，2 色顶到 clamp 的 C≥6 地板
#   noface-ink-gray     MONO 分支；色相跨度 23.8° 全库最窄；覆盖 cvd_w
#   gojo-sky            非 MONO 里色相最窄（35.2°）；6 色有 4 色落在 [30,78] 窗口外
#   hollowknight-pale   两两 ΔE00 最小（6.75），最贴 clamp 与 _edge_penalty 的边界
#   inkling-splat       两两 ΔE00 最大（28.63）；色相跨度 262.9°、平均彩度 50.6，都近全库上限
#   acheron-magenta     唯一能把上面 5 套补满 7/7 的一套 —— 它独家覆盖 hue_span 与 lmin
# 换 slug 前先把变异检验重跑一遍，别让覆盖率悄悄掉下去（换之前那组是 6/7，漏 hue_span）。
_PROFILE_SAMPLE = ["2b-achromatic", "noface-ink-gray", "gojo-sky",
                   "hollowknight-pale", "inkling-splat", "acheron-magenta"]


@pytest.mark.parametrize("slug", _PROFILE_SAMPLE)
def test_default_profile_reproduces_tuned_py(slug):
    """propose.py 要用不同权重跑 tune，所以把常量参数化了。

    默认 profile 必须与参数化之前逐位等价 —— 否则现有 58 套的 tuned.py 会变，
    CI 那道逐字节 diff 直接红，而且全部产物都要跟着重生成。
    """
    import data
    import tune
    import tuned
    p = next(x for x in data.PALETTES if x["slug"] == slug)
    got, _, _ = tune.tune(p["colors"], mono=slug in data.MONO)
    assert got == tuned.TUNED[slug], (
        f"{slug} 的默认 profile 输出与 tuned.py 不一致\n"
        f"  tuned.py: {tuned.TUNED[slug]}\n"
        f"  重算:     {got}"
    )


def test_profiles_are_five_and_named():
    import tune
    assert sorted(tune.PROFILES) == ["A", "B", "C", "D", "E"]
    for k, pf in tune.PROFILES.items():
        assert pf.label, f"profile {k} 没有中文标签"


@pytest.mark.parametrize("key", ["A", "B", "C", "D", "E"])
def test_every_profile_produces_six_valid_hexes(key):
    import tune
    cols = ["#4FA8DE", "#9CD2F0", "#2A6BA5", "#1F2430", "#B9C4D0", "#EAF2F8"]
    out, wn, wc = tune.tune(cols, profile=tune.PROFILES[key])
    assert len(out) == 6 and len(set(out)) == 6
    for c in out:
        assert len(c) == 7 and c[0] == "#"
        int(c[1:], 16)
    assert wn > 0 and wc > 0


def test_profile_a_stays_closer_to_source_than_profile_b():
    """A 是「忠于原作」、B 是「区分度优先」。A 的平均偏移必须比 B 小，
    否则这两个方案给用户的选择就是假的。"""
    import tune
    from colorlib import delta_e00, hex2lab
    cols = ["#4FA8DE", "#9CD2F0", "#2A6BA5", "#1F2430", "#B9C4D0", "#EAF2F8"]

    def drift(key):
        out, _, _ = tune.tune(cols, profile=tune.PROFILES[key])
        return sum(delta_e00(hex2lab(a), hex2lab(b)) for a, b in zip(cols, out)) / 6

    assert drift("A") < drift("B")


# ------------------------------------------------------------ propose
_PROPOSE_DEMO = ["#4FA8DE", "#9CD2F0", "#2A6BA5", "#1F2430", "#B9C4D0", "#EAF2F8"]


def test_propose_builds_five_candidates():
    import propose
    cands = propose.build(_PROPOSE_DEMO)
    assert [c.key for c in cands] == ["A", "B", "C", "D", "E"]
    for c in cands:
        assert len(c.colors) == 6 and len(set(c.colors)) == 6
        assert c.grade in "ABC"
        assert 0 <= c.safe_n <= 6
        assert c.min_de > 0 and c.cvd_de > 0 and c.drift >= 0


# C / D / E 三个 profile「名副其实」这件事，不能拿单独一套配色做单点比较。
# 理由是 tune() 对 profile 参数的敏感是**跳变式**的（坐标下降 + 随机重启，
# 见上面 _PROFILE_SAMPLE 那段变异检验：参数只推 0.01~0.1 就有 6~53/58 套整体
# 跳到另一个局部最优）。单点比较会被无关的小改动翻过去，红的原因和改动者的意图
# 毫无关系。加容差也没用 —— 这不是浮点误差，是目标函数地形。
#
# 全库 58 套实测（每套跑 A/C/D/E 四个 profile）：
#   C 的色盲 ΔE 高于 A ：56/58，反例 eren-survey-olive(-0.80)、noface-ink-gray(-0.20)
#   D 的明度间隔大于 A ：58/58，最薄 giyu-pine(+1.50)
#   E 的平均彩度低于 A ：58/58，最薄 2b-achromatic(-1.08)
# 所以 C 写成聚合断言（它确实只是统计性质），D / E 写成「这组全部成立」
# （它们是全库无例外的性质，逐套断言不脆弱，而且比原来只测一套更强）。
#
# 这 6 套是按 data.PALETTES 的顺序每隔 10 套取一个（`PALETTES[::10][:6]`），
# 不是挑 margin 好看的。
_PROPOSE_SET = ["asuka-vermilion", "pikachu-lemon", "miku-aqua",
                "ganyu-glacier", "yinlin-violetgold", "tarnished-gilded"]


@pytest.fixture(scope="module")
def profile_candidates():
    """这 6 套各跑一遍 propose.build()（约 11s），下面三条语义测试共用。"""
    import data
    import propose
    out = {}
    for slug in _PROPOSE_SET:
        p = next(x for x in data.PALETTES if x["slug"] == slug)
        out[slug] = {c.key: c for c in propose.build(p["colors"], mono=slug in data.MONO)}
    return out


def _mean_chroma(cand):
    from colorlib import lch
    return sum(lch(x)[1] for x in cand.colors) / len(cand.colors)


def test_propose_cvd_profile_actually_weights_cvd(profile_candidates):
    """精确钉住 cvd_w：C 与默认 profile 只差这一个参数（1.60 vs 0.65），
    所以「C 的色盲 ΔE 平均高于默认调优」把这个权重单独隔离了出来 ——
    把 cvd_w 改回 0.65，C 就等同于默认 profile，这个均值会**精确变成 0.00**。
    实测健康时 +1.93。默认 profile 的输出就是 tuned.py 里存的色值，直接读。
    （对比之下「C 比 A 好」不是好的检测器：把 cvd_w 改回去之后，全库仍有
      47/58 套的 C 比 A 强 —— 因为 A 还额外压着 penalty_w=1.60、hue_span=2.0。）
    """
    import propose
    import tuned
    gains = [by["C"].cvd_de - round(propose._cvd_de(tuned.TUNED[slug]), 1)
             for slug, by in profile_candidates.items()]
    mean = sum(gains) / len(gains)
    assert mean > 0.5, (
        f"C 相对默认 profile 的色盲 ΔE 平均增益只有 {mean:+.2f}（健康时 +1.93，"
        f"cvd_w 被改回 0.65 时精确为 0.00），逐套 {[round(g, 1) for g in gains]}")


def test_propose_cvd_profile_is_friendlier_than_faithful(profile_candidates):
    """用户可见的那句话：C 通常比「忠于原作」的 A 更耐色盲。
    这只是统计性质（全库 56/58，两个反例见上面注释），所以断言写成
    「6 套里至少 5 套」。实测健康 6/6，cvd_w 被改回 0.65 时掉到 3/6。"""
    ok = [s for s, by in profile_candidates.items() if by["C"].cvd_de > by["A"].cvd_de]
    assert len(ok) >= 5, (
        "6 套里只有 %d 套的 C 比 A 更耐色盲：%s"
        % (len(ok), {s: (by["C"].cvd_de, by["A"].cvd_de)
                     for s, by in profile_candidates.items()}))


def test_propose_grayscale_profile_spreads_lightness(profile_candidates):
    """D 是灰度打印方案，最小明度间隔必须比忠于原作的 A 更大，否则名不副实。
    全库 58/58 成立（最薄 +1.50），所以要求这 6 套无一例外。
    把 spread_w 归零后本组最薄变成 -4.30，会红。"""
    bad = {s: (by["D"].gray_gap, by["A"].gray_gap)
           for s, by in profile_candidates.items()
           if by["D"].gray_gap <= by["A"].gray_gap}
    assert not bad, f"这些配色的 D 没比 A 拉开明度（D, A）：{bad}"


def test_propose_soft_profile_is_less_saturated(profile_candidates):
    """E 是柔和低饱和方案，6 色平均彩度必须低于忠于原作的 A，
    否则 chroma_hi 那个 0.85 上限被改掉也不会有测试红。
    全库 58/58 成立（最薄 -1.08），所以要求这 6 套无一例外。
    把 chroma_hi 改回 1.20 后本组最薄变成 +2.75（方向反了），会红。"""
    bad = {s: (round(_mean_chroma(by["E"]), 2), round(_mean_chroma(by["A"]), 2))
           for s, by in profile_candidates.items()
           if _mean_chroma(by["E"]) >= _mean_chroma(by["A"])}
    assert not bad, f"这些配色的 E 没比 A 更低饱和（E, A）：{bad}"


def test_propose_rejects_bad_input():
    import propose
    with pytest.raises(SystemExit):
        propose.parse_args(["--slug", "x", "--zh", "x", "--en", "X", "--tone-zh", "x",
                            "--tone-en", "X", "--family", "蓝", "--source", "x",
                            "--colors", "#FFFFFF,#000000"])          # 只有 2 色
    with pytest.raises(SystemExit):
        propose.parse_args(["--slug", "x", "--zh", "x", "--en", "X", "--tone-zh", "x",
                            "--tone-en", "X", "--family", "不存在的色系", "--source", "x",
                            "--colors", ",".join(_PROPOSE_DEMO)])
    with pytest.raises(SystemExit):
        propose.parse_args(["--slug", "miku-aqua", "--zh", "x", "--en", "X", "--tone-zh", "x",
                            "--tone-en", "X", "--family", "蓝", "--source", "x",
                            "--colors", ",".join(_PROPOSE_DEMO)])     # slug 已存在


def test_propose_ansi_row_is_printable():
    import propose
    row = propose.ansi_row(_PROPOSE_DEMO)
    assert "\x1b[" in row and row.endswith("\x1b[0m")


def test_propose_ansi_row_carries_the_real_rgb():
    """光检查「有 ESC 且以 reset 收尾」拦不住真正会犯的错：colorlib.hex2rgb
    返回的是 0-1 浮点，忘了乘 255 的话每个通道都被 %d 截成 0，整行印成纯黑，
    上面那条断言照样全绿 —— 预览是这个工具的全部价值，得验到数值。"""
    import re
    import propose
    got = [tuple(int(v) for v in m)
           for m in re.findall(r"\x1b\[48;2;(\d+);(\d+);(\d+)m", propose.ansi_row(
               ["#FFFFFF", "#000000", "#4FA8DE"]))]
    assert got == [(255, 255, 255), (0, 0, 0), (0x4F, 0xA8, 0xDE)], got


def test_propose_html_is_selfcontained():
    import propose
    cands = propose.build(_PROPOSE_DEMO)
    meta = dict(slug="test-char", zh="测试", en="Test", tone_zh="霜蓝",
                tone_en="Frost", family="蓝", source="测试")
    html = propose.render_html(cands, _PROPOSE_DEMO, meta)
    assert html.lstrip().startswith("<!DOCTYPE html>")
    assert "http://" not in html and "https://" not in html, "预览页不许引外部资源"
    for c in cands:
        assert c.label in html
        for x in c.colors:
            assert x in html
    assert html.count("linear-gradient") >= len(cands) * 4, "每个方案要有 4 条色标"


def _parse_gradients(html):
    """从 render_html() 输出里按出现顺序抠出每条 linear-gradient 的 stop 颜色列表。
    render_html() 对每个方案固定按 seq/flow/div/cyclic 的顺序拼 4 条，
    所以第 i 个方案对应 grads[4*i : 4*i+4]。"""
    grads = re.findall(r"linear-gradient\(90deg,([^)]*)\)", html)
    return [[stop.split()[0] for stop in g.split(",")] for g in grads]


def test_propose_html_ramps_carry_real_colors_and_correct_semantics():
    """`test_propose_html_is_selfcontained` 的 4 条断言全是形状/计数
    （DOCTYPE 开头、无 http、6 个原始 hex 出现、linear-gradient 数量够）——
    没有一条解析渐变里的实际 stop 颜色。把 `_grad()` 改成对每个 stop 都吐
    `#000000`，上面那条测试照样全绿，跟上一轮 `ansi_row()` 全黑那个 bug
    是同一个模子（见 `test_propose_ansi_row_carries_the_real_rgb`）。

    这里解析出每条渐变的真实 stop 颜色，按 CLAUDE.md「色标语义不能混用」
    那条验四条色标各自的语义：seq/flow 明度单调、div 中点接近白、
    cyclic 首尾同色闭环。既能抓「_grad 退化成纯色」，也能抓
    「_ramps() 里 seq/flow/div/cyclic 顺序被打乱」。"""
    import propose
    from colorlib import lch
    cands = propose.build(_PROPOSE_DEMO)
    meta = dict(slug="test-char", zh="测试", en="Test", tone_zh="霜蓝",
                tone_en="Frost", family="蓝", source="测试")
    html = propose.render_html(cands, _PROPOSE_DEMO, meta)
    grads = _parse_gradients(html)
    assert len(grads) == len(cands) * 4
    for i, c in enumerate(cands):
        seq, flow, div, cyclic = grads[i * 4:i * 4 + 4]
        for name, ramp in (("seq", seq), ("flow", flow), ("div", div), ("cyclic", cyclic)):
            assert len(set(ramp)) > 1, f"{c.key} 方案的 {name} 色标退化成单一颜色（比如全黑）"

        Ls_seq = [lch(h)[0] for h in seq]
        assert all(a >= b - 1e-6 for a, b in zip(Ls_seq, Ls_seq[1:])), \
            f"{c.key} 方案的 seq 色标明度不单调：{[round(x, 1) for x in Ls_seq]}"

        Ls_flow = [lch(h)[0] for h in flow]
        assert all(a >= b - 1e-6 for a, b in zip(Ls_flow, Ls_flow[1:])), \
            f"{c.key} 方案的 flow 色标明度不单调：{[round(x, 1) for x in Ls_flow]}"

        Ls_div = [lch(h)[0] for h in div]
        Cs_div = [lch(h)[1] for h in div]
        mid = len(div) // 2
        assert Ls_div[mid] > max(Ls_div[0], Ls_div[-1]) + 15, (
            f"{c.key} 方案的 div 色标中点不比两端亮很多，不像发散色标：首 "
            f"{Ls_div[0]:.1f} 中 {Ls_div[mid]:.1f} 尾 {Ls_div[-1]:.1f}")
        assert Cs_div[mid] < 10, f"{c.key} 方案的 div 色标中点彩度 {Cs_div[mid]:.1f} 不够接近白"

        assert cyclic[0] == cyclic[-1], \
            f"{c.key} 方案的 cyclic 色标首尾不同色（{cyclic[0]} vs {cyclic[-1]}），没有闭环"


def _copy_editable_sources(dest):
    """把 --apply 会读写的那几个手写源文件拷到临时目录。

    apply() 是就地改写 data.py / tuned.py 的，测试必须跑在副本上，
    绝不能碰真仓库。"""
    import shutil
    src_dir = os.path.join(_ROOT, "src")
    for name in ("data.py", "tuned.py", "colorlib.py", "tune.py", "propose.py"):
        shutil.copy(os.path.join(src_dir, name), os.path.join(str(dest), name))


def _isolate_modules(tmp_path, monkeypatch):
    """让 import data / tuned / propose 落到 tmp_path 的副本上。

    monkeypatch 只还原 sys.path 和 cwd，不还原 sys.modules；副本里的 data
    带着测试新加的 slug，漏掉清理会污染同一次 pytest 里后面的用例。
    调用方负责在 finally 里再 pop 一次。"""
    monkeypatch.syspath_prepend(str(tmp_path))
    monkeypatch.chdir(str(tmp_path))
    for m in ("data", "tuned", "propose", "tune", "colorlib"):
        sys.modules.pop(m, None)


def _drop_isolated_modules():
    for m in ("data", "tuned", "propose", "tune", "colorlib"):
        sys.modules.pop(m, None)


_PROPOSE_META = dict(slug="zzz-test", zh="测试", en="Test", tone_zh="霜蓝",
                     tone_en="Frost Blue", family="蓝", source="测试作品")


def test_propose_render_record_is_valid_python():
    import propose
    src = propose.render_record(_PROPOSE_META, _PROPOSE_DEMO)
    ns = {}
    exec("PALETTES = [\n" + src + "\n]", ns)
    rec = ns["PALETTES"][0]
    assert rec["slug"] == "zzz-test"
    assert rec["family"] == "蓝"
    assert rec["colors"] == _PROPOSE_DEMO
    # 元数据要一条不落地写进去，不能只对 slug/family 两个字段
    for k, v in _PROPOSE_META.items():
        assert rec[k] == v, f"{k} 没有写进记录：期望 {v!r}，实际 {rec.get(k)!r}"
    assert src.startswith("    dict("), "缩进要和 data.py 里现有记录一致"


def test_propose_apply_writes_importable_files(tmp_path, monkeypatch):
    """--apply 会就地改写手写源文件。在临时副本上验证写完还能 import、
    指纹对得上、且没动到别的 slug。"""
    _copy_editable_sources(tmp_path)
    _isolate_modules(tmp_path, monkeypatch)
    try:
        import propose as fresh
        import tuned as old_tuned
        before = dict(old_tuned.TUNED)
        # 真实调用链里 parse_args() 会先 import data 做 family/slug 校验，
        # 所以 apply() 跑的时候 data 一定已经在 sys.modules 里了。测试必须
        # 复现这一点：否则 apply() 里那句 sys.modules.pop("data") 删掉也照样
        # 绿（第一次 import 自然读的就是新文件），而真跑 CLI 时指纹会是旧的。
        import data as _stale        # noqa: F841
        assert "data" in sys.modules

        cand = fresh.build(_PROPOSE_DEMO)[0]
        fresh.apply(_PROPOSE_META, _PROPOSE_DEMO, list(cand.colors))

        for m in ("data", "tuned"):
            sys.modules.pop(m, None)
        import data as d2
        import tuned as t2
        assert t2.SOURCE == d2.source_fingerprint(), "写完之后指纹对不上"
        assert t2.TUNED["zzz-test"] == list(cand.colors)
        assert {p["slug"] for p in d2.PALETTES} >= set(before) | {"zzz-test"}
        for k, v in before.items():
            assert t2.TUNED[k] == v, f"{k} 的调优结果被误改了"

        # 值断言：写进 data.py 的必须是用户敲的原始色和完整元数据，
        # 不是「文件被改过」就算数（前两轮的教训：形状断言全绿但内容是黑的）
        rec = next(p for p in d2.PALETTES if p["slug"] == "zzz-test")
        assert rec["colors"] == _PROPOSE_DEMO, "data.py 里存的应是原始色，不是调优后的色"
        for k, v in _PROPOSE_META.items():
            assert rec[k] == v, f"data.py 里 {k} 写错了：{rec.get(k)!r}"
        # tuned.py 里存的则是调优后的色，两者必须不同名不同物
        assert t2.TUNED["zzz-test"] != _PROPOSE_DEMO, "tuned.py 里存的应是调优后的色"
        # 既有条目连顺序都不该变，新 slug 追加在末尾 —— git diff 才只有一行新增
        assert list(t2.TUNED)[:len(before)] == list(before), "既有 slug 的顺序被打乱了"
        assert list(t2.TUNED)[-1] == "zzz-test"
        assert len(t2.TUNED) == len(before) + 1
    finally:
        _drop_isolated_modules()


def test_propose_apply_refuses_when_anchor_is_missing(tmp_path, monkeypatch):
    """data.py 结构变了导致找不到插入锚点时，必须明确报错退出。

    静默无操作比报错更糟：用户会以为已经写回去了，接着 make all 又什么都没变。"""
    _copy_editable_sources(tmp_path)
    data_path = os.path.join(str(tmp_path), "data.py")
    with open(data_path, encoding="utf-8") as f:
        broken = f.read().replace("# 每套配色的“签名色”", "# ANCHOR GONE")
    with open(data_path, "w", encoding="utf-8") as f:
        f.write(broken)
    _isolate_modules(tmp_path, monkeypatch)
    try:
        import propose as fresh
        with pytest.raises(SystemExit):
            fresh.apply(_PROPOSE_META, _PROPOSE_DEMO, list(_PROPOSE_DEMO))
        # 报错之后不许留下半截写入
        with open(data_path, encoding="utf-8") as f:
            assert "zzz-test" not in f.read(), "锚点没找到却还是改了 data.py"
    finally:
        _drop_isolated_modules()


def test_propose_apply_via_main_writes_the_named_profile(tmp_path, monkeypatch, capsys):
    """走完整的 `--apply B` 命令行链路，验证写进去的是 B 方案的色值。

    直接调 apply() 的那条测试绕开了 parse_args 和字母→候选的映射，
    抓不到「--apply B 却写了 A 的色」这类接线错误。"""
    _copy_editable_sources(tmp_path)
    _isolate_modules(tmp_path, monkeypatch)
    try:
        import propose as fresh
        cands = {c.key: list(c.colors) for c in fresh.build(_PROPOSE_DEMO)}
        assert cands["A"] != cands["B"], "A/B 两个 profile 结果相同，这条测试就失去意义了"

        fresh.main(["--slug", "zzz-main", "--zh", "测试", "--en", "Test",
                    "--tone-zh", "霜蓝", "--tone-en", "Frost Blue",
                    "--family", "蓝", "--source", "测试作品",
                    "--colors", ",".join(_PROPOSE_DEMO), "--apply", "B"])
        assert "已写入" in capsys.readouterr().out

        for m in ("data", "tuned"):
            sys.modules.pop(m, None)
        import data as d2
        import tuned as t2
        assert t2.SOURCE == d2.source_fingerprint(), "走 main() 之后指纹对不上"
        assert t2.TUNED["zzz-main"] == cands["B"], "--apply B 写进去的不是 B 方案"
        assert t2.TUNED["zzz-main"] != cands["A"]
        rec = next(p for p in d2.PALETTES if p["slug"] == "zzz-main")
        assert rec["colors"] == _PROPOSE_DEMO
    finally:
        _drop_isolated_modules()


def test_propose_apply_refuses_double_quotes_in_meta(tmp_path, monkeypatch):
    """元数据里含英文双引号会写出语法错误的 data.py —— 必须在动文件之前就拦住。

    `--zh 'A"B'` 渲染出来是 `zh="A"B"`，下一行 `import data` 立刻 SyntaxError。
    那是响亮失败不是静默失败，但 data.py 已经被改脏了，所以校验要前置。"""
    _copy_editable_sources(tmp_path)
    data_path = os.path.join(str(tmp_path), "data.py")
    with open(data_path, encoding="utf-8") as f:
        before = f.read()
    _isolate_modules(tmp_path, monkeypatch)
    try:
        import propose as fresh
        bad = dict(_PROPOSE_META, slug="zzz-quote", zh='测试"引号')
        with pytest.raises(SystemExit) as e:
            fresh.apply(bad, _PROPOSE_DEMO, list(_PROPOSE_DEMO))
        assert "双引号" in str(e.value), f"报错信息没点明原因：{e.value!r}"
        with open(data_path, encoding="utf-8") as f:
            assert f.read() == before, "校验不通过却已经改了 data.py"
    finally:
        _drop_isolated_modules()


def test_propose_html_lands_where_the_message_says(tmp_path, monkeypatch, capsys):
    """--html 的落点必须锚在 src/ 上，且提示里印的路径要真能打开。

    用相对 "build/" 的话，从仓库根跑 `python src/propose.py --html` 会把页面
    写进根目录的 build/，提示却写着 src/build/ —— 用户按提示去开会扑空。"""
    _copy_editable_sources(tmp_path)
    _isolate_modules(tmp_path, monkeypatch)
    try:
        import propose as fresh
        # cwd 换到 tmp_path 的上一级，模拟「从别的目录跑 src/propose.py」
        monkeypatch.chdir(str(tmp_path.parent))
        fresh.main(["--slug", "zzz-html", "--zh", "测试", "--en", "Test",
                    "--tone-zh", "霜蓝", "--tone-en", "Frost Blue",
                    "--family", "蓝", "--source", "测试作品",
                    "--colors", ",".join(_PROPOSE_DEMO), "--html"])
        line = [x for x in capsys.readouterr().out.splitlines() if x.startswith("预览页：")]
        assert line, "没打印预览页路径"
        shown = line[0].split("：", 1)[1]
        assert os.path.exists(shown), f"提示里的路径打不开：{shown}"
        assert os.path.samefile(shown, os.path.join(str(tmp_path), "build",
                                                    "propose-zzz-html.html"))
    finally:
        _drop_isolated_modules()


def test_skill_documents_how_to_add_a_palette():
    ref = os.path.join(_ROOT, "skills", "anime-palettes", "references", "add-palette.md")
    assert os.path.exists(ref), "缺 references/add-palette.md"
    with open(ref, encoding="utf-8") as f:
        body = f.read()
    for must in ("propose.py", "--apply", "make tune", "make skill", "[30, 78]"):
        assert must in body, f"add-palette.md 没写到 {must!r}"
    with open(os.path.join(_ROOT, "skills", "anime-palettes", "SKILL.md"),
              encoding="utf-8") as f:
        skill = f.read()
    assert "add-palette.md" in skill, "SKILL.md 没有指向 add-palette.md"


def test_skill_package_matches_directory():
    """.skill 是 zip 增量更新的，删过文件之后不重打包会留旧条目 —— CI 会因此红。"""
    import zipfile
    pkg = os.path.join(_ROOT, "skills", "anime-palettes.skill")
    root = os.path.join(_ROOT, "skills", "anime-palettes")
    with zipfile.ZipFile(pkg) as z:
        names = {n for n in z.namelist() if not n.endswith("/")}
    on_disk = set()
    for dirpath, _, files in os.walk(root):
        for fn in files:
            if fn == ".DS_Store":
                continue
            rel = os.path.relpath(os.path.join(dirpath, fn), os.path.dirname(root))
            on_disk.add(rel)
    assert names == on_disk, f"包内多出：{names - on_disk}；包内缺少：{on_disk - names}"
