#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.9"
# dependencies = [
#   "anime-palettes @ git+https://github.com/zomosky/anime-palettes.git",
#   "matplotlib",
#   "numpy",
# ]
# ///
"""PEP 723 单文件脚本 —— 不需要建项目、不需要预装任何东西。

    uv run examples/uv_single_file.py

uv 会读上面注释里的依赖清单，自建一个临时环境装好再跑。
第一次几秒钟，之后走缓存基本秒开。
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import anime_palettes as ap

ap.use_cjk_font()
rng = np.random.default_rng(0)
x = rng.normal(0, 1, 600)
y = 0.7 * x + rng.normal(0, 0.7, 600)

with ap.using("ganyu"):
    fig, ax = plt.subplots(figsize=(6, 4.6))
    sc = ax.scatter(x, y, c=x + y, s=40, edgecolor="white", linewidth=.35,
                    cmap=ap.cmap("ganyu", "flow", crop=(.10, .93)))
    fig.colorbar(sc, ax=ax, label="强度")
    ax.set(title="甘雨 · 冰蓝 — flow 色标", xlabel="x", ylabel="y")
    fig.tight_layout()
    fig.savefig("uv_single_file.png", dpi=200)

print("已生成 uv_single_file.png")
