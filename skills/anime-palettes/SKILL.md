---
name: anime-palettes
description: 用 anime-palettes 色库给图表、幻灯片和文档定配色（58 套取自动漫/游戏角色、做过 ΔE2000 区分度与色盲优化的配色，每套含 6 主色、深浅变体、seq/flow/div/cyclic 四条连续色标）。**只要任务涉及画图就用它**：matplotlib / seaborn / plotly / ggplot / Origin 出图、科研配图、论文插图、PPT 与幻灯片、海报、仪表盘、数据可视化、热图、散点图、折线图、柱状图，或者用户提到"配色""颜色""色板""colormap""cmap""好看一点""风格统一""色盲友好""灰度打印"。做规划或设计方案时也要用——把配色决策显式写进方案，而不是等画图时临时拍脑袋。
---

# anime-palettes：给图表定配色

这个技能解决两件事：**选对配色**，以及**把配色决策固化进方案**，让一份文档/一套图从头到尾颜色自洽。

不要每张图临时挑颜色。**一个交付物（一篇论文、一套幻灯片、一个仪表盘）只锁一套配色**，
所有图表复用同一个 slug、同一个排序、同一套类别→颜色的映射。

---

## 0. 先拿到库

按可用性从上往下试，任一成功即可：

```bash
python -c "import anime_palettes" 2>/dev/null && echo 已可用       # ① 已装
pip install git+https://github.com/zomosky/anime-palettes.git      # ② 装
curl -fsSLO https://raw.githubusercontent.com/zomosky/anime-palettes/main/anime_palettes.py   # ③ 单文件，零依赖
```

装不上也没关系 —— `references/palettes.md` 里有全部 58 套的 HEX，直接硬编码进代码即可，
只是拿不到 256 级色标。需要色标时改从
`https://raw.githubusercontent.com/zomosky/anime-palettes/main/dist/anime_palettes.json`
读 `seq` / `flow` / `div` / `cyclic` 字段。

---

## 1. 先判断：颜色在这张图里表达什么

这是所有决策的分叉点，**先回答它再选颜色**。

| 颜色表达 | 用什么 | 硬性要求 |
|---|---|---|
| **哪一类**（组别、方法、地区、实验条件） | 6 主色，`order="distinct"` | 系列数 ≤ 该配色的安全色数 |
| **多少**（浓度、温度、概率、误差） | 连续色标 `seq` 或 `flow` | **明度必须单调** |
| **偏离某个中心**（相关系数、差值、异常） | `div` | vmin/vmax 必须对称 |
| **周期**（相位、角度、风向、一天中的时刻） | `cyclic` | 不要拿它表示大小 |

一句话：**表达「多少」就必须明度单调，表达「哪一类」才用离散主色。**
把 6 个离散主色喂给连续变量，或者用 `cyclic` 表示大小，都是明确的错误。

---

## 2. 选哪一套

按这个顺序过滤，通常两三步就定了：

1. **色盲要求**。要投期刊、要做无障碍、系列数 ≥ 4 → 只在 **A 级**里选。
   系列数 ≤ 3 → 任意等级都行，取前 3 色即可。
2. **色系**。按内容领域挑，见 `references/palettes.md` 每个色系的适用提示。
   电力/气象/遥感/金融 → 蓝；水文/流体 → 青；生态/农业 → 绿；材料/地学 → 橙金；
   风险/热 → 红；抽象量/算法 → 紫；灰度打印 → 中性。
3. **具体角色**。同色系内哪套都行，让用户挑，或者按主题挑一个有语义呼应的。

不确定就用 `ganyu`（甘雨·冰蓝，A 级，冷静专业）—— 它是最安全的默认值。

**主动告诉用户你选了哪套、为什么**，一句话即可：
「用了甘雨·冰蓝（A 级色盲友好，冷色系配电力数据）」。用户往往会顺手换一个他更喜欢的。

---

## 3. 落到代码

```python
import anime_palettes as ap

ap.use_cjk_font()                       # 图里有中文就必须先调这个
ap.use("ganyu", order="distinct")       # 接管颜色循环 + 坐标轴 + 网格 + 默认 cmap
```

