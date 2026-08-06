# 配色增补 · 标志物开关 · 自助加角色 —— 实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 把配色库从 36 套扩到 58 套堵上色相/彩度/明度空白，给色卡库加一个默认关闭的标志物开关，再提供 `src/propose.py` 让别人自助加自己喜欢的角色。

**Architecture:** 一切仍从 `src/data.py` 派生（`tune` → `derive` → 各 gen 脚本）。标志物作为第二份手写数据源 `src/marks.py` 直接喂 `gen_html.py`，不进 `derive.py`、不进 `library.json`。`propose.py` 把 `tune.py` 的目标函数常量收进 profile 参数，用不同 profile 跑出 5 个候选方案供人挑，选定后增量写回 `data.py` 和 `tuned.py`。

**Tech Stack:** Python 3.8+（核心零依赖，只用 stdlib + `src/colorlib.py`）、make、pytest。生成 xlsx 需 `openpyxl`，pptx 需 `node + pptxgenjs`，配图需 `matplotlib numpy`。

## Global Constraints

- **文档、注释、commit message 一律中文。**
- **永远不要手改这些产物**：`anime_palettes.py`、`dist/**`、`src/tuned.py`、`src/library.json`、`skills/anime-palettes/references/palettes.md`、`skills/anime-palettes.skill`。它们由生成链路产出，CI 会逐字节 diff。
- **生成脚本假定 cwd 是 `src/`**（`library.json`、`build/` 都是相对路径）。走 `make`，或 `cd src && python xxx.py`。
- **改了 `data.py` 里的色值或增删 slug，必须 `make tune`**，否则 `derive.py` 会因指纹不符直接报错退出。
- **加了新 slug 必须 `make skill`**，否则 CI 的速查表一致性检查失败。
- **`tune()` 的默认 profile 数值必须与改造前逐位一致**：`_penalty` 权重 `0.55`、`_min_pair(weight_cvd=0.65)`、`LMIN=30.0`、`LMAX=78.0`、`MONO_LMIN=20.0`、`MONO_LMAX=86.0`、`seed=7`、`iters=340`、`restart=6`。任何偏差都会让现有 36 套的 `tuned.py` 变化，CI 逐字节 diff 直接红。
- **6 主色取色必须落在 `L* ∈ [30, 78]`**（`MONO` 集合 `[20, 86]`），且对白对比度在 `[2, 14]` 内。超出窗口会被 `tune` 拽回来，近中性色还会被甩掉色相（`#1A1A1A` → `#404944` 绿灰）。
- **`marks.py` 只被 `gen_html.py` 引用**，不得进入 `derive.py` 或 `library.json` —— 那会破坏 `dist/anime_palettes.json` 与 `src/library.json` 内容完全相同这条不变量。
- **标志物只画通用物件的通用画法**，不画人物形象，不复制作品 logo / 纹章 / 族徽 / 特定图案设计。
- **色盲评级如实标注**，达不到 A 就给安全子集，不硬改色值粉饰。

---

## 文件结构

| 文件 | 职责 | 本计划中的动作 |
| --- | --- | --- |
| `src/data.py` | 唯一手写色值源 | 修改：修正 1 处 family、追加 22 条记录 |
| `src/marks.py` | **新**：手写标志物 SVG 源 | 创建：58 条 `slug → (viewBox, path_d)` |
| `src/tune.py` | 坐标下降调优器 | 修改：常量收进 `Profile`，新增 5 个预设 |
| `src/propose.py` | **新**：候选方案生成 + 写回 | 创建 |
| `src/gen_html.py` | 单文件色卡库 | 修改：接标志物开关 |
| `src/gen_skill_table.py` | skill 速查表 | 修改：标题计数 |
| `tests/test_palettes.py` | 全部测试 | 修改：计数、新增 8 组测试 |
| `skills/anime-palettes/references/add-palette.md` | **新**：自助加配色指南 | 创建 |
| `skills/anime-palettes/SKILL.md` | skill 主文档 | 修改：加一节指向上面 |
| `README.md` / `docs/USAGE.md` / `docs/INSTALL.md` / `src/README.md` | 文档 | 修改：计数与统计 |

---

## Task 1: 修正 howl 归类，并加上 family / slug 的合法性守卫

`howl-iridescent` 的签名色 `#C4548C` 是 LCh 色相 350 的粉红，却归在「紫」family，检索时会误导。
family **不参与** `source_fingerprint()`（它只哈希 slug + colors + mono），所以这一步**不需要 `make tune`**。

**Files:**
- Modify: `src/data.py:108-110`（`howl-iridescent` 记录的 `family`）
- Test: `tests/test_palettes.py`

**Interfaces:**
- Consumes: 无
- Produces: 无新接口。后续任务依赖这里新增的 `test_family_is_valid` / `test_slug_is_unique` 自动覆盖新配色。

- [ ] **Step 1: 写失败测试**

在 `tests/test_palettes.py` 的 `test_tuned_is_in_sync_with_data` 之后插入：

```python
def test_family_is_valid():
    """family 是检索标签，拼错或用了没定义的标签会让 HTML 的筛选按钮筛不到东西。"""
    import data
    for p in data.PALETTES:
        assert p["family"] in data.FAMILY_ORDER, \
            f"{p['slug']} 的 family {p['family']!r} 不在 FAMILY_ORDER 里"


def test_slug_is_unique():
    import data
    slugs = [p["slug"] for p in data.PALETTES]
    dup = {s for s in slugs if slugs.count(s) > 1}
    assert not dup, f"slug 重复：{dup}"


def test_purple_family_signature_is_actually_purple():
    """「紫」这个标签的签名色必须真落在紫区（LCh 色相 285-335）。

    howl-iridescent 的 #C4548C 是 h=350 的粉红，一度被归在紫 —— 检索「紫」的人
    会拿到一套粉配色。这里守住这条线。
    """
    from colorlib import lch
    for slug in ALL:
        e = ap.PALETTES[slug]
        if e["family"] != "紫":
            continue
        h = lch(e["colors"][0])[2]
        assert 285 <= h <= 335, f"{slug} 归在紫，但签名色 {e['colors'][0]} 的 h={h:.1f}"
```

- [ ] **Step 2: 跑测试确认失败**

```bash
python -m pytest tests/test_palettes.py::test_purple_family_signature_is_actually_purple -q
```

预期：FAIL，`howl-iridescent 归在紫，但签名色 #C4548C 的 h=350.3`

- [ ] **Step 3: 改 data.py**

把 `howl-iridescent` 记录里的 `family="紫"` 改成 `family="粉"`：

```python
    dict(slug="howl-iridescent", zh="哈尔", en="Howl", tone_zh="金蓝虹", tone_en="Iridescent Gold",
         family="粉", source="哈尔的移动城堡",
         colors=["#C4548C", "#3E6E9E", "#D9B44A", "#7FB7D4", "#5A8C6E", "#EFE7D6"]),
```

同时把它从「紫」分组的注释块挪到「粉」分组的末尾（`aerith-rose-sage` 之后），保持文件里分组与 family 一致。

- [ ] **Step 4: 重新生成产物并跑全量测试**

```bash
make all
```

预期：`derive` 正常跑完（指纹没变，不需要 tune），测试全绿。`dist/**` 里带 family 的产物会有 diff，这是预期内的。

- [ ] **Step 5: 提交**

```bash
git add src/data.py tests/test_palettes.py anime_palettes.py src/library.json dist docs/images skills
git commit -m "修正 howl 的色系归类：签名色是 h=350 的粉红，不该归在紫

顺带补上 family 合法性、slug 唯一性、紫系签名色色相三条守卫，
后面加 22 套新配色时能自动覆盖。"
```

---

## Task 2: 增补 7 套动漫配色

7 套全部堵在设计文档量出的空洞上。色值已实测过 `tune()`，评级 A2 / B5，无 C。

**Files:**
- Modify: `src/data.py`（各 family 分组末尾追加）
- Modify: `tests/test_palettes.py`（`test_palette_count`）
- Test: `tests/test_palettes.py`

**Interfaces:**
- Consumes: Task 1 的 `test_family_is_valid` / `test_slug_is_unique`
- Produces: 7 个新 slug，供 Task 5 的计数更新和 Task 6 的 `marks.py` 引用：
  `eren-survey-olive`、`haku-river`、`muichiro-mist`、`rem-peacock`、`violet-evergarden`、`nyanko-fortune`、`rx78-trikolor`

- [ ] **Step 1: 写失败测试**

把 `tests/test_palettes.py` 的 `test_palette_count` 改成 43，并在其后新增：

```python
def test_palette_count():
    assert len(ALL) == 43
    assert len({ap.PALETTES[s]["name_zh"] for s in ALL}) == 43


# 新增配色的验收线：不能有 C 级，且最小色差要够画多系列图
NEW_ANIME = {
    "eren-survey-olive": "B", "haku-river": "B", "muichiro-mist": "B",
    "rem-peacock": "A", "violet-evergarden": "B", "nyanko-fortune": "A",
    "rx78-trikolor": "A",
}


@pytest.mark.parametrize("slug,expect", sorted(NEW_ANIME.items()))
def test_new_anime_palettes_meet_the_bar(slug, expect):
    e = ap.PALETTES[slug]
    assert e["cvd_grade"] == expect, f"{slug} 评级是 {e['cvd_grade']}，预期 {expect}"
    assert e["min_de"] >= 10.0, f"{slug} 最小 ΔE00 只有 {e['min_de']}"
```

- [ ] **Step 2: 跑测试确认失败**

```bash
python -m pytest tests/test_palettes.py::test_palette_count -q
```

预期：FAIL，`assert 36 == 43`

- [ ] **Step 3: 往 data.py 追加 7 条记录**

按 family 分组插到对应位置（绿组末尾、青组末尾、紫组末尾、中性组末尾、撞色组末尾）：

```python
    # 绿组末尾（totoro-moss-gray 之后）
    dict(slug="eren-survey-olive", zh="艾伦", en="Eren", tone_zh="橄榄", tone_en="Survey Olive",
         family="绿", source="进击的巨人",
         colors=["#6E7A3C", "#A8B073", "#43505C", "#8E5A38", "#9E3A2E", "#D8D2BE"]),

    # 青组末尾（giyu-pine 之后）
    dict(slug="haku-river", zh="白龙", en="Haku", tone_zh="湖水", tone_en="River Jade",
         family="青", source="千与千寻",
         colors=["#6EC4CC", "#A8DEE0", "#2E6B78", "#C4483A", "#4A5A50", "#E0E8E4"]),
    dict(slug="muichiro-mist", zh="时透无一郎", en="Muichiro", tone_zh="雾青", tone_en="Mist Teal",
         family="青", source="鬼灭之刃",
         colors=["#4FA8B8", "#A0D4DC", "#2E5A66", "#8C8CB4", "#6E8C68", "#DCD8CC"]),
    dict(slug="rem-peacock", zh="蕾姆", en="Rem", tone_zh="孔雀", tone_en="Peacock Blue",
         family="青", source="Re:从零开始的异世界生活",
         colors=["#4FB0C8", "#A4DCE8", "#2E6B80", "#3E4250", "#5A6BA8", "#E4E2DC"]),

    # 紫组末尾（eva01-violet-lime 之后，howl 已在 Task 1 挪走）
    dict(slug="violet-evergarden", zh="薇尔莉特", en="Violet", tone_zh="紫罗兰", tone_en="Violet Bloom",
         family="紫", source="紫罗兰永恒花园",
         colors=["#9B4FA8", "#C48CD0", "#5E2E6E", "#D9B45C", "#4A7FC4", "#E8E0D4"]),

    # 中性组末尾（kakashi-silver-navy 之后）
    dict(slug="nyanko-fortune", zh="猫咪老师", en="Nyanko-sensei", tone_zh="招财米", tone_en="Fortune Beige",
         family="中性", source="夏目友人帐",
         colors=["#C9B48C", "#E0D4B8", "#8A7654", "#C4453A", "#E0A83A", "#4E4A42"]),

    # 撞色组末尾（luffy-red-straw 之后）
    dict(slug="rx78-trikolor", zh="RX-78-2", en="RX-78-2", tone_zh="三色旗", tone_en="Trikolor",
         family="撞色", source="机动战士高达",
         colors=["#1B4E9B", "#C8102E", "#E8B800", "#C4C8CC", "#6E727A", "#2E3238"]),
```

