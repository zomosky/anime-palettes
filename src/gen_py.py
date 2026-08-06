# -*- coding: utf-8 -*-
"""生成 anime_palettes.py（可直接 import 的 matplotlib 配色模块）。"""
import os
import json, io, textwrap

os.makedirs('build', exist_ok=True)
lib = json.load(open('library.json'))

def compact(entry):
    return dict(
        slug=entry['slug'], zh=entry['zh'], en=entry['en'],
        tone_zh=entry['tone_zh'], tone_en=entry['tone_en'],
        name_zh=entry['name_zh'], name_en=entry['name_en'],
        family=entry['family'], source=entry['source'], kind=entry['kind'],
        colors=entry['colors'], dark=entry['dark'], light=entry['light'],
        bg=entry['bg'], bg2=entry['bg2'], ink=entry['ink'], muted=entry['muted'],
        seq=[entry['seq'][i] for i in range(0, 256, 15)] + [entry['seq'][255]],
        div=[entry['div'][i] for i in range(0, 256, 15)] + [entry['div'][255]],
        flow=[entry['flow'][i] for i in range(0, 256, 9)] + [entry['flow'][255]],
        cyclic=[entry['cyclic'][i] for i in range(0, 256, 9)] + [entry['cyclic'][255]],
        wheel=entry['wheel'], ramp_stats=entry['ramp_stats'],
        cvd_grade=entry['cvd_grade'], safe_set=entry['safe_set'],
        orders=entry['orders'],
        min_de=entry['min_de'], cvd=entry['cvd'],
    )

DATA = {e['slug']: compact(e) for e in lib}

HEAD = '''# -*- coding: utf-8 -*-
"""anime_palettes —— 动漫/游戏角色配色库（%d 套 × 6 主色）

用法
----
    import anime_palettes as ap

    ap.ls()                       # 打印全部配色（带色调标签与色盲等级）
    ap.ls(family="蓝")            # 按色系筛选
    ap.find("初音")                # 模糊搜索，中英文/slug 都行

    c = ap.colors("miku")         # 6 个主色，默认「平滑」排列
    ap.colors("miku", n=3)        # 只要前 3 个
    ap.colors("miku", order="distinct")   # 换排序：多系列图表推荐
    ap.safe("miku")               # 色盲下仍可分的推荐子集

    ap.use("miku")                # 一键设置 matplotlib 全局风格
    with ap.using("hutao"):       # 或者临时用
        ax.plot(...)

    cm  = ap.cmap("miku")          # 连续色标 seq（单色相，热图/密度图）
    ap.cmap("miku", "flow")        # 多色相连续色标 —— **散点连续着色首选**
    ap.cmap("miku", "div")         # 发散色标（相关系数、差值图）
    ap.cmap("miku", "cyclic")      # 环形色标（相位、角度、风向、时刻）
    ap.cmap("miku", "flow_r")      # 反向；crop=(0.05,0.9) 可裁掉太浅/太深的两端

    ap.preview("miku")             # 六联示意图
    ap.wheel("miku")               # 色环：看这套色的色相/彩度分布
    ap.wheel_all()                 # 58 套一起看
    ap.scatter_guide("miku")       # 散点图四种配色策略的对照

四种排序（order 参数，各函数通用）：
  "smooth"   相邻色差最小的路径，过渡最顺滑 —— **默认**，色带/装饰/配图协调用
  "distinct" 区分度优先，前几色差异最大 —— **画多系列折线、柱状、散点时用这个**
  "hue"      色相环顺序 红→橙→黄→绿→青→蓝→紫
  "light"    明度由浅到深，也最适合灰度打印

配色三档色盲友好度：A = 红/绿色盲下 6 色全部可分；B = 大部分可分；
C = 角色本身就是同色系，建议只用 ap.safe() 给出的子集。
"""
from __future__ import annotations

__version__ = "1.0"

'''

