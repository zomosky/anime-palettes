# -*- coding: utf-8 -*-
"""从 library.json 重新生成 skill 的 36 套速查表（保证 HEX 永远和库一致）。
由 `make skill` 调用；也可以 `python -c "exec(open('src/gen_skill_table.py').read())"`。"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import anime_palettes as ap

FAM_HINT = {
    "红": "能量、风险、热、警示；医学与生命科学的活性组",
    "橙": "温度、成本、产量、时间演进；地学与材料",
    "黄": "辐照、光照、能量密度；需要高亮度对比时",
    "绿": "生态、农业、可持续、生物量；植被与化学",
    "青": "水文、海洋、流体、制冷；清爽干净的技术感",
    "蓝": "电力、气象、遥感、金融；最“中性专业”的默认选择",
    "紫": "电化学、量子、算法、抽象量；需要与蓝区分时",
    "粉": "生物医学染色、细胞、社会科学；柔和不刺眼",
    "中性": "灰度打印、极简排版、把颜色让位给数据本身",
    "撞色": "教学演示、海报、需要远距离辨识的场合",
}

rows = sorted(
    ((e["family"], s, e["name_zh"], e["source"], e["cvd_grade"],
      len(e["safe_set"]), " ".join(ap.colors(s, order="distinct")))
     for s, e in ap.PALETTES.items()),
    key=lambda r: (ap.FAMILIES.index(r[0]), r[1]))

out = ["# 36 套配色速查", "",
       "给 agent 挑配色用。**HEX 按「区分度优先」顺序列出**（画多系列图直接从左往右取）；",
       "要平滑色带就用 `ap.colors(slug)` 的默认顺序。", "",
       "`安全` 列 = 红/绿色盲下仍两两可分的颜色个数（满分 6）。",
       "色盲等级 A = 6 色全可分；B = 大部分；C = 角色本身同色系，多系列时**只能**用 `ap.safe(slug)`。", ""]
cur = None
for fam, slug, zh, src, grade, nsafe, hexes in rows:
    if fam != cur:
        cur = fam
        out += ["", f"## {fam}系　—　{FAM_HINT[fam]}", "",
                "| slug | 名称 | 出处 | 色盲 | 安全 | 6 主色（区分度序） |",
                "|---|---|---|---|---|---|"]
    out.append(f"| `{slug}` | {zh} | {src} | **{grade}** | {nsafe}/6 | `{hexes}` |")

out += ["", "---", "", "## 按需求快速定位", "", "| 需求 | 直接用 |", "|---|---|",
        "| 不确定用什么 / 要最稳妥 | `ganyu`（冰蓝，A 级）、`taki`（夜靛，A 级）、`cloud`（军蓝，A 级） |",
        "| 要 6 个系列且必须色盲安全 | 任一 A 级：`nausicaa` `link` `cloud` `mario` `eva01` `zhongli` `raiden` |",
        "| 灰度打印 / 黑白期刊 | `2b`（素墨）、`noface`（墨灰）、`kakashi`（银藏）—— 明度阶梯本身就是信息 |",
        "| 要低调、不抢主体 | `totoro`（苔灰）、`zhongli`（琥珀岩金）、`kakashi`（银藏） |",
        "| 要抓眼球（海报、封面、教学） | `mario`（正红蓝）、`eva01`（紫萤）、`luffy`（赤麦）、`pikachu`（柠黄） |",
        "| 冷暖对撞、需要强烈对比 | `nausicaa`（天青金）、`naruto`（橙靛）、`mitsuha`（暮橙） |",
        '| 只画 2–3 条线 | 任意一套取 `ap.colors(slug, n=3, order="distinct")` |',
        '| 热图 / 密度图 | `ap.cmap(slug, "seq")` |',
        '| 散点按连续变量着色 | `ap.cmap(slug, "flow", crop=(.10, .93))` |',
        '| 相关矩阵 / 差值图 | `ap.cmap(slug, "div")`，vmin/vmax 必须对称 |',
        '| 相位 / 角度 / 风向 / 时刻 | `ap.cmap(slug, "cyclic")` |', ""]

dst = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   "skills", "anime-palettes", "references", "palettes.md")
open(dst, "w").write("\n".join(out))
print("wrote", dst)
