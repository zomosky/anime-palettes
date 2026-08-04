# 安装与使用 —— 完整手法

按「你有多想省事」从上到下排。**前两节完全不用装东西。**

- [零安装](#零安装) · [pip](#pip) · [uv](#uv) · [conda / mamba](#conda--mamba)
- [离线 / 内网](#离线--内网) · [网络慢怎么办](#网络慢怎么办) · [其他语言](#其他语言直接读-json)
- [命令行](#命令行) · [卸载与升级](#卸载与升级) · [排错](#排错)

仓库地址：`https://github.com/zomosky/anime-palettes`

---

## 零安装

### 1. 在线打开色卡库

仓库开了 GitHub Pages 之后直接访问（Settings → Pages → Source 选 `main` / `root`）：

```
https://zomosky.github.io/anime-palettes/dist/anime-palettes.html
```

没开 Pages 也能看，用 htmlpreview 代理渲染：

```
https://htmlpreview.github.io/?https://github.com/zomosky/anime-palettes/blob/main/dist/anime-palettes.html
```

点色标条就能拿 Python / R / MATLAB / Origin / CSS 代码，复制或下载成文件，这条路根本不碰 Python。

### 2. 抓单文件模块（核心 API 零依赖）

`anime_palettes.py` 是**自包含单文件**，配色数据就在里面，不 import 任何第三方库
（matplotlib 只在你真的画图时才懒加载）。丢进项目目录就能用：

```bash
# macOS / Linux
curl -fsSLO https://raw.githubusercontent.com/zomosky/anime-palettes/main/anime_palettes.py

# Windows PowerShell
irm https://raw.githubusercontent.com/zomosky/anime-palettes/main/anime_palettes.py -OutFile anime_palettes.py
```

```python
import anime_palettes as ap
ap.use("hutao", order="distinct")
```

### 3. Jupyter / Colab 一行

```python
!curl -fsSLO https://raw.githubusercontent.com/zomosky/anime-palettes/main/anime_palettes.py
import anime_palettes as ap
```

或者干脆装进内核：

```python
%pip install -q git+https://github.com/zomosky/anime-palettes.git
```

### 4. 只要颜色，连文件都不想下

`dist/anime_palettes.json` 是完整数据（含 256 级色标），任何语言都能读：

```python
import json, urllib.request
URL = "https://raw.githubusercontent.com/zomosky/anime-palettes/main/dist/anime_palettes.json"
lib = json.load(urllib.request.urlopen(URL))
miku = next(e for e in lib if e["slug"] == "miku-aqua")
print(miku["colors"], miku["flow"][::32])
```

> 不建议用 `exec(urlopen(...).read())` 这类「远程执行」写法 —— 下载成文件再 import，
> 可复现，也不会因为断网就跑不了。

---

## pip

### 直接从 Git 安装（推荐，不需要发布到 PyPI）

```bash
pip install git+https://github.com/zomosky/anime-palettes.git
```

装完就能 `import anime_palettes`，同时多一个 `anime-palettes` 命令。

**钉死版本**（推荐写进项目依赖，避免以后配色改了导致图变样）：

```bash
pip install "anime-palettes @ git+https://github.com/zomosky/anime-palettes.git@v1.0.0"
```

也可以钉 commit：`...git@0f5e78e`。

**带画图依赖一起装**：

```bash
pip install "anime-palettes[plot] @ git+https://github.com/zomosky/anime-palettes.git"
```

`[plot]` = matplotlib + numpy；`[build]` 再多一个 openpyxl（只有要重新生成整个色库才需要）。

### 写进 requirements.txt

```
anime-palettes @ git+https://github.com/zomosky/anime-palettes.git@v1.0.0
```

`pyproject.toml`（PEP 508）：

```toml
dependencies = [
  "anime-palettes @ git+https://github.com/zomosky/anime-palettes.git@v1.0.0",
]
```

### 没有 Git 命令的机器

pip 从 git+ 装需要系统里有 `git`。没有的话直接装 zip 包：

```bash
pip install https://github.com/zomosky/anime-palettes/archive/refs/heads/main.zip
# 或指定 tag
pip install https://github.com/zomosky/anime-palettes/archive/refs/tags/v1.0.0.zip
```

### 虚拟环境（不想污染系统 Python）

```bash
python3 -m venv .venv
source .venv/bin/activate            # Windows: .venv\Scripts\activate
pip install "anime-palettes[plot] @ git+https://github.com/zomosky/anime-palettes.git"
```

不想建虚拟环境又遇到系统 Python 拒绝写入（Debian/Ubuntu 的 externally-managed 报错）：

```bash
pip install --user git+https://github.com/zomosky/anime-palettes.git
# 实在要覆盖系统环境（不推荐）：加 --break-system-packages
```

### 本地开发（改配色）

```bash
git clone https://github.com/zomosky/anime-palettes.git
cd anime-palettes
pip install -e ".[build]"            # 可编辑安装，改了立刻生效
make test
```

---

## uv

[uv](https://docs.astral.sh/uv/) 是 Rust 写的 Python 包管理器，比 pip 快一到两个数量级，
还能管 Python 版本本身。**没有 uv 的话先装它**（三选一，都不需要预先有 Python）：

```bash
# macOS / Linux —— 官方安装脚本
curl -LsSf https://astral.sh/uv/install.sh | sh

# macOS —— Homebrew
brew install uv

# Windows PowerShell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
# 或 winget install --id=astral-sh.uv -e

# 已经有 pip 的话最省事
pip install uv          # 或 pipx install uv
```

装完 `uv --version` 能出版本号就行。下面四种用法按场景挑：

### ① 项目依赖（最常用）

```bash
uv init myproject && cd myproject
uv add "anime-palettes @ git+https://github.com/zomosky/anime-palettes.git"
uv add matplotlib numpy
uv run python my_figure.py
```

钉版本：

```bash
uv add "anime-palettes @ git+https://github.com/zomosky/anime-palettes.git@v1.0.0"
```

uv 会把精确版本和哈希写进 `uv.lock`，换台机器 `uv sync` 就能还原一模一样的环境。

### ② 临时跑一下，不建项目

```bash
uv run --with "anime-palettes @ git+https://github.com/zomosky/anime-palettes.git" \
       --with matplotlib --with numpy \
       python my_figure.py
```

`--with` 的依赖装在临时环境里，跑完不留痕迹，也不碰你现有的环境。

### ③ 单文件脚本自带依赖（PEP 723，最优雅）

在脚本开头写一段元数据注释，`uv run` 会自动建环境：

```python
#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.9"
# dependencies = [
#   "anime-palettes @ git+https://github.com/zomosky/anime-palettes.git",
#   "matplotlib", "numpy",
# ]
# ///
import anime_palettes as ap
ap.use("ganyu", order="distinct")
...
```

```bash
uv run my_figure.py          # 就这样，不用装任何前置
chmod +x my_figure.py && ./my_figure.py    # 或者直接执行
```

仓库里的 [`examples/uv_single_file.py`](../examples/uv_single_file.py) 就是现成的例子。
这是「挂在 git 上直接用」最干净的形态 —— 脚本本身就声明了从哪个仓库的哪个版本取配色。

### ④ 只用命令行工具，不写代码

```bash
uvx --from git+https://github.com/zomosky/anime-palettes anime-palettes ls
uvx --from git+https://github.com/zomosky/anime-palettes anime-palettes show 胡桃
uvx --from git+https://github.com/zomosky/anime-palettes anime-palettes \
    code ganyu --ramp flow --lang r > ganyu_flow.R
```

`uvx` 每次跑在隔离环境里，什么都不留。想常驻就装成工具：

```bash
uv tool install "anime-palettes @ git+https://github.com/zomosky/anime-palettes.git"
anime-palettes ls          # 之后直接用
uv tool upgrade anime-palettes
```

> pip 用户的等价物是 `pipx install "anime-palettes @ git+https://..."`。

### uv 的 pip 兼容层

已有 requirements.txt 的项目想提速，不改任何写法：

```bash
uv pip install git+https://github.com/zomosky/anime-palettes.git
uv pip install -r requirements.txt
```

---

## conda / mamba

conda 生态里没有这个包，但 conda 环境里可以正常用 pip：

```bash
conda create -n fig python=3.11 matplotlib numpy -y
conda activate fig
pip install git+https://github.com/zomosky/anime-palettes.git
```

`environment.yml`：

```yaml
name: fig
channels: [conda-forge]
dependencies:
  - python=3.11
  - matplotlib
  - numpy
  - pip
  - pip:
      - anime-palettes @ git+https://github.com/zomosky/anime-palettes.git@v1.0.0
```

---

## 离线 / 内网

配色数据全在 `anime_palettes.py` 一个文件里，所以离线最简单的办法就是**把这个文件拷过去**。

要完整安装的话，在有网的机器上：

```bash
pip download git+https://github.com/zomosky/anime-palettes.git -d ./pkgs --no-deps
# 或者直接下 zip
curl -fsSLO https://github.com/zomosky/anime-palettes/archive/refs/tags/v1.0.0.zip
```

拷到内网机器：

```bash
pip install --no-index --find-links=./pkgs anime-palettes
# 或
pip install ./v1.0.0.zip
```

---

## 网络慢怎么办

国内直连 GitHub 不稳时：

- **先 clone 再本地装**：`git clone` 失败可以重试续传，比 pip 一把梭稳
  ```bash
  git clone --depth 1 https://github.com/zomosky/anime-palettes.git
  pip install ./anime-palettes
  ```
- **只取单文件**：`anime_palettes.py` 只有 ~130 KB，从 raw 或任意 GitHub 加速前缀取都很快
- **走代理**：`pip install --proxy http://127.0.0.1:7890 git+https://...`，
  或者给 git 设 `git config --global http.proxy http://127.0.0.1:7890`
- **PyPI 镜像救不了 git+ 依赖**（镜像只镜像 PyPI 上的包），但能加速 matplotlib / numpy 这些：
  ```bash
  pip install matplotlib numpy -i https://pypi.tuna.tsinghua.edu.cn/simple
  ```
  uv 同理：`UV_DEFAULT_INDEX=https://pypi.tuna.tsinghua.edu.cn/simple uv add ...`

---

## 其他语言（直接读 JSON）

`dist/anime_palettes.json` 是完整数据，字段见 [USAGE.md](USAGE.md)。

**R**

```r
library(jsonlite)
URL <- "https://raw.githubusercontent.com/zomosky/anime-palettes/main/dist/anime_palettes.json"
lib <- fromJSON(URL, simplifyVector = FALSE)
miku <- Filter(function(e) e$slug == "miku-aqua", lib)[[1]]
cols <- unlist(miku$colors)

ggplot(df, aes(x, y, colour = g)) + geom_point() +
  scale_colour_manual(values = cols)

flow <- colorRampPalette(unlist(miku$flow), space = "Lab")
ggplot(df, aes(x, y, colour = v)) + geom_point() +
  scale_colour_gradientn(colours = flow(256))
```

更省事：直接用 CLI 生成 R 代码 ——
`anime-palettes code miku --ramp flow --lang r > miku_flow.R`

**MATLAB**

```matlab
lib = jsondecode(webread('https://raw.githubusercontent.com/zomosky/anime-palettes/main/dist/anime_palettes.json'));
```

或 `anime-palettes code miku --ramp flow --lang matlab > miku_flow.m`，得到一个 256×3 矩阵。

**JavaScript / Observable**

```js
const lib = await fetch(
  "https://raw.githubusercontent.com/zomosky/anime-palettes/main/dist/anime_palettes.json"
).then(r => r.json());
const miku = lib.find(e => e.slug === "miku-aqua");
d3.scaleSequential(t => d3.interpolateRgbBasis(miku.flow)(t));
```

**Origin / GraphPad / AI / PS**：仓库 `dist/` 下有现成的
`origin-hex/`（逐行 HEX）、`ase/`（Adobe 色板）、`gpl/`（GIMP 色板）、
`ppt-theme-colors/`（PowerPoint 主题色）。

---

## 命令行

装完（pip / uv tool / pipx 任一）就有 `anime-palettes` 命令。没装也能用：
`python anime_palettes.py <命令>`。

```bash
anime-palettes ls                          # 全部 36 套，终端里直接显示色块
anime-palettes ls --family 蓝 --grade A     # 按色系 / 色盲等级筛
anime-palettes show 胡桃                    # 单套全貌：深浅变体、中性色、四种排序、四条色标
anime-palettes show miku --order distinct

anime-palettes hex miku -n 3               # 只出 HEX，方便管道
anime-palettes hex 甘雨 --safe              # 色盲安全子集
anime-palettes hex hutao --variant dark

anime-palettes code ganyu --ramp flow --lang python > ganyu_flow.py
anime-palettes code ganyu --ramp cyclic --lang matlab > ganyu_cyclic.m
#   --ramp  seq | flow | div | cyclic
#   --lang  python | python256 | r | matlab | origin | css | hex

anime-palettes search 原神
anime-palettes json miku | jq '.colors'
```

色块用的是终端真彩色（24-bit）。iTerm2、Windows Terminal、VS Code 终端、
现代 GNOME Terminal 都支持；不支持的终端会退化成纯文字，HEX 照样能看。

---

## 卸载与升级

```bash
pip install -U --force-reinstall git+https://github.com/zomosky/anime-palettes.git
pip uninstall anime-palettes

uv add "anime-palettes @ git+https://github.com/zomosky/anime-palettes.git@v1.1.0"   # 换版本
uv tool upgrade anime-palettes
uv tool uninstall anime-palettes
```

> 从 git 装的包，pip 不会自动发现上游有新提交。想更新必须
> `--force-reinstall`，或者钉一个新的 tag / commit。这其实是好事 ——
> 配色悄悄变了会让你以前的图对不上。

---

## 排错

| 症状 | 原因 / 解决 |
|---|---|
| `error: externally-managed-environment` | 系统 Python 保护。用虚拟环境，或 `pip install --user`，或（不推荐）`--break-system-packages` |
| `git: command not found` | 改用 zip 安装：`pip install https://github.com/zomosky/anime-palettes/archive/refs/heads/main.zip` |
| `ModuleNotFoundError: matplotlib` | 核心 API 不需要它，但 `cmap` / `use` / `preview` 需要。`pip install matplotlib numpy` 或装 `[plot]` extra |
| 图里中文变方框 | 先调 `ap.use_cjk_font()`；系统里一个中文字体都没有的话装 `fonts-noto-cjk`（Linux）或指定 `ap.use_cjk_font("SimHei")` |
| `anime-palettes: command not found` | 装到了用户目录但 `~/.local/bin` 不在 PATH。加进 PATH，或直接 `python -m anime_palettes` 不行时用 `python anime_palettes.py` |
| 终端里色块是乱码 | 终端不支持 24-bit 色。看 HEX 就行，或用 `--lang hex` 输出纯文本 |
| `uv` 装了但找不到命令 | 重开一个终端，或 `source ~/.local/bin/env` |
| 从 git 装很慢 / 超时 | 见[网络慢怎么办](#网络慢怎么办) |

还有问题就开 [issue](https://github.com/zomosky/anime-palettes/issues)。
