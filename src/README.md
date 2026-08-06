# 生成链路

改配色只需要动 `data.py`，其余全部自动派生。

```
data.py        58 套配色的原始色值（角色立绘印象色）+ 中英文名 / 色调标签 / 色系
   │
   ├─ tune.py      科研可用性微调：锁死色相角，只调 L*/C*，坐标下降最大化
   │               「正常视觉 + 红/绿色盲模拟」下的最小 ΔE2000  →  tuned.py
   │
   └─ derive.py    以调优后的色值为输入，派生
                     · 4 种排序（平滑 / 区分度 / 色相环 / 明度）
                     · 深 / 浅变体、纸色 bg / bg2 / muted / ink
                     · 4 条色标 seq / flow / div / cyclic（各 256 级）
                     · 色环数据、色标体检、色盲评级与安全子集
                   →  library.json
                          │
   ┌──────────────────────┼──────────────────────┬─────────────────┐
gen_py.py            gen_html.py            gen_files.py      gen_pptx.js
Python 模块          单文件交互色卡库        csv/xlsx/ase/      PPT 取色板
                          ↑                  gpl/主题色/origin   （需 node）
marks.py ─────────────────┘
58 套配色的「标志物」SVG（竹筒 / 闪电 / 叶伞…），色卡库里那个默认关闭的开关用的。
第二份手写数据源，与 data.py 并列，**只喂 gen_html.py，不进 derive.py** ——
它不是色彩科学数据，进了 library.json 会破坏「dist/anime_palettes.json 与
library.json 内容完全相同」这条不变量。
```

`colorlib.py` 是零依赖的色彩科学工具箱：sRGB ↔ CIELAB ↔ LCh、CIEDE2000、
WCAG 对比度、Machado 色觉模拟矩阵、LCh 插值、ΔE 弧长重采样、色标体检，
以及色盲评级三件套 `cvd_min` / `safe_set` / `grade` 与发散色标选端 `pick_diverging_pair`
（后四个原本在 derive.py 里，搬过来是为了让 propose.py 能用而不必 import derive）。
`check.py` 是配色的严格体检（比 tests/ 更啰嗦，用于人工调色时看问题在哪）。

`propose.py` 是给别人自助加配色用的命令行：输入 6 个取色，一次给出 5 个调色方案
（忠于原作 / 区分度优先 / 色盲友好 / 灰度打印 / 柔和低饱和）+ 体检数据 + 终端 ANSI 预览，
`--html` 出对比页，挑好 `--apply` 写回 data.py 与 tuned.py。
它**刻意不 import derive** —— derive 模块级有指纹校验，仓库处于「改了 data.py 还没 tune」
时会 SystemExit，而那正是最需要这个工具的时候。用法见
`skills/anime-palettes/references/add-palette.md`。

`sheet2.py` 生成 README 的配色总览图，中文字体走 `anime_palettes.use_cjk_font()`
自动挑，挑不到直接报错退出 —— 免得静默产出一张中文全是方框的图（CI 不比对 PNG 字节）。

## 重新生成

```bash
make all          # 全套（tune 除外，结果已固化在 tuned.py）
make tune         # 只在改了 data.py 的色值后需要，全库跑一遍约 20~60s（视机器）
make skill        # 改了 skills/ 目录后必须跑，否则 CI 的 skill 关会红
make test
```