- [ ] **Step 4: 重新调优（约 50s）**

```bash
make tune
```

预期：终端逐行打出 43 套的 `minΔE / CVDΔE`，写入 `src/tuned.py`。
现有 36 套的调优结果**必须一字不变** —— `tune()` 逐套独立，加新记录不影响老的。用这条确认：

```bash
git diff --stat src/tuned.py
```

预期：只有新增行 + `SOURCE` 那一行变化。若老配色的色值也变了，说明误改了 `tune.py`，停下来排查。

- [ ] **Step 5: 重新生成全部产物**

```bash
make all
```

- [ ] **Step 6: 跑测试确认通过**

```bash
python -m pytest tests/ -q
```

预期：全绿。

- [ ] **Step 7: 提交**

```bash
git add -A
git commit -m "增补 7 套动漫配色：艾伦 / 白龙 / 时透 / 蕾姆 / 薇尔莉特 / 猫咪老师 / RX-78-2

堵的是量出来的空洞：青蓝 51° 空洞由白龙(209)、时透(216)、蕾姆(224) 三套填上，
黄绿洞由艾伦(114)、紫红洞由薇尔莉特(323)。猫咪老师补暖中性 —— 现有 3 套中性全是冷调。
RX-78-2 把撞色从 2 套补到 3 套。评级 A2/B5，无 C。"
```

---

## Task 3: 增补 8 套游戏配色（一）

**Files:**
- Modify: `src/data.py`
- Modify: `tests/test_palettes.py`
- Test: `tests/test_palettes.py`

**Interfaces:**
- Consumes: Task 2 的 43 套基线
- Produces: 8 个新 slug：`ichika-leoneed`、`minori-emerald`、`inkling-splat`、`joker-phantom`、`tarnished-gilded`、`nekomata-neon`、`acheron-magenta`、`dusk-inkvermilion`

- [ ] **Step 1: 写失败测试**

`test_palette_count` 改成 51，并新增：

```python
NEW_GAME_1 = {
    "ichika-leoneed": "A", "minori-emerald": "B", "inkling-splat": "A",
    "joker-phantom": "B", "tarnished-gilded": "A", "nekomata-neon": "A",
    "acheron-magenta": "B", "dusk-inkvermilion": "A",
}


@pytest.mark.parametrize("slug,expect", sorted(NEW_GAME_1.items()))
def test_new_game_palettes_1_meet_the_bar(slug, expect):
    e = ap.PALETTES[slug]
    assert e["cvd_grade"] == expect, f"{slug} 评级是 {e['cvd_grade']}，预期 {expect}"
    assert e["min_de"] >= 10.0, f"{slug} 最小 ΔE00 只有 {e['min_de']}"


def test_warm_dark_signature_exists():
    """增补前 L*<35 的签名色全部挤在 h 276-291 的蓝紫带，红/橙/绿/青一个都没有。

    dusk-inkvermilion（墨朱，h≈20 L≈33）是全库第一个暖调暗色签名。
    """
    from colorlib import lch
    warm_dark = [s for s in ALL
                 if (lambda t: t[0] < 35 and (t[2] < 100 or t[2] > 330))(lch(ap.PALETTES[s]["colors"][0]))]
    assert "dusk-inkvermilion" in warm_dark, f"暖调暗色签名只有 {warm_dark}"
```

- [ ] **Step 2: 跑测试确认失败**

```bash
python -m pytest tests/test_palettes.py::test_palette_count -q
```

预期：FAIL，`assert 43 == 51`

- [ ] **Step 3: 往 data.py 追加 8 条记录**

```python
    # 红组末尾（chihiro-vermilion-fern 之后）
    dict(slug="dusk-inkvermilion", zh="夕", en="Dusk", tone_zh="墨朱", tone_en="Ink & Vermilion",
         family="红", source="明日方舟",
         colors=["#8C2E3A", "#C46A6A", "#3E4A50", "#C4A45A", "#7A9EA8", "#DCD4C4"]),

    # 黄组末尾（zelda-pale-gold 之后）
    dict(slug="nekomata-neon", zh="猫又", en="Nekomata", tone_zh="荧柠黄", tone_en="Neon Lemon",
         family="黄", source="绝区零",
         colors=["#E8D42E", "#F0E88C", "#8C7A18", "#E0508C", "#3E3A40", "#D8D4C8"]),

    # 绿组末尾（eren-survey-olive 之后）
    dict(slug="minori-emerald", zh="花里みのり", en="Minori", tone_zh="翡翠", tone_en="Emerald Jump",
         family="绿", source="世界计划",
         colors=["#00BB88", "#F0849E", "#4A7FC4", "#E0B040", "#7A5240", "#DCE8E2"]),

    # 蓝组末尾（cloud-soldier 之后）
    dict(slug="ichika-leoneed", zh="星乃一歌", en="Ichika", tone_zh="电光蓝", tone_en="Leo/need Blue",
         family="蓝", source="世界计划",
         colors=["#4455DD", "#33AAEE", "#F0C82E", "#EE6666", "#2ECC94", "#D8DCE8"]),

    # 粉组末尾（aerith-rose-sage 之后，howl 也在这组）
    dict(slug="acheron-magenta", zh="黄泉", en="Acheron", tone_zh="洋红雷", tone_en="Nihility Magenta",
         family="粉", source="崩坏：星穹铁道",
         colors=["#B0308C", "#E89AC8", "#3A3448", "#C8C4CC", "#D9B45C", "#8C3A4A"]),

    # 中性组末尾（nyanko-fortune 之后）
    dict(slug="tarnished-gilded", zh="褪色者", en="Tarnished", tone_zh="黄金暗夜", tone_en="Gilded Nightfall",
         family="中性", source="艾尔登法环",
         colors=["#5A4A34", "#C9A24A", "#E0CFA4", "#8E3A2E", "#8A8478", "#3A3228"]),

    # 撞色组末尾（rx78-trikolor 之后）
    dict(slug="inkling-splat", zh="Inkling", en="Inkling", tone_zh="荧墨", tone_en="Splat Neon",
         family="撞色", source="斯普拉遁",
         colors=["#F02D7D", "#5FD424", "#FF7A00", "#00B4D8", "#3E3A44", "#DCD8D0"]),
    dict(slug="joker-phantom", zh="雨宫莲", en="Joker", tone_zh="怪盗红黑", tone_en="Phantom Crimson",
         family="撞色", source="女神异闻录5",
         colors=["#E60012", "#8E1420", "#3A3A3E", "#C8C4BE", "#7A5A48", "#E8DED0"]),
```

- [ ] **Step 4: 重新调优（约 58s）**

```bash
make tune && git diff --stat src/tuned.py
```

预期：老配色的色值不变，只有新增行 + `SOURCE`。

- [ ] **Step 5: 重新生成全部产物**

```bash
make all
```

- [ ] **Step 6: 跑测试确认通过**

```bash
python -m pytest tests/ -q
```

- [ ] **Step 7: 提交**

```bash
git add -A
git commit -m "增补 8 套游戏配色（一）：一歌 / みのり / Inkling / Joker / 褪色者 / 猫又 / 黄泉 / 夕

星乃一歌(h298 C81) 把 145-305 半圈的签名色彩度天花板从 48 抬到 81；
黄泉(h339 C69) 填玫红洞并把该区彩度从 49 抬到 69；
夕(h20 L33) 是全库第一个暖调暗色签名。评级 A5/B3，无 C。"
```

---

## Task 4: 增补 7 套游戏配色（二）

**Files:**
- Modify: `src/data.py`
- Modify: `tests/test_palettes.py`
- Test: `tests/test_palettes.py`

**Interfaces:**
- Consumes: Task 3 的 51 套基线
- Produces: 7 个新 slug：`yinlin-violetgold`、`jiyan-windteal`、`amiya-originium`、`texas-inkgray`、`robin-goldfeather`、`saber-knightblue`、`hollowknight-pale`。至此 58 套定型，Task 5/6 依赖这个全集。

- [ ] **Step 1: 写失败测试**

`test_palette_count` 改成 58，并新增：

```python
NEW_GAME_2 = {
    "yinlin-violetgold": "A", "jiyan-windteal": "B", "amiya-originium": "A",
    "texas-inkgray": "B", "robin-goldfeather": "A", "saber-knightblue": "A",
    "hollowknight-pale": "B",
}


@pytest.mark.parametrize("slug,expect", sorted(NEW_GAME_2.items()))
def test_new_game_palettes_2_meet_the_bar(slug, expect):
    e = ap.PALETTES[slug]
    assert e["cvd_grade"] == expect, f"{slug} 评级是 {e['cvd_grade']}，预期 {expect}"
    assert e["min_de"] >= 10.0, f"{slug} 最小 ΔE00 只有 {e['min_de']}"


def test_hue_coverage_has_no_big_hole():
    """58 套签名色沿色相环铺开后，最大空洞不得超过 25°。

    增补前最大空洞是 h 188->239 的 51°（miku 的青碧之后直接跳到 rei 的粉蓝），
    多系列图想在青蓝区找主色时无处可选。增补后实测 19°。
    """
    from colorlib import lch
    hs = sorted(lch(ap.PALETTES[s]["colors"][0])[2] for s in ALL)
    gaps = [b - a for a, b in zip(hs, hs[1:])] + [hs[0] + 360 - hs[-1]]
    assert max(gaps) <= 25.0, f"最大色相空洞 {max(gaps):.0f}°"


def test_no_c_grade_among_new_palettes():
    """新增的 22 套一个 C 级都不该有 —— C 级意味着 6 色在红/绿色盲下并团，
    只能退回安全子集。老库里有 3 套 C 是角色本身同色系，新增的没有这个包袱。"""
    new = set(NEW_ANIME) | set(NEW_GAME_1) | set(NEW_GAME_2)
    bad = {s for s in new if ap.PALETTES[s]["cvd_grade"] == "C"}
    assert not bad, f"新增配色里有 C 级：{bad}"
```

- [ ] **Step 2: 跑测试确认失败**

```bash
python -m pytest tests/test_palettes.py::test_palette_count -q
```

预期：FAIL，`assert 51 == 58`

- [ ] **Step 3: 往 data.py 追加 7 条记录**

```python
    # 黄组末尾（nekomata-neon 之后）
    dict(slug="robin-goldfeather", zh="知更鸟", en="Robin", tone_zh="金羽", tone_en="Gold Feather",
         family="黄", source="崩坏：星穹铁道",
         colors=["#D9B45A", "#EBD8A4", "#8E6E28", "#4A5A8C", "#C46E8C", "#DCD8CC"]),

    # 青组末尾（rem-peacock 之后）
    dict(slug="jiyan-windteal", zh="忌炎", en="Jiyan", tone_zh="风主青", tone_en="Windborne Teal",
         family="青", source="鸣潮",
         colors=["#2E8C8C", "#7FC0BC", "#1E5A5E", "#C4A45A", "#5A5A66", "#DCE0DC"]),

    # 蓝组末尾（ichika-leoneed 之后）
    dict(slug="saber-knightblue", zh="阿尔托莉雅", en="Artoria", tone_zh="骑士蓝金", tone_en="Knight Blue",
         family="蓝", source="Fate/Grand Order",
         colors=["#3E5FA8", "#8CA4D0", "#26386E", "#D4B45A", "#C8CCD4", "#4A4E56"]),

    # 紫组末尾（violet-evergarden 之后）
    dict(slug="yinlin-violetgold", zh="吟霖", en="Yinlin", tone_zh="紫金雷", tone_en="Violet Gold",
         family="紫", source="鸣潮",
         colors=["#7A4A9E", "#B08CC8", "#4A2A64", "#D4B45A", "#3E4A6E", "#E0DCE4"]),
    dict(slug="amiya-originium", zh="阿米娅", en="Amiya", tone_zh="源石紫", tone_en="Originium Violet",
         family="紫", source="明日方舟",
         colors=["#5A4FA8", "#9A90D0", "#342C6E", "#D4B048", "#5E7A9E", "#DEDCE6"]),

    # 中性组末尾（tarnished-gilded 之后）
    dict(slug="texas-inkgray", zh="德克萨斯", en="Texas", tone_zh="冷墨灰", tone_en="Cold Ink Gray",
         family="中性", source="明日方舟",
         colors=["#3E4A5E", "#8A94A4", "#2A3240", "#C4C8CE", "#7A5A4A", "#5A6E8C"]),
    dict(slug="hollowknight-pale", zh="小骑士", en="The Knight", tone_zh="骨白深渊", tone_en="Pale Abyss",
         family="中性", source="空洞骑士",
         colors=["#C8C4B4", "#E4E0D2", "#8A8878", "#3A404E", "#3E8CA8", "#7A5F4A"]),
```

