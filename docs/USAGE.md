# 详细使用说明

> landing page 见仓库根目录的 [README.md](../README.md)，这里是完整版。

58 套角色配色，每套 6 主色 + 深/浅变体 + 四种连续色标（seq / flow / div / cyclic）+ 配套中性色。
面向 PPT 与科研配图，颜色在保留角色辨识度的前提下做过可用性微调。
每套预置 4 种排列顺序，默认「平滑」。

---

## 目录

| 文件 / 目录 | 用途 |
|---|---|
| `dist/anime-palettes.html` | **交互色卡库**（单文件，双击用浏览器打开）。筛选、搜索、点击复制 HEX、**点色标条取 colormap 代码**、色环、色盲模拟、深浅变体、迷你图表预览 |
| `dist/anime-palettes-picker.pptx` | **PPT 取色板**：59 页，每页一套配色 + 原生柱状/折线图示例，用取色器直接吸色 |
| `dist/ppt-theme-colors/*.xml` | PowerPoint 主题色文件，整套切换配色 |
| `anime_palettes.py` | **Python 模块**，一行接管 matplotlib 全局风格 |
| `dist/anime_palettes.xlsx` | 六表：色卡总览 / 逐色明细 / 深浅延伸 / 排序方案 / 色标采样 / 使用说明 |
| `dist/anime_palettes.csv` | 同样内容的纯文本表，348 行（58×6） |
| `dist/anime_palettes.json` | 完整数据，含 256 级 colormap，供二次开发 |
| `dist/ase/*.ase` | Adobe 色板（AI / PS / ID）。`_ALL-58-anime-palettes.ase` 是含 58 个分组的合集 |
| `dist/gpl/*.gpl` | GIMP / Inkscape / Krita 色板 |
| `dist/origin-hex/平滑\|区分度/*.txt` | Origin、GraphPad 等逐行粘贴用的 HEX 清单，两种排序各一份 |
| `dist/origin-hex/flow色标/*.txt` | flow 色标的 16 级取样，给 Origin 做自定义 colormap |
| `docs/images/配色总览.png` | 一张图看全 58 套 |
| `docs/images/色环总览.png` | 全库 348 个色点在色轮上的分布，看还缺哪一块色相 |
| `docs/images/散点配色策略.png` | 散点图四种配色策略的对照图 |

---

## 命名规则

```
角色名 · 色调标签          slug（英文，程序里用）
胡桃 · 绯梅               hutao-plum
初音未来 · 青碧            miku-aqua
无脸男 · 墨灰              noface-ink-gray
```

色调标签是「一眼识别」的那一半：看到 *绯梅 / 冰蓝 / 苔灰 / 紫萤 / 素墨*
就知道大概长什么样，不必先想起角色。

按色系归为 10 类，方便按需求检索：
**红 橙 黄 绿 青 蓝 紫 粉 中性 撞色**

---

## 每套配色的结构

| 部件 | 数量 | 说明 |
|---|---|---|
| `colors` 主色 | 6 | 默认按**平滑**排列（见下节）。画多系列图表时切到**区分度优先** |
| `light` 浅色 | 6 | L\* +16、彩度 ×0.78。误差带、置信区间、次要背景 |
| `dark` 深色 | 6 | L\* −15。同一系列的强调、标注、深色底上的线条 |
| `bg` / `bg2` | 2 | 纸色（L\*96.5）与次级底色（L\*91），带一点主色的色相 |
| `muted` | 1 | 中性辅助灰，用于网格线、次要文字 |
| `ink` | 1 | 墨色（L\*21），坐标轴、正文 |
| `seq` 连续色标 | 256 | 单色相、明度单调，热图、密度图、地图 |
| `flow` 强过渡色标 | 256 | **多色相** + 明度严格单调，散点连续着色、需要强过渡的图 |
| `div` 发散色标 | 256 | 中点近白，相关系数、差值、异常偏离 |
| `cyclic` 环形色标 | 256 | 首尾相接、明度恒定，相位、角度、风向、一天中的时刻 |

---

## 四种排列顺序