`ap.use()` 之后正常画图即可，不用再手动传 color。需要显式取色：

```python
cs = ap.colors("ganyu", n=4, order="distinct")   # 4 个分类色
ap.colors("ganyu", variant="light")              # 误差带、置信区间
ap.colors("ganyu", variant="dark")               # 强调、标注
ap.neutrals("ganyu")                             # bg / bg2 / muted / ink
ap.safe("ganyu")                                 # 色盲下仍可分的子集
```

### 排序：默认值不适合画图

| order | 什么时候用 |
|---|---|
| `"distinct"` | **画多系列图表一律用这个** —— 前几色差异最大 |
| `"smooth"`（库的默认值） | 色带、装饰、想让一套色看起来"像一套"时 |
| `"hue"` / `"light"` | 色相环顺序 / 明度浅→深（有序类别、灰度打印） |

`ap.use(name)` 不传 order 会用 `smooth`，相邻系列颜色接近 —— **画图时务必显式传 `order="distinct"`**。

### 连续色标

```python
ax.imshow(Z, cmap=ap.cmap("ganyu", "seq"))                       # 热图、密度
ax.scatter(x, y, c=v, s=42, edgecolor="white", linewidth=.35,
           cmap=ap.cmap("ganyu", "flow", crop=(.10, .93)))       # 散点连续着色
ax.imshow(C, cmap=ap.cmap("ganyu", "div"), vmin=-1, vmax=1)      # 相关矩阵
```

`crop` 对散点是**必须的**：色标最浅那一端（L\* > 88）的小点在白底上根本看不见。
点特别多（几千以上）时改 `crop=(.35, 1)` 并降 alpha、去描边 —— alpha 叠加会整体提亮。

不写 Python 的场景（R / MATLAB / Origin / CSS）用 CLI 生成代码：

```bash
anime-palettes code ganyu --ramp flow --lang r > ganyu_flow.R
```

`--lang` 支持 `python` / `python256` / `r` / `matlab` / `origin` / `css` / `hex`。
更多配方见 `references/recipes.md`。

---

## 4. 把配色写进规划 / 设计（这一步最容易被跳过）

做方案、写设计文档、规划一份报告或一套幻灯片时，**把配色当作一个显式的决策项**，
和字体、版式、图表类型并列，而不是等到动手画图才想。

### 在方案里落一条「配色锁」

在计划或设计文档里写下这么一段，之后所有产出都照它执行：

```markdown
## 配色（全文统一）
- 配色：ganyu（甘雨 · 冰蓝）· 色盲友好度 A · 排序 distinct
- 类别绑定：对照组 #5586CB ／ 处理组 #C34759 ／ 基线 #8A8F96
- 连续量：flow，crop=(0.10, 0.93)
- 差值图：div，vmin/vmax 对称
- 中性：底 #EEF2F8 ／ 网格 #DCE6F2 ／ 文字 #1B2735
```

三条纪律：

- **一个交付物一套配色。** 跨图表复用同一个 slug 和 order。
- **类别绑定要固定。** "对照组"在第 1 张图是蓝色，在第 7 张图就不能变成橙色。
  绑定一旦定下，写进方案，后续所有图查表取色。
- **中性色也来自同一套。** 坐标轴、网格、注释文字用 `ap.neutrals()`，
  不要留 matplotlib 的默认灰 —— 那是配色不统一最明显的破绽。

### 交接给代码

在项目里放一个小模块，所有画图脚本 import 它，配色只在一处定义：

```python
# figstyle.py
import anime_palettes as ap
PALETTE, ORDER = "ganyu", "distinct"
C = dict(zip(["对照", "处理", "基线"], ap.colors(PALETTE, order=ORDER)))

def setup():
    ap.use_cjk_font()
    ap.use(PALETTE, order=ORDER)
```

写进 `CLAUDE.md` / README 一行，后续所有会话都会遵守：

```
本项目所有图表用 anime-palettes 的 ganyu 配色，order="distinct"，见 figstyle.py
```

### 幻灯片 / 文档

