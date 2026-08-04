# 各工具里的具体写法

## matplotlib

```python
import anime_palettes as ap
import matplotlib.pyplot as plt

ap.use_cjk_font()
ap.use("ganyu", order="distinct")        # 全局；或 with ap.using("ganyu", order="distinct"):

# 多系列折线
for i, g in enumerate(groups):
    ax.plot(g.x, g.y, label=g.name)      # 颜色自动来自循环

# 误差带用同色的 light 变体
cs = ap.colors("ganyu", order="distinct")
li = ap.colors("ganyu", order="distinct", variant="light")
ax.plot(x, mu, color=cs[0])
ax.fill_between(x, mu - sd, mu + sd, color=li[0], alpha=.55, linewidth=0)

# 分类散点：白描边 + 形状冗余
for i, g in enumerate(groups):
    ax.scatter(g.x, g.y, s=46, color=cs[i], marker=["o","s","^","D","v","P"][i],
               edgecolor="white", linewidth=.7, alpha=.95, label=g.name)

# 连续着色
sc = ax.scatter(x, y, c=v, s=42, edgecolor="white", linewidth=.35,
                cmap=ap.cmap("ganyu", "flow", crop=(.10, .93)))
fig.colorbar(sc, ax=ax, label="强度")

# 点很多
ax.scatter(x, y, c=v, s=9, alpha=.42, linewidth=0,
           cmap=ap.cmap("ganyu", "flow", crop=(.35, 1.0)))

# 热图 / 相关矩阵
ax.imshow(Z, cmap=ap.cmap("ganyu", "seq"))
ax.imshow(C, cmap=ap.cmap("ganyu", "div"), vmin=-1, vmax=1)

# 相位
ax.scatter(x, y, c=phase, cmap=ap.cmap("ganyu", "cyclic"), vmin=0, vmax=2*np.pi)

# 注册后可用字符串引用
ap.register()
ax.imshow(Z, cmap="ganyu_flow")
```

**中性色别忘了**：

```python
n = ap.neutrals("ganyu")
ax.set_facecolor("white")
ax.grid(color=n["bg2"], linewidth=.8)
ax.tick_params(colors=n["ink"])
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
ax.annotate("说明", ..., color=n["muted"])
```

（`ap.use()` 已经把这些设进 rcParams 了，手动画时才需要。）

---

## seaborn

```python
import seaborn as sns
cs = ap.colors("ganyu", order="distinct")

sns.set_palette(cs)                                   # 全局
sns.scatterplot(data=df, x="x", y="y", hue="group", palette=cs[:df.group.nunique()])
sns.heatmap(corr, cmap=ap.cmap("ganyu", "div"), center=0, vmin=-1, vmax=1)
sns.kdeplot(data=df, x="x", y="y", fill=True, cmap=ap.cmap("ganyu", "seq"))
```

`hue` 的类别数超过安全色数时，改用 `ap.safe("ganyu")` 或换 A 级配色。

---

## plotly

```python
import plotly.express as px
cs = ap.colors("ganyu", order="distinct")

px.scatter(df, x="x", y="y", color="group", color_discrete_sequence=cs)
px.density_heatmap(df, x="x", y="y",
                   color_continuous_scale=[c for c in ap.get("ganyu")["flow"]])
px.imshow(corr, color_continuous_scale=ap.get("ganyu")["div"],
          color_continuous_midpoint=0)
```

plotly 的 `color_continuous_scale` 直接吃 HEX 列表，把 `flow` / `seq` / `div` 传进去即可。

---

## R / ggplot2

先生成代码：

```bash
anime-palettes hex ganyu --order distinct > ganyu.txt
anime-palettes code ganyu --ramp flow --lang r > ganyu_flow.R
```

```r
ganyu <- c("#5586CB", "#9BBADF", "#8A8F96", "#C34759", "#766987", "#33466E")

ggplot(df, aes(x, y, colour = group)) + geom_point(size = 2.4) +
  scale_colour_manual(values = ganyu)

source("ganyu_flow.R")      # 定义了 ganyu_flow()
ggplot(df, aes(x, y, colour = v)) + geom_point() +
  scale_colour_gradientn(colours = ganyu_flow(256))

ggplot(df, aes(x, y, fill = d)) + geom_tile() +
  scale_fill_gradient2(low = "#33466E", mid = "white", high = "#C34759",
                       midpoint = 0)
```

不想装 CLI 就直接读 JSON：

```r
lib <- jsonlite::fromJSON(
  "https://raw.githubusercontent.com/zomosky/anime-palettes/main/dist/anime_palettes.json",
  simplifyVector = FALSE)
e <- Filter(function(x) x$slug == "ganyu-glacier", lib)[[1]]
unlist(e$colors); unlist(e$flow)
```

---

## MATLAB

```bash
anime-palettes code ganyu --ramp flow --lang matlab > ganyu_flow.m
```

```matlab
ganyu_flow;                                  % 定义 256x3 矩阵
colormap(ganyu_flow);
scatter(x, y, 36, v, "filled"); colorbar

cs = [0.333 0.525 0.796; 0.608 0.729 0.875];  % 分类色，从 hex 转
```

---

## Origin

`dist/origin-hex/` 下三个目录：`平滑/`、`区分度/`（各 36 个 txt，逐行 HEX）、
`flow色标/`（16 级取样，用来做自定义色阶）。
打开对应 txt，全选复制，粘进 Origin 的自定义颜色列表 / Color Palette 编辑器。

---

## PPT / Keynote

1. **整份换色**：把 `dist/ppt-theme-colors/<slug>.xml` 复制到
   - Windows `%APPDATA%\Microsoft\Templates\Document Themes\Theme Colors\`
   - macOS `~/Library/Group Containers/UBF8T346G9.Office/User Content/Themes/Theme Colors/`

   重启 PowerPoint，「设计 → 变体 → 颜色」里选。`accent1–6` 是按区分度序排的，
   所以 PowerPoint 原生图表按 accent 循环取色时相邻系列自然分得开。

2. **单个吸色**：打开 `dist/anime-palettes-picker.pptx`，取色器直接吸，HEX 印在色块上。

3. Keynote / Google Slides 没有主题色导入，直接抄 HEX。

---

## HTML / CSS / 网页

```bash
anime-palettes code ganyu --ramp flow --lang css
```

```css
:root {
  --c1: #5586CB; --c2: #9BBADF; --c3: #8A8F96;
  --c4: #C34759; --c5: #766987; --c6: #33466E;
  --bg: #F2F6FB; --bg2: #E0E9F4; --muted: #7E858F; --ink: #1B2735;
}
.ramp { background: linear-gradient(90deg, /* flow 的 12 级 */); }
```

D3 / Observable：

```js
const lib = await fetch("https://raw.githubusercontent.com/zomosky/anime-palettes/main/dist/anime_palettes.json").then(r => r.json());
const e = lib.find(p => p.slug === "ganyu-glacier");
const color = d3.scaleOrdinal(e.colors);
const heat  = d3.scaleSequential(t => d3.interpolateRgbBasis(e.flow)(t));
```

---

## Adobe / GIMP

- AI / PS / ID：`色板 → 打开色板库 → 其他库`，选 `dist/ase/_ALL-36-anime-palettes.ase`（36 个分组），或单套的 `dist/ase/<slug>.ase`
- GIMP / Inkscape / Krita：把 `dist/gpl/<slug>.gpl` 放进各自的 palettes 目录