同样 6 个颜色，排列方式换一下，观感差别很大。库里预置了 4 种，**默认是「平滑」**。

| 排序 | 依据 | 什么时候用 |
|---|---|---|
| **平滑** `smooth`（默认） | 以角色主色为起点，穷举 6! 条路径取**相邻 ΔE₀₀ 之和最小**的那条 | 色带、装饰条、整体配图协调、想让一套色看起来「像一套」时 |
| **区分度优先** `distinct` | 前几个颜色彼此差异最大（配色调优时的原始顺序） | **画多系列折线 / 柱状 / 散点**。只画 2–3 条线时直接取前 2–3 色 |
| **色相环** `hue` | CIELAB 色相角，红→橙→黄→绿→青→蓝→紫，近中性色排末尾 | 需要规律性、好预测的场合；明度会跳 |
| **明度浅→深** `light` | 按 L\* 降序 | 表达强弱/多少的有序数据，也最适合灰度打印 |

58 套合计的相邻色差总和：平滑 6841，明度 8107，色相 8560，区分度 9402
—— 平滑约为区分度排序的 73%，58 套里有 46 套它是四者中最小的。
（剩下 8 套之所以不是全局最小，是因为平滑路径**被约束从角色主色出发**，
这样 `colors[0]` 才始终是那套配色最有代表性的颜色；代价平均只有 9%。）

平滑排列的代价是相邻两色变接近 —— 所以它**不适合直接拿去画多系列图**。

切换方式：

- HTML 色卡库：工具栏「排序」四个按钮，色块、迷你图表和复制内容会同步变
- Python：`ap.colors("miku", order="distinct")`、`ap.use("miku", order="distinct")`
- Excel：「排序方案」表列出了每套的四种顺序；「逐色明细」表有四列位次可排序
- Origin：`origin-hex/平滑/` 与 `origin-hex/区分度/` 两个目录
- PPT 取色板：每页色块是平滑序，右下角小色条是区分度序，页内图表用的就是后者
- PPT 主题色 `.xml`：`accent1–6` 用**区分度优先**顺序 —— PowerPoint 图表是按 accent 顺序循环取色的

`.ase` / `.gpl` 色板、`csv` / `xlsx` 主表、`配色总览.png` 都用默认的平滑序。

---

## 色环

每张色卡右下角有一个小色环：**角度 = CIELAB 色相 h，半径 = 彩度 C**，
连线是当前排序下的走位。一眼能看出这套色占了色轮的哪几块、彩度够不够、有没有色相扎堆。
切排序时连线会跟着变 —— 「平滑」排序的连线通常最短最顺。

Python 里：

```python
ap.wheel("miku")                # 单套色环
ap.wheel("miku", order="hue")   # 换排序看走位
ap.wheel_all()                  # 全库 58×6 = 348 个色点的色相/彩度分布
```

`docs/images/色环总览.png` 是全库的分布图。看下来目前的覆盖情况：
红–橙–黄和蓝–青这两段最厚，**高彩度的纯绿（120–150°）和纯青（180–200°）偏薄**
—— 如果你的图需要那两块，路易吉·草绿、索隆·苔墨、初音未来·青碧、温迪·风薄荷是最靠外的几个。

---

## 散点图 / 强过渡场景怎么配

散点和折线、柱状很不一样：**点小、面积碎、还常常要用颜色编码第三个连续变量**。
分类用的 6 主色直接拿去做连续着色是不行的 —— 那是 6 个离散色，中间没有过渡。
库里为此专门做了 `flow` 色标，`docs/images/散点配色策略.png` 是四种典型场景的对照图。

### ① 分类散点（颜色 = 类别）

```python
ap.use("miku", order="distinct")
for i, g in enumerate(groups):
    ax.scatter(g.x, g.y, s=46, color=ap.colors("miku", order="distinct")[i],
               marker=["o","s","^","D","v","P"][i],
               edgecolor="white", linewidth=.7, alpha=.95)
```

三个要点：**区分度优先**排序、**白描边**（点重叠时边界不糊成一团）、
**形状冗余**（灰度打印和色盲下还能分）。类别多于 4 个时先查 `ap.safe()`。

