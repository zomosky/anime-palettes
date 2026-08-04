# -*- coding: utf-8 -*-
"""五分钟上手：把一套角色配色接到 matplotlib 上。

    python examples/quickstart.py
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

import anime_palettes as ap

PALETTE = "ganyu"          # 甘雨 · 冰蓝；换成 "hutao" / "初音未来" / "eva01" 都行

ap.use_cjk_font()          # 让中文标签正常显示

# ---------------------------------------------------------------- 1. 看看有什么
ap.ls(family="蓝")          # 按色系筛
print(ap.get(PALETTE)["name_zh"], ap.colors(PALETTE))
print("色盲安全子集:", ap.safe(PALETTE))
print("flow 色标体检:", ap.ramp_info(PALETTE, "flow"))

# ---------------------------------------------------------------- 2. 多系列折线
# 画多系列一定要 order="distinct"，默认的 "smooth" 相邻色太接近
with ap.using(PALETTE, order="distinct"):
    fig, ax = plt.subplots(figsize=(7, 4))
    x = np.linspace(0, 10, 200)
    for i in range(5):
        ax.plot(x, np.sin(x + i * .7) + i * .5, label=f"组 {i + 1}")
    ax.set(xlabel="时间 / h", ylabel="观测值", title=f"多系列折线 · {ap.get(PALETTE)['name_zh']}")
    ax.legend(ncol=3)
    fig.tight_layout()
    fig.savefig("quickstart_lines.png", dpi=200)

# ---------------------------------------------------------------- 3. 散点连续着色
# 用 flow（多色相 + 明度单调），并 crop 掉最浅端，否则小点在白底上看不见
with ap.using(PALETTE):
    rng = np.random.default_rng(0)
    x = rng.normal(0, 1, 500)
    y = .75 * x + rng.normal(0, .7, 500)
    v = x + y

    fig, ax = plt.subplots(figsize=(6, 4.6))
    sc = ax.scatter(x, y, c=v, s=44, cmap=ap.cmap(PALETTE, "flow", crop=(.10, .93)),
                    edgecolor="white", linewidth=.35)
    fig.colorbar(sc, ax=ax, label="强度")
    ax.set(xlabel="x", ylabel="y", title="散点连续着色 · flow 色标")
    fig.tight_layout()
    fig.savefig("quickstart_scatter.png", dpi=200)

# ---------------------------------------------------------------- 4. 热图 / 相关矩阵
fig, axes = plt.subplots(1, 2, figsize=(9.5, 4))
g = np.add.outer(np.linspace(0, 1, 60), np.linspace(0, 1, 60))
axes[0].imshow(g, cmap=ap.cmap(PALETTE, "seq"))
axes[0].set_title("seq（单色相）")
im = axes[1].imshow(g - 1, cmap=ap.cmap(PALETTE, "div"), vmin=-1, vmax=1)
axes[1].set_title("div（发散，vmin/vmax 要对称）")
fig.colorbar(im, ax=axes[1])
for a in axes:
    a.set_xticks([]); a.set_yticks([])
fig.tight_layout()
fig.savefig("quickstart_maps.png", dpi=200)

# ---------------------------------------------------------------- 5. 内置示意图
ap.preview(PALETTE, save="quickstart_preview.png")
ap.wheel(PALETTE, save="quickstart_wheel.png")
ap.scatter_guide(PALETTE, save="quickstart_scatter_guide.png")

print("\n已生成 quickstart_*.png")