- PPT：把 `dist/ppt-theme-colors/<slug>.xml` 装进 PowerPoint 的 Theme Colors，整份换色；
  或从 `dist/anime-palettes-picker.pptx` 用取色器吸
- HTML / 网页：`anime-palettes code <slug> --ramp seq --lang css`，或直接把 6 个 HEX 写成 CSS 变量
- 正文强调色、表头底色、引用块边框都从同一套里取，别另起一套

---

## 5. 交付前自检

画完图、交出去之前过一遍：

- [ ] 系列数 ≤ 安全色数？超了就换 A 级配色，或改用 `ap.safe()` 的子集
- [ ] 分类散点有没有加白描边 + 换 marker 形状？（灰度和色盲下的冗余）
- [ ] 连续着色用的是 `seq` / `flow` 而不是离散色？`ap.ramp_info(slug, "flow")["monotonic"]` 是 True？
- [ ] 散点的 `flow` 有没有 `crop` 掉最浅端？
- [ ] `div` 的 vmin/vmax 对称吗？
- [ ] 坐标轴、网格、文字用的是这套配色的中性色吗？
- [ ] 同一份文档里所有图用的是同一套、同一个 order、同一套类别绑定吗？
- [ ] 图里有中文的话，`ap.use_cjk_font()` 调了吗？

需要给用户看效果，用内置的示意图，别自己重画：

```python
ap.preview("ganyu")          # 折线/柱状/散点/连续/发散/深浅 六联图
ap.wheel("ganyu")            # 色环：色相与彩度分布
ap.scatter_guide("ganyu")    # 散点四种策略对照
```

---

## 6. 常见错误

| 错误 | 后果 | 正确做法 |
|---|---|---|
| `ap.use(name)` 不传 order 就画多系列 | 相邻系列颜色接近，读者分不开 | 显式 `order="distinct"` |
| 把 6 主色当连续色标 | 中间没有过渡，数值大小读不出来 | 用 `flow` |
| C 级配色画 5 个系列 | 色盲用户看到的是同一种颜色 | 换 A 级，或只用 `ap.safe()` |
| 散点直接用未裁剪的 `flow` | 最浅端的点在白底上消失 | `crop=(.10, .93)` |
| `div` 用了不对称的 vmin/vmax | 白色中点跑偏，读者误判正负 | 对称设置 |
| 用 `cyclic` 表示浓度/温度 | 明度恒定，大小完全读不出 | 用 `seq` / `flow` |
| 每张图换一套配色 | 整份文档看起来是拼的 | 一个交付物锁一套 |
| 坐标轴留默认灰 | 配色统一性最明显的破绽 | `ap.neutrals()` |

---

## 何时不要用这个库

- 用户/机构已有品牌配色或期刊指定配色 —— 那个优先，本库让位
- 需要严格的感知均匀标准色标（如某些定量遥感产品）—— 用 viridis / cividis，
  本库的 `flow` 感知均匀度在 0.53–0.82 之间，够用但不是为计量场景设计的
- 用户明确说不要动画/游戏相关的东西

这些情况下直接说明理由，用常规配色即可，不要硬套。

---

## 自己加一套配色

库里没有你要的角色，可以自己加。`python src/propose.py` 输入 6 个取色，
一次给出 5 个调色方案（忠于原作 / 区分度优先 / 色盲友好 / 灰度打印 / 柔和低饱和），
每个都附 minΔE₀₀、色盲 ΔE、评级、安全子集和相对原色的偏移量，挑一个 `--apply` 就写回库里。

取色时最容易踩的坑是明度：6 主色必须落在 `L* ∈ [30, 78]`，越界的会被硬拽回来
（纯黑纯白尤其糟，会变成发绿的灰）。完整流程、两个坑的实测数据、体检数据怎么读：
`references/add-palette.md`

---

## 参考文件

- `references/palettes.md` —— 58 套速查表：HEX、色盲等级、安全色数、按需求定位
- `references/recipes.md` —— matplotlib / seaborn / plotly / ggplot / Origin / PPT / CSS 的具体写法
- `references/api.md` —— 完整 API 与数据字段
- `references/add-palette.md` —— 自己加一套配色：取色约束、5 个方案怎么选、落地与回滚