### ② 连续变量着色（颜色 = 数值）—— 用 `flow`

```python
ax.scatter(x, y, c=v, cmap=ap.cmap("miku", "flow", crop=(.10, .93)),
           s=42, edgecolor="white", linewidth=.35)
```

`flow` 是用这套配色**自己的色相**搭出来的一条明度严格单调的通路（viridis 的做法）：

- 明度单调 → 颜色深浅本身就编码了大小，灰度打印和色盲下都还成立
- 跨色相 → 相邻数值的色差比单色相的 `seq` 大得多，小点也分得开
- 在 LCh 里插值 + 设了彩度下限 → 中段不会掉成脏灰
- 最后按 ΔE₀₀ 弧长重采样过，相邻步长的色差基本一致（感知均匀）

58 套的 `flow` 全部明度单调，明度跨度 ~70 L\*，感知均匀度中位数 0.68。
`ap.ramp_info("miku", "flow")` 可以查单套的数值。

**`crop` 很重要**：色标最浅那一端（L\*>88）的点在白底上基本看不见。
散点默认 `crop=(0.10, 0.93)`，把两端各切掉一点。

### ③ 点特别多（几千个以上）

```python
ax.scatter(x, y, c=v, s=9, alpha=.42, linewidth=0,
           cmap=ap.cmap("miku", "flow", crop=(.35, 1.0)))
```

缩点径、降 alpha、去描边；`crop=(0.35, 1)` 只留色标较深的一半 ——
alpha 叠加会整体提亮，不砍浅端的话密集区会糊成白。

### ④ 双变量（类别 × 强度）

类别定色相，强度在该色的 `light → main → dark` 之间走：

```python
from matplotlib.colors import LinearSegmentedColormap
cm = LinearSegmentedColormap.from_list("t", [lo, base, hi])   # 同一色相的浅/主/深
```

这样两个维度分别由色相和明度承担，不会互相干扰。

### 其他强过渡场景

| 场景 | 用哪个 |
|---|---|
| 热图、密度图、等高线填充 | `seq`（单色相更"素"）或 `flow`（层次更多） |
| 相关系数矩阵、差值图、以 0 为中心 | `div` |
| 相位、角度、风向、一天中的时刻、周期 | `cyclic` |
| 3D 曲面 / 地形 | `flow`，并把光照关掉或调弱，否则明度编码会被打乱 |
| 需要灰度打印 | `flow` 或 `seq`（都明度单调）；别用 `div`、`cyclic` |

一句话判断标准：**颜色要表达"多少"就必须明度单调**（`seq` / `flow`），
要表达"哪一类"才用离散主色。`ap.ramp_info()` 里的 `monotonic` 字段就是这个检查。

```python
ap.scatter_guide("miku")        # 直接画出上面四种策略的对照图
```

### 不想装模块：直接从 HTML 取代码

色卡底部那四条色标条**是可以点的**（标题上的 `↓` 也能点）。点开会出一个代码面板：

- 上方是该色标的实时预览和体检数据（L\* 跨度 / 明度是否单调 / 感知均匀度）
- 七种格式随便切：**Python**（`LinearSegmentedColormap`，带对应场景的调用示例）、
  **Python 256**（256 级查找表 + `ListedColormap`）、**R**（`colorRampPalette` + ggplot2 用法）、
  **MATLAB**（256×3 数值矩阵）、**Origin**（16 级 HEX，逐行粘）、**CSS**（`linear-gradient`）、**HEX**
- 「复制代码」直接进剪贴板；「下载文件」存成 `<slug>_<色标>.py/.R/.m/.txt/.css`
- 「下载整套 .py」把这套配色的 6 主色、深/浅变体、中性色、色盲安全子集、
  四条 colormap 和一个 `use()` 函数打包成一个可直接 `exec` / `import` 的文件

Esc 或点空白处关闭。

---

## 科研可用性：做了什么、没做什么