- [ ] **Step 4: 重新调优（约 65s）**

```bash
make tune && git diff --stat src/tuned.py
```

- [ ] **Step 5: 重新生成全部产物并检查发散色标**

```bash
make all
cd src && python -c "
import json
lib = json.load(open('library.json'))
for e in lib:
    if e['div_note'] == 'derived':
        print(e['slug'], '发散色标走了单色系派生分支，检查一下是否需要 DIVERGING_OVERRIDE')
" ; cd ..
```

`pick_diverging()` 会自动挑色相最对立的两色（要求相差 ≥80°、彩度 ≥16，冷色在低值端）。
只有找不到合格对子时才落到 `derived` 分支。上面的命令列出走了该分支的 slug；
若新增配色里出现，去 `src/data.py` 的 `DIVERGING_OVERRIDE` 里手动指定两端下标（**下标是 `data.py` 里的原始顺序**），然后重跑 `make all`。

- [ ] **Step 6: 跑测试确认通过**

```bash
python -m pytest tests/ -q
```

- [ ] **Step 7: 提交**

```bash
git add -A
git commit -m "增补 7 套游戏配色（二）：吟霖 / 忌炎 / 阿米娅 / 德克萨斯 / 知更鸟 / Saber / 小骑士

至此 58 套定型，游戏 30 : 动漫 28，IP 数从 19 增到 33，原神占比 16.7% 降到 10.3%。
最大色相空洞从 51° 收到 19°，新增的 22 套评级 A12/B10，零个 C。"
```

---

## Task 5: 把全库计数 36 更新到 58，并重算文档里的统计数字

`36` 硬编码在 15 处，`docs/USAGE.md` 里还有几个按 36 套算出来的统计量。

**Files:**
- Modify: `README.md:5,24,148,273`
- Modify: `docs/USAGE.md:5,26,77,78,150,244`
- Modify: `docs/INSTALL.md:384`
- Modify: `src/README.md:6`
- Modify: `src/gen_html.py:30,31,34,161`
- Modify: `src/gen_py.py:57`
- Modify: `src/gen_pptx.js:31`
- Modify: `src/sheet2.py:27`
- Modify: `src/gen_skill_table.py:2,32`
- Modify: `skills/anime-palettes/SKILL.md:3,25,225`

**Interfaces:**
- Consumes: Task 4 的 58 套全集
- Produces: 无新接口

- [ ] **Step 1: 算出新的统计数字，直接打印成可粘贴的整句**

```bash
cd src && python - <<'EOF'
import json
from colorlib import delta_e00, hex2lab

lib = json.load(open('library.json'))
KEYS = ('smooth', 'distinct', 'hue', 'light')


def chain(e, k):
    cs = [e['colors'][i] for i in e['orders'][k]]
    return sum(delta_e00(hex2lab(cs[i]), hex2lab(cs[i + 1])) for i in range(5))


tot = {k: round(sum(chain(e, k) for e in lib)) for k in KEYS}
n_smooth_wins = sum(1 for e in lib if min(chain(e, k) for k in KEYS) == chain(e, 'smooth'))
mono = sum(1 for e in lib if e['ramp_stats']['flow']['monotonic'])
us = sorted(e['ramp_stats']['flow']['uniformity'] for e in lib)
Ls = sorted(e['ramp_stats']['flow']['L_range'] for e in lib)
N = len(lib)

print('=== 粘贴到 docs/USAGE.md:77-78 ===')
print(f"{N} 套合计的相邻色差总和：平滑 {tot['smooth']}，明度 {tot['light']}，"
      f"色相 {tot['hue']}，区分度 {tot['distinct']}")
print(f"—— 平滑约为区分度排序的 {round(100 * tot['smooth'] / tot['distinct'])}%，"
      f"{N} 套里有 {n_smooth_wins} 套它是四者中最小的。")
print()
print('=== 粘贴到 docs/USAGE.md:150 ===')
print(f"{N} 套的 `flow` {'全部' if mono == N else f'有 {mono}/{N}'}明度单调，"
      f"明度跨度 ~{Ls[N // 2]:.0f} L\\*，感知均匀度中位数 {us[N // 2]:.2f}。")
print()
print('评级分布：', {g: sum(1 for e in lib if e['cvd_grade'] == g) for g in 'ABC'})
EOF
cd ..
```

把打印出来的两段留着，下一步直接粘贴。

- [ ] **Step 2: 批量替换计数，再手工核对**

```bash
grep -rln "36 套\|36套\|· 36\|全部 36\|收录的 36" \
  README.md docs/USAGE.md docs/INSTALL.md src/README.md \
  src/gen_html.py src/gen_py.py src/gen_pptx.js src/sheet2.py \
  src/gen_skill_table.py skills/anime-palettes/SKILL.md \
  | xargs sed -i '' 's/36 套/58 套/g; s/36套/58套/g'
grep -rn "36" README.md docs/USAGE.md docs/INSTALL.md src/README.md \
  src/gen_html.py src/gen_py.py src/gen_pptx.js src/sheet2.py \
  src/gen_skill_table.py skills/anime-palettes/SKILL.md
```

第二条命令用来人工核对：剩下的 `36` 应该只有色值、版本号一类的无关数字。
特别检查 `README.md:148` 的小标题「## 收录的 36 套」和 `docs/USAGE.md:244` 的「打印全部 36 套」。

- [ ] **Step 3: 用第 1 步打印出来的整句替换 docs/USAGE.md 的统计段**

第 1 步最后打印的两段就是可以直接粘贴的成品。把 `docs/USAGE.md:77-78`
（「36 套合计的相邻色差总和：…」那两行）和 `:150`（「36 套的 `flow` 全部明度单调…」那行）
整段换成打印出来的内容。

**不要只把行首的 36 改成 58** —— 里面每个数字都是按 36 套算的，全都变了。

- [ ] **Step 4: 更新 README 的收录表**

`README.md:148` 之后是按 family 分组的收录表。追加 22 行新配色，格式跟现有行保持一致。
表里的 HEX 从库里取，别手抄：

```bash
cd src && python -c "
import sys, os
sys.path.insert(0, '..')
import anime_palettes as ap
for s, e in ap.PALETTES.items():
    print(f\"| \`{s}\` | {e['name_zh']} | {e['source']} | {e['cvd_grade']} | \" +
          ' '.join(ap.colors(s, order='distinct')) + ' |')
" ; cd ..
```

- [ ] **Step 5: 重新生成产物与 skill**

```bash
make all && make skill
```

`make skill` 会用新的计数重写 `skills/anime-palettes/references/palettes.md`（标题里的 36 也在这一步被 `gen_skill_table.py` 改掉）。

- [ ] **Step 6: 确认 skill 打包一致性**

```bash
python src/gen_skill_table.py && git diff --quiet skills/anime-palettes/references/palettes.md \
  && echo "速查表已是最新" || echo "速查表有 diff —— make skill 没跑或跑早了"
rm -rf /tmp/skillcheck && mkdir -p /tmp/skillcheck \
  && unzip -q skills/anime-palettes.skill -d /tmp/skillcheck \
  && diff -r skills/anime-palettes /tmp/skillcheck/anime-palettes && echo ".skill 与目录一致"
```

这两条就是 CI 的 skill 关做的事，本地先过一遍。

- [ ] **Step 7: 跑全量测试并提交**

```bash
python -m pytest tests/ -q
git add -A
git commit -m "全库计数 36 -> 58，重算 USAGE 里按 36 套统计的数字

README 的收录表补上 22 行；USAGE 里相邻色差总和、flow 明度跨度与均匀度
中位数都按 58 套重算，不是照着旧数字改个前缀。"
```

---

## Task 6: 新建 `src/marks.py` 标志物数据源

58 条 `slug → (viewBox, path_d)`。这一步只建数据源和结构测试，不接 HTML。

**Files:**
- Create: `src/marks.py`
- Test: `tests/test_palettes.py`

**Interfaces:**
- Consumes: Task 4 的 58 个 slug
- Produces: `marks.MARKS: dict[str, tuple[str, str]]`，键是 slug，值是 `(viewBox, path_d)`。
  Task 7 的 `gen_html.py` 按 `MARKS[slug]` 取用。

**画法约定（必须遵守）：**
- viewBox 一律 `"0 0 24 24"`，**单条 `path`**，纯填充无描边，`fill-rule` 用默认的 nonzero
- 路径命令只用 `M L H V C S Q T A Z m l h v c s q t a z` 和数字 / 空格 / 逗号 / 小数点 / 负号
- 图形要在 24×24 内留约 2 单位边距，主体占 20×20，这样 44px 渲染时不贴边
- **只画通用物件的通用画法**，不画人物形象，不复制作品 logo / 纹章 / 族徽 / 特定图案设计

- [ ] **Step 1: 写失败测试**

在 `tests/test_palettes.py` 末尾新增：

```python
# ------------------------------------------------------------ 标志物
_MARK_CMDS = set("MLHVCSQTAZmlhvcsqtaz")
_MARK_NUMS = set("0123456789 ,.-eE")


def test_every_slug_has_a_mark():
    """标志物开关打开后，缺 mark 的卡片会露出空洞。键集合必须严格相等。"""
    import data
    import marks
    slugs = {p["slug"] for p in data.PALETTES}
    assert set(marks.MARKS) == slugs, (
        f"缺 mark：{sorted(slugs - set(marks.MARKS))}；"
        f"多余 mark：{sorted(set(marks.MARKS) - slugs)}"
    )


def test_mark_is_wellformed():
    """不要用 @parametrize 展开 —— 那会在收集阶段就 import marks，
    marks.py 还没建的时候整个测试模块都收集不起来。"""
    import marks
    for slug, (vb, d) in sorted(marks.MARKS.items()):
        parts = vb.split()
        assert len(parts) == 4, f"{slug} 的 viewBox 不是四段：{vb!r}"
        for x in parts:
            float(x)
        assert d.strip(), f"{slug} 的 path 是空的"
        assert d.lstrip()[0] in "Mm", f"{slug} 的 path 不是以 M/m 开头：{d[:12]!r}"
        bad = set(d) - _MARK_CMDS - _MARK_NUMS
        assert not bad, f"{slug} 的 path 含非法字符：{sorted(bad)}"


def test_marks_do_not_leak_into_library():
    """marks 是展示资源不是色彩数据。让它进 library.json 会破坏
    dist/anime_palettes.json 与 src/library.json 内容完全相同这条不变量。"""
    import json
    lib = json.load(open(os.path.join(_ROOT, "src", "library.json")))
    for e in lib:
        assert "mark" not in e and "path" not in e, f"{e['slug']} 的库记录里混进了标志物字段"
```

- [ ] **Step 2: 跑测试确认失败**

```bash
python -m pytest tests/test_palettes.py::test_every_slug_has_a_mark -q
```

预期：FAIL，`ModuleNotFoundError: No module named 'marks'`

- [ ] **Step 3: 建 `src/marks.py`，先放框架和 4 个样板**