TAIL = r'''

FAMILIES = ["红", "橙", "黄", "绿", "青", "蓝", "紫", "粉", "中性", "撞色"]

_ALIAS = {}
for _s, _e in PALETTES.items():
    for _k in (_s, _s.split('-')[0], _e['zh'], _e['en'].lower(),
               _e['name_zh'], _e['name_en'].lower(), _e['tone_zh']):
        _ALIAS.setdefault(str(_k).lower(), _s)

# 作品名（一个作品对应多套配色，只用于 find()，不用于精确解析）
_SOURCE = {}
for _s, _e in PALETTES.items():
    _SOURCE.setdefault(_e['source'], []).append(_s)


CJK_FONTS = ["Noto Sans CJK SC", "Source Han Sans SC", "Microsoft YaHei",
             "PingFang SC", "Heiti SC", "SimHei", "WenQuanYi Zen Hei",
             "Noto Sans SC", "Hiragino Sans GB"]


def use_cjk_font(name: str = None) -> str:
    """让 matplotlib 能正常显示中文（自动挑一个系统里存在的中文字体）。"""
    import matplotlib
    from matplotlib import font_manager
    have = {f.name for f in font_manager.fontManager.ttflist}
    for f in ([name] if name else []) + CJK_FONTS:
        if f in have:
            matplotlib.rcParams["font.sans-serif"] = [f] + list(
                matplotlib.rcParams.get("font.sans-serif", []))
            matplotlib.rcParams["axes.unicode_minus"] = False
            return f
    return ""


def _cjk_ok() -> bool:
    import matplotlib
    from matplotlib import font_manager
    have = {f.name for f in font_manager.fontManager.ttflist}
    return bool(have & set(CJK_FONTS)) or bool(
        set(matplotlib.rcParams.get("font.sans-serif", [])) & set(CJK_FONTS))


def _resolve(name):
    k = str(name).strip().lower()
    if k in _ALIAS:
        return _ALIAS[k]
    hits = [s for a, s in _ALIAS.items() if k and k in a]
    if len(set(hits)) == 1:
        return hits[0]
    if hits:
        raise KeyError(f"'{name}' 匹配到多套配色: {sorted(set(hits))}")
    raise KeyError(f"未找到配色 '{name}'，用 anime_palettes.ls() 查看全部")


def get(name) -> dict:
    """返回该配色的完整字典。"""
    return PALETTES[_resolve(name)]


ORDERS = ("smooth", "distinct", "hue", "light")
ORDER_LABEL = {"smooth": "平滑（相邻色差最小）", "distinct": "区分度优先",
               "hue": "色相环顺序", "light": "明度浅→深"}
DEFAULT_ORDER = "smooth"


def colors(name, n: int = 6, variant: str = "main", order: str = None) -> list:
    """主色列表。

    variant : main / dark / light
    order   : smooth（默认，过渡平滑）/ distinct（区分度优先，多系列图表用）
              / hue（色相环）/ light（明度浅→深）
    """
    e = get(name)
    key = {"main": "colors", "dark": "dark", "light": "light"}[variant]
    idx = e["orders"][order or DEFAULT_ORDER]
    seq = [e[key][i] for i in idx]
    return [seq[i % len(seq)] for i in range(n)]


def order_of(name, order: str = None) -> list:
    """该排序下的颜色下标（相对 PALETTES[..]["colors"] 的规范顺序）。"""
    return get(name)["orders"][order or DEFAULT_ORDER]


def safe(name) -> list:
    """红/绿色盲下两两仍可分辨的推荐子集。"""
    e = get(name)
    return [e["colors"][i] for i in e["safe_set"]]


def neutrals(name) -> dict:
    """配套中性色：bg 纸色 / bg2 次级底 / muted 辅助灰 / ink 墨色。"""
    e = get(name)
    return {k: e[k] for k in ("bg", "bg2", "muted", "ink")}


def ls(family: str = None, grade: str = None, kind: str = None):
    """打印配色清单。"""
    rows = [e for e in PALETTES.values()
            if (family is None or e["family"] == family)
            and (grade is None or e["cvd_grade"] == grade)
            and (kind is None or e["kind"] == kind)]
    rows.sort(key=lambda e: (FAMILIES.index(e["family"]), e["slug"]))
    print(f"{'slug':<24}{'名称':<20}{'色系':<5}{'色盲':<5}{'主色'}")
    for e in rows:
        print(f"{e['slug']:<24}{e['name_zh']:<18}{e['family']:<5}"
              f"{e['cvd_grade']:<5}{' '.join(colors(e['slug']))}")
    print(f"\n共 {len(rows)} 套")
    return [e["slug"] for e in rows]


def find(q: str):
    """模糊搜索，返回匹配的 slug 列表。角色名 / 色调 / 作品名都可以。"""
    q = q.strip().lower()
    hit = {s for a, s in _ALIAS.items() if q in a}
    for src, ss in _SOURCE.items():
        if q in src.lower():
            hit.update(ss)
    out = sorted(hit)
    for s in out:
        e = PALETTES[s]
        print(f"{s:<24}{e['name_zh']} / {e['name_en']}  [{e['source']}]")
    return out


# ---------------------------------------------------------------- matplotlib

def _mpl():
    import matplotlib
    return matplotlib


RAMPS = ("seq", "flow", "div", "cyclic")
RAMP_LABEL = {
    "seq": "连续（单色相）：热图、密度、单调强度",
    "flow": "连续（多色相）：散点连续着色、需要强过渡的图",
    "div": "发散：相关系数、差值、以 0 为中心的量",
    "cyclic": "环形：相位、角度、风向、一天中的时刻",
}


def cmap(name, which: str = "seq", n: int = 256, crop=None):
    """构造 matplotlib colormap。

    which : seq / flow / div / cyclic，加 `_r` 反向
    crop  : (lo, hi)，0–1，裁掉两端。散点图上小点太浅会看不见，
            常用 crop=(0.12, 0.95)
    """
    from matplotlib.colors import LinearSegmentedColormap
    e = get(name)
    rev = which.endswith("_r")
    key = which[:-2] if rev else which
    stops = list(e[key])
    if rev:
        stops = stops[::-1]
    if crop:
        lo, hi = crop
        k = len(stops) - 1
        a, b = int(round(lo * k)), int(round(hi * k))
        stops = stops[a:b + 1] or stops
    return LinearSegmentedColormap.from_list(f"{e['slug']}_{which}", stops, N=n)


def ramp_info(name, which: str = "flow") -> dict:
    """色标体检数据：明度跨度 / 是否单调 / 感知均匀度。"""
    return get(name)["ramp_stats"][which.replace("_r", "")]


def listed(name, n: int = 6, order: str = None):
    """构造离散 ListedColormap。"""
    from matplotlib.colors import ListedColormap
    return ListedColormap(colors(name, n, order=order), name=_resolve(name))


def register(name=None):
    """把 colormap 注册到 matplotlib，之后可用字符串引用，如 cmap='miku_seq'。"""
    import matplotlib
    names = [_resolve(name)] if name else list(PALETTES)
    done = []
    for s in names:
        for w in ("seq", "seq_r", "flow", "flow_r", "div", "div_r",
                  "cyclic", "cyclic_r"):
            cm = cmap(s, w)
            cm.name = f"{s.split('-')[0]}_{w}"
            try:
                matplotlib.colormaps.register(cm, force=True)
            except AttributeError:                       # matplotlib < 3.5
                matplotlib.cm.register_cmap(cm.name, cm)
            done.append(cm.name)
    return done


import warnings as _warnings
_warnings.filterwarnings("ignore", message="Overwriting the cmap")


def rc(name, n: int = 6, order: str = None) -> dict:
    """返回该配色对应的 rcParams 字典（不直接生效）。

    画多系列图表时建议 order="distinct"。
    """
    e = get(name)
    from cycler import cycler
    return {
        "axes.prop_cycle": cycler(color=colors(name, n, order=order)),
        "figure.facecolor": "white",
        "axes.facecolor": "white",
        "axes.edgecolor": e["ink"],
        "axes.labelcolor": e["ink"],
        "axes.titlecolor": e["ink"],
        "axes.grid": True,
        "axes.axisbelow": True,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "grid.color": e["bg2"],
        "grid.linewidth": 0.8,
        "text.color": e["ink"],
        "xtick.color": e["ink"],
        "ytick.color": e["ink"],
        "xtick.direction": "out",
        "ytick.direction": "out",
        "legend.frameon": False,
        "image.cmap": f"{_resolve(name).split('-')[0]}_seq",
        "savefig.facecolor": "white",
        "savefig.dpi": 300,
        "figure.dpi": 120,
        "lines.linewidth": 2.0,
        "lines.markersize": 5,
        "font.size": 10,
    }


def use(name, n: int = 6, order: str = None):
    """全局套用该配色（颜色循环 + 坐标轴 + 默认 colormap）。

    order 默认 "smooth"（过渡平滑）。**画多系列图表时传 order="distinct"**，
    相邻系列的颜色差异会明显更大。
    """
    import matplotlib.pyplot as plt
    register(name)
    plt.rcParams.update(rc(name, n, order))
    return _resolve(name)


class using:
    """上下文管理器：with anime_palettes.using('miku'): ..."""

    def __init__(self, name, n=6, order=None):
        self.name, self.n, self.order = name, n, order

    def __enter__(self):
        import matplotlib.pyplot as plt
        self._old = dict(plt.rcParams)
        use(self.name, self.n, self.order)
        return _resolve(self.name)

    def __exit__(self, *a):
        import matplotlib.pyplot as plt
        plt.rcParams.update(self._old)
        return False


def preview(name, save: str = None, order: str = None):
    """画一张该配色的示意图（折线 / 柱状 / 散点 / 热图 / 色阶）。"""
    import numpy as np
    import matplotlib.pyplot as plt
    e = get(name)
    od = order or DEFAULT_ORDER
    use_cjk_font()
    title = (f"{e['name_zh']}  ·  {e['name_en']}   [{e['source']}]  色盲友好度 "
             f"{e['cvd_grade']}  ·  排序 {ORDER_LABEL[od]}"
             if _cjk_ok() else
             f"{e['name_en']}   CVD grade {e['cvd_grade']}   order: {od}")
    with using(name, order=od):
        use_cjk_font()
        fig, ax = plt.subplots(2, 3, figsize=(12, 6.4))
        x = np.linspace(0, 10, 120)
        for i in range(6):
            ax[0, 0].plot(x, np.sin(x + i * 0.6) + i * 0.35, label=f"S{i+1}")
        ax[0, 0].set_title("line"); ax[0, 0].legend(ncol=3, fontsize=7)
        cs = colors(name, order=od)
        ax[0, 1].bar(range(6), [5, 7, 4, 8, 6, 3], color=cs)
        ax[0, 1].set_title("bar")
        rng = np.random.default_rng(0)
        for i, c in enumerate(cs):
            ax[0, 2].scatter(rng.normal(i, .6, 40), rng.normal(i, .6, 40), s=18,
                             color=c, edgecolor="white", linewidth=.4)
        ax[0, 2].set_title("scatter")
        g = np.add.outer(np.linspace(0, 1, 40), np.linspace(0, 1, 40))
        ax[1, 0].imshow(g, cmap=cmap(name, "flow")); ax[1, 0].set_title("flow（多色相连续）")
        ax[1, 1].imshow(g - 1, cmap=cmap(name, "div"), vmin=-1, vmax=1)
        ax[1, 1].set_title("diverging（发散）")
        for a in (ax[1, 0], ax[1, 1]):
            a.grid(False)
        li = colors(name, variant="light", order=od)
        di_ = colors(name, variant="dark", order=od)
        for i, c in enumerate(cs):
            for j, v in enumerate((li[i], c, di_[i])):
                ax[1, 2].add_patch(plt.Rectangle((i, -j), 1, 1, color=v))
        for k in range(48):
            ax[1, 2].add_patch(plt.Rectangle((k / 8.0, -4.1), 1 / 8.0, .9,
                                             color=e["seq"][round(k * (len(e["seq"]) - 1) / 47)]))
            ax[1, 2].add_patch(plt.Rectangle((k / 8.0, -5.2), 1 / 8.0, .9,
                                             color=e["cyclic"][round(k * (len(e["cyclic"]) - 1) / 47)]))
        ax[1, 2].text(6.1, -3.65, "seq", fontsize=7, va="center")
        ax[1, 2].text(6.1, -4.75, "cyclic", fontsize=7, va="center")
        ax[1, 2].set_xlim(0, 6.9); ax[1, 2].set_ylim(-5.4, 1); ax[1, 2].axis("off")
        ax[1, 2].set_title("light / main / dark")
        for a in ax.ravel()[:3]:
            a.grid(alpha=.35)
        fig.suptitle(title, fontsize=12)
        fig.tight_layout()
        if save:
            fig.savefig(save, dpi=200, bbox_inches="tight")
        return fig


def wheel(name=None, ax=None, save: str = None, order: str = None, show_path: bool = True):
    """画色环：极坐标里 角度 = CIELAB 色相 h，半径 = 彩度 C，点的明暗即 L*。
    一眼看出这套配色占了色轮的哪几块、彩度够不够、有没有色相扎堆。
    name=None 时画整个色库的色相分布。"""
    import numpy as np
    import matplotlib.pyplot as plt
    use_cjk_font()
    if name is None:
        return wheel_all(save=save)
    e = get(name)
    idx = e["orders"][order or DEFAULT_ORDER]
    if ax is None:
        fig, ax = plt.subplots(figsize=(4.6, 4.6), subplot_kw=dict(projection="polar"))
    else:
        fig = ax.figure
    # 背景色轮
    TH, RR = np.meshgrid(np.linspace(0, 2 * np.pi, 217), np.linspace(0, 1, 34))
    bg = np.zeros(TH.shape + (3,))
    for i in range(TH.shape[0]):
        for j in range(TH.shape[1]):
            bg[i, j] = _lab_rgb(76.0, 66 * RR[i, j] * np.cos(TH[i, j]),
                                66 * RR[i, j] * np.sin(TH[i, j]))
    ax.pcolormesh(TH, RR * 66, bg, shading="gouraud", alpha=0.42,
                  rasterized=True, zorder=0)
    pts = [(np.radians(e["wheel"][i]["h"]), e["wheel"][i]["C"],
            e["colors"][i], e["wheel"][i]["L"]) for i in idx]
    if show_path:
        ax.plot([p[0] for p in pts], [p[1] for p in pts],
                color=e["ink"], lw=1.1, alpha=.45, zorder=2)
    for k, (th, C, col, L) in enumerate(pts):
        ax.scatter([th], [C], s=340, color=col, edgecolor="white",
                   linewidth=1.8, zorder=3)
        ax.annotate(str(k + 1), (th, C), color="#fff" if L < 62 else "#111",
                    ha="center", va="center", fontsize=8.5, zorder=4)
    ax.set_theta_zero_location("E")
    ax.set_rmax(66)
    ax.set_rticks([20, 40, 60])
    ax.set_yticklabels(["C20", "C40", "C60"], fontsize=7, color="#999")
    ax.set_xticks(np.radians([0, 60, 120, 180, 240, 300]))
    ax.set_xticklabels(["红 0°", "黄 60°", "绿 120°", "青 180°", "蓝 240°", "紫 300°"],
                       fontsize=8)
    ax.grid(color="#ddd", lw=.6)
    ax.set_title(f"{e['name_zh']}  色环（角度=色相，半径=彩度）"
                 if _cjk_ok() else f"{e['name_en']}  hue wheel", fontsize=11, pad=14)
    if save:
        fig.savefig(save, dpi=200, bbox_inches="tight", facecolor="white")
    return ax


def _lab_rgb(L, a, b):
    """Lab -> sRGB（0–1，越界按彩度收敛），仅供画色环底图用。"""
    import numpy as np
    def f_inv(t):
        return t ** 3 if t ** 3 > 216 / 24389 else (t - 4 / 29) * 108 / 841
    for scale in (1.0, .8, .65, .5, .35, .2, .1):
        fy = (L + 16) / 116
        fx, fz = fy + a * scale / 500, fy - b * scale / 200
        X, Y, Z = f_inv(fx) * .95047, f_inv(fy), f_inv(fz) * 1.08883
        r = 3.2404542 * X - 1.5371385 * Y - .4985314 * Z
        g = -.9692660 * X + 1.8760108 * Y + .0415560 * Z
        bl = .0556434 * X - .2040259 * Y + 1.0572252 * Z
        out = []
        for c in (r, g, bl):
            c = max(0.0, min(1.0, c))
            out.append(12.92 * c if c <= .0031308 else 1.055 * c ** (1 / 2.4) - .055)
        if all(0 <= v <= 1 for v in (r, g, bl)):
            return np.array(out)
    return np.array(out)


def wheel_all(save: str = None, annotate: bool = False):
    """整个色库的色相/彩度分布：看还缺哪一块色相。"""
    import numpy as np
    import matplotlib.pyplot as plt
    use_cjk_font()
    fig, ax = plt.subplots(figsize=(6.4, 6.4), subplot_kw=dict(projection="polar"))
    for s, e in PALETTES.items():
        for w, col in zip(e["wheel"], e["colors"]):
            ax.scatter([np.radians(w["h"])], [w["C"]], s=58, color=col,
                       edgecolor="white", linewidth=.7, alpha=.92)
    ax.set_theta_zero_location("E")
    ax.set_rmax(70)
    ax.set_xticks(np.radians([0, 60, 120, 180, 240, 300]))
    ax.set_xticklabels(["红 0°", "黄 60°", "绿 120°", "青 180°", "蓝 240°", "紫 300°"],
                       fontsize=9)
    ax.set_rticks([20, 40, 60])
    ax.set_yticklabels(["C20", "C40", "C60"], fontsize=7, color="#999")
    ax.grid(color="#ddd", lw=.6)
    ax.set_title(f"全库 {len(PALETTES)} 套 × 6 色的色相 / 彩度分布"
                 if _cjk_ok() else "library hue / chroma coverage", fontsize=12, pad=16)
    if save:
        fig.savefig(save, dpi=200, bbox_inches="tight", facecolor="white")
    return ax


def _most_separated(hexes, k=3):
    """从一套色里挑 k 个两两色差最大的（用于只需要少数几类的图）。"""
    import itertools as _it
    from math import inf
    def de(a, b):
        la, lb = _lab(a), _lab(b)
        return sum((x - y) ** 2 for x, y in zip(la, lb)) ** .5
    best, bs = None, -inf
    for comb in _it.combinations(range(len(hexes)), k):
        m = min(de(hexes[i], hexes[j]) for i, j in _it.combinations(comb, 2))
        if m > bs:
            best, bs = comb, m
    return list(best)


def _lab(h):
    import math as _m
    def s2l(c):
        return c / 12.92 if c <= .04045 else ((c + .055) / 1.055) ** 2.4
    r, g, b = [s2l(int(h[1:][i:i + 2], 16) / 255) for i in (0, 2, 4)]
    X = .4124564 * r + .3575761 * g + .1804375 * b
    Y = .2126729 * r + .7151522 * g + .0721750 * b
    Z = .0193339 * r + .1191920 * g + .9503041 * b
    def f(t):
        return t ** (1 / 3) if t > 216 / 24389 else (841 / 108) * t + 4 / 29
    fx, fy, fz = f(X / .95047), f(Y), f(Z / 1.08883)
    return (116 * fy - 16, 500 * (fx - fy), 200 * (fy - fz))


def scatter_guide(name, save: str = None, seed: int = 3):
    """散点图四种配色策略的对照图：
    分类散点 / 连续变量着色 / 密度大时的处理 / 双变量（类别×强度）。"""
    import numpy as np
    import matplotlib.pyplot as plt
    e = get(name)
    use_cjk_font()
    cn = _cjk_ok()
    rng = np.random.default_rng(seed)
    with using(name):
        use_cjk_font()
        fig, ax = plt.subplots(2, 2, figsize=(11, 8.6))

        # ① 分类散点：区分度优先 + 白描边 + 形状冗余
        cs = colors(name, order="distinct")
        marks = ["o", "s", "^", "D", "v", "P"]
        for i in range(5):
            x = rng.normal(i * .8, 1.05, 55)
            y = rng.normal(i * .75, 1.05, 55)
            ax[0, 0].scatter(x, y, s=46, color=cs[i], marker=marks[i],
                             edgecolor="white", linewidth=.7, alpha=.95,
                             label=f"{'组' if cn else 'G'}{i+1}")
        ax[0, 0].legend(fontsize=8, ncol=3)
        ax[0, 0].set_title("① 分类散点：order='distinct' + 白描边 + 形状冗余" if cn
                           else "1. categorical: distinct order + white edge + markers",
                           fontsize=11)

        # ② 连续变量着色：flow 色标（多色相，强过渡）
        n = 420
        x = rng.normal(0, 1, n); y = x * .75 + rng.normal(0, .75, n)
        v = x + y + rng.normal(0, .35, n)
        sc = ax[0, 1].scatter(x, y, c=v, s=42, cmap=cmap(name, "flow", crop=(.10, .93)),
                              edgecolor="white", linewidth=.35)
        fig.colorbar(sc, ax=ax[0, 1], shrink=.85, label="强度" if cn else "value")
        ax[0, 1].set_title("② 连续着色：cmap='flow' + crop 掉最浅端" if cn
                           else "2. continuous: flow cmap, cropped", fontsize=11)

        # ③ 点太多：去描边 + 降 alpha + 只用色标深段
        n = 3500
        x = rng.normal(0, 1, n); y = x * .6 + rng.normal(0, .8, n)
        v = np.hypot(x, y)
        ax[1, 0].scatter(x, y, c=v, s=9, alpha=.42, linewidth=0,
                         cmap=cmap(name, "flow", crop=(.35, 1.0)))
        ax[1, 0].set_title("③ 密度大：s↓ alpha↓ 去描边 + crop=(0.35,1) 保持可见" if cn
                           else "3. dense: smaller, alpha, dark half only", fontsize=11)

        # ④ 双变量：类别定色相，强度走该色的 light→dark
        from matplotlib.colors import LinearSegmentedColormap
        tri = _most_separated(e["colors"], 3)
        li3 = [e["light"][k] for k in tri]
        dk3 = [e["dark"][k] for k in tri]
        for i in range(3):
            base, lo, hi = e["colors"][tri[i]], li3[i], dk3[i]
            cm = LinearSegmentedColormap.from_list("t", [lo, base, hi])
            x = rng.normal(i * 1.6, .85, 90); y = rng.normal(i * .9, .85, 90)
            ax[1, 1].scatter(x, y, c=np.linspace(0, 1, 90), cmap=cm, s=42,
                             edgecolor="white", linewidth=.4)
        ax[1, 1].set_title("④ 双变量：类别定色相，强度走 light→main→dark" if cn
                           else "4. bivariate: hue = class, lightness = value", fontsize=11)

        for a in ax.ravel():
            a.grid(alpha=.3)
        fig.suptitle(f"{e['name_zh']} · 散点图配色策略" if cn
                     else f"{e['name_en']} · scatter strategies", fontsize=13)
        fig.tight_layout()
        if save:
            fig.savefig(save, dpi=180, bbox_inches="tight")
        return fig


def to_hex_block(name, order: str = None) -> str:
    """给 Origin / GraphPad / AI 直接粘贴的十六进制清单。"""
    return "\n".join(colors(name, order=order))


# ================================================================ 命令行
# 零依赖，方便 `uvx --from git+... anime-palettes ls` 直接用。

_LANGS = ("python", "python256", "r", "matlab", "origin", "css", "hex")


def _sample(stops, n):
    """在 sRGB 里线性重采样到 n 级（stops 已足够密，误差可忽略）。"""
    def hx(h):
        return [int(h[1:][i:i + 2], 16) / 255 for i in (0, 2, 4)]

    def xh(v):
        return "#" + "".join("%02X" % max(0, min(255, round(c * 255))) for c in v)
    out = []
    for i in range(n):
        t = i / (n - 1) * (len(stops) - 1)
        k = min(int(t), len(stops) - 2)
        f = t - k
        a, b = hx(stops[k]), hx(stops[k + 1])
        out.append(xh([a[j] + (b[j] - a[j]) * f for j in range(3)]))
    return out


def code(name, ramp: str = "flow", lang: str = "python") -> str:
    """生成可直接粘贴的色标代码。lang: python/python256/r/matlab/origin/css/hex"""
    e = get(name)
    ramp = ramp.replace("_r", "")
    if ramp not in RAMPS:
        raise ValueError(f"ramp 只能是 {RAMPS}")
    if lang not in _LANGS:
        raise ValueError(f"lang 只能是 {_LANGS}")
    stops = e[ramp]
    st = e["ramp_stats"][ramp]
    v = f"{e['slug'].split('-')[0]}_{ramp}"
    head = f"{e['name_zh']} / {e['name_en']} — {RAMP_LABEL[ramp]}"
    meta = (f"L* 跨度 {st['L_range']} · 明度单调 {'是' if st['monotonic'] else '否'}"
            f" · 感知均匀度 {st['uniformity']}")

    def wrap(items, per, ind):
        rows = [ind + ", ".join(items[i:i + per]) for i in range(0, len(items), per)]
        return ",\n".join(rows)

    q = [f'"{c}"' for c in stops]
    if lang == "python":
        tail = {
            "flow": f'# ax.scatter(x, y, c=v, cmap={v}, s=42, edgecolor="white", linewidth=.35)',
            "div": f"# ax.imshow(C, cmap={v}, vmin=-1, vmax=1)   # vmin/vmax 要对称",
            "cyclic": f"# ax.scatter(x, y, c=phase, cmap={v}, vmin=0, vmax=2*np.pi)",
            "seq": f"# ax.imshow(Z, cmap={v})",
        }[ramp]
        return (f"# {head}\n# {meta}\n"
                f"from matplotlib.colors import LinearSegmentedColormap\n\n"
                f'{v} = LinearSegmentedColormap.from_list("{e["slug"]}_{ramp}", [\n'
                f"{wrap(q, 4, '    ')},\n])\n\n{tail}\n")
    if lang == "python256":
        s256 = [f'"{c}"' for c in _sample(stops, 256)]
        return (f"# {head}  —  256 级查找表\n# {meta}\n"
                f"{v}_hex = [\n{wrap(s256, 6, '    ')},\n]\n\n"
                f"from matplotlib.colors import ListedColormap\n"
                f'{v} = ListedColormap({v}_hex, name="{e["slug"]}_{ramp}")\n')
    if lang == "r":
        return (f"# {head}\n# {meta}\n"
                f"{v}_stops <- c(\n{wrap(q, 4, '  ')}\n)\n"
                f'{v} <- grDevices::colorRampPalette({v}_stops, space = "Lab")\n\n'
                f"# + scale_colour_gradientn(colours = {v}(256))\n"
                f"# + scale_fill_gradientn(colours = {v}(256))\n")
    if lang == "matlab":
        rows = []
        for c in _sample(stops, 256):
            r, g, b = [int(c[1:][i:i + 2], 16) / 255 for i in (0, 2, 4)]
            rows.append(f"    {r:.4f} {g:.4f} {b:.4f}")
        return (f"% {head}\n% {meta}\n{v} = [\n" + ";\n".join(rows) + "\n];\n\n"
                f"% colormap({v}); scatter(x, y, 36, v, \"filled\"); colorbar\n")
    if lang == "origin":
        return f"# {head}  —  16 级\n# {meta}\n" + "\n".join(_sample(stops, 16)) + "\n"
    if lang == "css":
        s12 = _sample(stops, 12)
        grad = ",\n".join(f"    {c} {i * 100 / 11:.1f}%" for i, c in enumerate(s12))
        return (f"/* {head} */\n/* {meta} */\n.{e['slug']}-{ramp} {{\n"
                f"  background: linear-gradient(90deg,\n{grad}\n  );\n}}\n")
    return f"{head}\n{meta}\n\n" + "\n".join(_sample(stops, 32)) + "\n"


def _swatch(hexes, width=8):
    """终端真彩色色块（不支持真彩色的终端会退化成普通文字）。"""
    out = []
    for c in hexes:
        r, g, b = [int(c[1:][i:i + 2], 16) for i in (0, 2, 4)]
        fg = "0;0;0" if (0.299 * r + 0.587 * g + 0.114 * b) > 150 else "255;255;255"
        out.append(f"\033[48;2;{r};{g};{b}m\033[38;2;{fg}m{c.center(width)}\033[0m")
    return "".join(out)


def main(argv=None):
    """命令行入口：anime-palettes <命令> ..."""
    import argparse
    import json as _json
    p = argparse.ArgumentParser(
        prog="anime-palettes",
        description="动漫 / 游戏角色配色库 —— 58 套，面向科研配图与 PPT",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""示例:
  anime-palettes ls --family 蓝 --grade A
  anime-palettes show 胡桃 --order distinct
  anime-palettes hex miku -n 3
  anime-palettes code ganyu --ramp flow --lang python > ganyu_flow.py
  anime-palettes search 原神
  anime-palettes json miku | jq .colors
""")
    sub = p.add_subparsers(dest="cmd", required=True)

    a = sub.add_parser("ls", help="列出全部配色（带色块预览）")
    a.add_argument("--family", help="按色系筛：红 橙 黄 绿 青 蓝 紫 粉 中性 撞色")
    a.add_argument("--grade", choices=list("ABC"), help="按色盲友好度筛")
    a.add_argument("--order", choices=ORDERS, default=DEFAULT_ORDER)

    a = sub.add_parser("show", help="显示单套配色的全部细节")
    a.add_argument("name")
    a.add_argument("--order", choices=ORDERS, default=DEFAULT_ORDER)

    a = sub.add_parser("hex", help="只输出 HEX，一行一个，方便管道")
    a.add_argument("name")
    a.add_argument("-n", type=int, default=6)
    a.add_argument("--order", choices=ORDERS, default=DEFAULT_ORDER)
    a.add_argument("--variant", choices=("main", "dark", "light"), default="main")
    a.add_argument("--safe", action="store_true", help="只输出色盲安全子集")

    a = sub.add_parser("code", help="生成色标代码")
    a.add_argument("name")
    a.add_argument("--ramp", choices=RAMPS, default="flow")
    a.add_argument("--lang", choices=_LANGS, default="python")

    a = sub.add_parser("search", help="按角色 / 色调 / 作品模糊搜索")
    a.add_argument("query")

    a = sub.add_parser("json", help="输出该配色的完整 JSON")
    a.add_argument("name")

    ns = p.parse_args(argv)

    if ns.cmd == "ls":
        rows = [e for e in PALETTES.values()
                if (not ns.family or e["family"] == ns.family)
                and (not ns.grade or e["cvd_grade"] == ns.grade)]
        rows.sort(key=lambda e: (FAMILIES.index(e["family"]), e["slug"]))
        for e in rows:
            print(f"{e['name_zh']:<14}{e['family']}  {e['cvd_grade']}  "
                  f"{_swatch(colors(e['slug'], order=ns.order), 9)}  {e['slug']}")
        print(f"\n共 {len(rows)} 套 · 色盲友好度 A=全可分 B=大部分 C=只用安全子集")
        return 0

    if ns.cmd == "search":
        for s in find(ns.query):
            pass
        return 0

    e = get(ns.name)

    if ns.cmd == "json":
        print(_json.dumps(e, ensure_ascii=False, indent=1))
        return 0

    if ns.cmd == "hex":
        cs = safe(ns.name) if ns.safe else colors(
            ns.name, n=ns.n, variant=ns.variant, order=ns.order)
        print("\n".join(cs))
        return 0

    if ns.cmd == "code":
        print(code(ns.name, ns.ramp, ns.lang), end="")
        return 0

    # show
    print(f"\n  {e['name_zh']}   {e['name_en']}")
    print(f"  {e['source']} · 色系 {e['family']} · 色盲友好度 {e['cvd_grade']}"
          f" · 最小 ΔE00 {e['min_de']}\n")
    for label, variant in (("浅 light", "light"), ("主 main ", "main"), ("深 dark ", "dark")):
        print(f"  {label}  {_swatch(colors(ns.name, variant=variant, order=ns.order), 9)}")
    print(f"\n  中性色     {_swatch([e['bg'], e['bg2'], e['muted'], e['ink']], 9)}"
          f"   bg / bg2 / muted / ink")
    print(f"  色盲安全   {_swatch(safe(ns.name), 9)}")
    print(f"\n  排序 {ORDER_LABEL[ns.order]}")
    for o in ORDERS:
        if o != ns.order:
            print(f"       {ORDER_LABEL[o]:<18}{_swatch(colors(ns.name, order=o), 9)}")
    print()
    for r in RAMPS:
        st = e["ramp_stats"][r]
        print(f"  {r:<7}{_swatch(_sample(e[r], 8), 7)}  L*{st['L_range']:>5} "
              f"单调{'是' if st['monotonic'] else '否'} 均匀{st['uniformity']}  {RAMP_LABEL[r]}")
    print(f"\n  取代码: anime-palettes code {e['slug']} --ramp flow --lang python\n")
    return 0


__all__ = ["PALETTES", "FAMILIES", "ORDERS", "ORDER_LABEL", "order_of", "code", "main", "get", "colors", "safe", "neutrals", "ls",
           "find", "cmap", "listed", "register", "rc", "use", "using",
           "preview", "to_hex_block", "use_cjk_font", "wheel", "wheel_all",
           "scatter_guide", "RAMPS", "RAMP_LABEL", "ramp_info"]


if __name__ == "__main__":
    import sys as _sys
    _sys.exit(main())
'''

with io.StringIO() as f:
    f.write(HEAD % len(lib))
    f.write("PALETTES = {\n")
    for s, e in DATA.items():
        f.write(f"  {json.dumps(s, ensure_ascii=False)}: {{\n")
        for k, v in e.items():
            f.write(f"    {json.dumps(k, ensure_ascii=False)}: {v!r},\n")
        f.write("  },\n")
    f.write("}\n")
    f.write(TAIL)
    open('build/anime_palettes.py', 'w').write(f.getvalue())
print('wrote build/anime_palettes.py')
