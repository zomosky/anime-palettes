# API 与数据字段

## 查询

```python
ap.ls(family="蓝", grade="A", kind=None)   # 打印清单，返回 slug 列表
ap.find("原神")                             # 按角色 / 色调 / 作品模糊搜
ap.get("ganyu")                             # 该配色的完整字典
ap.order_of("ganyu", "distinct")            # 该排序对应的下标
ap.FAMILIES                                 # ["红","橙","黄","绿","青","蓝","紫","粉","中性","撞色"]
ap.ORDERS                                   # ("smooth","distinct","hue","light")
ap.RAMPS                                    # ("seq","flow","div","cyclic")
ap.ORDER_LABEL / ap.RAMP_LABEL              # 中文说明
```

名字解析很宽松：`"miku"`、`"初音未来"`、`"miku-aqua"`、`"青碧"`、`"Miku"` 指同一套。
歧义会抛 `KeyError` 并列出候选。

## 取色

```python
ap.colors(name, n=6, variant="main", order=None)
#   variant : main / dark / light
#   order   : smooth（默认）/ distinct / hue / light
#   n > 6 时循环取色
ap.safe(name)          # 红/绿色盲下仍两两可分的子集（按规范顺序的下标取）
ap.neutrals(name)      # {"bg","bg2","muted","ink"}
ap.to_hex_block(name, order=None)   # 一行一个 HEX，给 Origin / GraphPad 粘
```

## colormap

```python
ap.cmap(name, which="seq", n=256, crop=None)
#   which : seq / flow / div / cyclic，加 "_r" 反向
#   crop  : (lo, hi)，0–1，裁掉两端。散点常用 (0.10, 0.93)
ap.listed(name, n=6, order=None)      # 离散 ListedColormap
ap.register(name=None)                # 注册到 matplotlib，之后可用字符串 "ganyu_flow"
ap.ramp_info(name, "flow")            # {"L_range","L_min","L_max","monotonic","total_dE","uniformity"}
```

## 样式

```python
ap.use_cjk_font(name=None)            # 自动挑一个系统里存在的中文字体，返回字体名（找不到返回 ""）
ap.rc(name, n=6, order=None)          # 返回 rcParams 字典，不生效
ap.use(name, n=6, order=None)         # 全局生效
with ap.using(name, n=6, order=None): # 临时生效，退出恢复
    ...
```

## 画图辅助

```python
ap.preview(name, save=None, order=None)   # 六联示意图
ap.wheel(name, ax=None, save=None, order=None, show_path=True)   # 色环
ap.wheel_all(save=None)                    # 全库色相/彩度分布
ap.scatter_guide(name, save=None)          # 散点四策略对照
```

## 代码生成（不写 Python 时用）

```python
ap.code(name, ramp="flow", lang="python")
#   ramp : seq / flow / div / cyclic
#   lang : python / python256 / r / matlab / origin / css / hex
```

CLI 同名子命令：`anime-palettes code ganyu --ramp flow --lang r`

## 命令行

```bash
anime-palettes ls [--family 蓝] [--grade A] [--order distinct]
anime-palettes show <name> [--order distinct]
anime-palettes hex <name> [-n 3] [--order] [--variant main|dark|light] [--safe]
anime-palettes code <name> [--ramp seq|flow|div|cyclic] [--lang ...]
anime-palettes search <query>
anime-palettes json <name>
```

没安装也能跑：`python anime_palettes.py <命令>`。
`ls` / `show` 会输出终端 24-bit 真彩色色块。

---

## `ap.get(name)` / JSON 的字段

| 字段 | 说明 |
|---|---|
| `slug` `zh` `en` `tone_zh` `tone_en` `name_zh` `name_en` | 标识与命名 |
| `family` | 色系：红 橙 黄 绿 青 蓝 紫 粉 中性 撞色 |
| `source` | 出处作品 |
| `kind` | `cat`（分类）/ `mono`（单色阶） |
| `colors` | 6 主色，**规范顺序 = 平滑序** |
| `dark` / `light` | 深/浅变体，与 `colors` 同下标 |
| `bg` `bg2` `muted` `ink` | 中性色 |
| `orders` | `{"smooth":[...], "distinct":[...], "hue":[...], "light":[...]}`，都是 `colors` 的下标置换 |
| `seq` `flow` `div` `cyclic` | 四条色标。JSON 里是 256 级；Python 模块里是抽稀后的 stop 列表（`ap.cmap` 会插值还原） |
| `ramp_stats` | 每条色标的 `L_range` / `monotonic` / `uniformity` / `total_dE` |
| `wheel` | 6 个颜色的 `{i, L, C, h}`，用于画色环 |
| `cvd` | `{"protan","deutan","tritan"}` 模拟后的最小 ΔE2000 |
| `cvd_grade` | A / B / C |
| `safe_set` | 色盲安全子集的下标（相对 `colors`） |
| `min_de` | 正常视觉下同套内最小 ΔE2000 |
| `contrast_white` | 每色对白底的 WCAG 对比度 |
| `L` | 每色的 L\* |
| `div_pair` `div_note` `signature` | 发散色标两端、来源（auto/manual/derived）、签名色 |

JSON 直链：
`https://raw.githubusercontent.com/zomosky/anime-palettes/main/dist/anime_palettes.json`

---

## 判定阈值（写死在库里，供你解释给用户）

- **色盲等级**：红/绿色盲模拟（Machado et al. 2009，severity 1.0）下 6 色两两最小 ΔE2000
  ≥ 13 → A；≥ 9 → B；否则 C
- **安全子集**：按区分度序贪心挑出、模拟后两两 ΔE2000 ≥ 12 的最大子集
- **配色调优**：色相角锁定（±7° 上限），L\* ∈ [30, 78]（单色系 [20, 86]），
  彩度在原值 0.45–1.20 倍内，坐标下降最大化「正常视觉 + 红/绿色盲」下的最小 ΔE2000，
  白底对比度约束 2.0–14
- **色标**：`seq` / `flow` 明度严格单调、跨度 ≥ 60 L\*；`cyclic` 首尾闭合、色相单向走满一圈；
  全部按 ΔE2000 弧长重采样做感知均匀化，`uniformity` = 1 − 相邻步长色差的变异系数