```python
# -*- coding: utf-8 -*-
"""每套配色的「标志物」图形 —— 色卡库 HTML 里那个默认关闭的开关用的。
这是与 data.py 并列的第二份手写数据源，只被 gen_html.py 读，**不进 derive.py**。

画什么：角色相关的通用物件，用通用画法。祢豆子 = 竹筒，善逸 = 闪电，
龙猫 = 叶伞，初音 = 葱，马力欧 = 蘑菇，2B = 眼罩。

不画什么：人物形象，以及作品的 logo / 纹章 / 族徽 / 特定图案设计 ——
那些和角色形象一样受版权保护。艾伦画一对普通翅膀轮廓，不画「自由之翼」徽章。
本仓库 MIT 协议且发布到公开的 GitHub Pages，这条线不能越。

格式：slug -> (viewBox, path_d)
  · viewBox 一律 "0 0 24 24"，单条 path，纯填充无描边
  · 图形留约 2 单位边距，主体占 20x20，44px 渲染时不贴边
  · 路径命令只用 MLHVCSQTAZ（含小写）和数字 / 空格 / 逗号 / 小数点 / 负号
"""

VB = "0 0 24 24"

MARKS = {
    # ---- 样板：新增条目照这四个的复杂度和画法来 ----

    # 祢豆子 —— 竹筒（两道竹节的圆筒）
    "nezuko-crimson-pink": (VB, "M8 3h8v18H8Z M8 8h8v1.4H8Z M8 14.6h8V16H8Z"),

    # 我妻善逸 —— 闪电
    "zenitsu-lightning": (VB, "M13.6 2 6 13h4.6l-1.2 9 8.6-12h-5.2Z"),

    # 龙猫 —— 叶伞（一片叶子加叶柄）
    "totoro-moss-gray": (VB, "M12 3c4.4 1.6 7 5 7 8.6 0 2.4-1.6 4.4-4 4.4-3.4 0-6-3.6-6-8 0-1.8.4-3.6 1-5Z M11.4 14.6 9 22h1.6l2.2-6.8Z"),

    # 初音未来 —— 葱
    "miku-aqua": (VB, "M12 2c.7 1.6 1.1 3.2 1.1 4.8h-2.2C10.9 5.2 11.3 3.6 12 2Z M10.9 7.4h2.2v6h-2.2Z M12 13c2.6 0 4.4 1.9 4.4 4.4S14.6 22 12 22s-4.4-1.9-4.4-4.6S9.4 13 12 13Z"),
}
```

- [ ] **Step 4: 跑测试，确认样板通过结构校验但键集合仍不全**

```bash
python -m pytest "tests/test_palettes.py::test_mark_is_wellformed" -q
python -m pytest tests/test_palettes.py::test_every_slug_has_a_mark -q
```

预期：前者 4 项全过（说明格式约定成立），后者 FAIL 并列出缺的 54 个 slug。

- [ ] **Step 5: 补齐剩下 54 条**

按下表逐条画。物件已经选好，画法照 Step 3 的四个样板。

| slug | 标志物 | slug | 标志物 |
| --- | --- | --- | --- |
| `asuka-vermilion` | 驾驶舱插头 | `hutao-plum` | 梅花 |
| `ponyo-coral` | 小鱼 | `chihiro-vermilion-fern` | 蕨叶 |
| `mitsuha-twilight` | 组纽结绳 | `naruto-orange-indigo` | 漩涡纹 |
| `zhongli-amber` | 琥珀原石 | `nausicaa-sky-gold` | 滑翔翼 |
| `pikachu-lemon` | 闪电尾 | `zelda-pale-gold` | 三角力量 |
| `luigi-grass` | 水管 | `zoro-moss-ink` | 三把刀 |
| `tanjiro-ink-ember` | 炭块 | `giyu-pine` | 水波纹 |
| `venti-mint` | 竖琴 | `gojo-sky` | 眼罩布条 |
| `rei-pale-blue` | 绷带卷 | `ayaka-frost` | 折扇 |
| `ganyu-glacier` | 冰晶 | `link-champion` | 盾牌 |
| `taki-night-indigo` | 彗星 | `cloud-soldier` | 巨剑 |
| `raiden-electro` | 雷纹 | `eva01-violet-lime` | 长枪 |
| `howl-iridescent` | 星辰 | `march7-sakura-ice` | 相机 |
| `aerith-rose-sage` | 花篮 | `noface-ink-gray` | 面具 |
| `2b-achromatic` | 眼罩 | `kakashi-silver-navy` | 卷轴 |
| `mario-primary` | 蘑菇 | `luffy-red-straw` | 草帽 |
| `eren-survey-olive` | 翅膀 | `haku-river` | 水流龙纹 |
| `muichiro-mist` | 云雾 | `rem-peacock` | 流星锤 |
| `violet-evergarden` | 钢笔尖 | `nyanko-fortune` | 铃铛 |
| `rx78-trikolor` | 机甲头盔 | `ichika-leoneed` | 吉他 |
| `minori-emerald` | 麦克风 | `inkling-splat` | 墨滴 |
| `joker-phantom` | 面具 | `tarnished-gilded` | 残剑 |
| `nekomata-neon` | 猫爪 | `acheron-magenta` | 雷刃 |
| `dusk-inkvermilion` | 毛笔 | `yinlin-violetgold` | 锁链 |
| `jiyan-windteal` | 长枪 | `amiya-originium` | 源石结晶 |
| `texas-inkgray` | 雨伞 | `robin-goldfeather` | 羽毛 |
| `saber-knightblue` | 剑 | `hollowknight-pale` | 钉 |

同物件在不同套里出现时（面具、长枪、眼罩、剑）要画得能区分开 —— 无脸男的面具是圆的、
Joker 的面具是尖角的；Saber 的剑有十字护手、褪色者的是断口残剑、小骑士的钉是细长的。

- [ ] **Step 6: 跑标志物测试确认全过**

```bash
python -m pytest tests/test_palettes.py -q -k "mark"
```

预期：`test_every_slug_has_a_mark` 通过，`test_mark_is_wellformed` 58 项全过。

- [ ] **Step 7: 目视检查所有 58 个图形**

```bash
cd src && python -c "
import marks
cells = ''.join(
    f'<figure><svg viewBox=\"{vb}\" width=\"48\" height=\"48\"><path d=\"{d}\" fill=\"#2E7D6B\"/></svg>'
    f'<figcaption>{s}</figcaption></figure>'
    for s, (vb, d) in sorted(marks.MARKS.items()))
open('build/marks-preview.html','w').write(
    '<style>body{font:12px sans-serif;display:flex;flex-wrap:wrap;gap:14px}'
    'figure{margin:0;width:96px;text-align:center}figcaption{word-break:break-all}</style>' + cells)
print('wrote src/build/marks-preview.html')
" ; cd ..
open src/build/marks-preview.html
```

逐个看：有没有画糊的、超出 viewBox 的、和相邻条目撞脸的。有问题就回 Step 5 改。

- [ ] **Step 8: 提交**

```bash
git add src/marks.py tests/test_palettes.py
git commit -m "新增 src/marks.py：58 套配色的标志物图形

画角色相关的通用物件（竹筒 / 闪电 / 叶伞 / 葱 …），不画人物形象，
也不复制作品 logo 与纹章 —— 本仓库 MIT 且发布到公开 Pages，这条线不能越。

marks.py 与 data.py 并列，只被 gen_html.py 读，不进 derive.py，
免得污染 library.json 这份纯色彩数据。"
```

---

## Task 7: 把标志物接进 `gen_html.py`，默认关闭

**Files:**
- Modify: `src/gen_html.py`（DATA 构造、CSS、工具栏、卡片模板、事件、`render`）
- Test: `tests/test_palettes.py`

**Interfaces:**
- Consumes: `marks.MARKS`（Task 6）
- Produces: 无 Python 接口。HTML 内新增 `state.mark`（布尔）、`MK` 常量、`#mkbtn` 按钮。

- [ ] **Step 1: 写失败测试**

```python
def test_html_ships_marks_off_by_default():
    """标志物默认关闭。开关按钮不能带 on 类，且 MK 常量必须内嵌进单文件 HTML。"""
    import re
    html = open(os.path.join(_ROOT, "dist", "anime-palettes.html"), encoding="utf-8").read()
    assert "const MK=" in html, "标志物数据没内嵌进 HTML"
    m = re.search(r'<button id="mkbtn"[^>]*>', html)
    assert m, "找不到标志物开关按钮"
    assert "class=" not in m.group(0), f"开关默认带了类，应该是关闭态：{m.group(0)}"
    import marks
    for slug in list(marks.MARKS)[:5]:
        assert slug in html
```

- [ ] **Step 2: 跑测试确认失败**

```bash
python -m pytest tests/test_palettes.py::test_html_ships_marks_off_by_default -q
```

预期：FAIL，`标志物数据没内嵌进 HTML`

- [ ] **Step 3: 改 `src/gen_html.py`**

**3a. 顶部导入并构造 MK（在 `lib = json.load(...)` 之后）：**

```python
from marks import MARKS
```

**3b. 在 `out = HTML.replace('__DATA__', ...)` 那一行之前，加 MK 的注入。**
把文件末尾的写出改成：

```python
out = HTML.replace('__DATA__', json.dumps(DATA, ensure_ascii=False, separators=(',', ':')))
out = out.replace('__MARKS__', json.dumps(MARKS, ensure_ascii=False, separators=(',', ':')))
open('build/anime-palettes.html', 'w', encoding='utf-8').write(out)
print('wrote build/anime-palettes.html  %.0f KB' % (len(out.encode()) / 1024))
```

**3c. CSS —— 在 `.badges` 那条规则之后加：**

```css
.mark{width:44px;height:44px;flex-shrink:0;display:block}
.chead .right{display:flex;align-items:center;gap:8px}
```

**3d. 工具栏 —— 在 `<div class="seg" id="theme">` 那行之前插入开关：**

```html
   <div class="seg" id="mark"><button id="mkbtn" title="显示每套配色的标志物图形">标志物</button></div>
```

按钮**不带 `class="on"`**，这就是默认关闭。

**3e. `<script>` 里，`const DATA = __DATA__;` 之后加：**

```javascript
const MK = __MARKS__;
```

并把 `state` 初始化加上 `mark:false`：

```javascript
let state = {q:"", fam:"", grade:"", cvd:"none", view:"main", order:"smooth", mark:false};
```

**3f. 卡片模板 —— 把 `.chead` 那段改成：**

```javascript
   <div class="chead">
     <div>
       <div class="cname">${p.zh} <span class="tone">· ${p.tone}</span></div>
       <div class="cmeta">${p.en} · ${p.toneEn} &nbsp;|&nbsp; ${p.src}</div>
     </div>
     <div class="right">
     ${state.mark && MK[p.slug] ? `<svg class="mark" viewBox="${MK[p.slug][0]}" aria-hidden="true"><path d="${MK[p.slug][1]}" fill="${sim(p.c[0])}"/></svg>` : ``}
     <div class="badges">
       <span class="badge">${p.fam}</span>
       <span class="badge g${p.grade}" title="色盲友好度：A 全可分 / B 大部分 / C 建议取子集">色盲 ${p.grade}</span>
     </div>
     </div>
   </div>
```

关闭时三元表达式返回空串，**整个 svg 节点根本不进 DOM**。
填充色走 `sim()`，所以色盲模拟一开，标志物跟着色块一起变 —— 和其余元素行为一致。

**3g. 事件 —— 在 `tbtn` 那段监听器之前加：**

```javascript
document.getElementById('mkbtn').addEventListener('click',e=>{
  state.mark=!state.mark;
  e.target.classList.toggle('on',state.mark);
  render();
});
```

跟深色界面开关一样不做持久化，刷新即复位。

- [ ] **Step 4: 重新生成并跑测试**

```bash
make html
python -m pytest tests/test_palettes.py::test_html_ships_marks_off_by_default -q
```

预期：PASS。同时留意 `make html` 打印的体积，应该在 175 KB 上下。

- [ ] **Step 5: 浏览器里手工验收**

```bash
open dist/anime-palettes.html
```

逐条确认：

1. 打开时**没有**标志物，「标志物」按钮是未选中态
2. 点「标志物」→ 每张卡片右上角出现图形，颜色 = 该套签名色
3. 切到「红色盲」→ 标志物跟着变色，和左边色块的变化一致
4. 再点「标志物」关掉 → 图形消失
5. 切「深色界面」→ 标志物在深色底上仍然看得清
6. 手机宽度（浏览器调窄到 380px）→ 标志物不把卡头挤变形

