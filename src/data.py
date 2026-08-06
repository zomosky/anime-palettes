# -*- coding: utf-8 -*-
"""动漫 / 游戏角色配色库 —— 原始数据。
每套 6 主色，顺序即建议的系列使用顺序（前 3 色区分度最高）。
tone = 一眼识别的色调标签；family = 检索用色系归类。
"""

FAMILY_ORDER = ["红", "橙", "黄", "绿", "青", "蓝", "紫", "粉", "中性", "撞色"]

# 单色相配色：tune 时放宽 L* 范围，derive 时走单色相分支。
# 两处都从这里读，避免各存一份走岔。
MONO = {"noface-ink-gray", "2b-achromatic"}

PALETTES = [
    # ---------------- 红 / 绯 ----------------
    dict(slug="asuka-vermilion", zh="明日香", en="Asuka", tone_zh="朱赤", tone_en="Vermilion Red",
         family="红", source="新世纪福音战士",
         colors=["#D6402E", "#F0836E", "#9E2622", "#E09A38", "#2E3A52", "#EFDACB"]),
    dict(slug="hutao-plum", zh="胡桃", en="Hu Tao", tone_zh="绯梅", tone_en="Plum Crimson",
         family="红", source="原神",
         colors=["#C24A4A", "#E8916E", "#7A2E3E", "#3B3550", "#D9B94A", "#EBDCCE"]),
    dict(slug="ponyo-coral", zh="波妞", en="Ponyo", tone_zh="珊瑚", tone_en="Coral Red",
         family="红", source="崖上的波妞",
         colors=["#E8503C", "#F79A7E", "#B03050", "#3E8CB5", "#8ED0E0", "#F2E2CE"]),
    dict(slug="chihiro-vermilion-fern", zh="千寻", en="Chihiro", tone_zh="朱绿", tone_en="Vermilion & Fern",
         family="红", source="千与千寻",
         colors=["#C7412F", "#E8886A", "#4E7A4A", "#93AE6E", "#2E3A44", "#E9DDC9"]),

    # ---------------- 橙 / 金 ----------------
    dict(slug="mitsuha-twilight", zh="三叶", en="Mitsuha", tone_zh="暮橙", tone_en="Twilight Orange",
         family="橙", source="你的名字",
         colors=["#E8763C", "#F5A96E", "#C4487A", "#4A4E8C", "#8093D4", "#F0E0CC"]),
    dict(slug="naruto-orange-indigo", zh="鸣人", en="Naruto", tone_zh="橙靛", tone_en="Orange & Indigo",
         family="橙", source="火影忍者",
         colors=["#E87722", "#F5A85E", "#2E4A8C", "#EFC53A", "#7A94C9", "#2B2B33"]),
    dict(slug="zhongli-amber", zh="钟离", en="Zhongli", tone_zh="琥珀岩金", tone_en="Amber Geo",
         family="橙", source="原神",
         colors=["#C8912F", "#E6C67A", "#8A5A2B", "#3E3A38", "#6E7F72", "#EBDFC9"]),
    dict(slug="nausicaa-sky-gold", zh="娜乌西卡", en="Nausicaä", tone_zh="天青金", tone_en="Sky & Gold",
         family="橙", source="风之谷",
         colors=["#D9A93A", "#3E7FA8", "#8FC0D9", "#B5623A", "#5F7A5A", "#EEE8D6"]),

    # ---------------- 黄 ----------------
    dict(slug="zenitsu-lightning", zh="我妻善逸", en="Zenitsu", tone_zh="雷明黄", tone_en="Lightning Yellow",
         family="黄", source="鬼灭之刃",
         colors=["#EFB818", "#FFE58A", "#E8712E", "#B03A26", "#6E5326", "#F7EEDA"]),
    dict(slug="pikachu-lemon", zh="皮卡丘", en="Pikachu", tone_zh="柠黄", tone_en="Lemon Yellow",
         family="黄", source="宝可梦",
         colors=["#F2C61E", "#FFE97A", "#E8443A", "#7A4A22", "#2B2B2B", "#FBF1CE"]),
    dict(slug="zelda-pale-gold", zh="塞尔达", en="Zelda", tone_zh="淡金", tone_en="Pale Gold",
         family="黄", source="塞尔达传说",
         colors=["#C4A03A", "#E6D6A2", "#2F5C8A", "#7FA3C4", "#8FA88C", "#F3EFE2"]),

    # ---------------- 绿 ----------------
    dict(slug="luigi-grass", zh="路易吉", en="Luigi", tone_zh="草绿", tone_en="Grass Green",
         family="绿", source="超级马力欧",
         colors=["#3AA349", "#82D091", "#186B3C", "#2B54B0", "#E0B93A", "#E9E3D2"]),
    dict(slug="zoro-moss-ink", zh="索隆", en="Zoro", tone_zh="苔墨", tone_en="Moss & Ink",
         family="绿", source="海贼王",
         colors=["#5F8C3A", "#96BE6E", "#33502A", "#C9A227", "#2A2E2E", "#E5E1D2"]),
    dict(slug="tanjiro-ink-ember", zh="灶门炭治郎", en="Tanjiro", tone_zh="墨绿炭赤", tone_en="Ink Green & Ember",
         family="绿", source="鬼灭之刃",
         colors=["#4A6B4A", "#8FB08A", "#9E3B2A", "#D4703F", "#2A2E2A", "#E4D8C4"]),
    dict(slug="totoro-moss-gray", zh="龙猫", en="Totoro", tone_zh="苔灰", tone_en="Moss Gray",
         family="绿", source="龙猫",
         colors=["#5F6E6A", "#96A79C", "#3B4A45", "#8A7550", "#C0C8BC", "#E7E7DC"]),

    # ---------------- 青 / 薄荷 ----------------
    dict(slug="miku-aqua", zh="初音未来", en="Miku", tone_zh="青碧", tone_en="Aqua Teal",
         family="青", source="VOCALOID",
         colors=["#39C5BB", "#8CE0D8", "#127C86", "#3B4252", "#D8496B", "#E6EFEE"]),
    dict(slug="venti-mint", zh="温迪", en="Venti", tone_zh="风薄荷", tone_en="Anemo Mint",
         family="青", source="原神",
         colors=["#4EB89A", "#9BDCC6", "#2E6E62", "#3B5A6E", "#D3BE8E", "#E7F0EB"]),
    dict(slug="giyu-pine", zh="富冈义勇", en="Giyu", tone_zh="松青", tone_en="Pine Teal",
         family="青", source="鬼灭之刃",
         colors=["#2E6B63", "#7FB0A5", "#8C3A3A", "#C9A227", "#243447", "#DCE4E0"]),

    # ---------------- 蓝 ----------------
    dict(slug="gojo-sky", zh="五条悟", en="Gojo", tone_zh="晴空蓝", tone_en="Six-Eyes Sky",
         family="蓝", source="咒术回战",
         colors=["#4FA8DE", "#9CD2F0", "#2A6BA5", "#1F2430", "#B9C4D0", "#EAF2F8"]),
    dict(slug="rei-pale-blue", zh="绫波丽", en="Rei", tone_zh="苍白蓝", tone_en="Pale Blue",
         family="蓝", source="新世纪福音战士",
         colors=["#8FC0D8", "#C6DEEA", "#4A7E9E", "#C4384A", "#E8873A", "#EEF5F8"]),
    dict(slug="ayaka-frost", zh="神里绫华", en="Ayaka", tone_zh="霜蓝", tone_en="Frost Blue",
         family="蓝", source="原神",
         colors=["#6FA8DC", "#C6DEF2", "#2F5F8F", "#9E8FC4", "#D9748C", "#EFF5FA"]),
    dict(slug="ganyu-glacier", zh="甘雨", en="Ganyu", tone_zh="冰蓝", tone_en="Glacier Blue",
         family="蓝", source="原神",
         colors=["#5B7FB8", "#A9C4E4", "#2B3F66", "#8C6FB0", "#C4485A", "#E9EEF6"]),
    dict(slug="link-champion", zh="林克", en="Link", tone_zh="苍蓝", tone_en="Champion Blue",
         family="蓝", source="塞尔达传说",
         colors=["#4A7FB5", "#8FB8D9", "#D9C07A", "#8A6A4A", "#22364F", "#DEDACC"]),
    dict(slug="taki-night-indigo", zh="泷", en="Taki", tone_zh="夜靛", tone_en="Night Indigo",
         family="蓝", source="你的名字",
         colors=["#2F4A7A", "#6E8FB5", "#1B2A44", "#8FA8D0", "#C46E5A", "#E4EAF3"]),
    dict(slug="cloud-soldier", zh="克劳德", en="Cloud", tone_zh="军蓝", tone_en="Soldier Blue",
         family="蓝", source="最终幻想VII",
         colors=["#2F4A72", "#6E8CB5", "#3FA8D4", "#E0C46A", "#6B5A48", "#E5EAF1"]),

    # ---------------- 紫 ----------------
    dict(slug="raiden-electro", zh="雷电将军", en="Raiden", tone_zh="雷紫", tone_en="Electro Violet",
         family="紫", source="原神",
         colors=["#8A6FD1", "#B9A3E8", "#5A3E8C", "#3A3550", "#C86FA8", "#E9E3F5"]),
    dict(slug="eva01-violet-lime", zh="初号机", en="EVA-01", tone_zh="紫萤", tone_en="Violet & Lime",
         family="紫", source="新世纪福音战士",
         colors=["#6B3FA0", "#A182CC", "#3A2260", "#8CC63F", "#CFE38A", "#E8E2F0"]),
    # 归在「粉」：签名色 #C4548C 的 LCh 色相是 350°，落在粉区而非紫区（285-335）。
    # 物理位置仍留在「紫」分组里，是为了不打乱 PALETTES 列表顺序——
    # 顺序参与 source_fingerprint()，挪动会要求重跑 make tune（这里不需要）。
    dict(slug="howl-iridescent", zh="哈尔", en="Howl", tone_zh="金蓝虹", tone_en="Iridescent Gold",
         family="粉", source="哈尔的移动城堡",
         colors=["#C4548C", "#3E6E9E", "#D9B44A", "#7FB7D4", "#5A8C6E", "#EFE7D6"]),

    # ---------------- 粉 ----------------
    dict(slug="nezuko-crimson-pink", zh="祢豆子", en="Nezuko", tone_zh="绯粉", tone_en="Crimson Pink",
         family="粉", source="鬼灭之刃",
         colors=["#D6486B", "#F4A3BC", "#E4703C", "#8E3B5C", "#3B2430", "#F0DCC8"]),
    dict(slug="march7-sakura-ice", zh="三月七", en="March 7th", tone_zh="樱冰", tone_en="Sakura Ice",
         family="粉", source="崩坏：星穹铁道",
         colors=["#EE9CBE", "#F7CADC", "#7FC4E4", "#3E6B9E", "#B04E7E", "#F6F1F4"]),
    dict(slug="aerith-rose-sage", zh="爱丽丝", en="Aerith", tone_zh="玫粉鼠尾草", tone_en="Rose & Sage",
         family="粉", source="最终幻想VII",
         colors=["#D96E8C", "#EFA9BC", "#B03A3A", "#4E8C5A", "#6B4A32", "#F1E4E7"]),

    # ---------------- 中性 / 低饱和 ----------------
    dict(slug="noface-ink-gray", zh="无脸男", en="No-Face", tone_zh="墨灰", tone_en="Ink Gray",
         family="中性", source="千与千寻",
         colors=["#2C2C34", "#50505E", "#7C7C8C", "#A9A9B8", "#D5D5DE", "#6E5A7A"]),
    dict(slug="2b-achromatic", zh="2B", en="2B", tone_zh="素墨", tone_en="Achromatic Ink",
         family="中性", source="尼尔：机械纪元",
         colors=["#26262B", "#4E4E58", "#82828E", "#AFACA6", "#D8D3C8", "#8C7B5E"]),
    dict(slug="kakashi-silver-navy", zh="卡卡西", en="Kakashi", tone_zh="银藏", tone_en="Silver & Navy",
         family="中性", source="火影忍者",
         colors=["#8E96A0", "#C0C7CE", "#2E3A4E", "#4E6B8C", "#B04A3A", "#E6E9EC"]),

    # ---------------- 撞色 / 高对比 ----------------
    dict(slug="mario-primary", zh="马力欧", en="Mario", tone_zh="正红蓝", tone_en="Primary Red & Blue",
         family="撞色", source="超级马力欧",
         colors=["#E52521", "#2B54B0", "#EFC000", "#6B4423", "#EABF98", "#2E2E33"]),
    dict(slug="luffy-red-straw", zh="路飞", en="Luffy", tone_zh="赤麦", tone_en="Red & Straw",
         family="撞色", source="海贼王",
         colors=["#D6302B", "#E8C46A", "#2B5FA8", "#F09A4E", "#3A2E28", "#F0E6D4"]),
]

