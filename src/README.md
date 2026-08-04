# 生成链路

改配色只需要动 `data.py`，其余全部自动派生。

```
data.py        36 套配色的原始色值（角色立绘印象色）+ 中英文名 / 色调标签 / 色系
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
                                            gpl/主题色/origin   （需 node）
```

`colorlib.py` 是零依赖的色彩科学工具箱：sRGB ↔ CIELAB ↔ LCh、CIEDE2000、
WCAG 对比度、Machado 色觉模拟矩阵、LCh 插值、ΔE 弧长重采样、色标体检。
`check.py` 是配色的严格体检（比 tests/ 更啰嗦，用于人工调色时看问题在哪）。

## 重新生成

```bash
make all          # 全套（tune 除外，那个 40s 且结果已固化在 tuned.py）
make tune         # 只在改了 data.py 的色值后需要
make test
```