- [ ] **Step 6: 跑全量测试并提交**

```bash
make all && python -m pytest tests/ -q
git add -A
git commit -m "色卡库加标志物开关，默认关闭

关闭时整个 svg 节点不进 DOM，零渲染开销；开启时填充色取签名色，
标志物本身就是一块色样。色盲模拟开着的时候它跟色块一起走 sim()，不搞特例。
不做持久化，与深色界面开关行为一致。"
```

---

## Task 8: 把 `tune.py` 的目标函数常量收进 profile

`propose.py` 要用不同权重跑出不同取向的方案，所以先把写死的常量参数化。
**默认 profile 必须让现有 58 套的调优结果逐位不变** —— 这是整个任务最重要的约束。

**Files:**
- Modify: `src/tune.py`
- Test: `tests/test_palettes.py`

**Interfaces:**
- Consumes: 无
- Produces:
  - `tune.Profile`：具名元组，字段 `(name, label, penalty_w, cvd_w, lmin, lmax, hue_span, chroma_hi, chroma_lo, spread_w)`
  - `tune.DEFAULT: Profile` —— 与改造前逐位等价
  - `tune.PROFILES: dict[str, Profile]` —— 键为 `"A" "B" "C" "D" "E"`
  - `tune.tune(colors, mono=False, seed=7, iters=340, profile=None) -> (hexes, worst_normal, worst_cvd)`
    `profile=None` 时用 `DEFAULT`；`mono=True` 时把 `lmin/lmax` 换成 `MONO_LMIN/MONO_LMAX`。

- [ ] **Step 1: 写失败测试**

```python
# ------------------------------------------------------------ 调优器 profile
# 抽样而不是全跑：单套调优约 1.1s，58 套要 65s，CI 三个 Python 版本就是 3 分钟。
# 全量校验放在 Task 8 的手工步骤和 CI 的 tuned.py 逐字节 diff 里，这里只挡住常见破坏。
# 抽样覆盖：MONO 两套、单色相与多色相、高彩度与低彩度、6 色差异大与小。
_PROFILE_SAMPLE = ["2b-achromatic", "noface-ink-gray", "miku-aqua",
                   "ponyo-coral", "totoro-moss-gray", "eva01-violet-lime"]


@pytest.mark.parametrize("slug", _PROFILE_SAMPLE)
def test_default_profile_reproduces_tuned_py(slug):
    """propose.py 要用不同权重跑 tune，所以把常量参数化了。

    默认 profile 必须与参数化之前逐位等价 —— 否则现有 58 套的 tuned.py 会变，
    CI 那道逐字节 diff 直接红，而且全部产物都要跟着重生成。
    """
    import data
    import tune
    import tuned
    p = next(x for x in data.PALETTES if x["slug"] == slug)
    got, _, _ = tune.tune(p["colors"], mono=slug in data.MONO)
    assert got == tuned.TUNED[slug], (
        f"{slug} 的默认 profile 输出与 tuned.py 不一致\n"
        f"  tuned.py: {tuned.TUNED[slug]}\n"
        f"  重算:     {got}"
    )


def test_profiles_are_five_and_named():
    import tune
    assert sorted(tune.PROFILES) == ["A", "B", "C", "D", "E"]
    for k, pf in tune.PROFILES.items():
        assert pf.label, f"profile {k} 没有中文标签"


@pytest.mark.parametrize("key", ["A", "B", "C", "D", "E"])
def test_every_profile_produces_six_valid_hexes(key):
    import tune
    cols = ["#4FA8DE", "#9CD2F0", "#2A6BA5", "#1F2430", "#B9C4D0", "#EAF2F8"]
    out, wn, wc = tune.tune(cols, profile=tune.PROFILES[key])
    assert len(out) == 6 and len(set(out)) == 6
    for c in out:
        assert len(c) == 7 and c[0] == "#"
        int(c[1:], 16)
    assert wn > 0 and wc > 0


def test_profile_a_stays_closer_to_source_than_profile_b():
    """A 是「忠于原作」、B 是「区分度优先」。A 的平均偏移必须比 B 小，
    否则这两个方案给用户的选择就是假的。"""
    import tune
    from colorlib import delta_e00, hex2lab
    cols = ["#4FA8DE", "#9CD2F0", "#2A6BA5", "#1F2430", "#B9C4D0", "#EAF2F8"]

    def drift(key):
        out, _, _ = tune.tune(cols, profile=tune.PROFILES[key])
        return sum(delta_e00(hex2lab(a), hex2lab(b)) for a, b in zip(cols, out)) / 6

    assert drift("A") < drift("B")
```

- [ ] **Step 2: 跑测试确认失败**

```bash
python -m pytest tests/test_palettes.py::test_profiles_are_five_and_named -q
```

预期：FAIL，`AttributeError: module 'tune' has no attribute 'PROFILES'`

- [ ] **Step 3: 改 `src/tune.py`**

在 `LMIN, LMAX = 30.0, 78.0` 之后插入：

```python
from collections import namedtuple

Profile = namedtuple("Profile", "name label penalty_w cvd_w lmin lmax "
                                "hue_span chroma_hi chroma_lo spread_w")

# 默认：与参数化之前的写死常量逐位等价。改这里会让 tuned.py 整体变化，
# CI 的逐字节 diff 会红 —— 要动之前先想清楚。
DEFAULT = Profile("default", "默认", 0.55, 0.65, LMIN, LMAX, 7.0, 1.20, 0.45, 0.0)

PROFILES = {
    # 偏离惩罚拉高 3 倍、色相几乎焊死 —— 色值基本不动
    "A": Profile("faithful", "忠于原作", 1.60, 0.65, LMIN, LMAX, 2.0, 1.20, 0.45, 0.0),
    # 惩罚压到一半以下、明度窗口放宽 —— 换取最大的两两色差
    "B": Profile("distinct", "区分度优先", 0.25, 0.65, 26.0, 82.0, 7.0, 1.30, 0.40, 0.0),
    # 色盲项权重拉到 2.5 倍 —— 冲 grade A
    "C": Profile("cvdsafe", "色盲友好", 0.55, 1.60, LMIN, LMAX, 7.0, 1.20, 0.45, 0.0),
    # 加明度间距项 —— 灰度打印下也能靠深浅区分
    "D": Profile("grayscale", "灰度打印", 0.45, 0.40, 28.0, 80.0, 7.0, 1.20, 0.45, 1.10),
    # 压彩度上限、抬明度下限 —— 适合大面积填充与背景
    "E": Profile("soft", "柔和低饱和", 0.55, 0.65, 42.0, 84.0, 7.0, 0.85, 0.40, 0.0),
}
```

把 `_min_pair`、`_penalty`、`score`、`tune` 改成吃 profile。注意 `_penalty` 的分母 `9.0 / 16.0 / 2.5`
和 `_edge_penalty` 的阈值保持不变，只有权重和范围来自 profile：

```python
def _spread(cur):
    """明度间距项：6 个 L* 排序后相邻间隔的最小值。越大灰度下越好分。"""
    Ls = sorted(t[0] for t in cur)
    return min(b - a for a, b in zip(Ls, Ls[1:]))


def score(cur, orig, lmin, lmax, pf=DEFAULT):
    hexes = [lch2hex(*t) for t in cur]
    s, wn, wc = _min_pair(hexes, pf.cvd_w)
    s = s - pf.penalty_w * _penalty(cur, orig) - _edge_penalty(hexes, lmin, lmax)
    if pf.spread_w:
        s += pf.spread_w * _spread(cur)
    return s, wn, wc


def tune(colors, mono=False, seed=7, iters=340, profile=None):
    pf = profile or DEFAULT
    rng = random.Random(seed)
    lmin, lmax = (MONO_LMIN, MONO_LMAX) if mono else (pf.lmin, pf.lmax)
    orig = [lab2lch(hex2lab(c)) for c in colors]

    def clamp(t, o):
        L, C, h = t
        L = max(lmin, min(lmax, L))
        cmax = max(o[1] * pf.chroma_hi, 6.0)
        cmin = min(o[1] * pf.chroma_lo, o[1])
        C = max(cmin, min(cmax, C))
        dh = (h - o[2] + 180) % 360 - 180
        dh = max(-pf.hue_span, min(pf.hue_span, dh))
        return (L, C, (o[2] + dh) % 360)
    ...
```

`tune` 函数体里剩下的部分只需把 `score(...)` 的调用都补上 `pf`，其余一行不动
（`restart` 循环、`step` 衰减、`rng` 调用顺序都必须原样保留，否则默认输出会变）。

`_min_pair` 的签名从 `weight_cvd=0.65` 改成位置参数 `_min_pair(hexes, cvd_w=0.65)`，默认值保持 `0.65`。

- [ ] **Step 4: 跑回归测试确认默认输出没变**

先跑抽样版（约 7s）：

```bash
python -m pytest tests/test_palettes.py::test_default_profile_reproduces_tuned_py -q
```

再手工跑一次全量 58 套（约 65s，只在这个任务里跑一次，不进测试套件）：

```bash
cd src && python -c "
import data, tune, tuned
bad = []
for p in data.PALETTES:
    got, _, _ = tune.tune(p['colors'], mono=p['slug'] in data.MONO)
    if got != tuned.TUNED[p['slug']]:
        bad.append(p['slug'])
print('全部一致' if not bad else '不一致：' + ', '.join(bad))
" ; cd ..
```

预期：抽样 PASS，全量打印「全部一致」。
**任何一个红了都说明改动破坏了默认行为，必须回到 Step 3 排查，不要往下走。**

常见踩坑：`rng` 的调用次数或顺序变了、`_spread` 在 `spread_w=0` 时仍被调用并影响了浮点累加、
`clamp` 里 `max/min` 的嵌套顺序被改。

- [ ] **Step 5: 跑其余 profile 测试**

```bash
python -m pytest tests/test_palettes.py -q -k "profile"
```

预期：全过。若 `test_profile_a_stays_closer_to_source_than_profile_b` 红了，
调 A 的 `penalty_w` 往上、B 的往下，直到成立。

- [ ] **Step 6: 确认 tuned.py 没被动过**

```bash
git diff --quiet src/tuned.py && echo "tuned.py 未变 —— 正确" || echo "tuned.py 变了 —— 默认 profile 不等价，回 Step 3"
```

- [ ] **Step 7: 提交**

```bash
git add src/tune.py tests/test_palettes.py
git commit -m "tune.py 的目标函数常量收进 Profile，新增 5 个取向预设

propose.py 要用不同权重跑出不同取向的候选方案。默认 profile 与参数化之前
逐位等价，有专门的回归测试钉住 —— 否则 tuned.py 一变，CI 的逐字节 diff 全红。"
```

---

## Task 9: `src/propose.py` —— 五个方案 + 终端预览

**Files:**
- Modify: `src/colorlib.py`（接收从 `derive.py` 搬过来的三个函数）
- Modify: `src/derive.py:28-46`（删掉三个函数定义，改从 `colorlib` 导入）
- Create: `src/propose.py`
- Test: `tests/test_palettes.py`

**先决改动：把 `cvd_min` / `safe_set` / `grade` 从 `derive.py` 搬进 `colorlib.py`。**

`derive.py` 的模块级有指纹校验（`SOURCE != source_fingerprint()` 就 `raise SystemExit`）。
`propose.py` 如果 `from derive import grade, safe_set`，那么**只要仓库处于「改了 data.py 还没 tune」
的状态，propose.py 就连启动都启动不了** —— 而这恰恰是用户最需要它的时候。

这三个函数是纯色彩科学、只依赖 `colorlib` 自己的原语，本来就该住在 `colorlib.py`
（那里已经放着 CIEDE2000、色觉模拟、对比度）。搬过去之后 `derive.py` 从 `colorlib` 导入，
输出一字不变。

**Interfaces:**
- Consumes: `tune.PROFILES`、`tune.tune`（Task 8），`colorlib.grade` / `colorlib.safe_set`
- Produces:
  - `colorlib.cvd_min(hexes, kinds=('protan','deutan','tritan')) -> dict[str, float]`
  - `colorlib.safe_set(hexes, thr=12.0) -> list[int]`
  - `colorlib.grade(hexes) -> str`
  - `propose.Candidate`：具名元组 `(key, label, colors, min_de, cvd_de, grade, safe_n, gray_gap, drift)`
  - `propose.build(colors, mono=False) -> list[Candidate]` —— 5 个方案，顺序 A→E
  - `propose.parse_args(argv) -> argparse.Namespace`
  - `propose.ansi_row(colors) -> str`