# 每套配色的“签名色”（用于生成连续 colormap）默认取第 1 色；
# 少数配色第 1 色不是最具辨识度的，在此覆盖。
SIGNATURE_OVERRIDE = {
    "nausicaa-sky-gold": 0,
    "howl-iridescent": 0,
    "mario-primary": 0,
}

# 发散型 colormap 的两端（低值端, 高值端），默认取 (colors[2], colors[0])
DIVERGING_OVERRIDE = {
    "miku-aqua": (0, 4),
    "eva01-violet-lime": (0, 3),
    "mario-primary": (1, 0),
    "naruto-orange-indigo": (2, 0),
    "zelda-pale-gold": (2, 0),
    "luigi-grass": (3, 0),
}


def source_fingerprint():
    """tune.py 实际吃进去的那部分数据（slug + 6 原始色 + 是否单色相）的指纹。

    写进 tuned.py，由 derive.py 和测试校验。没有它的话，改了上面的色值却忘了
    `make tune`，derive 照样读旧的 TUNED，全部产物一字不变、测试全绿 ——
    改动静默消失，没有任何地方会提示。
    """
    import hashlib
    payload = "\n".join(
        "{}|{}|{}".format(p["slug"], ",".join(p["colors"]), int(p["slug"] in MONO))
        for p in PALETTES
    )
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16]