配色取向是 **忠实角色 + 可用性微调**：每个颜色的**色相角基本锁定**（角色辨识度不丢），
只在 CIELAB 里调整明度 L\* 与彩度 C\*，用坐标下降最大化以下目标：

- 正常视觉下，同套 6 色两两 **ΔE₀₀** 尽量大（多数配色 ≥ 17）
- 红/绿色盲模拟（Machado et al. 2009 矩阵）下的最小 ΔE₀₀ 也纳入目标
- 白底对比度约束在 **2.0 – 14**：太浅的线看不见，太深的块压住页面
- L\* 限制在 30–78（单色系配色放宽到 20–86）

### 色盲友好度三档

| 等级 | 含义 | 用法 |
|---|---|---|
| **A**（30 套） | 红/绿色盲下 6 色两两 ΔE₀₀ ≥ 13 | 整套随便用，多系列图首选 |
| **B**（23 套） | 大部分可分 | 建议 4 个系列以内，或按「安全子集」取 |
| **C**（5 套） | 角色本身就是同色系 | 多系列时**只用**安全子集；单系列/装饰性用途不受限 |

每套都给出了 **安全子集**（`ap.safe()` / 表里的「色盲安全序号」/ HTML 里没有小圆点的色块）
——按顺序贪心挑出的、在红绿色盲下仍两两可分的最大子集。

> 没有把所有配色都强行做成色盲安全：那样会把角色配色改得面目全非。
> 取而代之的是**如实标注 + 给出安全子集**，需要严格无障碍时用 A 级或安全子集即可。

---

## Python 用法

装法见 [INSTALL.md](INSTALL.md)（pip / uv / 零安装单文件都有），无第三方依赖，
matplotlib 相关功能是懒加载的。

```python
import anime_palettes as ap

ap.ls()                     # 打印全部 58 套
ap.ls(family="蓝")           # 按色系筛
ap.ls(grade="A")            # 只看色盲友好的
ap.find("原神")              # 按角色/色调/作品模糊搜

ap.colors("miku")                     # 6 个主色，默认平滑序
ap.colors("miku", n=3)                # 只要前 3 个
ap.colors("miku", order="distinct")   # 换排序：smooth/distinct/hue/light
ap.colors("hutao", variant="dark")
ap.ORDER_LABEL                        # 四种排序的中文说明
ap.safe("nezuko")           # 色盲下仍可分的子集
ap.neutrals("gojo")         # {'bg':…, 'bg2':…, 'muted':…, 'ink':…}
```

一键接管全局风格（颜色循环 + 坐标轴 + 网格 + 默认 colormap）：

```python
ap.use_cjk_font()                     # 让中文正常显示
ap.use("hutao", order="distinct")     # 画多系列图，用区分度优先

fig, ax = plt.subplots()
for i in range(4):
    ax.plot(x, y[i], label=f"组 {i+1}")
ax.legend()
```

> `ap.use(name)` 不传 `order` 时用默认的平滑序，相邻系列的颜色会比较接近。
> **多系列图表请显式传 `order="distinct"`。**

临时套用，不污染全局：

```python
with ap.using("gojo"):
    ...
```

colormap：

```python
ax.imshow(Z, cmap=ap.cmap("ganyu"))            # 连续 seq
ax.scatter(x, y, c=v, cmap=ap.cmap("ganyu", "flow"))   # 强过渡（散点）
ax.imshow(C, cmap=ap.cmap("miku", "div"),      # 发散
          vmin=-1, vmax=1)
ap.cmap("ganyu", "seq_r")                      # 反向
ap.cmap("ganyu", "flow", crop=(.1, .93))       # 强过渡 + 裁掉太浅的一端
ap.cmap("ganyu", "cyclic")                     # 环形
ap.ramp_info("ganyu", "flow")                  # 明度跨度 / 是否单调 / 感知均匀度

ap.register()                                   # 注册全部，之后可用字符串
ax.imshow(Z, cmap="ganyu_flow")
```

看一眼效果：

```python
ap.preview("eva01")                    # 折线/柱状/散点/连续/发散/深浅 六联图
ap.preview("eva01", order="distinct")  # 对比不同排序的效果
ap.wheel("eva01")                      # 色环
ap.scatter_guide("eva01")              # 散点配色四策略对照
```