- [ ] **Step 1: 写失败测试**

```python
# ------------------------------------------------------------ propose
_PROPOSE_DEMO = ["#4FA8DE", "#9CD2F0", "#2A6BA5", "#1F2430", "#B9C4D0", "#EAF2F8"]


def test_propose_builds_five_candidates():
    import propose
    cands = propose.build(_PROPOSE_DEMO)
    assert [c.key for c in cands] == ["A", "B", "C", "D", "E"]
    for c in cands:
        assert len(c.colors) == 6 and len(set(c.colors)) == 6
        assert c.grade in "ABC"
        assert 0 <= c.safe_n <= 6
        assert c.min_de > 0 and c.cvd_de > 0 and c.drift >= 0


def test_propose_grayscale_profile_spreads_lightness():
    """D 是灰度打印方案，它的最小明度间隔必须比忠于原作的 A 更大，
    否则这个方案名不副实。"""
    import propose
    by = {c.key: c for c in propose.build(_PROPOSE_DEMO)}
    assert by["D"].gray_gap > by["A"].gray_gap


def test_propose_rejects_bad_input():
    import propose
    with pytest.raises(SystemExit):
        propose.parse_args(["--slug", "x", "--zh", "x", "--en", "X", "--tone-zh", "x",
                            "--tone-en", "X", "--family", "蓝", "--source", "x",
                            "--colors", "#FFFFFF,#000000"])          # 只有 2 色
    with pytest.raises(SystemExit):
        propose.parse_args(["--slug", "x", "--zh", "x", "--en", "X", "--tone-zh", "x",
                            "--tone-en", "X", "--family", "不存在的色系", "--source", "x",
                            "--colors", ",".join(_PROPOSE_DEMO)])
    with pytest.raises(SystemExit):
        propose.parse_args(["--slug", "miku-aqua", "--zh", "x", "--en", "X", "--tone-zh", "x",
                            "--tone-en", "X", "--family", "蓝", "--source", "x",
                            "--colors", ",".join(_PROPOSE_DEMO)])     # slug 已存在


def test_propose_ansi_row_is_printable():
    import propose
    row = propose.ansi_row(_PROPOSE_DEMO)
    assert "\x1b[" in row and row.endswith("\x1b[0m")
```

- [ ] **Step 2: 跑测试确认失败**

```bash
python -m pytest tests/test_palettes.py::test_propose_builds_five_candidates -q
```

预期：FAIL，`ModuleNotFoundError: No module named 'propose'`

- [ ] **Step 3a: 把三个函数从 `derive.py` 搬进 `colorlib.py`**

从 `src/derive.py` 剪切 `cvd_min`、`safe_set`、`grade` 三个函数定义（连同注释），
原样粘到 `src/colorlib.py` 末尾。`colorlib.py` 里已经有 `hex2lab` / `delta_e00` / `simulate_cvd`，
所以粘过去之后只需在文件顶部确认 `import itertools` 存在。

然后把 `src/derive.py` 的导入改成：

```python
from colorlib import (hex2lab, lab2hex, delta_e00, simulate_cvd, contrast,
                      sequential, diverging, lch, lab2rgb, hex2rgb,
                      flow, cyclic, uniformize, ramp_stats,
                      cvd_min, safe_set, grade)
```

验证搬家没改变任何输出：

```bash
make derive && git diff --quiet src/library.json \
  && echo "library.json 一字未变 —— 搬家安全" || echo "library.json 变了，搬家出错了"
```

- [ ] **Step 3b: 写 `src/propose.py`**

```python
# -*- coding: utf-8 -*-
"""给自己喜欢的角色加一套配色：输入 6 个原始色，输出 5 个调色方案供挑选。

    python src/propose.py --slug my-char --zh 角色名 --en Name \
        --tone-zh 霜蓝 --tone-en Frost --family 蓝 --source 出处 \
        --colors "#4FA8DE,#9CD2F0,#2A6BA5,#1F2430,#B9C4D0,#EAF2F8"

五个方案的差别在 tune 的目标函数取向，不在色相 —— 角色的辨识度色相始终锁着。
挑好之后 `--apply B` 写回 data.py 与 tuned.py，再跑 `make all && make skill`。

零依赖，只用 stdlib 和同目录的 colorlib / tune / derive。
"""
import argparse
import itertools
import os
import sys
from collections import namedtuple

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 只依赖 colorlib，刻意不 import derive —— derive 的模块级有指纹校验，
# 仓库处于「改了 data.py 还没 tune」时会 SystemExit，而那正是最需要 propose 的时候。
from colorlib import (delta_e00, hex2lab, lch, simulate_cvd, hex2rgb,   # noqa: E402
                      grade, safe_set)
import tune as tunemod                                                  # noqa: E402

Candidate = namedtuple("Candidate",
                       "key label colors min_de cvd_de grade safe_n gray_gap drift")


def _min_pairwise(hexes, transform=lambda c: c):
    labs = [hex2lab(transform(c)) for c in hexes]
    return min(delta_e00(labs[i], labs[j])
               for i, j in itertools.combinations(range(len(hexes)), 2))


def _gray_gap(hexes):
    """排序后相邻明度间隔的最小值 —— 灰度打印能不能分开就看它。"""
    Ls = sorted(lch(c)[0] for c in hexes)
    return min(b - a for a, b in zip(Ls, Ls[1:]))


def build(colors, mono=False):
    """跑 5 个 profile，返回按 A-E 排好的候选列表。"""
    out = []
    for key in ("A", "B", "C", "D", "E"):
        pf = tunemod.PROFILES[key]
        hexes, _, _ = tunemod.tune(colors, mono=mono, profile=pf)
        cvd = min(_min_pairwise(hexes, lambda c: simulate_cvd(c, 'protan')),
                  _min_pairwise(hexes, lambda c: simulate_cvd(c, 'deutan')))
        drift = sum(delta_e00(hex2lab(a), hex2lab(b))
                    for a, b in zip(colors, hexes)) / len(colors)
        out.append(Candidate(
            key=key, label=pf.label, colors=hexes,
            min_de=round(_min_pairwise(hexes), 1),
            cvd_de=round(cvd, 1),
            grade=grade(hexes),
            safe_n=len(safe_set(hexes)),
            gray_gap=round(_gray_gap(hexes), 1),
            drift=round(drift, 1),
        ))
    return out


def ansi_row(colors):
    """一行 24 位真彩色块。终端不支持真彩时会退化成近似色，不影响判断。"""
    cells = "".join("\x1b[48;2;%d;%d;%dm      " % hex2rgb(c) for c in colors)
    return cells + "\x1b[0m"


def _report(cands, colors):
    print("原始色  ", ansi_row(colors))
    print()
    print(f"{'':4}{'方案':<12}{'minΔE':>7}{'色盲ΔE':>8}{'级':>3}{'安全':>6}{'灰度间隔':>9}{'偏移':>7}")
    for c in cands:
        print(f"{c.key:<4}{c.label:<12}{c.min_de:7.1f}{c.cvd_de:8.1f}"
              f"{c.grade:>3}{c.safe_n:>4}/6{c.gray_gap:9.1f}{c.drift:7.1f}")
    print()
    for c in cands:
        print(f"{c.key} {c.label}")
        print(f"   正常   {ansi_row(c.colors)}")
        print(f"   红色盲 {ansi_row([simulate_cvd(x, 'protan') for x in c.colors])}")
        print(f"   灰度   {ansi_row([_gray(x) for x in c.colors])}")
        print("   " + " ".join(c.colors))
        print()
    print("偏移 = 相对原始色的平均 ΔE00，越小越忠于原作。")
    print("挑好之后：python src/propose.py ...（同样参数）--apply <方案字母>")


def _gray(hexcode):
    from colorlib import lab2hex
    L = lch(hexcode)[0]
    return lab2hex((L, 0.0, 0.0))


def parse_args(argv):
    ap = argparse.ArgumentParser(
        prog="propose.py", description="给新角色生成 5 个调色方案")
    ap.add_argument("--slug", required=True, help="小写连字符，如 my-char")
    ap.add_argument("--zh", required=True, help="中文角色名")
    ap.add_argument("--en", required=True, help="英文角色名")
    ap.add_argument("--tone-zh", required=True, help="中文色调标签，如 霜蓝")
    ap.add_argument("--tone-en", required=True, help="英文色调标签，如 Frost Blue")
    ap.add_argument("--family", required=True, help="色系标签")
    ap.add_argument("--source", required=True, help="出处作品")
    ap.add_argument("--colors", required=True, help="6 个 HEX，逗号分隔")
    ap.add_argument("--mono", action="store_true", help="单色相配色，放宽明度范围")
    ap.add_argument("--html", action="store_true", help="额外生成对比预览页")
    ap.add_argument("--apply", metavar="ABCDE", help="选定方案并写回 data.py / tuned.py")
    a = ap.parse_args(argv)

    import data
    if a.family not in data.FAMILY_ORDER:
        ap.error(f"--family 只能是 {data.FAMILY_ORDER} 之一，收到 {a.family!r}")
    if a.slug in {p["slug"] for p in data.PALETTES}:
        ap.error(f"slug {a.slug!r} 已存在")

    cs = [c.strip().upper() for c in a.colors.split(",") if c.strip()]
    if len(cs) != 6:
        ap.error(f"--colors 需要正好 6 个 HEX，收到 {len(cs)} 个")
    for c in cs:
        if len(c) != 7 or c[0] != "#":
            ap.error(f"{c!r} 不是 #RRGGBB 形式")
        try:
            int(c[1:], 16)
        except ValueError:
            ap.error(f"{c!r} 不是合法的 HEX")
    if len(set(cs)) != 6:
        ap.error("6 个色里有重复")
    if a.apply and a.apply.upper() not in "ABCDE":
        ap.error("--apply 只能是 A / B / C / D / E")
    a.colors = cs
    return a


def main(argv=None):
    a = parse_args(argv if argv is not None else sys.argv[1:])
    for c in a.colors:
        L = lch(c)[0]
        lo, hi = (20, 86) if a.mono else (30, 78)
        if not lo <= L <= hi:
            print(f"提示：{c} 的 L*={L:.0f} 在可用窗口 [{lo}, {hi}] 之外，"
                  f"tune 会把它拽回来，保真度会下降。", file=sys.stderr)
    cands = build(a.colors, mono=a.mono)
    _report(cands, a.colors)
    return cands, a


if __name__ == "__main__":
    main()
```

- [ ] **Step 4: 跑测试确认通过**

```bash
python -m pytest tests/test_palettes.py -q -k "propose"
```

预期：全过。若 `test_propose_grayscale_profile_spreads_lightness` 红了，
把 profile D 的 `spread_w` 从 `1.10` 往上调，重跑。

- [ ] **Step 5: 手工跑一遍看输出好不好读**

```bash
cd src && python propose.py --slug test-char --zh 测试 --en Test \
  --tone-zh 霜蓝 --tone-en Frost --family 蓝 --source 测试 \
  --colors "#4FA8DE,#9CD2F0,#2A6BA5,#1F2430,#B9C4D0,#EAF2F8" ; cd ..
```

确认：5 个方案的色块能看出差别、表格对齐、`#1F2430`（L=15）触发窗口提示。

- [ ] **Step 6: 提交**

```bash
git add src/propose.py tests/test_palettes.py
git commit -m "新增 src/propose.py：给新角色一次生成 5 个调色方案

忠于原作 / 区分度优先 / 色盲友好 / 灰度打印 / 柔和低饱和，
每个都附 minΔE00、色盲ΔE、评级、安全子集、灰度间隔和相对原色的平均偏移 ——
把「忠于原作」量化，不靠感觉挑。终端 ANSI 真彩打三行预览，零依赖。"
```

---

## Task 10: `propose.py --html` 对比预览页

