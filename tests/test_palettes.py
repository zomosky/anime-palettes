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


def test_marks_do_not_leak_into_library():
    """marks 是展示资源不是色彩数据。让它进 library.json 会破坏
    dist/anime_palettes.json 与 src/library.json 内容完全相同这条不变量。"""
    import json
    lib = json.load(open(os.path.join(_ROOT, "src", "library.json")))
    for e in lib:
        assert "mark" not in e and "path" not in e, f"{e['slug']} 的库记录里混进了标志物字段"