名字很宽松：`"miku"` `"初音未来"` `"miku-aqua"` `"青碧"` `"Miku"` 都指同一套。

---

## PPT 用法

**方式一（推荐，最快）**：打开 `anime-palettes-picker.pptx`，
用「格式 → 形状填充 → 取色器」直接从色块吸色。HEX 值就印在色块上。
大色块是平滑序，右下角的小色条是「区分度优先」序 —— 页内的柱状图和折线图用的就是后者，
可以直接看这套色在真实图表里的样子。

**方式二（整套切换）**：把 `ppt-theme-colors/` 里的 `.xml` 复制到

- Windows：`%APPDATA%\Microsoft\Templates\Document Themes\Theme Colors\`
- macOS：`~/Library/Group Containers/UBF8T346G9.Office/User Content/Themes/Theme Colors/`

重启 PowerPoint，在「设计 → 变体 → 颜色」里就能看到，选中即整份幻灯片换色。
映射关系：`accent1–6` = 6 个主色（按**区分度优先**顺序，因为 PowerPoint 图表是按 accent
顺序循环取色的），`lt2` = 纸色 bg，`dk2` = 墨色 ink。

**方式三**：从 `anime_palettes.xlsx` 复制 HEX。

---

## 其他软件

- **AI / PS / InDesign**：`色板 → 打开色板库 → 其他库` 选 `ase/_ALL-58-anime-palettes.ase`（58 个分组），或单独导入某一套
- **GIMP / Inkscape / Krita**：把 `gpl/*.gpl` 放进各自的 palettes 目录
- **Origin**：`origin-hex/平滑/` 或 `origin-hex/区分度/` 里的 HEX 逐行粘进自定义颜色列表
- **R**：HTML 里每张卡片的「R」按钮直接复制成 `c("#…", …)` 向量

---

## 收录清单

| 色系 | 配色 |
|---|---|
| 红 | 明日香·朱赤　胡桃·绯梅　波妞·珊瑚　千寻·朱绿　夕·墨朱 |
| 橙 | 三叶·暮橙　鸣人·橙靛　钟离·琥珀岩金　娜乌西卡·天青金 |
| 黄 | 我妻善逸·雷明黄　皮卡丘·柠黄　塞尔达·淡金　猫又·荧柠黄　知更鸟·金羽 |
| 绿 | 路易吉·草绿　索隆·苔墨　灶门炭治郎·墨绿炭赤　龙猫·苔灰　艾伦·橄榄　花里みのり·翡翠 |
| 青 | 初音未来·青碧　温迪·风薄荷　富冈义勇·松青　白龙·湖水　时透无一郎·雾青　蕾姆·孔雀　忌炎·风主青 |
| 蓝 | 五条悟·晴空蓝　绫波丽·苍白蓝　神里绫华·霜蓝　甘雨·冰蓝　林克·苍蓝　泷·夜靛　克劳德·军蓝　星乃一歌·电光蓝　阿尔托莉雅·骑士蓝金 |
| 紫 | 雷电将军·雷紫　初号机·紫萤　薇尔莉特·紫罗兰　吟霖·紫金雷　阿米娅·源石紫 |
| 粉 | 哈尔·金蓝虹　祢豆子·绯粉　三月七·樱冰　爱丽丝·玫粉鼠尾草　黄泉·洋红雷 |
| 中性 | 无脸男·墨灰　2B·素墨　卡卡西·银藏　猫咪老师·招财米　褪色者·黄金暗夜　德克萨斯·冷墨灰　小骑士·骨白深渊 |
| 撞色 | 马力欧·正红蓝　路飞·赤麦　RX-78-2·三色旗　Inkling·荧墨　雨宫莲·怪盗红黑 |

想加角色只要给名字，补进库里重新生成即可。

---

*配色为基于角色视觉印象的原创色值，不含任何原作素材。角色与作品名称仅作为色板标识使用。许可见 [LICENSE](../LICENSE)。*