**Files:**
- Modify: `src/propose.py`
- Test: `tests/test_palettes.py`

**Interfaces:**
- Consumes: `propose.build`（Task 9）、`colorlib.sequential` / `flow` / `diverging` / `cyclic`
- Produces: `propose.render_html(cands, colors, meta) -> str`

预览页**只依赖 `colorlib` 自渲染，不读 `library.json`** —— 全新 clone 上没跑过 `make derive` 也能用。

- [ ] **Step 1: 写失败测试**

```python
def test_propose_html_is_selfcontained():
    import propose
    cands = propose.build(_PROPOSE_DEMO)
    meta = dict(slug="test-char", zh="测试", en="Test", tone_zh="霜蓝",
                tone_en="Frost", family="蓝", source="测试")
    html = propose.render_html(cands, _PROPOSE_DEMO, meta)
    assert html.lstrip().startswith("<!DOCTYPE html>")
    assert "http://" not in html and "https://" not in html, "预览页不许引外部资源"
    for c in cands:
        assert c.label in html
        for x in c.colors:
            assert x in html
    assert html.count("linear-gradient") >= len(cands) * 4, "每个方案要有 4 条色标"
```

- [ ] **Step 2: 跑测试确认失败**

```bash
python -m pytest tests/test_palettes.py::test_propose_html_is_selfcontained -q
```

预期：FAIL，`AttributeError: module 'propose' has no attribute 'render_html'`

- [ ] **Step 3: 往 `src/propose.py` 加 `render_html`**

在 `parse_args` 之前插入：

```python
def _ramps(cs):
    """四条色标，直接用 colorlib 现算，不读 library.json ——
    这样全新 clone 上没跑过 make derive 也能用这个预览页。"""
    from colorlib import sequential, flow, diverging, cyclic, uniformize, lch as _lch
    sig = cs[0]
    warm = [c for c in cs if _lch(c)[1] >= 16]
    lo, hi = (warm[-1], warm[0]) if len(warm) >= 2 else (cs[-1], cs[0])
    return [("seq", uniformize(sequential(sig, 64))),
            ("flow", flow(cs, 64)),
            ("div", diverging(lo, hi, 64)),
            ("cyclic", cyclic(cs, 64))]


def _grad(seq):
    n = len(seq)
    stops = ",".join(f"{c} {i * 100 / (n - 1):.1f}%" for i, c in enumerate(seq))
    return f"linear-gradient(90deg,{stops})"


def render_html(cands, colors, meta):
    """5 个方案并排 + 每个的 4 条色标。单文件，不引任何外部资源。"""
    head = (
        "<!DOCTYPE html>\n<html lang=\"zh-CN\"><head><meta charset=\"utf-8\">"
        "<meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">"
        f"<title>{meta['zh']} · {meta['tone_zh']} —— 5 个调色方案</title><style>"
        "body{font:14px/1.6 system-ui,-apple-system,'PingFang SC',sans-serif;"
        "background:#f6f6f4;color:#1d1d21;margin:0;padding:26px}"
        "h1{font-size:19px;margin:0 0 4px}.meta{color:#6c6c76;font-size:12.5px;margin-bottom:20px}"
        ".card{background:#fff;border:1px solid #e4e4e0;border-radius:10px;padding:15px;margin-bottom:14px}"
        ".hd{display:flex;justify-content:space-between;align-items:baseline;gap:12px;margin-bottom:10px}"
        ".hd b{font-size:15px}.stat{color:#6c6c76;font-size:12px;font-variant-numeric:tabular-nums}"
        ".sw{display:flex;border-radius:6px;overflow:hidden;margin-bottom:9px}"
        ".sw div{flex:1;height:52px;display:flex;align-items:flex-end;justify-content:center;"
        "font-size:10px;padding-bottom:4px;font-family:ui-monospace,monospace}"
        ".rl{display:flex;gap:8px;font-size:11px;color:#6c6c76;margin-bottom:3px}"
        ".rl span{flex:1}.rs{display:flex;gap:8px}.rs i{flex:1;height:13px;border-radius:3px}"
        "</style></head><body>")
    ink = lambda c: "#111" if lch(c)[0] > 58 else "#fff"
    parts = [head,
             f"<h1>{meta['zh']} · {meta['tone_zh']}</h1>",
             f"<div class=\"meta\">{meta['en']} · {meta['tone_en']} &nbsp;|&nbsp; "
             f"{meta['source']} &nbsp;|&nbsp; 色系 {meta['family']} &nbsp;|&nbsp; "
             f"slug <code>{meta['slug']}</code></div>",
             "<div class=\"card\"><div class=\"hd\"><b>原始取色</b>"
             "<span class=\"stat\">未调优</span></div><div class=\"sw\">",
             "".join(f"<div style=\"background:{c};color:{ink(c)}\">{c[1:]}</div>" for c in colors),
             "</div></div>"]
    for c in cands:
        parts.append(
            f"<div class=\"card\"><div class=\"hd\"><b>{c.key} · {c.label}</b>"
            f"<span class=\"stat\">minΔE₀₀ {c.min_de} · 色盲ΔE {c.cvd_de} · "
            f"{c.grade} 级 · 安全 {c.safe_n}/6 · 灰度间隔 {c.gray_gap} · 偏移 {c.drift}</span></div>"
            "<div class=\"sw\">"
            + "".join(f"<div style=\"background:{x};color:{ink(x)}\">{x[1:]}</div>" for x in c.colors)
            + "</div><div class=\"rl\">"
            + "".join(f"<span>{k}</span>" for k, _ in _ramps(c.colors))
            + "</div><div class=\"rs\">"
            + "".join(f"<i style=\"background:{_grad(v)}\"></i>" for _, v in _ramps(c.colors))
            + "</div></div>")
    parts.append("</body></html>")
    return "".join(parts)
```

在 `main()` 里 `_report(...)` 之后加：

```python
    if a.html:
        os.makedirs("build", exist_ok=True)
        meta = dict(slug=a.slug, zh=a.zh, en=a.en, tone_zh=a.tone_zh,
                    tone_en=a.tone_en, family=a.family, source=a.source)
        path = os.path.join("build", f"propose-{a.slug}.html")
        with open(path, "w", encoding="utf-8") as f:
            f.write(render_html(cands, a.colors, meta))
        print(f"预览页：src/{path}")
```

- [ ] **Step 4: 跑测试确认通过**

```bash
python -m pytest tests/test_palettes.py::test_propose_html_is_selfcontained -q
```

- [ ] **Step 5: 手工生成并看一眼**

```bash
cd src && python propose.py --slug test-char --zh 测试 --en Test \
  --tone-zh 霜蓝 --tone-en Frost --family 蓝 --source 测试 \
  --colors "#4FA8DE,#9CD2F0,#2A6BA5,#3E4A5E,#B9C4D0,#8A94A4" --html ; cd ..
open src/build/propose-test-char.html
```

确认：6 个卡片（原始 + 5 方案）、每个方案 4 条色标、体检数字对齐、页面在窄屏下不横向滚动。

- [ ] **Step 6: 提交**

```bash
git add src/propose.py tests/test_palettes.py
git commit -m "propose.py 加 --html 对比预览页

5 个方案并排，每个带 4 条色标。只用 colorlib 自渲染、不读 library.json，
全新 clone 上没跑过 make derive 也能直接用。单文件不引外部资源。"
```

---

## Task 11: `propose.py --apply` 写回 `data.py` 与 `tuned.py`

**Files:**
- Modify: `src/propose.py`
- Test: `tests/test_palettes.py`

**Interfaces:**
- Consumes: `propose.build`、`data.source_fingerprint`、`tuned.TUNED`
- Produces:
  - `propose.render_record(meta, colors) -> str` —— 一条 `data.py` 记录的源码文本
  - `propose.apply(meta, raw_colors, tuned_colors) -> None` —— 就地改写 `data.py` 与 `tuned.py`

`tune()` 逐套独立，所以只需把新 slug 的结果并进 `TUNED` 再重算指纹，单套约 1s，不用重跑 65s 全库。

- [ ] **Step 1: 写失败测试**

```python
def test_propose_render_record_is_valid_python():
    import propose
    meta = dict(slug="zzz-test", zh="测试", en="Test", tone_zh="霜蓝",
                tone_en="Frost Blue", family="蓝", source="测试作品")
    src = propose.render_record(meta, _PROPOSE_DEMO)
    ns = {}
    exec("PALETTES = [\n" + src + "\n]", ns)
    rec = ns["PALETTES"][0]
    assert rec["slug"] == "zzz-test"
    assert rec["family"] == "蓝"
    assert rec["colors"] == _PROPOSE_DEMO


def test_propose_apply_writes_importable_files(tmp_path, monkeypatch):
    """--apply 会就地改写手写源文件。在临时副本上验证写完还能 import、
    指纹对得上、且没动到别的 slug。"""
    import shutil
    src_dir = os.path.join(_ROOT, "src")
    for name in ("data.py", "tuned.py", "colorlib.py", "tune.py", "propose.py"):
        shutil.copy(os.path.join(src_dir, name), tmp_path / name)
    monkeypatch.syspath_prepend(str(tmp_path))
    monkeypatch.chdir(tmp_path)
    for m in ("data", "tuned", "propose", "tune", "colorlib"):
        sys.modules.pop(m, None)
    import propose as fresh
    import tuned as old_tuned
    before = dict(old_tuned.TUNED)

    meta = dict(slug="zzz-test", zh="测试", en="Test", tone_zh="霜蓝",
                tone_en="Frost Blue", family="蓝", source="测试作品")
    cand = fresh.build(_PROPOSE_DEMO)[0]
    fresh.apply(meta, _PROPOSE_DEMO, list(cand.colors))

    for m in ("data", "tuned"):
        sys.modules.pop(m, None)
    import data as d2
    import tuned as t2
    assert t2.SOURCE == d2.source_fingerprint(), "写完之后指纹对不上"
    assert t2.TUNED["zzz-test"] == list(cand.colors)
    assert {p["slug"] for p in d2.PALETTES} >= set(before) | {"zzz-test"}
    for k, v in before.items():
        assert t2.TUNED[k] == v, f"{k} 的调优结果被误改了"
```

- [ ] **Step 2: 跑测试确认失败**

```bash
python -m pytest tests/test_palettes.py::test_propose_render_record_is_valid_python -q
```

预期：FAIL，`AttributeError: module 'propose' has no attribute 'render_record'`

- [ ] **Step 3: 往 `src/propose.py` 加 `render_record` 和 `apply`**

```python
_HERE = os.path.dirname(os.path.abspath(__file__))


def render_record(meta, colors):
    """一条 data.py 记录的源码文本，缩进与现有记录一致（4 空格 + 续行 9 空格）。"""
    cols = ", ".join(f'"{c}"' for c in colors)
    return (
        f'    dict(slug="{meta["slug"]}", zh="{meta["zh"]}", en="{meta["en"]}", '
        f'tone_zh="{meta["tone_zh"]}", tone_en="{meta["tone_en"]}",\n'
        f'         family="{meta["family"]}", source="{meta["source"]}",\n'
        f'         colors=[{cols}]),'
    )


def apply(meta, raw_colors, tuned_colors):
    """把新配色写回 data.py 与 tuned.py。

    tune() 逐套独立，别的 slug 的调优结果不受影响，所以这里只并入新条目
    再重算指纹 —— 单套约 1s，不用重跑 65s 全库。
    """
    data_path = os.path.join(_HERE, "data.py")
    text = open(data_path, encoding="utf-8").read()
    anchor = "\n]\n\n# 每套配色的“签名色”"
    if anchor not in text:
        raise SystemExit("data.py 的结构变了，找不到 PALETTES 列表的结尾，请手动添加记录")
    text = text.replace(anchor, "\n" + render_record(meta, raw_colors) + anchor, 1)
    open(data_path, "w", encoding="utf-8").write(text)

    for m in ("data", "tuned"):
        sys.modules.pop(m, None)
    import data as _data
    import tuned as _tuned

    merged = dict(_tuned.TUNED)
    merged[meta["slug"]] = list(tuned_colors)
    tuned_path = os.path.join(_HERE, "tuned.py")
    with open(tuned_path, "w", encoding="utf-8") as f:
        f.write("# -*- coding: utf-8 -*-\n# 自动生成：科研可用性微调后的配色\n")
        f.write("# SOURCE = 生成这份结果时 data.py 的指纹，对不上就说明该重跑 `make tune` 了\n")
        f.write("SOURCE = %r\n\nTUNED = " % _data.source_fingerprint())
        f.write(repr(merged).replace("], ", "],\n  "))
        f.write("\n")

    print(f"已写入 src/data.py 与 src/tuned.py（{meta['slug']}）")
    print("接下来跑：make all && make skill")
    print("对结果不满意的话：git checkout src/data.py src/tuned.py")
```

在 `main()` 末尾、`return` 之前加：

```python
    if a.apply:
        key = a.apply.upper()
        chosen = next(c for c in cands if c.key == key)
        meta = dict(slug=a.slug, zh=a.zh, en=a.en, tone_zh=a.tone_zh,
                    tone_en=a.tone_en, family=a.family, source=a.source)
        apply(meta, a.colors, list(chosen.colors))
```

注意 `apply` 写 `tuned.py` 用的是**新 slug 追加在末尾**的 `dict` 顺序。
Python 3.7+ 的 dict 保序，所以现有条目的相对顺序不变，`git diff` 只会显示新增行。

- [ ] **Step 4: 跑测试确认通过**

```bash
python -m pytest tests/test_palettes.py -q -k "propose"
```

- [ ] **Step 5: 在真仓库上端到端演练一次，然后回滚**

```bash
cd src && python propose.py --slug demo-apply --zh 演练 --en Demo \
  --tone-zh 霜蓝 --tone-en Frost --family 蓝 --source 演练 \
  --colors "#4FA8DE,#9CD2F0,#2A6BA5,#3E4A5E,#B9C4D0,#8A94A4" --apply B ; cd ..
git diff --stat src/data.py src/tuned.py
cd src && python derive.py >/dev/null && echo "derive 通过，指纹正确" ; cd ..
git checkout src/data.py src/tuned.py src/library.json
```

预期：`git diff --stat` 显示 `data.py` +3 行、`tuned.py` 一行新增加 `SOURCE` 变化；
`derive.py` 不报指纹错误。演练完必须回滚。

- [ ] **Step 6: 确认工作区干净并提交**

```bash
git status --porcelain src/data.py src/tuned.py src/library.json
git add src/propose.py tests/test_palettes.py
git commit -m "propose.py 加 --apply：选定方案后写回 data.py 与 tuned.py

tune() 逐套独立，所以只并入新条目再重算指纹，单套约 1s，
不用为加一个角色重跑 65s 全库。写完提示跑 make all && make skill，
以及不满意时怎么 git checkout 回去。"
```

---

## Task 12: skill 侧文档

**Files:**
- Create: `skills/anime-palettes/references/add-palette.md`
- Modify: `skills/anime-palettes/SKILL.md`
- Test: `tests/test_palettes.py`

**Interfaces:**
- Consumes: Task 9–11 的 `propose.py` 命令行
- Produces: 无代码接口

- [ ] **Step 1: 写失败测试**

```python
def test_skill_documents_how_to_add_a_palette():
    ref = os.path.join(_ROOT, "skills", "anime-palettes", "references", "add-palette.md")
    assert os.path.exists(ref), "缺 references/add-palette.md"
    body = open(ref, encoding="utf-8").read()
    for must in ("propose.py", "--apply", "make tune", "make skill", "[30, 78]"):
        assert must in body, f"add-palette.md 没写到 {must!r}"
    skill = open(os.path.join(_ROOT, "skills", "anime-palettes", "SKILL.md"),
                 encoding="utf-8").read()
    assert "add-palette.md" in skill, "SKILL.md 没有指向 add-palette.md"


def test_skill_package_matches_directory():
    """.skill 是 zip 增量更新的，删过文件之后不重打包会留旧条目 —— CI 会因此红。"""
    import zipfile
    pkg = os.path.join(_ROOT, "skills", "anime-palettes.skill")
    root = os.path.join(_ROOT, "skills", "anime-palettes")
    names = {n for n in zipfile.ZipFile(pkg).namelist() if not n.endswith("/")}
    on_disk = set()
    for dirpath, _, files in os.walk(root):
        for fn in files:
            if fn == ".DS_Store":
                continue
            rel = os.path.relpath(os.path.join(dirpath, fn), os.path.dirname(root))
            on_disk.add(rel)
    assert names == on_disk, f"包内多出：{names - on_disk}；包内缺少：{on_disk - names}"
```

- [ ] **Step 2: 跑测试确认失败**

```bash
python -m pytest tests/test_palettes.py::test_skill_documents_how_to_add_a_palette -q
```

预期：FAIL，`缺 references/add-palette.md`

- [ ] **Step 3: 写 `skills/anime-palettes/references/add-palette.md`**

```markdown
# 自己加一套配色

库里 58 套没有你想要的角色？三步加进去。全程零依赖，只要 Python 3.8+。

## 1. 取 6 个色

从角色立绘里吸 6 个色：**主色 + 一个浅一档 + 一个深一档 + 2-3 个点缀色 + 一个背景/中性色**。

**最容易踩的坑：色值必须落在 `L* ∈ [30, 78]`。** 调优器会把 6 主色约束在这个窗口里
（单色相配色加 `--mono` 放宽到 `[20, 86]`），因为这 6 个色是要画进图里当数据系列的 ——
纯黑纯白当线条色没法用。

超出窗口会发生什么：

- `#1A1A1A`（L=9）→ `#404944`，不但被提亮，**色相还会甩到绿灰** —— 近中性色没有可锁的色相
- `#FFE600`（L=91）→ `#938400`，荧光黄被腰斩

所以别放纯黑纯白。真正的极暗极亮由 `derive` 自动派生的 `ink` / `bg` / `dark[]` / `light[]` 承载，
不用你操心。

第二个坑：**别放 3 个同色系的色**。红/绿色盲下它们会并成一团，评级直接掉到 C。
想要「深浅三档同色」的效果，用库里自带的 `dark[]` / `light[]` 变体，不要占用 6 主色的名额。

## 2. 生成 5 个方案挑一个

```bash
python src/propose.py --slug my-char --zh 角色名 --en Name \
    --tone-zh 霜蓝 --tone-en Frost Blue --family 蓝 --source 出处 \
    --colors "#4FA8DE,#9CD2F0,#2A6BA5,#3E4A5E,#B9C4D0,#8A94A4" --html
```

终端会打出 5 个方案的色块和体检数据，`--html` 再出一个带 4 条色标的对比页
（`src/build/propose-my-char.html`）。

| 方案 | 什么时候选它 |
| --- | --- |
| **A 忠于原作** | 角色配色本身就够分，只想要个规范化版本 |
| **B 区分度优先** | 要画 6 条线 / 6 组柱，色差最重要，能接受色值偏离原作 |
| **C 色盲友好** | 投稿有无障碍要求，或者读者群里有色觉障碍 |
| **D 灰度打印** | 黑白期刊、复印件，靠深浅而不是色相区分 |
| **E 柔和低饱和** | 大面积填充（地图、堆叠面积图）或者当背景，高饱和会刺眼 |

怎么读体检数据：

- **minΔE₀₀** —— 6 色两两最小色差。**≥ 10** 才够画多系列图，越大越好分
- **色盲ΔE** —— 红/绿色盲模拟下的最小色差。≥ 13 是 A 级，≥ 9 是 B 级
- **级** —— A 全可分 / B 大部分 / C 只能用安全子集
- **安全 n/6** —— 色盲下仍两两可分的最大子集大小
- **灰度间隔** —— 明度排序后相邻的最小间隔，灰度打印看这个
- **偏移** —— 相对你原始取色的平均 ΔE₀₀，**越小越忠于原作**

## 3. 落地

```bash
python src/propose.py ...（跟上面完全一样的参数）--apply B
make all && make skill
```

`--apply` 会把记录追加进 `src/data.py`、把选中方案并进 `src/tuned.py` 并重算指纹。
因为调优是逐套独立的，加一个角色只要约 1 秒，**不用重跑 `make tune`**（那是 65 秒）。

`make all` 重新生成全部交付物（Python 模块、HTML 色卡库、Excel、ase、gpl、PPT 主题色…），
`make skill` 更新速查表并重新打包 `.skill`。

不满意就回滚：

```bash
git checkout src/data.py src/tuned.py
```

## 常见问题

**评级出来是 C 怎么办？** 说明 6 色在色盲下并团了。先试 C 方案；还是 C 的话，
回第 1 步换掉最相近的那一两个色 —— 通常是三个同色系的色挤在一起。
库里的原则是**如实标注不粉饰**，C 级配色照样收录，只是用的时候要走 `ap.safe(slug)` 取子集。

**改了 `data.py` 里已有配色的色值怎么办？** 那必须跑 `make tune`（约 65 秒）。
漏了这步改动会完全静默失效 —— `derive.py` 读的是 `tuned.py`。不过它会检查指纹并报错退出，
`test_tuned_is_in_sync_with_data` 也会红，跑不掉。

**想加标志物图形？** 往 `src/marks.py` 加一条 `slug -> (viewBox, path_d)`。
规矩是**只画角色相关的通用物件、用通用画法**，不画人物形象，也不复制作品的
logo / 纹章 / 族徽 —— 那些和角色形象一样受版权保护。
```

- [ ] **Step 4: 往 `SKILL.md` 加一节**

在 `## 参考文件` 那一节之前插入：

```markdown
## 自己加一套配色

库里没有你要的角色，可以自己加。`python src/propose.py` 输入 6 个取色，
一次给出 5 个调色方案（忠于原作 / 区分度优先 / 色盲友好 / 灰度打印 / 柔和低饱和），
每个都附 minΔE₀₀、色盲 ΔE、评级、安全子集和相对原色的偏移量，挑一个 `--apply` 就写回库里。

完整流程、取色的两个坑、体检数据怎么读：`references/add-palette.md`
```

并在 `## 参考文件` 的列表里补一行：

```markdown
- `references/add-palette.md` —— 自己加一套配色：取色约束、5 个方案怎么选、落地与回滚
```

- [ ] **Step 5: 重新打包并跑测试**

```bash
make skill
python -m pytest tests/test_palettes.py -q -k "skill"
```

预期：两条测试都通过。

- [ ] **Step 6: 跑全量测试并提交**

```bash
python -m pytest tests/ -q
git add -A
git commit -m "skill 加自助配色文档：references/add-palette.md

写清 L* [30,78] 窗口这个最容易踩的坑（超出会被拽回来，近中性色还会被甩掉色相），
5 个方案各自的适用场景，以及 minΔE00 / 色盲ΔE / 灰度间隔 / 偏移怎么读。
顺带补两条测试：文档存在性、.skill 包与目录逐文件一致。"
```

---

## 收尾检查

全部 12 个任务做完后，跑一遍 CI 的四道关：

```bash
# 1. test 关
python -m pytest tests/ -q
python -c "import anime_palettes"                      # 零依赖可 import
python anime_palettes.py ls | head -5                  # 未安装也能跑

# 2. build 关 —— 重跑生成链路必须逐字节一致
make derive py html files
git diff --quiet anime_palettes.py dist/anime-palettes.html \
  dist/anime_palettes.csv dist/anime_palettes.json \
  && echo "build 关通过：产物可复现" || echo "build 关失败：产物不可复现"

# 3. skill 关
python src/gen_skill_table.py
git diff --quiet skills/anime-palettes/references/palettes.md \
  && echo "速查表一致" || echo "速查表有 diff"
python -c "
import json, os
mk = json.load(open('.claude-plugin/marketplace.json')) if os.path.exists('.claude-plugin/marketplace.json') else None
print('marketplace.json 不存在，跳过' if mk is None else 'marketplace 路径检查见 CI')
"

# 4. 人工验收
open dist/anime-palettes.html    # 标志物开关默认关闭，点开正常，色盲模拟联动
```

`dist/anime_palettes.xlsx`、`dist/anime-palettes-picker.pptx`、`docs/images/*.png`
内嵌创建时间戳，不参与逐字节比对，有 diff 是正常的。
