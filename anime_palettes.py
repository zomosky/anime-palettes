# -*- coding: utf-8 -*-
"""anime_palettes —— 动漫/游戏角色配色库（51 套 × 6 主色）

用法
----
    import anime_palettes as ap

    ap.ls()                       # 打印全部配色（带色调标签与色盲等级）
    ap.ls(family="蓝")            # 按色系筛选
    ap.find("初音")                # 模糊搜索，中英文/slug 都行

    c = ap.colors("miku")         # 6 个主色，默认「平滑」排列
    ap.colors("miku", n=3)        # 只要前 3 个
    ap.colors("miku", order="distinct")   # 换排序：多系列图表推荐
    ap.safe("miku")               # 色盲下仍可分的推荐子集

    ap.use("miku")                # 一键设置 matplotlib 全局风格
    with ap.using("hutao"):       # 或者临时用
        ax.plot(...)

    cm  = ap.cmap("miku")          # 连续色标 seq（单色相，热图/密度图）
    ap.cmap("miku", "flow")        # 多色相连续色标 —— **散点连续着色首选**
    ap.cmap("miku", "div")         # 发散色标（相关系数、差值图）
    ap.cmap("miku", "cyclic")      # 环形色标（相位、角度、风向、时刻）
    ap.cmap("miku", "flow_r")      # 反向；crop=(0.05,0.9) 可裁掉太浅/太深的两端

    ap.preview("miku")             # 六联示意图
    ap.wheel("miku")               # 色环：看这套色的色相/彩度分布
    ap.wheel_all()                 # 36 套一起看
    ap.scatter_guide("miku")       # 散点图四种配色策略的对照

四种排序（order 参数，各函数通用）：
  "smooth"   相邻色差最小的路径，过渡最顺滑 —— **默认**，色带/装饰/配图协调用
  "distinct" 区分度优先，前几色差异最大 —— **画多系列折线、柱状、散点时用这个**
  "hue"      色相环顺序 红→橙→黄→绿→青→蓝→紫
  "light"    明度由浅到深，也最适合灰度打印

配色三档色盲友好度：A = 红/绿色盲下 6 色全部可分；B = 大部分可分；
C = 角色本身就是同色系，建议只用 ap.safe() 给出的子集。
"""
from __future__ import annotations

__version__ = "1.0"

PALETTES = {
  "asuka-vermilion": {
    "slug": 'asuka-vermilion',
    "zh": '明日香',
    "en": 'Asuka',
    "tone_zh": '朱赤',
    "tone_en": 'Vermilion Red',
    "name_zh": '明日香 · 朱赤',
    "name_en": 'Asuka · Vermilion Red',
    "family": '红',
    "source": '新世纪福音战士',
    "kind": 'cat',
    "colors": ['#E63B2A', '#8D1316', '#3B4760', '#BFB6B0', '#FF9C88', '#DF9730'],
    "dark": ['#B40009', '#570000', '#18263D', '#978E88', '#D37461', '#B17100'],
    "light": ['#FF8168', '#AF5044', '#656D82', '#EAE3DE', '#FFDBD3', '#FFC887'],
    "bg": '#FFF2EF',
    "bg2": '#FBDFD9',
    "ink": '#55231A',
    "muted": '#9A7D76',
    "seq": ['#FFF4F2', '#FFEAE5', '#FFDED7', '#FFD2C8', '#FFC4B6', '#FFB3A3', '#FFA490', '#FD917B', '#F97F68', '#F36B53', '#ED563F', '#E73D2C', '#D73022', '#C6231A', '#B51411', '#9D0E0D', '#840E0A', '#6C0D06', '#6C0D06'],
    "div": ['#3C4251', '#4D5568', '#5E6881', '#727C95', '#8791A9', '#9EA7BC', '#B8BDCE', '#D0D3DE', '#E7E8ED', '#F3E7DC', '#EFCEAC', '#E5B57F', '#D59C56', '#C18431', '#AA6F1A', '#935C00', '#784B02', '#5E3A02', '#5E3A02'],
    "flow": ['#F9E8DD', '#FADFCE', '#FCD6C0', '#FDCAAF', '#FFBD9F', '#FFB08E', '#FCA478', '#F69862', '#F08E4A', '#E88331', '#E67629', '#E46823', '#E2591F', '#E04A1D', '#DD3D23', '#D73B32', '#CF3B3E', '#C53D49', '#B94053', '#AA445A', '#9A495F', '#8A4C61', '#7B4E61', '#6F505F', '#684D59', '#66434D', '#633A41', '#5F3133', '#5A2A26', '#592922'],
    "cyclic": ['#E87364', '#E27957', '#DA7E4B', '#CF8540', '#C48B39', '#B69034', '#A89633', '#979B36', '#83A03F', '#6AA44D', '#4AA860', '#0CAB76', '#00A98C', '#00A89E', '#00A6AD', '#00A5BD', '#00A3CF', '#009FE3', '#379AF3', '#6395F2', '#7F90ED', '#978AE7', '#AD83DE', '#C37BD0', '#D674BE', '#E46EA7', '#EB6C90', '#EC6E7C', '#E9726A', '#E87364'],
    "wheel": [{'i': 0, 'L': 52.0, 'C': 80.9, 'h': 37.6}, {'i': 1, 'L': 29.9, 'C': 58.6, 'h': 34.0}, {'i': 2, 'L': 30.1, 'C': 16.4, 'h': 277.6}, {'i': 3, 'L': 74.6, 'C': 4.7, 'h': 63.1}, {'i': 4, 'L': 74.1, 'C': 43.6, 'h': 37.0}, {'i': 5, 'L': 68.0, 'C': 64.2, 'h': 73.1}],
    "ramp_stats": {'seq': {'L_range': 75.1, 'L_min': 21.9, 'L_max': 97.0, 'monotonic': True, 'total_dE': 92.6, 'uniformity': 0.68}, 'div': {'L_range': 67.7, 'L_min': 27.9, 'L_max': 95.6, 'monotonic': False, 'total_dE': 155.1, 'uniformity': 0.667}, 'flow': {'L_range': 70.0, 'L_min': 23.1, 'L_max': 93.0, 'monotonic': True, 'total_dE': 125.9, 'uniformity': 0.705}, 'cyclic': {'L_range': 0.5, 'L_min': 61.7, 'L_max': 62.3, 'monotonic': True, 'total_dE': 184.8, 'uniformity': 0.773}},
    "cvd_grade": 'B',
    "safe_set": [0, 1, 2, 4],
    "orders": {'smooth': [0, 1, 2, 3, 4, 5], 'distinct': [0, 4, 1, 5, 2, 3], 'hue': [1, 4, 0, 5, 2, 3], 'light': [3, 4, 5, 0, 2, 1]},
    "min_de": 20.6,
    "cvd": {'protan': 11.5, 'deutan': 11.5, 'tritan': 4.8},
  },
  "hutao-plum": {
    "slug": 'hutao-plum',
    "zh": '胡桃',
    "en": 'Hu Tao',
    "tone_zh": '绯梅',
    "tone_en": 'Plum Crimson',
    "name_zh": '胡桃 · 绯梅',
    "name_en": 'Hu Tao · Plum Crimson',
    "family": '红',
    "source": '原神',
    "kind": 'cat',
    "colors": ['#C74E4D', '#792C3D', '#49435F', '#DE9476', '#BCB6AF', '#D5B326'],
    "dark": ['#9B232B', '#52011D', '#27223C', '#B36D50', '#948E87', '#A88C00'],
    "light": ['#E7837D', '#9A5A65', '#706A81', '#FFC5AD', '#E8E3DD', '#FFE083'],
    "bg": '#FCF3F2',
    "bg2": '#F4E1DF',
    "ink": '#4D2826',
    "muted": '#947F7D',
    "seq": ['#FFF4F3', '#FDE8E6', '#FBDBD8', '#F7CBC7', '#F3BCB7', '#EFADA7', '#E89A94', '#E18781', '#D97670', '#D16460', '#C95351', '#BE4847', '#B13F3F', '#A33537', '#942D2F', '#812729', '#702223', '#601E1E', '#601E1E'],
    "div": ['#444050', '#575267', '#6B6580', '#7F7894', '#948DA8', '#A9A3BB', '#C0BBCE', '#D5D2DE', '#EAE8ED', '#F0E8DA', '#E5D2A6', '#D5BC75', '#C0A548', '#AA8F1E', '#937A0F', '#7C6700', '#665300', '#504100', '#504100'],
    "flow": ['#F5E9DB', '#F7E4CD', '#F8DEBE', '#FAD9AD', '#FBD198', '#FBC881', '#FABE66', '#F8B455', '#F3AB5A', '#EFA35E', '#E79B63', '#E19467', '#D78D6A', '#D48263', '#D1765A', '#CE6A52', '#CB5E4C', '#C7544A', '#BE5251', '#B45157', '#A9505C', '#9C5060', '#8D5061', '#7F5061', '#73505E', '#694D5A', '#61434E', '#5A3A42', '#513137', '#4E2E33'],
    "cyclic": ['#DE7689', '#DE7879', '#DB7C6C', '#D58061', '#CF8458', '#C58950', '#BB8E4B', '#B09348', '#A29748', '#939C4C', '#81A054', '#6BA361', '#51A772', '#2FA883', '#00A995', '#00A7A4', '#00A6B2', '#00A4C0', '#00A2D1', '#239FDF', '#539AE2', '#6F96E0', '#8591DD', '#988CD8', '#AA87D0', '#BC81C4', '#CC7CB5', '#D777A2', '#DD768F', '#DE7689'],
    "wheel": [{'i': 0, 'L': 49.7, 'C': 54.7, 'h': 28.2}, {'i': 1, 'L': 29.9, 'C': 35.8, 'h': 11.4}, {'i': 2, 'L': 30.1, 'C': 18.2, 'h': 300.7}, {'i': 3, 'L': 68.0, 'C': 36.7, 'h': 48.0}, {'i': 4, 'L': 74.3, 'C': 4.4, 'h': 78.6}, {'i': 5, 'L': 73.9, 'C': 69.5, 'h': 90.8}],
    "ramp_stats": {'seq': {'L_range': 75.0, 'L_min': 22.0, 'L_max': 97.0, 'monotonic': True, 'total_dE': 92.7, 'uniformity': 0.685}, 'div': {'L_range': 67.6, 'L_min': 28.0, 'L_max': 95.7, 'monotonic': False, 'total_dE': 153.8, 'uniformity': 0.649}, 'flow': {'L_range': 69.9, 'L_min': 23.0, 'L_max': 92.9, 'monotonic': True, 'total_dE': 113.8, 'uniformity': 0.683}, 'cyclic': {'L_range': 0.5, 'L_min': 61.8, 'L_max': 62.3, 'monotonic': True, 'total_dE': 169.1, 'uniformity': 0.749}},
    "cvd_grade": 'B',
    "safe_set": [0, 1, 2, 3, 4, 5],
    "orders": {'smooth': [0, 1, 2, 3, 4, 5], 'distinct': [0, 3, 1, 2, 5, 4], 'hue': [1, 0, 3, 5, 2, 4], 'light': [4, 5, 3, 0, 2, 1]},
    "min_de": 20.0,
    "cvd": {'protan': 12.5, 'deutan': 12.5, 'tritan': 8.8},
  },
  "ponyo-coral": {
    "slug": 'ponyo-coral',
    "zh": '波妞',
    "en": 'Ponyo',
    "tone_zh": '珊瑚',
    "tone_en": 'Coral Red',
    "name_zh": '波妞 · 珊瑚',
    "name_en": 'Ponyo · Coral Red',
    "family": '红',
    "source": '崖上的波妞',
    "kind": 'cat',
    "colors": ['#ED3124', '#A12044', '#FDA083', '#8C867E', '#92BFCA', '#2284B1'],
    "dark": ['#B50009', '#6D0026', '#D1785C', '#666059', '#6A97A2', '#005D82'],
    "light": ['#FF826A', '#C05D6E', '#FFDDD2', '#B5B0AA', '#C7EAF3', '#72ACD1'],
    "bg": '#FFF2EF',
    "bg2": '#FCDFD8',
    "ink": '#572218',
    "muted": '#9C7D76',
    "seq": ['#FFF4F2', '#FFEAE5', '#FFDFD8', '#FFD2C9', '#FFC6B9', '#FFB8A8', '#FFA794', '#FE9580', '#FC826B', '#F96C54', '#F4553F', '#EF3A2A', '#E0281E', '#CD1A15', '#BA080C', '#A20208', '#880305', '#700401', '#700401'],
    "div": ['#2E464B', '#3A5A61', '#466E77', '#5B828B', '#7197A0', '#8DACB4', '#AAC2C8', '#C7D6DB', '#E3EAEC', '#F6E5E1', '#FDC7BB', '#FFA795', '#FF836A', '#FA5B43', '#E43E2C', '#CC1E18', '#A51F16', '#7F1D13', '#7F1D13'],
    "flow": ['#FFE6DE', '#FFDDCA', '#FAD8BA', '#ECD5B5', '#DCD0B0', '#CCCCAE', '#BFC3A8', '#BEB89D', '#BDAF96', '#BBA48E', '#B89A89', '#BD917D', '#C5876D', '#CF7A5D', '#D9694D', '#E2533F', '#EB3136', '#EC133D', '#E3164C', '#D71F5B', '#C82B68', '#B53772', '#A03F78', '#8A4679', '#764B76', '#6B476A', '#693D59', '#633347', '#5B2A35', '#592830'],
    "cyclic": ['#E47385', '#E37674', '#DF7967', '#D97E5B', '#D18350', '#C78948', '#BC8E43', '#AE9340', '#A09840', '#909D46', '#7BA14F', '#63A55E', '#44A871', '#06AA84', '#00A896', '#00A7A5', '#00A6B4', '#00A4C4', '#00A2D4', '#159EE7', '#5199E9', '#7094E7', '#878FE3', '#9C8ADC', '#B084D4', '#C37EC6', '#D377B4', '#DE739F', '#E4728B', '#E47385'],
    "wheel": [{'i': 0, 'L': 52.2, 'C': 86.9, 'h': 37.5}, {'i': 1, 'L': 36.0, 'C': 54.6, 'h': 12.9}, {'i': 2, 'L': 74.6, 'C': 43.2, 'h': 43.2}, {'i': 3, 'L': 56.2, 'C': 5.2, 'h': 81.5}, {'i': 4, 'L': 74.6, 'C': 16.1, 'h': 220.2}, {'i': 5, 'L': 51.9, 'C': 33.6, 'h': 249.7}],
    "ramp_stats": {'seq': {'L_range': 74.9, 'L_min': 22.1, 'L_max': 97.0, 'monotonic': True, 'total_dE': 91.9, 'uniformity': 0.686}, 'div': {'L_range': 67.8, 'L_min': 28.0, 'L_max': 95.7, 'monotonic': False, 'total_dE': 152.4, 'uniformity': 0.676}, 'flow': {'L_range': 69.9, 'L_min': 23.2, 'L_max': 93.1, 'monotonic': True, 'total_dE': 149.0, 'uniformity': 0.742}, 'cyclic': {'L_range': 0.5, 'L_min': 61.7, 'L_max': 62.3, 'monotonic': True, 'total_dE': 176.0, 'uniformity': 0.759}},
    "cvd_grade": 'A',
    "safe_set": [0, 1, 2, 3, 4, 5],
    "orders": {'smooth': [0, 1, 2, 3, 4, 5], 'distinct': [0, 2, 1, 5, 4, 3], 'hue': [1, 0, 2, 4, 5, 3], 'light': [2, 4, 3, 0, 5, 1]},
    "min_de": 22.1,
    "cvd": {'protan': 16.9, 'deutan': 17.7, 'tritan': 17.7},
  },
  "chihiro-vermilion-fern": {
    "slug": 'chihiro-vermilion-fern',
    "zh": '千寻',
    "en": 'Chihiro',
    "tone_zh": '朱绿',
    "tone_en": 'Vermilion & Fern',
    "name_zh": '千寻 · 朱绿',
    "name_en": 'Chihiro · Vermilion & Fern',
    "family": '红',
    "source": '千与千寻',
    "kind": 'cat',
    "colors": ['#C6402E', '#FD9E81', '#BBB6AD', '#7FA054', '#536950', '#394855'],
    "dark": ['#990A0B', '#D1765A', '#938E85', '#58792E', '#30452E', '#172733'],
    "light": ['#E77863', '#FFDBD0', '#E7E3DB', '#B0C98C', '#7E907C', '#626E79'],
    "bg": '#FDF3F0',
    "bg2": '#F7E1DC',
    "ink": '#50271F',
    "muted": '#977E79',
    "seq": ['#FFF4F2', '#FEE9E4', '#FDDDD6', '#FBCFC5', '#F8C0B3', '#F4B1A2', '#F0A392', '#EB9380', '#E4816C', '#DC6F5A', '#D35D48', '#CB4B38', '#C03C2B', '#B23324', '#A2281C', '#8F2117', '#781E14', '#641B11', '#641B11'],
    "div": ['#394537', '#495946', '#596D56', '#6D816A', '#82967F', '#9AAB97', '#B4C2B2', '#CDD6CC', '#E6EAE5', '#F7E5DF', '#FDC7BA', '#FCA997', '#F38A75', '#E56C56', '#D05440', '#B83E2C', '#953426', '#732A1F', '#732A1F'],
    "flow": ['#F2EADB', '#F0E3CB', '#EDDAB8', '#E8D2A4', '#E4C88E', '#DBBF7A', '#CDBD73', '#BDBA6D', '#ACB869', '#9AB567', '#85B167', '#6FAE69', '#65A657', '#5F9C41', '#5C9329', '#598906', '#4C8414', '#3E8129', '#317D38', '#277845', '#23734D', '#256D55', '#2D6758', '#366159', '#385A58', '#335254', '#314950', '#304149', '#2F3A43', '#2F3840'],
    "cyclic": ['#D08170', '#CC8467', '#C5885F', '#BC8D59', '#B29156', '#A79555', '#9B9957', '#8D9C5B', '#7EA063', '#6FA26C', '#5AA57B', '#45A68A', '#2CA798', '#05A7A7', '#00A6B4', '#00A4C1', '#24A2CD', '#489ED3', '#629AD6', '#7796D5', '#8992D2', '#998DCD', '#A889C7', '#B784BC', '#C580AF', '#CF7D9F', '#D47C8E', '#D47E80', '#D28074', '#D08170'],
    "wheel": [{'i': 0, 'L': 46.8, 'C': 65.9, 'h': 37.6}, {'i': 1, 'L': 74.1, 'C': 44.1, 'h': 42.9}, {'i': 2, 'L': 74.2, 'C': 5.2, 'h': 88.2}, {'i': 3, 'L': 61.9, 'C': 43.4, 'h': 124.5}, {'i': 4, 'L': 42.0, 'C': 17.7, 'h': 139.9}, {'i': 5, 'L': 29.8, 'C': 10.0, 'h': 256.0}],
    "ramp_stats": {'seq': {'L_range': 74.9, 'L_min': 22.1, 'L_max': 97.0, 'monotonic': True, 'total_dE': 91.9, 'uniformity': 0.682}, 'div': {'L_range': 67.9, 'L_min': 27.8, 'L_max': 95.7, 'monotonic': False, 'total_dE': 152.1, 'uniformity': 0.689}, 'flow': {'L_range': 69.9, 'L_min': 23.0, 'L_max': 92.9, 'monotonic': True, 'total_dE': 130.7, 'uniformity': 0.689}, 'cyclic': {'L_range': 0.5, 'L_min': 61.8, 'L_max': 62.3, 'monotonic': True, 'total_dE': 155.4, 'uniformity': 0.678}},
    "cvd_grade": 'C',
    "safe_set": [0, 1, 5],
    "orders": {'smooth': [0, 1, 2, 3, 4, 5], 'distinct': [0, 1, 4, 3, 5, 2], 'hue': [0, 1, 3, 4, 2, 5], 'light': [2, 1, 3, 0, 4, 5]},
    "min_de": 22.2,
    "cvd": {'protan': 8.9, 'deutan': 10.5, 'tritan': 10.4},
  },
  "dusk-inkvermilion": {
    "slug": 'dusk-inkvermilion',
    "zh": '夕',
    "en": 'Dusk',
    "tone_zh": '墨朱',
    "tone_en": 'Ink & Vermilion',
    "name_zh": '夕 · 墨朱',
    "name_en": 'Dusk · Ink & Vermilion',
    "family": '红',
    "source": '明日方舟',
    "kind": 'cat',
    "colors": ['#8E2736', '#C46A6A', '#566269', '#719DA9', '#BCB7AD', '#C9A54A'],
    "dark": ['#610018', '#9A4346', '#333F45', '#4A7682', '#948F85', '#9E7E20'],
    "light": ['#AF5B60', '#E69B99', '#808A90', '#A5C7D1', '#E8E4DB', '#F3D18A'],
    "bg": '#FBF3F3',
    "bg2": '#F2E1E1',
    "ink": '#4A292B',
    "muted": '#927F7F',
    "seq": ['#FFF4F4', '#F8E3E3', '#F3D5D5', '#EBC3C3', '#E2B0B0', '#DBA2A3', '#D39293', '#CB8385', '#C27476', '#B96569', '#B2575D', '#A8484F', '#9D3642', '#922E3B', '#872835', '#7A2430', '#6A232B', '#5C2127', '#5C2127'],
    "div": ['#2F464C', '#3B5A62', '#466E78', '#5B828C', '#7197A1', '#8DACB5', '#AAC2C8', '#C7D6DB', '#E3EAEC', '#F1E6E6', '#EFCBCA', '#E8B0AE', '#DA9493', '#CA7B7A', '#B66565', '#A05051', '#814242', '#643434', '#643434'],
    "flow": ['#F2EADB', '#EDE3C8', '#E4DDB3', '#D5D69C', '#C1D086', '#AACD7F', '#95CA8A', '#83C596', '#76C0A1', '#6EBAA9', '#6DB2AE', '#72A9AF', '#6DA2B1', '#649BB6', '#6293BA', '#698BBC', '#7383BB', '#7E7BB7', '#8973B0', '#9569A7', '#81669C', '#6F638E', '#615E80', '#56586F', '#545065', '#56485D', '#583E52', '#593542', '#562D32', '#542B2D'],
    "cyclic": ['#D77C80', '#D57E73', '#D08268', '#CA865F', '#C18A58', '#B88F53', '#AE9351', '#A29751', '#959B54', '#849E5C', '#71A266', '#5CA575', '#44A784', '#26A894', '#00A8A3', '#00A6B0', '#00A5BD', '#00A3CC', '#34A0D5', '#559BD9', '#6E97D9', '#8293D7', '#938FD3', '#A48ACD', '#B485C2', '#C380B6', '#CE7CA6', '#D57B95', '#D77B84', '#D77C80'],
    "wheel": [{'i': 0, 'L': 32.9, 'C': 46.9, 'h': 20.3}, {'i': 1, 'L': 55.2, 'C': 39.1, 'h': 24.3}, {'i': 2, 'L': 40.8, 'C': 6.3, 'h': 241.9}, {'i': 3, 'L': 62.1, 'C': 16.2, 'h': 223.0}, {'i': 4, 'L': 74.6, 'C': 5.7, 'h': 90.1}, {'i': 5, 'L': 69.3, 'C': 51.0, 'h': 86.6}],
    "ramp_stats": {'seq': {'L_range': 75.0, 'L_min': 22.0, 'L_max': 97.0, 'monotonic': True, 'total_dE': 90.3, 'uniformity': 0.732}, 'div': {'L_range': 67.8, 'L_min': 27.9, 'L_max': 95.7, 'monotonic': False, 'total_dE': 147.7, 'uniformity': 0.723}, 'flow': {'L_range': 69.9, 'L_min': 23.0, 'L_max': 92.9, 'monotonic': True, 'total_dE': 154.3, 'uniformity': 0.692}, 'cyclic': {'L_range': 0.5, 'L_min': 61.8, 'L_max': 62.3, 'monotonic': True, 'total_dE': 159.4, 'uniformity': 0.69}},
    "cvd_grade": 'A',
    "safe_set": [0, 1, 2, 3, 4, 5],
    "orders": {'smooth': [0, 1, 2, 3, 4, 5], 'distinct': [0, 1, 2, 5, 3, 4], 'hue': [0, 1, 5, 3, 4, 2], 'light': [4, 5, 3, 1, 2, 0]},
    "min_de": 20.2,
    "cvd": {'protan': 15.8, 'deutan': 15.8, 'tritan': 15.3},
  },
  "mitsuha-twilight": {
    "slug": 'mitsuha-twilight',
    "zh": '三叶',
    "en": 'Mitsuha',
    "tone_zh": '暮橙',
    "tone_en": 'Twilight Orange',
    "name_zh": '三叶 · 暮橙',
    "name_en": 'Mitsuha · Twilight Orange',
    "family": '橙',
    "source": '你的名字',
    "kind": 'cat',
    "colors": ['#CB5C21', '#F4A665', '#BDB5AD', '#8093D4', '#474B89', '#C75681'],
    "dark": ['#9C3600', '#C87E3E', '#958D85', '#576DAC', '#1E2A64', '#9D2B5C'],
    "light": ['#EE8E5F', '#FFDEC5', '#E8E2DB', '#B2BEF3', '#7473A7', '#E68BAA'],
    "bg": '#FDF3EF',
    "bg2": '#F5E1D9',
    "ink": '#4C2A18',
    "muted": '#957F76',
    "seq": ['#FFF4EF', '#FEE9DF', '#FCDCCD', '#FACFBC', '#F6C0A7', '#F2B192', '#EDA17C', '#E69268', '#DF8152', '#D6713E', '#CE6229', '#C1551B', '#B44C14', '#A5420A', '#943802', '#823003', '#6F2902', '#5E2200', '#5E2200'],
    "div": ['#374163', '#455380', '#53669F', '#697AB3', '#7F8FC6', '#99A5D5', '#B4BCE2', '#CED2EC', '#E7E8F4', '#F2E6E2', '#EECDB7', '#E4B490', '#D59B6D', '#C3834D', '#AD6D36', '#965920', '#7A491C', '#5F3918', '#5F3918'],
    "flow": ['#FFE6D5', '#FFDCC4', '#FAD1B7', '#ECC8B4', '#DDC0B1', '#DCB8AB', '#DEB0A7', '#E0A8A6', '#E09FA7', '#DE97AB', '#D990B1', '#D28AB8', '#CE83B9', '#D375AC', '#D9689D', '#DC5B8C', '#DE4D7A', '#DE4068', '#D73A62', '#C93A68', '#BA3B6D', '#A93C70', '#973E71', '#853F70', '#733F6D', '#623E69', '#533C62', '#45395B', '#393652', '#35344E'],
    "cyclic": ['#D78054', '#CF854B', '#C48B43', '#B8903E', '#AA953D', '#9A9A3F', '#889F46', '#72A352', '#57A763', '#31A976', '#00A98B', '#00A89C', '#00A7AB', '#00A5BA', '#00A3CA', '#00A0DD', '#369CEB', '#5F97EB', '#7A92E8', '#8F8DE3', '#A487DB', '#B881D1', '#CB7AC1', '#DA74AD', '#E37198', '#E67284', '#E57472', '#E07964', '#D97E57', '#D78054'],
    "wheel": [{'i': 0, 'L': 52.4, 'C': 66.2, 'h': 51.8}, {'i': 1, 'L': 74.5, 'C': 50.1, 'h': 63.6}, {'i': 2, 'L': 74.1, 'C': 5.3, 'h': 74.4}, {'i': 3, 'L': 61.8, 'C': 36.7, 'h': 285.0}, {'i': 4, 'L': 34.3, 'C': 38.7, 'h': 294.5}, {'i': 5, 'L': 52.3, 'C': 49.4, 'h': 358.2}],
    "ramp_stats": {'seq': {'L_range': 74.9, 'L_min': 22.0, 'L_max': 96.9, 'monotonic': True, 'total_dE': 93.6, 'uniformity': 0.712}, 'div': {'L_range': 67.8, 'L_min': 27.9, 'L_max': 95.7, 'monotonic': False, 'total_dE': 147.5, 'uniformity': 0.711}, 'flow': {'L_range': 70.0, 'L_min': 22.9, 'L_max': 92.9, 'monotonic': True, 'total_dE': 124.1, 'uniformity': 0.698}, 'cyclic': {'L_range': 0.5, 'L_min': 61.8, 'L_max': 62.3, 'monotonic': True, 'total_dE': 178.0, 'uniformity': 0.763}},
    "cvd_grade": 'A',
    "safe_set": [0, 1, 2, 3, 4, 5],
    "orders": {'smooth': [0, 1, 2, 3, 4, 5], 'distinct': [0, 1, 5, 4, 3, 2], 'hue': [0, 1, 3, 4, 5, 2], 'light': [1, 2, 3, 0, 5, 4]},
    "min_de": 20.3,
    "cvd": {'protan': 15.5, 'deutan': 15.7, 'tritan': 5.6},
  },
  "naruto-orange-indigo": {
    "slug": 'naruto-orange-indigo',
    "zh": '鸣人',
    "en": 'Naruto',
    "tone_zh": '橙靛',
    "tone_en": 'Orange & Indigo',
    "name_zh": '鸣人 · 橙靛',
    "name_en": 'Naruto · Orange & Indigo',
    "family": '橙',
    "source": '火影忍者',
    "kind": 'cat',
    "colors": ['#D16409', '#DCB300', '#D4A986', '#7A94C9', '#324D90', '#46464C'],
    "dark": ['#9B4400', '#AD8C00', '#AA815F', '#516EA1', '#002C67', '#25252B'],
    "light": ['#F59656', '#FFE198', '#FBD7BA', '#ADBFEA', '#6774AC', '#6C6C71'],
    "bg": '#FDF3EE',
    "bg2": '#F6E1D6',
    "ink": '#4C2A13',
    "muted": '#957F73',
    "seq": ['#FFF4EE', '#FFE9DD', '#FEDECB', '#FCD0B7', '#F9C1A0', '#F5B187', '#EFA16F', '#E89157', '#E0813F', '#D87024', '#CD6208', '#BD5805', '#AC4F02', '#9C4501', '#8B3D01', '#7B3502', '#6A2D02', '#5A2500', '#5A2500'],
    "div": ['#533E2C', '#6B4F38', '#846143', '#997557', '#AE8A6D', '#C1A187', '#D3B9A5', '#E3D0C3', '#F0E7E1', '#F9E5D9', '#FCC9AB', '#F7AD7F', '#EA9157', '#D97632', '#C2611B', '#AA4C00', '#8A3F03', '#6C3204', '#6C3204'],
    "flow": ['#FFE9B9', '#FFDCA4', '#FBCF9C', '#F0C49E', '#E6BA9F', '#E7B19D', '#E6A89E', '#E3A0A1', '#DF98A6', '#D691AC', '#CA8CB3', '#CF7FAB', '#D76F9C', '#DD5F8A', '#E24F76', '#E43F62', '#E33250', '#DB305C', '#D03269', '#C23775', '#B13D7E', '#9E4384', '#8A4988', '#764C86', '#644E83', '#544973', '#484362', '#3F3D52', '#383845', '#363640'],
    "cyclic": ['#D4824C', '#CB8744', '#C08D3E', '#B3923A', '#A4973A', '#949C3E', '#80A147', '#67A556', '#47A869', '#04AA7D', '#00A991', '#00A8A2', '#00A6B1', '#00A4C0', '#00A2D2', '#009EE7', '#4799EE', '#6994EC', '#828FE8', '#998AE2', '#AE84D9', '#C27DCB', '#D475B9', '#E171A3', '#E76F8D', '#E8727B', '#E5756A', '#DF7A5B', '#D7804F', '#D4824C'],
    "wheel": [{'i': 0, 'L': 54.8, 'C': 72.7, 'h': 57.7}, {'i': 1, 'L': 74.5, 'C': 76.8, 'h': 88.9}, {'i': 2, 'L': 72.3, 'C': 26.4, 'h': 65.5}, {'i': 3, 'L': 61.2, 'C': 30.5, 'h': 278.0}, {'i': 4, 'L': 34.0, 'C': 42.1, 'h': 287.3}, {'i': 5, 'L': 29.9, 'C': 3.8, 'h': 290.9}],
    "ramp_stats": {'seq': {'L_range': 74.9, 'L_min': 21.9, 'L_max': 96.9, 'monotonic': True, 'total_dE': 92.9, 'uniformity': 0.69}, 'div': {'L_range': 67.7, 'L_min': 28.0, 'L_max': 95.7, 'monotonic': False, 'total_dE': 151.6, 'uniformity': 0.737}, 'flow': {'L_range': 70.1, 'L_min': 23.0, 'L_max': 93.0, 'monotonic': True, 'total_dE': 141.6, 'uniformity': 0.733}, 'cyclic': {'L_range': 0.5, 'L_min': 61.8, 'L_max': 62.3, 'monotonic': True, 'total_dE': 180.4, 'uniformity': 0.753}},
    "cvd_grade": 'A',
    "safe_set": [0, 1, 2, 3, 4, 5],
    "orders": {'smooth': [0, 1, 2, 3, 4, 5], 'distinct': [0, 2, 4, 1, 3, 5], 'hue': [0, 2, 1, 3, 4, 5], 'light': [1, 2, 3, 0, 4, 5]},
    "min_de": 19.6,
    "cvd": {'protan': 16.6, 'deutan': 14.4, 'tritan': 4.6},
  },
  "zhongli-amber": {
    "slug": 'zhongli-amber',
    "zh": '钟离',
    "en": 'Zhongli',
    "tone_zh": '琥珀岩金',
    "tone_en": 'Amber Geo',
    "name_zh": '钟离 · 琥珀岩金',
    "name_en": 'Zhongli · Amber Geo',
    "family": '橙',
    "source": '原神',
    "kind": 'cat',
    "colors": ['#B37C00', '#D3B46A', '#BBB6AC', '#6E7F72', '#4A4644', '#895829'],
    "dark": ['#835900', '#A88C43', '#938E84', '#4A5A4D', '#292523', '#613504'],
    "light": ['#DBA857', '#FDE1A6', '#E7E3DA', '#9AA89D', '#706C6B', '#AF825C'],
    "bg": '#FAF4EE',
    "bg2": '#EFE4D6',
    "ink": '#422F12',
    "muted": '#8E8273',
    "seq": ['#FEF5EA', '#F9E9D5', '#F3DCBF', '#EDCEA8', '#E5BF8E', '#DCB175', '#D2A25B', '#C79440', '#BC8622', '#AE7800', '#A06E00', '#926400', '#855A00', '#785100', '#6A4702', '#5E3E02', '#523701', '#493000', '#493000'],
    "div": ['#5A3D01', '#724E01', '#8C6000', '#A37319', '#BA882F', '#CE9F54', '#E0B77D', '#EDCFA8', '#F5E7D5', '#E5EAEA', '#BDD7E6', '#95C4DF', '#6EAFD1', '#459AC0', '#2985AB', '#007095', '#025C7A', '#034860', '#034860'],
    "flow": ['#FEE9BF', '#F1DEB9', '#E6D4B5', '#D9CAAF', '#D0C0A6', '#D1BB97', '#D2B485', '#D2AD71', '#D2A55A', '#D29C40', '#D19120', '#C2902A', '#B48E34', '#A78C3D', '#9B8846', '#90844F', '#878057', '#807D5D', '#7B775A', '#7A7050', '#796846', '#78613E', '#775A36', '#77522F', '#704A2D', '#64442E', '#583F2F', '#4D3A2F', '#43362F', '#40352F'],
    "cyclic": ['#C28A58', '#B98E54', '#B09251', '#A49651', '#979A54', '#889E59', '#76A163', '#63A470', '#4CA67F', '#32A78F', '#0AA89F', '#00A6AC', '#00A5BA', '#00A3C8', '#26A0D4', '#4F9CD8', '#6997D9', '#7E94D7', '#908FD4', '#A18BCE', '#B186C5', '#C181B8', '#CD7DA8', '#D57B97', '#D87B87', '#D67D78', '#D3806D', '#CD8462', '#C5895B', '#C28A58'],
    "wheel": [{'i': 0, 'L': 56.1, 'C': 63.4, 'h': 78.2}, {'i': 1, 'L': 74.5, 'C': 41.7, 'h': 87.6}, {'i': 2, 'L': 74.2, 'C': 5.7, 'h': 90.1}, {'i': 3, 'L': 51.5, 'C': 10.2, 'h': 150.9}, {'i': 4, 'L': 30.0, 'C': 2.2, 'h': 55.1}, {'i': 5, 'L': 41.9, 'C': 38.1, 'h': 65.8}],
    "ramp_stats": {'seq': {'L_range': 74.9, 'L_min': 22.1, 'L_max': 96.9, 'monotonic': True, 'total_dE': 99.1, 'uniformity': 0.727}, 'div': {'L_range': 67.6, 'L_min': 28.1, 'L_max': 95.7, 'monotonic': False, 'total_dE': 152.8, 'uniformity': 0.725}, 'flow': {'L_range': 69.9, 'L_min': 23.1, 'L_max': 93.1, 'monotonic': True, 'total_dE': 124.7, 'uniformity': 0.705}, 'cyclic': {'L_range': 0.5, 'L_min': 61.7, 'L_max': 62.2, 'monotonic': True, 'total_dE': 160.3, 'uniformity': 0.732}},
    "cvd_grade": 'A',
    "safe_set": [0, 1, 2, 3, 4, 5],
    "orders": {'smooth': [0, 1, 2, 3, 4, 5], 'distinct': [0, 1, 5, 4, 3, 2], 'hue': [5, 0, 1, 2, 3, 4], 'light': [1, 2, 0, 3, 5, 4]},
    "min_de": 17.4,
    "cvd": {'protan': 15.6, 'deutan': 15.4, 'tritan': 14.3},
  },
  "nausicaa-sky-gold": {
    "slug": 'nausicaa-sky-gold',
    "zh": '娜乌西卡',
    "en": 'Nausicaä',
    "tone_zh": '天青金',
    "tone_en": 'Sky & Gold',
    "name_zh": '娜乌西卡 · 天青金',
    "name_en": 'Nausicaä · Sky & Gold',
    "family": '橙',
    "source": '风之谷',
    "kind": 'cat',
    "colors": ['#B38708', '#BDB7A6', '#82BFDD', '#3176A0', '#6A7668', '#7D2D02'],
    "dark": ['#856200', '#958F7E', '#5797B4', '#005176', '#465144', '#461700'],
    "light": ['#DDB25D', '#E9E4D6', '#C1E9FF', '#729EC0', '#959F93', '#A15B39'],
    "bg": '#F9F4EE',
    "bg2": '#EEE4D6',
    "ink": '#3F3011',
    "muted": '#8D8272',
    "seq": ['#FDF5EA', '#F8EAD6', '#F3E0C3', '#ECD4AE', '#E5C897', '#DDBC81', '#D3AE66', '#C8A04B', '#BD932D', '#B18508', '#A27A05', '#957003', '#876401', '#795A00', '#6C4F01', '#5E4502', '#523C02', '#453200', '#453200'],
    "div": ['#24455C', '#2A5978', '#2F6D94', '#4981A9', '#6396BC', '#83ABCC', '#A3C2DB', '#C3D6E7', '#E2EAF2', '#EFE8DD', '#E7D0AB', '#DAB97C', '#C8A153', '#B38B2D', '#9C7618', '#856300', '#6C5100', '#553F00', '#553F00'],
    "flow": ['#F0EBDB', '#E1E5D0', '#D0E0C9', '#BBDBC6', '#A6D6C8', '#92D0CD', '#72CCC4', '#4DC8B5', '#1AC3A2', '#00BB8A', '#00B27E', '#00AA89', '#00A391', '#009A95', '#239196', '#448891', '#56818A', '#50788A', '#4D7089', '#4F6887', '#536183', '#58597D', '#5E5175', '#64496A', '#68405B', '#68394A', '#64343A', '#5D302C', '#552E20', '#522E1D'],
    "cyclic": ['#C4886C', '#BE8B65', '#B78E61', '#AF925E', '#A6955E', '#9B985F', '#8F9C63', '#819F6A', '#72A173', '#62A380', '#51A48D', '#42A59A', '#35A5A7', '#2FA4B3', '#35A2BD', '#46A0C6', '#5A9DCB', '#6C99CD', '#7C95CC', '#8B92CA', '#998FC6', '#A78BC0', '#B487B6', '#C083AA', '#C8819C', '#CC808E', '#CD8282', '#CA8477', '#C6876E', '#C4886C'],
    "wheel": [{'i': 0, 'L': 58.9, 'C': 63.1, 'h': 83.6}, {'i': 1, 'L': 74.5, 'C': 9.4, 'h': 95.1}, {'i': 2, 'L': 74.3, 'C': 24.3, 'h': 240.6}, {'i': 3, 'L': 47.2, 'C': 29.9, 'h': 255.2}, {'i': 4, 'L': 48.3, 'C': 9.6, 'h': 139.9}, {'i': 5, 'L': 30.0, 'C': 52.4, 'h': 51.1}],
    "ramp_stats": {'seq': {'L_range': 74.8, 'L_min': 22.1, 'L_max': 96.9, 'monotonic': True, 'total_dE': 97.9, 'uniformity': 0.699}, 'div': {'L_range': 67.9, 'L_min': 27.9, 'L_max': 95.7, 'monotonic': False, 'total_dE': 150.9, 'uniformity': 0.715}, 'flow': {'L_range': 69.9, 'L_min': 23.1, 'L_max': 93.0, 'monotonic': True, 'total_dE': 154.7, 'uniformity': 0.733}, 'cyclic': {'L_range': 0.4, 'L_min': 61.8, 'L_max': 62.2, 'monotonic': True, 'total_dE': 143.2, 'uniformity': 0.675}},
    "cvd_grade": 'A',
    "safe_set": [0, 1, 2, 3, 4, 5],
    "orders": {'smooth': [0, 1, 2, 3, 4, 5], 'distinct': [0, 3, 2, 5, 4, 1], 'hue': [5, 0, 2, 3, 1, 4], 'light': [1, 2, 0, 4, 3, 5]},
    "min_de": 24.1,
    "cvd": {'protan': 22.2, 'deutan': 22.1, 'tritan': 16.3},
  },
  "zenitsu-lightning": {
    "slug": 'zenitsu-lightning',
    "zh": '我妻善逸',
    "en": 'Zenitsu',
    "tone_zh": '雷明黄',
    "tone_en": 'Lightning Yellow',
    "name_zh": '我妻善逸 · 雷明黄',
    "name_en": 'Zenitsu · Lightning Yellow',
    "family": '黄',
    "source": '鬼灭之刃',
    "kind": 'cat',
    "colors": ['#E8B000', '#BEB6A3', '#948634', '#69563A', '#A32F1D', '#E25A00'],
    "dark": ['#B78A00', '#968E7C', '#6B6108', '#443419', '#750000', '#A73D00'],
    "light": ['#FFE1AE', '#E9E3D3', '#BFB06F', '#8F7E67', '#C5654F', '#FF935B'],
    "bg": '#FAF4EC',
    "bg2": '#F0E4D2',
    "ink": '#413006',
    "muted": '#8F826E',
    "seq": ['#FFF5E7', '#FCECD3', '#F9E2BF', '#F3D7A7', '#EECB8D', '#E6BE72', '#DAB057', '#D0A440', '#C49720', '#B68A00', '#A77D00', '#987200', '#8B6700', '#7C5C00', '#6E5101', '#5F4602', '#513B02', '#453200', '#453200'],
    "div": ['#742B00', '#943701', '#B54300', '#CE5817', '#E66E2D', '#F48B54', '#FDAA80', '#FFC8AC', '#FFE3D6', '#E8E9E7', '#BDD8DE', '#92C6D1', '#6AB1BF', '#429DAD', '#278897', '#007382', '#035E6A', '#044953', '#044953'],
    "flow": ['#FFE8C3', '#FFE2AF', '#FCDA9E', '#EED1A3', '#E1CAA7', '#D6C5AA', '#D0BEA2', '#CEB691', '#CCAE7F', '#C9A56D', '#C69C57', '#C49343', '#C58933', '#C77F22', '#C97412', '#CC6900', '#CB5F00', '#C75400', '#B75406', '#A65519', '#985524', '#8A552E', '#7E5437', '#72533D', '#695241', '#654837', '#613F2F', '#5D3627', '#5A2D21', '#58291F'],
    "cyclic": ['#E17961', '#DA7E55', '#D1834A', '#C78943', '#BB8E3D', '#B0933B', '#A2973C', '#919D41', '#7CA24A', '#63A659', '#41A86C', '#00AA81', '#01A994', '#00A7A4', '#00A6B4', '#00A4C4', '#00A1D5', '#1E9EE8', '#5199EC', '#7194EA', '#8A8EE5', '#9F89DE', '#B482D4', '#C87BC6', '#D875B2', '#E3709C', '#E77088', '#E67375', '#E27766', '#E17961'],
    "wheel": [{'i': 0, 'L': 75.0, 'C': 78.2, 'h': 83.9}, {'i': 1, 'L': 74.2, 'C': 10.7, 'h': 92.2}, {'i': 2, 'L': 55.7, 'C': 45.0, 'h': 96.4}, {'i': 3, 'L': 37.8, 'C': 19.6, 'h': 79.4}, {'i': 4, 'L': 37.7, 'C': 60.1, 'h': 39.1}, {'i': 5, 'L': 55.6, 'C': 82.1, 'h': 52.5}],
    "ramp_stats": {'seq': {'L_range': 74.8, 'L_min': 22.1, 'L_max': 97.0, 'monotonic': True, 'total_dE': 99.1, 'uniformity': 0.747}, 'div': {'L_range': 67.8, 'L_min': 27.9, 'L_max': 95.7, 'monotonic': False, 'total_dE': 155.5, 'uniformity': 0.724}, 'flow': {'L_range': 70.1, 'L_min': 22.9, 'L_max': 93.0, 'monotonic': True, 'total_dE': 120.8, 'uniformity': 0.717}, 'cyclic': {'L_range': 0.5, 'L_min': 61.8, 'L_max': 62.3, 'monotonic': True, 'total_dE': 179.5, 'uniformity': 0.751}},
    "cvd_grade": 'C',
    "safe_set": [0, 1, 2, 4],
    "orders": {'smooth': [0, 1, 2, 3, 4, 5], 'distinct': [0, 2, 5, 4, 3, 1], 'hue': [4, 5, 3, 0, 2, 1], 'light': [0, 1, 2, 5, 3, 4]},
    "min_de": 19.9,
    "cvd": {'protan': 6.6, 'deutan': 6.7, 'tritan': 17.0},
  },
  "pikachu-lemon": {
    "slug": 'pikachu-lemon',
    "zh": '皮卡丘',
    "en": 'Pikachu',
    "tone_zh": '柠黄',
    "tone_en": 'Lemon Yellow',
    "name_zh": '皮卡丘 · 柠黄',
    "name_en": 'Pikachu · Lemon Yellow',
    "family": '黄',
    "source": '宝可梦',
    "kind": 'cat',
    "colors": ['#DEB100', '#BCB7A6', '#847700', '#444845', '#7D491C', '#ED493E'],
    "dark": ['#AE8A00', '#948F7E', '#5C5200', '#232724', '#542800', '#BE0D1B'],
    "light": ['#FFDF9A', '#E8E3D6', '#AFA050', '#6B6E6C', '#A2734F', '#FF8F7E'],
    "bg": '#F9F4EC',
    "bg2": '#EEE4D2',
    "ink": '#3F3107',
    "muted": '#8D836F',
    "seq": ['#FEF6E8', '#FBEDD5', '#F6E3C0', '#F0D8A8', '#E9CB8D', '#E1C074', '#D6B35C', '#CCA743', '#C09A26', '#B18C00', '#A17F00', '#937400', '#846800', '#785E00', '#695201', '#5D4802', '#503E02', '#433300', '#433300'],
    "div": ['#534000', '#695200', '#806500', '#987802', '#B18C07', '#C7A23D', '#DBBA6D', '#EAD19E', '#F4E7D1', '#E5EAEB', '#BCD7EC', '#92C4E8', '#68AEDC', '#3B99CD', '#2284B5', '#006F9C', '#005B81', '#004766', '#004766'],
    "flow": ['#F0EBDB', '#EFE7CD', '#EDE3BC', '#EBDEA9', '#E7D993', '#E2D37A', '#DBCC5D', '#D4C43B', '#D3B829', '#D1AD0F', '#D0A200', '#CD9800', '#C19300', '#B39200', '#A59000', '#978D00', '#888A00', '#7A8706', '#6C8314', '#687A1A', '#65711E', '#616721', '#5C5E24', '#545728', '#49532B', '#404E2E', '#384831', '#324132', '#303B32', '#2F3932'],
    "cyclic": ['#E67565', '#DF7A57', '#D8804C', '#CD8642', '#C28B3B', '#B69137', '#A99636', '#989B39', '#85A041', '#6DA44F', '#4DA861', '#17AB77', '#01AA8C', '#00A89E', '#00A6AD', '#00A5BD', '#00A3CE', '#019FE2', '#399BF1', '#6395EF', '#7F90EB', '#978AE5', '#AD84DC', '#C27DCE', '#D475BC', '#E270A6', '#E96E90', '#EA6F7B', '#E7736A', '#E67565'],
    "wheel": [{'i': 0, 'L': 74.2, 'C': 76.8, 'h': 87.4}, {'i': 1, 'L': 74.4, 'C': 9.4, 'h': 97.4}, {'i': 2, 'L': 49.6, 'C': 55.5, 'h': 96.3}, {'i': 3, 'L': 30.1, 'C': 2.6, 'h': 152.0}, {'i': 4, 'L': 36.4, 'C': 39.5, 'h': 62.5}, {'i': 5, 'L': 55.2, 'C': 75.3, 'h': 34.5}],
    "ramp_stats": {'seq': {'L_range': 75.0, 'L_min': 22.2, 'L_max': 97.2, 'monotonic': True, 'total_dE': 97.6, 'uniformity': 0.731}, 'div': {'L_range': 67.7, 'L_min': 28.0, 'L_max': 95.7, 'monotonic': False, 'total_dE': 152.3, 'uniformity': 0.703}, 'flow': {'L_range': 70.2, 'L_min': 22.9, 'L_max': 93.0, 'monotonic': True, 'total_dE': 118.8, 'uniformity': 0.684}, 'cyclic': {'L_range': 0.5, 'L_min': 61.8, 'L_max': 62.3, 'monotonic': True, 'total_dE': 182.8, 'uniformity': 0.763}},
    "cvd_grade": 'B',
    "safe_set": [0, 1, 2, 3, 4],
    "orders": {'smooth': [0, 1, 2, 3, 4, 5], 'distinct': [0, 2, 5, 4, 3, 1], 'hue': [5, 4, 0, 2, 1, 3], 'light': [1, 0, 5, 2, 4, 3]},
    "min_de": 22.6,
    "cvd": {'protan': 9.1, 'deutan': 9.3, 'tritan': 16.1},
  },
  "zelda-pale-gold": {
    "slug": 'zelda-pale-gold',
    "zh": '塞尔达',
    "en": 'Zelda',
    "tone_zh": '淡金',
    "tone_en": 'Pale Gold',
    "name_zh": '塞尔达 · 淡金',
    "name_en": 'Zelda · Pale Gold',
    "family": '黄',
    "source": '塞尔达传说',
    "kind": 'cat',
    "colors": ['#A18001', '#C7B679', '#6B8469', '#AEACA7', '#7FA3C4', '#2F5C8A'],
    "dark": ['#755C00', '#9D8E52', '#465F45', '#868580', '#577C9C', '#003962'],
    "light": ['#CBAA57', '#F2E2B1', '#98AD96', '#DAD8D4', '#B3CEE9', '#6783A9'],
    "bg": '#F8F5EE',
    "bg2": '#ECE4D6',
    "ink": '#3D3113',
    "muted": '#8B8373',
    "seq": ['#FCF6EB', '#F5EAD6', '#EEDFC0', '#E4D0A8', '#DAC28F', '#CFB475', '#C3A55B', '#B89841', '#AB8A24', '#9E7E01', '#927301', '#866A00', '#795F00', '#6E5600', '#624D01', '#584402', '#4E3C02', '#433300', '#433300'],
    "div": ['#384637', '#475A46', '#576E56', '#6B826A', '#81977F', '#99AC97', '#B3C2B1', '#CCD6CB', '#E5EAE5', '#EEE8DA', '#E4D2AB', '#D6BB7F', '#C2A356', '#AC8D31', '#96781A', '#806500', '#695202', '#524003', '#524003'],
    "flow": ['#F6EBC8', '#E5DFBF', '#D5D4B7', '#C5C7AD', '#B7C2A9', '#A7BEA6', '#96BAA5', '#86B5A7', '#76B0AA', '#69AAAE', '#56A7AB', '#3EA5A2', '#1CA195', '#009D87', '#009877', '#009365', '#008F51', '#00894B', '#008354', '#007B5B', '#00745F', '#166C60', '#29655F', '#355F5C', '#30575B', '#2B5059', '#294956', '#284152', '#293A4D', '#2A384A'],
    "cyclic": ['#AB935C', '#A2965C', '#979A5E', '#8A9D63', '#7BA06B', '#6AA377', '#58A484', '#47A591', '#36A69F', '#29A5AB', '#25A4B8', '#32A2C3', '#489FCB', '#5D9BCF', '#7098CF', '#8194CE', '#9091CB', '#9E8DC6', '#AC89BF', '#BA85B4', '#C481A6', '#CC8098', '#CF808A', '#CE817D', '#CB8474', '#C6876B', '#C08B64', '#B88E5F', '#AF925C', '#AB935C'],
    "wheel": [{'i': 0, 'L': 55.1, 'C': 60.3, 'h': 87.6}, {'i': 1, 'L': 74.2, 'C': 33.4, 'h': 94.6}, {'i': 2, 'L': 52.6, 'C': 18.7, 'h': 141.3}, {'i': 3, 'L': 70.4, 'C': 2.8, 'h': 94.3}, {'i': 4, 'L': 65.5, 'C': 21.3, 'h': 258.7}, {'i': 5, 'L': 38.0, 'C': 30.1, 'h': 269.9}],
    "ramp_stats": {'seq': {'L_range': 74.9, 'L_min': 22.2, 'L_max': 97.1, 'monotonic': True, 'total_dE': 97.9, 'uniformity': 0.678}, 'div': {'L_range': 67.7, 'L_min': 28.0, 'L_max': 95.7, 'monotonic': False, 'total_dE': 149.8, 'uniformity': 0.703}, 'flow': {'L_range': 70.0, 'L_min': 23.0, 'L_max': 93.1, 'monotonic': True, 'total_dE': 129.9, 'uniformity': 0.639}, 'cyclic': {'L_range': 0.5, 'L_min': 61.8, 'L_max': 62.2, 'monotonic': True, 'total_dE': 146.9, 'uniformity': 0.652}},
    "cvd_grade": 'A',
    "safe_set": [0, 1, 2, 3, 4, 5],
    "orders": {'smooth': [0, 1, 2, 3, 4, 5], 'distinct': [0, 1, 5, 4, 2, 3], 'hue': [0, 1, 2, 4, 5, 3], 'light': [1, 3, 4, 0, 2, 5]},
    "min_de": 17.1,
    "cvd": {'protan': 16.9, 'deutan': 17.0, 'tritan': 12.4},
  },
  "nekomata-neon": {
    "slug": 'nekomata-neon',
    "zh": '猫又',
    "en": 'Nekomata',
    "tone_zh": '荧柠黄',
    "tone_en": 'Neon Lemon',
    "name_zh": '猫又 · 荧柠黄',
    "name_en": 'Nekomata · Neon Lemon',
    "family": '黄',
    "source": '绝区零',
    "kind": 'cat',
    "colors": ['#CFBD00', '#BCB7A9', '#9C9759', '#7D6C03', '#49454B', '#D14C83'],
    "dark": ['#A39400', '#948F81', '#747134', '#544800', '#28242A', '#A61A5E'],
    "light": ['#FEE970', '#E8E4D8', '#C7C190', '#A7954D', '#6F6B71', '#EF86AC'],
    "bg": '#F8F5EC',
    "bg2": '#EBE5D2',
    "ink": '#393306',
    "muted": '#8A846E',
    "seq": ['#FBF6E7', '#F5EED4', '#F0E5BE', '#E8DBA8', '#E0D18E', '#D4C471', '#C8B859', '#BAAA3D', '#AD9F1F', '#9F9200', '#918400', '#857900', '#786E00', '#6B6100', '#605601', '#544C02', '#484002', '#3C3500', '#3C3500'],
    "div": ['#4A4300', '#5E5600', '#736900', '#897D00', '#A09200', '#B8A83B', '#CFBE6C', '#E1D49E', '#F0E8D1', '#F8E4E3', '#F9C6D4', '#F5A8C2', '#EB89AB', '#DD6B96', '#C95281', '#B43B6D', '#913259', '#702945', '#702945'],
    "flow": ['#FEEB98', '#F5DF9D', '#ECD4A2', '#E1CBA7', '#D6C4AB', '#CFBA9F', '#CDAF8D', '#CAA47A', '#C79869', '#C98E60', '#CD845C', '#D07B5C', '#D2725D', '#D4685F', '#D45F63', '#D45569', '#D24B70', '#C74667', '#B94358', '#AA414A', '#9C403F', '#8D3D38', '#863B3F', '#7C3945', '#70384A', '#61384B', '#53384A', '#473746', '#3D3540', '#3B353E'],
    "cyclic": ['#AB952C', '#9D9A2E', '#899F36', '#71A444', '#51A857', '#19AB6D', '#00AA85', '#00A898', '#00A7A9', '#00A5B8', '#00A3CA', '#00A0DD', '#179BF6', '#5796F6', '#7890F2', '#928AED', '#A984E4', '#C07CD6', '#D573C4', '#E46CAD', '#ED6995', '#F06A7F', '#EE6E6C', '#E8745B', '#E17A4D', '#D78041', '#CB8737', '#BF8D31', '#B0932D', '#AB952C'],
    "wheel": [{'i': 0, 'L': 75.9, 'C': 77.8, 'h': 96.9}, {'i': 1, 'L': 74.5, 'C': 7.8, 'h': 95.1}, {'i': 2, 'L': 61.6, 'C': 34.1, 'h': 102.6}, {'i': 3, 'L': 45.8, 'C': 51.5, 'h': 93.5}, {'i': 4, 'L': 29.9, 'C': 4.2, 'h': 315.0}, {'i': 5, 'L': 52.2, 'C': 57.2, 'h': 357.4}],
    "ramp_stats": {'seq': {'L_range': 74.9, 'L_min': 22.0, 'L_max': 96.9, 'monotonic': True, 'total_dE': 94.8, 'uniformity': 0.722}, 'div': {'L_range': 67.6, 'L_min': 28.0, 'L_max': 95.6, 'monotonic': False, 'total_dE': 153.3, 'uniformity': 0.678}, 'flow': {'L_range': 69.8, 'L_min': 23.1, 'L_max': 92.9, 'monotonic': True, 'total_dE': 131.4, 'uniformity': 0.691}, 'cyclic': {'L_range': 0.5, 'L_min': 61.7, 'L_max': 62.2, 'monotonic': True, 'total_dE': 188.0, 'uniformity': 0.772}},
    "cvd_grade": 'A',
    "safe_set": [0, 1, 2, 3, 4, 5],
    "orders": {'smooth': [0, 1, 2, 3, 4, 5], 'distinct': [0, 2, 3, 5, 4, 1], 'hue': [3, 0, 2, 5, 1, 4], 'light': [0, 1, 2, 5, 3, 4]},
    "min_de": 17.0,
    "cvd": {'protan': 15.9, 'deutan': 15.8, 'tritan': 11.7},
  },
  "luigi-grass": {
    "slug": 'luigi-grass',
    "zh": '路易吉',
    "en": 'Luigi',
    "tone_zh": '草绿',
    "tone_en": 'Grass Green',
    "name_zh": '路易吉 · 草绿',
    "name_en": 'Luigi · Grass Green',
    "family": '绿',
    "source": '超级马力欧',
    "kind": 'cat',
    "colors": ['#009530', '#8ACB96', '#DAB32B', '#8F8C82', '#005B2D', '#2B54B0'],
    "dark": ['#006B1E', '#61A26F', '#AD8C00', '#69665C', '#003515', '#00337B'],
    "light": ['#67BD6C', '#C2F5CA', '#FFE197', '#B9B7AE', '#49815A', '#6D7CC8'],
    "bg": '#F0F7F0',
    "bg2": '#DBE9DA',
    "ink": '#1A391C',
    "muted": '#798878',
    "seq": ['#EFF9EE', '#E2F2E0', '#D3EAD1', '#C1E1BF', '#ADD8AB', '#98CD97', '#84C383', '#6DB86F', '#56AD5B', '#3BA248', '#149734', '#008B2C', '#007F27', '#007322', '#00661C', '#005816', '#004C11', '#003F0C', '#003F0C'],
    "div": ['#44423D', '#57544E', '#6A685F', '#7E7C73', '#939188', '#A9A79F', '#BFBDB8', '#D5D3CF', '#EAE8E7', '#E0ECDF', '#B9DDB7', '#91CC90', '#6AB86D', '#43A44D', '#278E38', '#017924', '#06631E', '#084D18', '#084D18'],
    "flow": ['#D0F4D5', '#C3EEC2', '#B8E8AB', '#B0E092', '#ABD877', '#A7CD64', '#A2C26F', '#9EB778', '#9BAE7E', '#97A684', '#92A180', '#869E72', '#769B63', '#619854', '#459445', '#0E9138', '#008A44', '#008552', '#00805C', '#007A63', '#007468', '#006E6A', '#00676C', '#006069', '#005A5C', '#00534D', '#004D40', '#104633', '#1E3F2B', '#213D29'],
    "cyclic": ['#B2932F', '#A2982F', '#909E35', '#7AA240', '#5FA650', '#3DA962', '#00AB78', '#00A98E', '#00A8A0', '#00A6AF', '#00A4BF', '#00A2D2', '#009FE8', '#3C99F6', '#6794F4', '#848EEF', '#9C88E8', '#B381DD', '#C979CE', '#DC70B9', '#E86BA1', '#EE6A8A', '#EE6D76', '#EA7164', '#E47855', '#DB7E48', '#D1843D', '#C48B34', '#B69130', '#B2932F'],
    "wheel": [{'i': 0, 'L': 53.7, 'C': 69.3, 'h': 142.2}, {'i': 1, 'L': 76.3, 'C': 37.3, 'h': 147.5}, {'i': 2, 'L': 74.4, 'C': 68.7, 'h': 88.8}, {'i': 3, 'L': 58.2, 'C': 5.8, 'h': 97.5}, {'i': 4, 'L': 33.3, 'C': 40.7, 'h': 150.6}, {'i': 5, 'L': 37.8, 'C': 56.5, 'h': 289.5}],
    "ramp_stats": {'seq': {'L_range': 74.7, 'L_min': 22.2, 'L_max': 96.9, 'monotonic': True, 'total_dE': 82.6, 'uniformity': 0.685}, 'div': {'L_range': 67.9, 'L_min': 27.9, 'L_max': 95.8, 'monotonic': False, 'total_dE': 151.9, 'uniformity': 0.611}, 'flow': {'L_range': 69.9, 'L_min': 23.1, 'L_max': 93.0, 'monotonic': True, 'total_dE': 128.7, 'uniformity': 0.63}, 'cyclic': {'L_range': 0.6, 'L_min': 61.7, 'L_max': 62.3, 'monotonic': True, 'total_dE': 187.5, 'uniformity': 0.791}},
    "cvd_grade": 'A',
    "safe_set": [0, 1, 2, 3, 4, 5],
    "orders": {'smooth': [0, 1, 2, 3, 4, 5], 'distinct': [0, 1, 4, 5, 2, 3], 'hue': [2, 0, 1, 4, 5, 3], 'light': [1, 2, 3, 0, 5, 4]},
    "min_de": 20.9,
    "cvd": {'protan': 14.7, 'deutan': 15.6, 'tritan': 13.2},
  },
  "zoro-moss-ink": {
    "slug": 'zoro-moss-ink',
    "zh": '索隆',
    "en": 'Zoro',
    "tone_zh": '苔墨',
    "tone_en": 'Moss & Ink',
    "name_zh": '索隆 · 苔墨',
    "name_en": 'Zoro · Moss & Ink',
    "family": '绿',
    "source": '海贼王',
    "kind": 'cat',
    "colors": ['#6D8557', '#9CC574', '#BAB7AC', '#B28E00', '#2F5025', '#454747'],
    "dark": ['#486033', '#739C4D', '#928F84', '#856900', '#0D2E01', '#242626'],
    "light": ['#9BAE88', '#D0F0AE', '#E6E3DB', '#DDB95D', '#5C7652', '#6C6D6D'],
    "bg": '#F4F5F2',
    "bg2": '#E3E6E0',
    "ink": '#2E3527',
    "muted": '#81857D',
    "seq": ['#F5F7F2', '#E4E9DF', '#D3DACB', '#C3CEB9', '#B2BFA5', '#A1B192', '#91A480', '#81966D', '#738A5D', '#688052', '#5F764A', '#576D43', '#4E633A', '#455933', '#3E502E', '#374728', '#313F24', '#2C3920', '#2C3920'],
    "div": ['#524000', '#695200', '#806500', '#977815', '#AE8D28', '#C4A34F', '#D7BB7A', '#E6D2A6', '#F2E8D5', '#E4E9EC', '#BDD7EC', '#94C3E7', '#6AAEDB', '#3E99CC', '#2584B4', '#006F9D', '#005B81', '#004767', '#004767'],
    "flow": ['#DCF2C4', '#D4E5BE', '#CCDAB8', '#C5CFB3', '#BDC6AC', '#B7C4A0', '#B0C193', '#A8BE84', '#9FBB74', '#93B862', '#85B34D', '#75AF36', '#6BA93B', '#62A346', '#5B9D4E', '#569656', '#53905B', '#528A5F', '#518361', '#487B5C', '#417357', '#396B52', '#30634C', '#2B5C4B', '#295549', '#284E47', '#284844', '#294240', '#2A3C3C', '#2A3A3A'],
    "cyclic": ['#AF9349', '#A2974A', '#949B4D', '#839F54', '#72A35E', '#5BA56D', '#3EA87F', '#10A990', '#00A8A0', '#00A6AD', '#00A5BC', '#00A2CB', '#07A0DC', '#499BE0', '#6797E0', '#7E92DD', '#928ED9', '#A489D2', '#B683C7', '#C77DB9', '#D479A7', '#DB7794', '#DD7883', '#DC7A74', '#D77E67', '#D1835C', '#C88854', '#BE8C4D', '#B3924A', '#AF9349'],
    "wheel": [{'i': 0, 'L': 52.6, 'C': 28.1, 'h': 128.3}, {'i': 1, 'L': 75.0, 'C': 45.6, 'h': 127.4}, {'i': 2, 'L': 74.4, 'C': 6.0, 'h': 98.7}, {'i': 3, 'L': 60.6, 'C': 65.2, 'h': 87.7}, {'i': 4, 'L': 30.6, 'C': 30.5, 'h': 135.1}, {'i': 5, 'L': 30.0, 'C': 0.9, 'h': 199.3}],
    "ramp_stats": {'seq': {'L_range': 74.8, 'L_min': 22.2, 'L_max': 97.0, 'monotonic': True, 'total_dE': 93.4, 'uniformity': 0.628}, 'div': {'L_range': 67.7, 'L_min': 28.0, 'L_max': 95.7, 'monotonic': False, 'total_dE': 151.0, 'uniformity': 0.718}, 'flow': {'L_range': 69.8, 'L_min': 23.1, 'L_max': 92.9, 'monotonic': True, 'total_dE': 103.8, 'uniformity': 0.6}, 'cyclic': {'L_range': 0.6, 'L_min': 61.8, 'L_max': 62.3, 'monotonic': True, 'total_dE': 167.7, 'uniformity': 0.72}},
    "cvd_grade": 'A',
    "safe_set": [0, 1, 2, 3, 4, 5],
    "orders": {'smooth': [0, 1, 2, 3, 4, 5], 'distinct': [0, 1, 4, 3, 5, 2], 'hue': [3, 1, 0, 4, 2, 5], 'light': [1, 2, 3, 0, 4, 5]},
    "min_de": 19.8,
    "cvd": {'protan': 13.7, 'deutan': 13.4, 'tritan': 12.4},
  },
  "tanjiro-ink-ember": {
    "slug": 'tanjiro-ink-ember',
    "zh": '灶门炭治郎',
    "en": 'Tanjiro',
    "tone_zh": '墨绿炭赤',
    "tone_en": 'Ink Green & Ember',
    "name_zh": '灶门炭治郎 · 墨绿炭赤',
    "name_en": 'Tanjiro · Ink Green & Ember',
    "family": '绿',
    "source": '鬼灭之刃',
    "kind": 'cat',
    "colors": ['#426B47', '#464746', '#8B2B1C', '#D4703F', '#C0B6A7', '#7CA377'],
    "dark": ['#1D4725', '#252625', '#5D0400', '#A84919', '#988E7F', '#557C51'],
    "light": ['#719274', '#6C6D6C', '#AD5D4B', '#F7A178', '#EBE3D7', '#ADCDA9'],
    "bg": '#F3F6F3',
    "bg2": '#E1E7E1',
    "ink": '#29362A',
    "muted": '#7F857F',
    "seq": ['#F3F8F3', '#E6EDE6', '#D5E0D5', '#C5D3C5', '#B4C5B4', '#A4B9A5', '#94AC95', '#849F86', '#749276', '#658768', '#577B5A', '#48704C', '#3E6643', '#355C3A', '#2E5232', '#2A4A2F', '#264129', '#233A26', '#233A26'],
    "div": ['#314733', '#3E5C41', '#4B714F', '#608563', '#759A78', '#90AF91', '#ABC4AD', '#C7D8C8', '#E4EBE4', '#F4E6E1', '#F6CABF', '#F1AE9E', '#E4927F', '#D57762', '#C0614C', '#A94B39', '#893F2F', '#6A3226', '#6A3226'],
    "flow": ['#F4EADB', '#ECE1CB', '#E1D9BB', '#D3D1AB', '#C4CA9C', '#BEC28A', '#BDBA74', '#BEB061', '#C0A74D', '#C39E3B', '#C0962F', '#B19532', '#A39437', '#94913D', '#868F43', '#798A4A', '#6D8551', '#667E4F', '#657540', '#666D33', '#666527', '#675D1B', '#655512', '#595318', '#4D4F1E', '#424B25', '#3A462A', '#34402E', '#313B31', '#313931'],
    "cyclic": ['#CE8371', '#C98669', '#C38962', '#BB8D5C', '#B39159', '#A89558', '#9D9859', '#909C5D', '#819F64', '#71A26E', '#5FA47B', '#4BA68A', '#37A698', '#21A6A5', '#0BA6B3', '#12A4C0', '#30A1CA', '#4E9ED0', '#6599D3', '#7996D2', '#8A92CF', '#998ECB', '#A88AC4', '#B785BA', '#C481AD', '#CD7E9D', '#D17E8E', '#D17F80', '#CF8274', '#CE8371'],
    "wheel": [{'i': 0, 'L': 41.4, 'C': 27.6, 'h': 145.2}, {'i': 1, 'L': 30.0, 'C': 0.8, 'h': 144.4}, {'i': 2, 'L': 32.5, 'C': 51.0, 'h': 38.6}, {'i': 3, 'L': 58.0, 'C': 56.6, 'h': 51.1}, {'i': 4, 'L': 74.5, 'C': 9.0, 'h': 83.8}, {'i': 5, 'L': 63.2, 'C': 28.9, 'h': 139.8}],
    "ramp_stats": {'seq': {'L_range': 75.1, 'L_min': 22.0, 'L_max': 97.1, 'monotonic': True, 'total_dE': 92.8, 'uniformity': 0.627}, 'div': {'L_range': 67.9, 'L_min': 27.8, 'L_max': 95.7, 'monotonic': False, 'total_dE': 149.0, 'uniformity': 0.726}, 'flow': {'L_range': 70.1, 'L_min': 23.0, 'L_max': 93.1, 'monotonic': True, 'total_dE': 130.5, 'uniformity': 0.661}, 'cyclic': {'L_range': 0.5, 'L_min': 61.8, 'L_max': 62.2, 'monotonic': True, 'total_dE': 151.0, 'uniformity': 0.655}},
    "cvd_grade": 'B',
    "safe_set": [0, 1, 3, 5],
    "orders": {'smooth': [0, 1, 2, 3, 4, 5], 'distinct': [0, 5, 2, 3, 1, 4], 'hue': [2, 3, 5, 0, 4, 1], 'light': [4, 5, 3, 0, 2, 1]},
    "min_de": 21.3,
    "cvd": {'protan': 11.1, 'deutan': 10.9, 'tritan': 18.3},
  },
  "totoro-moss-gray": {
    "slug": 'totoro-moss-gray',
    "zh": '龙猫',
    "en": 'Totoro',
    "tone_zh": '苔灰',
    "tone_en": 'Moss Gray',
    "name_zh": '龙猫 · 苔灰',
    "name_en": 'Totoro · Moss Gray',
    "family": '绿',
    "source": '龙猫',
    "kind": 'cat',
    "colors": ['#616967', '#3B4A45', '#8A7550', '#718578', '#9D9D99', '#B8C2B3'],
    "dark": ['#3E4543', '#1A2924', '#63512D', '#4C6053', '#767672', '#909A8B'],
    "light": ['#8B9190', '#63706C', '#B29F81', '#9EAEA3', '#C8C8C5', '#E6EEE2'],
    "bg": '#F4F5F5',
    "bg2": '#E4E5E5',
    "ink": '#313332',
    "muted": '#838484',
    "seq": ['#F6F7F6', '#DFE1E0', '#C8CCCB', '#B4B8B7', '#A2A7A6', '#919796', '#828987', '#737A78', '#636B69', '#59615E', '#535A58', '#4D5452', '#444A48', '#404745', '#3D4342', '#393F3E', '#363C3B', '#313635', '#313635'],
    "div": ['#4C412D', '#625338', '#786644', '#8D7958', '#A28E6D', '#B6A488', '#CABCA6', '#DCD2C3', '#EDE8E2', '#E5E9EC', '#C6D6E1', '#A7C2D4', '#88ABC3', '#6B96B1', '#53819E', '#3D6D8A', '#33596F', '#2A4556', '#2A4556'],
    "flow": ['#E4EEDF', '#DAE4D3', '#D2DDCB', '#C9D4BF', '#C0CBB4', '#B9C5AE', '#AFBEA7', '#A5B7A0', '#9BB19A', '#91AA95', '#88A48F', '#829D85', '#7D977C', '#799172', '#768B69', '#728560', '#6F7F58', '#677B58', '#5F7658', '#587258', '#516C57', '#4B6757', '#466155', '#425B53', '#3E544D', '#394E47', '#364842', '#31423C', '#2E3C38', '#2C3A35'],
    "cyclic": ['#AA936C', '#A3956B', '#9B986C', '#939A6F', '#8A9C73', '#819E78', '#789F7E', '#6EA087', '#63A292', '#5BA29D', '#56A1A7', '#57A0B0', '#5D9EB7', '#689CBD', '#739ABF', '#7E97C0', '#8994BF', '#9392BD', '#9E8FB8', '#A88CB3', '#B389AA', '#BB879F', '#C08693', '#C18789', '#C08880', '#BC8A78', '#B88D73', '#B28F6F', '#AD926C', '#AA936C'],
    "wheel": [{'i': 0, 'L': 43.7, 'C': 3.5, 'h': 178.9}, {'i': 1, 'L': 30.1, 'C': 7.2, 'h': 172.0}, {'i': 2, 'L': 50.3, 'C': 23.6, 'h': 83.4}, {'i': 3, 'L': 53.6, 'C': 11.0, 'h': 155.3}, {'i': 4, 'L': 64.6, 'C': 2.2, 'h': 109.9}, {'i': 5, 'L': 77.3, 'C': 8.9, 'h': 134.3}],
    "ramp_stats": {'seq': {'L_range': 75.0, 'L_min': 22.1, 'L_max': 97.1, 'monotonic': True, 'total_dE': 110.5, 'uniformity': 0.39}, 'div': {'L_range': 67.7, 'L_min': 27.9, 'L_max': 95.6, 'monotonic': False, 'total_dE': 157.7, 'uniformity': 0.708}, 'flow': {'L_range': 69.9, 'L_min': 23.1, 'L_max': 93.0, 'monotonic': True, 'total_dE': 94.1, 'uniformity': 0.549}, 'cyclic': {'L_range': 0.5, 'L_min': 61.8, 'L_max': 62.2, 'monotonic': True, 'total_dE': 125.4, 'uniformity': 0.552}},
    "cvd_grade": 'B',
    "safe_set": [0, 2, 5],
    "orders": {'smooth': [0, 1, 2, 3, 4, 5], 'distinct': [0, 3, 1, 2, 5, 4], 'hue': [2, 5, 4, 3, 0, 1], 'light': [5, 4, 3, 2, 0, 1]},
    "min_de": 12.0,
    "cvd": {'protan': 9.8, 'deutan': 10.1, 'tritan': 11.4},
  },
  "eren-survey-olive": {
    "slug": 'eren-survey-olive',
    "zh": '艾伦',
    "en": 'Eren',
    "tone_zh": '橄榄',
    "tone_en": 'Survey Olive',
    "name_zh": '艾伦 · 橄榄',
    "name_en": 'Eren · Survey Olive',
    "family": '绿',
    "source": '进击的巨人',
    "kind": 'cat',
    "colors": ['#6F7E32', '#A7B16C', '#B9B6AD', '#7B6152', '#89271F', '#43505C'],
    "dark": ['#495909', '#7F8946', '#918E85', '#563E2F', '#5E0000', '#212E39'],
    "light": ['#9CA66A', '#D5DCA4', '#E5E2DB', '#A18A7E', '#AB594C', '#6C7781'],
    "bg": '#F5F5F0',
    "bg2": '#E5E6DC',
    "ink": '#31351E',
    "muted": '#838579',
    "seq": ['#F6F7EF', '#E8EADB', '#D9DCC5', '#CBD0B1', '#BBC19B', '#ACB486', '#9DA671', '#8F9A5D', '#818E4B', '#748239', '#69782D', '#616F27', '#5A6821', '#505E1A', '#485516', '#404B13', '#363F11', '#30380F', '#30380F'],
    "div": ['#6A3129', '#893E33', '#AA4A3E', '#C06051', '#D57667', '#E49182', '#F1ADA0', '#F8C9C0', '#FAE4E0', '#E7E9E8', '#C1D8D8', '#9DC5C6', '#7BB0B1', '#5B9B9D', '#418689', '#287275', '#245D5F', '#1F484A', '#1F484A'],
    "flow": ['#F0EBDB', '#ECE4CD', '#E6DDBE', '#E1D6AF', '#DACE9E', '#D4C68C', '#CCBD7D', '#C4B26D', '#BDA85F', '#B69E50', '#B39650', '#B18F53', '#AC8957', '#A6835B', '#A17E5E', '#997961', '#927563', '#8E7063', '#896A62', '#846461', '#7E5F61', '#755960', '#6C545F', '#664E5B', '#644752', '#624048', '#5F393E', '#5B3333', '#562D28', '#542B25'],
    "cyclic": ['#C98478', '#C68770', '#C18A6A', '#BA8D64', '#B29061', '#AA945F', '#A09760', '#959A62', '#889D67', '#7AA070', '#6AA27B', '#5AA488', '#4BA595', '#3EA5A1', '#36A4AD', '#36A3B8', '#43A1C2', '#549DC9', '#689ACB', '#7897CC', '#8793CA', '#9590C7', '#A28DC1', '#AF89B9', '#BB85AF', '#C582A1', '#CA8193', '#CC8286', '#CA847C', '#C98478'],
    "wheel": [{'i': 0, 'L': 50.1, 'C': 42.4, 'h': 114.1}, {'i': 1, 'L': 70.0, 'C': 37.1, 'h': 113.0}, {'i': 2, 'L': 74.1, 'C': 5.0, 'h': 96.5}, {'i': 3, 'L': 43.3, 'C': 15.0, 'h': 56.9}, {'i': 4, 'L': 31.5, 'C': 50.2, 'h': 35.2}, {'i': 5, 'L': 33.4, 'C': 8.9, 'h': 256.9}],
    "ramp_stats": {'seq': {'L_range': 75.0, 'L_min': 21.9, 'L_max': 97.0, 'monotonic': True, 'total_dE': 86.5, 'uniformity': 0.672}, 'div': {'L_range': 67.9, 'L_min': 27.9, 'L_max': 95.8, 'monotonic': False, 'total_dE': 153.1, 'uniformity': 0.731}, 'flow': {'L_range': 70.2, 'L_min': 22.8, 'L_max': 93.0, 'monotonic': True, 'total_dE': 111.3, 'uniformity': 0.583}, 'cyclic': {'L_range': 0.5, 'L_min': 61.7, 'L_max': 62.2, 'monotonic': True, 'total_dE': 141.6, 'uniformity': 0.607}},
    "cvd_grade": 'B',
    "safe_set": [0, 1, 2, 3, 4, 5],
    "orders": {'smooth': [0, 1, 2, 3, 4, 5], 'distinct': [0, 1, 5, 3, 4, 2], 'hue': [4, 3, 1, 0, 2, 5], 'light': [2, 1, 0, 3, 5, 4]},
    "min_de": 17.6,
    "cvd": {'protan': 14.4, 'deutan': 12.3, 'tritan': 6.4},
  },
  "minori-emerald": {
    "slug": 'minori-emerald',
    "zh": '花里みのり',
    "en": 'Minori',
    "tone_zh": '翡翠',
    "tone_en": 'Emerald Jump',
    "name_zh": '花里みのり · 翡翠',
    "name_en": 'Minori · Emerald Jump',
    "family": '绿',
    "source": '世界计划',
    "kind": 'cat',
    "colors": ['#009167', '#4A7FC4', '#B5BAB8', '#BB8E13', '#7A5240', '#E1708D'],
    "dark": ['#006748', '#095A9C', '#8D9290', '#8D6900', '#542F1F', '#B64767'],
    "light": ['#65B995', '#88A8E1', '#E2E6E5', '#E5BA63', '#9E7C6C', '#FFA6B9'],
    "bg": '#F0F6F3',
    "bg2": '#DBE8E2',
    "ink": '#19382B',
    "muted": '#788780',
    "seq": ['#EEF9F4', '#DEF0E7', '#CBE6D9', '#B7DCCA', '#A2D0BA', '#8BC5AB', '#74B99A', '#5BAC8A', '#40A17B', '#1B956C', '#008A62', '#00805A', '#007552', '#00694A', '#005E41', '#005439', '#004831', '#003E29', '#003E29'],
    "div": ['#284368', '#305687', '#3769A8', '#517DBC', '#6B92CF', '#8AA8DD', '#AABEE8', '#C7D4F0', '#E4E9F5', '#F0E8DE', '#E8D0AB', '#DAB97C', '#C8A152', '#B38B2C', '#9C7617', '#856300', '#6C5100', '#553F00', '#553F00'],
    "flow": ['#DBF0E8', '#CBEEDF', '#B5EAD4', '#99E6C4', '#79E1AF', '#57D796', '#57C482', '#55B271', '#35AD7A', '#00A986', '#00A491', '#009E99', '#0098A0', '#0092A5', '#008AA9', '#0083AF', '#007BB4', '#2672B3', '#416BAC', '#5164A4', '#5E5D9A', '#67568E', '#6E4E80', '#72466F', '#72405D', '#6B3B4B', '#61383D', '#553633', '#48342D', '#44332C'],
    "cyclic": ['#DF758F', '#E0777E', '#DD7A6F', '#D87E63', '#D18258', '#C98750', '#BF8C4A', '#B39146', '#A69646', '#979A48', '#869F50', '#71A35B', '#58A66B', '#39A87D', '#00A98F', '#00A89F', '#00A6AD', '#00A5BC', '#00A3CC', '#00A0DD', '#449CE3', '#6597E3', '#7D92E0', '#928DDC', '#A588D5', '#B783CA', '#C87CBB', '#D678A9', '#DD7595', '#DF758F'],
    "wheel": [{'i': 0, 'L': 53.2, 'C': 45.5, 'h': 163.1}, {'i': 1, 'L': 52.5, 'C': 41.4, 'h': 275.3}, {'i': 2, 'L': 75.1, 'C': 2.2, 'h': 169.2}, {'i': 3, 'L': 61.6, 'C': 63.5, 'h': 83.7}, {'i': 4, 'L': 38.8, 'C': 22.5, 'h': 50.2}, {'i': 5, 'L': 61.2, 'C': 47.1, 'h': 6.0}],
    "ramp_stats": {'seq': {'L_range': 74.7, 'L_min': 22.3, 'L_max': 97.0, 'monotonic': True, 'total_dE': 88.5, 'uniformity': 0.699}, 'div': {'L_range': 67.8, 'L_min': 28.0, 'L_max': 95.8, 'monotonic': False, 'total_dE': 151.2, 'uniformity': 0.676}, 'flow': {'L_range': 70.2, 'L_min': 22.9, 'L_max': 93.1, 'monotonic': True, 'total_dE': 151.0, 'uniformity': 0.723}, 'cyclic': {'L_range': 0.5, 'L_min': 61.8, 'L_max': 62.2, 'monotonic': True, 'total_dE': 170.9, 'uniformity': 0.732}},
    "cvd_grade": 'B',
    "safe_set": [0, 1, 2, 3, 4],
    "orders": {'smooth': [0, 1, 2, 3, 4, 5], 'distinct': [0, 5, 1, 3, 4, 2], 'hue': [5, 4, 3, 0, 1, 2], 'light': [2, 3, 5, 0, 1, 4]},
    "min_de": 28.8,
    "cvd": {'protan': 16.1, 'deutan': 11.5, 'tritan': 8.1},
  },
  "miku-aqua": {
    "slug": 'miku-aqua',
    "zh": '初音未来',
    "en": 'Miku',
    "tone_zh": '青碧',
    "tone_en": 'Aqua Teal',
    "name_zh": '初音未来 · 青碧',
    "name_en": 'Miku · Aqua Teal',
    "family": '青',
    "source": 'VOCALOID',
    "kind": 'cat',
    "colors": ['#35CFC4', '#A8ACAB', '#689893', '#00737D', '#404757', '#D7486A'],
    "dark": ['#00A49B', '#818584', '#41716D', '#004C53', '#1F2635', '#AB1246'],
    "light": ['#93F9EF', '#D5D8D7', '#9CC1BD', '#5B9AA2', '#686D7B', '#F58397'],
    "bg": '#EFF6F5',
    "bg2": '#D9E8E6',
    "ink": '#123835',
    "muted": '#768785',
    "seq": ['#EDF9F7', '#DDF2EF', '#C9E9E5', '#B4E1DB', '#9ED7D1', '#89CFC8', '#71C5BC', '#58BBB2', '#37B0A6', '#00A399', '#00948B', '#00877E', '#007A72', '#006C65', '#00605A', '#00534E', '#004642', '#003C38', '#003C38'],
    "div": ['#004B46', '#00605A', '#00756E', '#148B83', '#25A199', '#58B6AE', '#85CAC3', '#B0DCD7', '#DAEDEA', '#E4EAEB', '#D0D4DA', '#BABDC8', '#A2A7B4', '#8B91A0', '#767C8C', '#626878', '#505562', '#3E424C', '#3E424C'],
    "flow": ['#B3F8F0', '#B3E7D9', '#B2D7C6', '#AEC7B4', '#A1B7A0', '#97A98C', '#959F79', '#9A9969', '#A1925B', '#A98A51', '#B08349', '#B87A45', '#C07144', '#C66846', '#CC5E4B', '#D05352', '#D4485B', '#CC4669', '#C04775', '#AF4B81', '#9C5089', '#88548D', '#74578D', '#625889', '#515882', '#455676', '#3F4B63', '#3A4255', '#353A46', '#333741'],
    "cyclic": ['#CC818C', '#CC8280', '#CA8475', '#C5886D', '#BF8B67', '#B78E62', '#AF925F', '#A5955E', '#9B9960', '#8E9B64', '#809F6C', '#70A176', '#60A382', '#4FA48F', '#42A59C', '#37A5A7', '#32A4B2', '#36A2BD', '#47A0C5', '#5A9CCB', '#6C99CD', '#7D96CC', '#8B92CA', '#988FC6', '#A68BC0', '#B387B8', '#BE84AC', '#C7819E', '#CB8190', '#CC818C'],
    "wheel": [{'i': 0, 'L': 75.7, 'C': 41.5, 'h': 188.1}, {'i': 1, 'L': 70.0, 'C': 1.6, 'h': 179.3}, {'i': 2, 'L': 59.4, 'C': 17.4, 'h': 188.4}, {'i': 3, 'L': 43.9, 'C': 26.8, 'h': 209.7}, {'i': 4, 'L': 30.1, 'C': 10.5, 'h': 276.9}, {'i': 5, 'L': 52.0, 'C': 59.5, 'h': 11.8}],
    "ramp_stats": {'seq': {'L_range': 75.0, 'L_min': 22.0, 'L_max': 97.0, 'monotonic': True, 'total_dE': 98.3, 'uniformity': 0.642}, 'div': {'L_range': 67.7, 'L_min': 28.0, 'L_max': 95.7, 'monotonic': False, 'total_dE': 158.5, 'uniformity': 0.651}, 'flow': {'L_range': 70.0, 'L_min': 23.1, 'L_max': 93.0, 'monotonic': True, 'total_dE': 153.4, 'uniformity': 0.762}, 'cyclic': {'L_range': 0.5, 'L_min': 61.7, 'L_max': 62.3, 'monotonic': True, 'total_dE': 142.1, 'uniformity': 0.633}},
    "cvd_grade": 'C',
    "safe_set": [0, 2, 3],
    "orders": {'smooth': [0, 1, 2, 3, 4, 5], 'distinct': [0, 2, 3, 4, 5, 1], 'hue': [5, 0, 2, 3, 1, 4], 'light': [0, 1, 2, 5, 3, 4]},
    "min_de": 16.7,
    "cvd": {'protan': 6.7, 'deutan': 8.2, 'tritan': 13.9},
  },
  "venti-mint": {
    "slug": 'venti-mint',
    "zh": '温迪',
    "en": 'Venti',
    "tone_zh": '风薄荷',
    "tone_en": 'Anemo Mint',
    "name_zh": '温迪 · 风薄荷',
    "name_en": 'Venti · Anemo Mint',
    "family": '青',
    "source": '原神',
    "kind": 'cat',
    "colors": ['#089275', '#216156', '#3B5A6E', '#949795', '#8FC2B0', '#C8B384'],
    "dark": ['#006953', '#003D34', '#15374A', '#6E716F', '#679A88', '#9F8B5D'],
    "light": ['#68BAA1', '#59877E', '#6A8191', '#BFC2C0', '#C4EDDE', '#F2E0BA'],
    "bg": '#F0F6F4',
    "bg2": '#DBE8E3',
    "ink": '#1A382F',
    "muted": '#788782',
    "seq": ['#EFF9F5', '#DDEFE8', '#C8E4DA', '#B2D8CB', '#9ACBBB', '#83BFAC', '#6AB29C', '#4FA68D', '#319B80', '#079073', '#058368', '#037860', '#016E57', '#00654F', '#005A46', '#004F3E', '#004535', '#003D2F', '#003D2F'],
    "div": ['#274841', '#305D53', '#397267', '#4F867B', '#669B90', '#83B0A6', '#A2C5BD', '#C2D8D3', '#E1EBE8', '#EAE9E2', '#DBD3C2', '#C9BCA2', '#B5A584', '#A08F68', '#8B7A53', '#76673F', '#605334', '#4B4129', '#4B4129'],
    "flow": ['#D5F1E7', '#CBEBDC', '#C1E3D0', '#B8DCC3', '#B0D3B4', '#A8CCA8', '#9DC5A7', '#93BDA5', '#8BB6A3', '#83AEA1', '#7CA69D', '#6CA299', '#5A9E96', '#459992', '#289590', '#008F8D', '#008788', '#008083', '#00797E', '#007177', '#146A70', '#236369', '#295D63', '#2A575F', '#2C505A', '#2D4A55', '#2D4550', '#2E3F49', '#2D3942', '#2D3841'],
    "cyclic": ['#A79469', '#9F9769', '#96996C', '#8C9C6F', '#819E76', '#74A07F', '#68A189', '#5EA292', '#56A29D', '#51A2A7', '#51A1B1', '#579FB9', '#619DBF', '#6E9AC2', '#7B98C2', '#8695C2', '#9192BF', '#9C8FBC', '#A78CB6', '#B189AE', '#BA87A3', '#C18597', '#C3868C', '#C38782', '#C08879', '#BC8B73', '#B78D6E', '#B1906B', '#AA9369', '#A79469'],
    "wheel": [{'i': 0, 'L': 53.9, 'C': 40.4, 'h': 171.1}, {'i': 1, 'L': 37.0, 'C': 23.2, 'h': 179.3}, {'i': 2, 'L': 36.7, 'C': 15.9, 'h': 249.9}, {'i': 3, 'L': 62.2, 'C': 1.6, 'h': 155.5}, {'i': 4, 'L': 74.5, 'C': 20.8, 'h': 169.9}, {'i': 5, 'L': 73.7, 'C': 26.8, 'h': 88.7}],
    "ramp_stats": {'seq': {'L_range': 75.0, 'L_min': 22.1, 'L_max': 97.1, 'monotonic': True, 'total_dE': 91.9, 'uniformity': 0.662}, 'div': {'L_range': 67.7, 'L_min': 27.9, 'L_max': 95.7, 'monotonic': False, 'total_dE': 154.6, 'uniformity': 0.726}, 'flow': {'L_range': 70.0, 'L_min': 22.9, 'L_max': 92.9, 'monotonic': True, 'total_dE': 105.4, 'uniformity': 0.606}, 'cyclic': {'L_range': 0.5, 'L_min': 61.8, 'L_max': 62.2, 'monotonic': True, 'total_dE': 128.0, 'uniformity': 0.566}},
    "cvd_grade": 'B',
    "safe_set": [0, 1, 4],
    "orders": {'smooth': [0, 1, 2, 3, 4, 5], 'distinct': [0, 4, 1, 2, 5, 3], 'hue': [5, 4, 0, 1, 2, 3], 'light': [4, 5, 3, 0, 1, 2]},
    "min_de": 17.9,
    "cvd": {'protan': 9.8, 'deutan': 9.3, 'tritan': 5.2},
  },
  "giyu-pine": {
    "slug": 'giyu-pine',
    "zh": '富冈义勇',
    "en": 'Giyu',
    "tone_zh": '松青',
    "tone_en": 'Pine Teal',
    "name_zh": '富冈义勇 · 松青',
    "name_en": 'Giyu · Pine Teal',
    "family": '青',
    "source": '鬼灭之刃',
    "kind": 'cat',
    "colors": ['#26635B', '#5F9A8E', '#B6B9B8', '#C9A227', '#863434', '#36485F'],
    "dark": ['#003F38', '#377368', '#8E9190', '#9C7B00', '#5D0B14', '#12273C'],
    "light": ['#5D8A82', '#95C3B9', '#E3E5E5', '#F4CE73', '#A8635F', '#616E81'],
    "bg": '#F2F6F5',
    "bg2": '#DFE7E5',
    "ink": '#253633',
    "muted": '#7D8584',
    "seq": ['#F2F8F7', '#E1EBE9', '#CFDEDB', '#B9CDC9', '#A7C0BB', '#92B1AB', '#82A49E', '#719790', '#5F8A83', '#4E7E76', '#3B7169', '#27645C', '#215C54', '#1D564F', '#174F48', '#184842', '#19403C', '#193A36', '#193A36'],
    "div": ['#284843', '#315C56', '#3B7169', '#50857D', '#679A92', '#84AFA8', '#A3C5BE', '#C2D8D4', '#E1EBE9', '#F1E6E5', '#EFCBC8', '#E8B0AB', '#DB9590', '#CB7B77', '#B66562', '#A0504E', '#814240', '#643432', '#643432'],
    "flow": ['#DAF0E9', '#CDEEDF', '#BFEACE', '#B7E5B9', '#B6DFA2', '#B9D989', '#BFD272', '#C7C95E', '#B7BE66', '#AAB36F', '#9EA876', '#969D74', '#929169', '#8D865F', '#877B56', '#887351', '#8B6C4D', '#8E654B', '#8F5E4C', '#8F574E', '#8E4F52', '#8A4957', '#83445E', '#734362', '#624262', '#52425F', '#454059', '#3B3D50', '#333945', '#313741'],
    "cyclic": ['#CE817D', '#CB8473', '#C7876B', '#C08A64', '#B88E5F', '#B0925C', '#A6955C', '#9A995D', '#8D9C62', '#7F9F6A', '#6EA274', '#5DA481', '#4CA58E', '#3CA59A', '#2EA5A7', '#25A4B4', '#2DA3C0', '#41A0C8', '#589DCD', '#6B99CF', '#7D95CE', '#8C91CC', '#9A8EC7', '#A88AC1', '#B686B7', '#C183AB', '#CA809C', '#CE808E', '#CE8181', '#CE817D'],
    "wheel": [{'i': 0, 'L': 38.0, 'C': 21.8, 'h': 183.5}, {'i': 1, 'L': 59.4, 'C': 22.1, 'h': 179.4}, {'i': 2, 'L': 74.9, 'C': 1.2, 'h': 173.6}, {'i': 3, 'L': 68.3, 'C': 64.0, 'h': 87.4}, {'i': 4, 'L': 33.5, 'C': 39.6, 'h': 27.3}, {'i': 5, 'L': 30.0, 'C': 15.8, 'h': 268.7}],
    "ramp_stats": {'seq': {'L_range': 75.2, 'L_min': 21.9, 'L_max': 97.1, 'monotonic': True, 'total_dE': 99.6, 'uniformity': 0.537}, 'div': {'L_range': 67.9, 'L_min': 27.8, 'L_max': 95.7, 'monotonic': False, 'total_dE': 148.2, 'uniformity': 0.735}, 'flow': {'L_range': 70.2, 'L_min': 22.9, 'L_max': 93.1, 'monotonic': True, 'total_dE': 146.3, 'uniformity': 0.651}, 'cyclic': {'L_range': 0.4, 'L_min': 61.8, 'L_max': 62.2, 'monotonic': True, 'total_dE': 145.4, 'uniformity': 0.623}},
    "cvd_grade": 'B',
    "safe_set": [0, 1, 3],
    "orders": {'smooth': [0, 1, 2, 3, 4, 5], 'distinct': [0, 1, 4, 3, 5, 2], 'hue': [4, 3, 1, 0, 5, 2], 'light': [2, 3, 1, 0, 4, 5]},
    "min_de": 21.3,
    "cvd": {'protan': 11.3, 'deutan': 11.4, 'tritan': 10.9},
  },
  "haku-river": {
    "slug": 'haku-river',
    "zh": '白龙',
    "en": 'Haku',
    "tone_zh": '湖水',
    "tone_en": 'River Jade',
    "name_zh": '白龙 · 湖水',
    "name_en": 'Haku · River Jade',
    "family": '青',
    "source": '千与千寻',
    "kind": 'cat',
    "colors": ['#57C6D2', '#A1ADA7', '#558C8E', '#006272', '#434A45', '#C4483A'],
    "dark": ['#179DA9', '#7A8680', '#2D6668', '#003D48', '#222924', '#971B18'],
    "light": ['#A1F0F9', '#CFD8D4', '#8AB5B6', '#538895', '#6A706C', '#E57E6D'],
    "bg": '#F1F6F7',
    "bg2": '#DCE7E9',
    "ink": '#1A373A',
    "muted": '#798688',
    "seq": ['#EFF8F9', '#DFF0F2', '#CCE6E9', '#BCDEE2', '#ABD6DB', '#94CBD2', '#7FC2CA', '#67B7C1', '#4DAEB8', '#2BA3AF', '#21949F', '#168590', '#0B7983', '#006D76', '#006069', '#00525A', '#00474D', '#003B41', '#003B41'],
    "div": ['#054A50', '#045E66', '#01737D', '#278892', '#429EA7', '#6AB2BA', '#92C7CD', '#B8DADE', '#DDECED', '#F4E6E2', '#FBC8BD', '#F9AA9B', '#EE8C7B', '#E0705E', '#CB5948', '#B44335', '#91382C', '#702D24', '#702D24'],
    "flow": ['#BFF4FB', '#B9E8E3', '#B6D9CA', '#B6CBB6', '#ABBBA1', '#A1AB8B', '#9E9E77', '#A59769', '#AD8F5E', '#B68657', '#BE7D54', '#C67355', '#CC695A', '#D15E62', '#D3536D', '#D14A7C', '#C7488E', '#B2509B', '#9B57A4', '#835DA8', '#6D61A8', '#5663A4', '#3E659C', '#27648C', '#246179', '#285B66', '#295254', '#2D4844', '#2F3D36', '#2F3932'],
    "cyclic": ['#CE8275', '#C9856C', '#C38964', '#BC8D5F', '#B2905B', '#A9945A', '#9E985B', '#919B5F', '#829F66', '#71A270', '#5EA47D', '#4DA58B', '#39A699', '#28A6A6', '#1BA5B2', '#1EA4BD', '#34A1C8', '#4D9ECE', '#649AD1', '#7796D1', '#8793CF', '#968FCA', '#A48BC5', '#B287BB', '#BF83B0', '#C980A1', '#CF7F93', '#D07F84', '#CF8178', '#CE8275'],
    "wheel": [{'i': 0, 'L': 74.2, 'C': 32.0, 'h': 209.0}, {'i': 1, 'L': 69.6, 'C': 5.6, 'h': 163.1}, {'i': 2, 'L': 54.7, 'C': 18.8, 'h': 201.1}, {'i': 3, 'L': 37.8, 'C': 24.2, 'h': 221.3}, {'i': 4, 'L': 30.7, 'C': 4.5, 'h': 153.1}, {'i': 5, 'L': 47.9, 'C': 59.7, 'h': 35.4}],
    "ramp_stats": {'seq': {'L_range': 75.0, 'L_min': 22.0, 'L_max': 97.0, 'monotonic': True, 'total_dE': 102.2, 'uniformity': 0.655}, 'div': {'L_range': 67.8, 'L_min': 28.0, 'L_max': 95.8, 'monotonic': False, 'total_dE': 152.2, 'uniformity': 0.669}, 'flow': {'L_range': 70.0, 'L_min': 22.9, 'L_max': 92.9, 'monotonic': True, 'total_dE': 173.4, 'uniformity': 0.769}, 'cyclic': {'L_range': 0.5, 'L_min': 61.8, 'L_max': 62.2, 'monotonic': True, 'total_dE': 148.5, 'uniformity': 0.663}},
    "cvd_grade": 'B',
    "safe_set": [0, 1, 2, 3, 4, 5],
    "orders": {'smooth': [0, 1, 2, 3, 4, 5], 'distinct': [0, 2, 3, 5, 4, 1], 'hue': [5, 2, 0, 3, 1, 4], 'light': [0, 1, 2, 5, 3, 4]},
    "min_de": 17.3,
    "cvd": {'protan': 12.6, 'deutan': 14.6, 'tritan': 15.2},
  },
  "muichiro-mist": {
    "slug": 'muichiro-mist',
    "zh": '时透无一郎',
    "en": 'Muichiro',
    "tone_zh": '雾青',
    "tone_en": 'Mist Teal',
    "name_zh": '时透无一郎 · 雾青',
    "name_en": 'Muichiro · Mist Teal',
    "family": '青',
    "source": '鬼灭之刃',
    "kind": 'cat',
    "colors": ['#1F8C9C', '#2D5965', '#6E8C68', '#BAB6A8', '#8CC0C8', '#999ACA'],
    "dark": ['#006471', '#003642', '#496644', '#928E80', '#6398A0', '#7173A2'],
    "light": ['#70B4C1', '#5F7F89', '#9DB597', '#E6E2D7', '#C3EBF1', '#C6C6ED'],
    "bg": '#F1F6F7',
    "bg2": '#DDE7E9',
    "ink": '#1D363B',
    "muted": '#7A8688',
    "seq": ['#F0F8FA', '#DEEEF1', '#C7E0E5', '#B3D4DA', '#9BC6CE', '#82B8C2', '#69AAB6', '#509EAB', '#3291A1', '#1B8696', '#147C8A', '#0D7280', '#036673', '#005E6A', '#00545F', '#004B56', '#00434C', '#003B44', '#003B44'],
    "div": ['#364633', '#455A41', '#546F4F', '#688363', '#7E9879', '#96AD92', '#B1C3AD', '#CBD7C8', '#E5EAE4', '#E7E9ED', '#D2D2E3', '#BCBBD7', '#A4A3C7', '#8D8DB6', '#7778A3', '#63658F', '#515273', '#3F4059', '#3F4059'],
    "flow": ['#D4F0F5', '#CAE8E6', '#C2DED4', '#BFD4C2', '#BFCAB2', '#C0C1A5', '#C3BA9C', '#C7B496', '#CBAD90', '#CEA68D', '#D19F8D', '#D2988E', '#D19092', '#CD8A98', '#C3869F', '#B583A5', '#A582AA', '#9581AC', '#8680AC', '#777FAB', '#687EA7', '#597DA3', '#4D7497', '#41698B', '#365E7E', '#2D546D', '#2A4C5E', '#294450', '#2A3C42', '#2A393E'],
    "cyclic": ['#7F9E79', '#74A082', '#69A18B', '#60A295', '#59A2A0', '#56A1A9', '#57A0B2', '#5E9EB8', '#689CBD', '#739ABF', '#7E97C0', '#8895BF', '#9292BD', '#9C90B9', '#A68DB3', '#B189AC', '#B988A1', '#BF8696', '#C1878B', '#C08882', '#BD897A', '#BA8C75', '#B48E70', '#AF916D', '#A8946C', '#A0966C', '#98996D', '#8E9B71', '#839D77', '#7F9E79'],
    "wheel": [{'i': 0, 'L': 53.4, 'C': 29.0, 'h': 215.8}, {'i': 1, 'L': 35.3, 'C': 16.3, 'h': 225.3}, {'i': 2, 'L': 55.1, 'C': 23.9, 'h': 138.5}, {'i': 3, 'L': 74.0, 'C': 7.7, 'h': 97.9}, {'i': 4, 'L': 74.5, 'C': 17.8, 'h': 212.3}, {'i': 5, 'L': 65.1, 'C': 26.7, 'h': 292.2}],
    "ramp_stats": {'seq': {'L_range': 74.9, 'L_min': 22.1, 'L_max': 97.0, 'monotonic': True, 'total_dE': 105.1, 'uniformity': 0.594}, 'div': {'L_range': 67.8, 'L_min': 27.9, 'L_max': 95.7, 'monotonic': False, 'total_dE': 146.1, 'uniformity': 0.703}, 'flow': {'L_range': 70.1, 'L_min': 22.9, 'L_max': 93.0, 'monotonic': True, 'total_dE': 140.5, 'uniformity': 0.648}, 'cyclic': {'L_range': 0.5, 'L_min': 61.8, 'L_max': 62.3, 'monotonic': True, 'total_dE': 124.8, 'uniformity': 0.536}},
    "cvd_grade": 'B',
    "safe_set": [0, 1, 2, 3, 4],
    "orders": {'smooth': [0, 1, 2, 3, 4, 5], 'distinct': [0, 4, 1, 5, 2, 3], 'hue': [2, 4, 0, 1, 5, 3], 'light': [4, 3, 5, 2, 0, 1]},
    "min_de": 18.5,
    "cvd": {'protan': 10.5, 'deutan': 10.4, 'tritan': 12.1},
  },
  "rem-peacock": {
    "slug": 'rem-peacock',
    "zh": '蕾姆',
    "en": 'Rem',
    "tone_zh": '孔雀',
    "tone_en": 'Peacock Blue',
    "name_zh": '蕾姆 · 孔雀',
    "name_en": 'Rem · Peacock Blue',
    "family": '青',
    "source": 'Re:从零开始的异世界生活',
    "kind": 'cat',
    "colors": ['#46C3E0', '#B9B7B1', '#748F95', '#6479C2', '#256980', '#45464D'],
    "dark": ['#009AB5', '#918F89', '#4E696F', '#39549A', '#004458', '#24252C'],
    "light": ['#A6EBFF', '#E5E4DF', '#A3B9BE', '#97A3DF', '#6390A3', '#6C6C72'],
    "bg": '#F0F6F8',
    "bg2": '#DBE7EB',
    "ink": '#17373F',
    "muted": '#79868A',
    "seq": ['#EFF8FB', '#E1F1F6', '#D0E9F0', '#BCDFE9', '#A8D6E2', '#92CCDC', '#7BC2D5', '#60B7CD', '#3FADC6', '#07A3BE', '#0493AC', '#02849B', '#01768C', '#00697C', '#005C6D', '#005060', '#004653', '#003B47', '#003B47'],
    "div": ['#364067', '#445286', '#5165A7', '#6879BB', '#7F8ECE', '#9AA4DC', '#B5BBE8', '#CFD2F0', '#E7E8F5', '#EDE8E3', '#DFD2B9', '#CDBC92', '#B9A66F', '#A4904F', '#8E7B38', '#786723', '#62531E', '#4D411A', '#4D411A'],
    "flow": ['#F0EBDB', '#E7E6D0', '#DDE3C7', '#D1E0C1', '#C3DEBD', '#B2DBB9', '#A0D8B9', '#8CD5BB', '#7ECFBC', '#7CC3B6', '#7BB7AF', '#7AACA8', '#74A5A3', '#60A1A4', '#4B9CA7', '#3097AB', '#0092AF', '#008AAE', '#0083AE', '#007AA1', '#007195', '#1E6988', '#2C6179', '#335A6E', '#375265', '#384B5D', '#394555', '#383E4C', '#353842', '#353640'],
    "cyclic": ['#46A2B3', '#4CA0BB', '#589EC2', '#669BC5', '#7498C7', '#8195C6', '#8D92C4', '#998FC0', '#A58CBB', '#B189B3', '#BB86A7', '#C3849B', '#C7838E', '#C78483', '#C5867A', '#C18972', '#BC8C6C', '#B58F68', '#AE9265', '#A59565', '#9C9865', '#919B69', '#859D6F', '#789F78', '#69A282', '#5CA38E', '#52A399', '#49A3A5', '#46A3B0', '#46A2B3'],
    "wheel": [{'i': 0, 'L': 73.4, 'C': 35.1, 'h': 224.3}, {'i': 1, 'L': 74.4, 'C': 3.3, 'h': 96.7}, {'i': 2, 'L': 57.6, 'C': 10.3, 'h': 218.0}, {'i': 3, 'L': 52.1, 'C': 42.5, 'h': 287.0}, {'i': 4, 'L': 41.3, 'C': 23.1, 'h': 235.1}, {'i': 5, 'L': 29.9, 'C': 4.5, 'h': 285.6}],
    "ramp_stats": {'seq': {'L_range': 74.8, 'L_min': 22.2, 'L_max': 97.0, 'monotonic': True, 'total_dE': 102.2, 'uniformity': 0.636}, 'div': {'L_range': 67.8, 'L_min': 27.9, 'L_max': 95.7, 'monotonic': False, 'total_dE': 148.9, 'uniformity': 0.71}, 'flow': {'L_range': 70.2, 'L_min': 22.9, 'L_max': 93.0, 'monotonic': True, 'total_dE': 118.3, 'uniformity': 0.647}, 'cyclic': {'L_range': 0.5, 'L_min': 61.7, 'L_max': 62.2, 'monotonic': True, 'total_dE': 133.8, 'uniformity': 0.604}},
    "cvd_grade": 'A',
    "safe_set": [0, 1, 2, 3, 4, 5],
    "orders": {'smooth': [0, 1, 2, 3, 4, 5], 'distinct': [0, 2, 4, 5, 3, 1], 'hue': [0, 4, 3, 1, 2, 5], 'light': [1, 0, 2, 3, 4, 5]},
    "min_de": 18.2,
    "cvd": {'protan': 14.1, 'deutan': 13.6, 'tritan': 8.2},
  },
  "gojo-sky": {
    "slug": 'gojo-sky',
    "zh": '五条悟',
    "en": 'Gojo',
    "tone_zh": '晴空蓝',
    "tone_en": 'Six-Eyes Sky',
    "name_zh": '五条悟 · 晴空蓝',
    "name_en": 'Gojo · Six-Eyes Sky',
    "family": '蓝',
    "source": '咒术回战',
    "kind": 'cat',
    "colors": ['#1394CE', '#85BEDC', '#B3B6B9', '#7F8995', '#296AA4', '#424754'],
    "dark": ['#006C99', '#5B96B3', '#8B8E91', '#59636F', '#004675', '#212632'],
    "light": ['#79BDEC', '#C1E9FF', '#E0E2E5', '#ABB3BD', '#6C92C2', '#696D78'],
    "bg": '#F1F5F9',
    "bg2": '#DDE6EF',
    "ink": '#1C3546',
    "muted": '#7B858E',
    "seq": ['#F0F7FE', '#E1EDFA', '#D0E4F5', '#BFD9F0', '#B0D0EC', '#9DC5E7', '#87BAE1', '#6BADDB', '#4BA0D4', '#1C95CF', '#0E88BE', '#087CAE', '#0471A0', '#00658F', '#005A81', '#004F71', '#004463', '#003954', '#003954'],
    "div": ['#034765', '#025B81', '#006F9D', '#2B84B4', '#4799C9', '#70AED9', '#97C3E5', '#BCD7EE', '#DFEAF5', '#EFE7E5', '#EACEBE', '#E0B59A', '#D09C7A', '#BE845C', '#A86F47', '#925B33', '#774A2A', '#5C3A22', '#5C3A22'],
    "flow": ['#D4EFFF', '#CBE7F9', '#C4DFF2', '#BCD7EA', '#B4CEE1', '#ACC6DB', '#9EC1DD', '#8FBCDE', '#7CB6E0', '#67B0E2', '#4BAAE4', '#41A3DD', '#4F9BCF', '#5894C2', '#5E8DB5', '#6386A8', '#65809C', '#657B93', '#5C7490', '#536F8E', '#48688B', '#3D6189', '#325A85', '#345379', '#364D6D', '#374762', '#374257', '#353D4D', '#343844', '#333741'],
    "cyclic": ['#579EC0', '#659CC4', '#7299C6', '#7E96C6', '#8A93C4', '#9690C1', '#A28DBC', '#AD8AB4', '#B887AB', '#C1859F', '#C58492', '#C68487', '#C5867D', '#C28875', '#BC8B6E', '#B68E69', '#AF9167', '#A89465', '#9F9766', '#959A68', '#899C6D', '#7C9F75', '#6EA17F', '#61A38B', '#56A396', '#4CA3A1', '#48A3AC', '#4AA2B6', '#539FBE', '#579EC0'],
    "wheel": [{'i': 0, 'L': 57.8, 'C': 40.3, 'h': 253.8}, {'i': 1, 'L': 74.2, 'C': 23.5, 'h': 242.4}, {'i': 2, 'L': 73.9, 'C': 1.9, 'h': 255.8}, {'i': 3, 'L': 56.7, 'C': 7.7, 'h': 262.2}, {'i': 4, 'L': 43.4, 'C': 37.1, 'h': 269.7}, {'i': 5, 'L': 30.2, 'C': 8.5, 'h': 278.0}],
    "ramp_stats": {'seq': {'L_range': 74.7, 'L_min': 22.2, 'L_max': 96.9, 'monotonic': True, 'total_dE': 95.8, 'uniformity': 0.746}, 'div': {'L_range': 67.8, 'L_min': 27.9, 'L_max': 95.7, 'monotonic': False, 'total_dE': 150.6, 'uniformity': 0.725}, 'flow': {'L_range': 69.9, 'L_min': 23.1, 'L_max': 93.0, 'monotonic': True, 'total_dE': 110.6, 'uniformity': 0.69}, 'cyclic': {'L_range': 0.6, 'L_min': 61.7, 'L_max': 62.3, 'monotonic': True, 'total_dE': 132.9, 'uniformity': 0.603}},
    "cvd_grade": 'B',
    "safe_set": [0, 1, 3, 4, 5],
    "orders": {'smooth': [0, 1, 2, 3, 4, 5], 'distinct': [0, 1, 4, 5, 3, 2], 'hue': [1, 0, 4, 2, 3, 5], 'light': [1, 2, 0, 3, 4, 5]},
    "min_de": 14.9,
    "cvd": {'protan': 11.9, 'deutan': 13.5, 'tritan': 11.0},
  },
  "rei-pale-blue": {
    "slug": 'rei-pale-blue',
    "zh": '绫波丽',
    "en": 'Rei',
    "tone_zh": '苍白蓝',
    "tone_en": 'Pale Blue',
    "name_zh": '绫波丽 · 苍白蓝',
    "name_en": 'Rei · Pale Blue',
    "family": '蓝',
    "source": '新世纪福音战士',
    "kind": 'cat',
    "colors": ['#82BFDC', '#3D7CA0', '#7F949F', '#B5B8B9', '#E8873A', '#C5394A'],
    "dark": ['#5797B3', '#00577A', '#596E78', '#8D9091', '#BB600C', '#980029'],
    "light": ['#C0EAFF', '#79A4C2', '#AEBEC7', '#E2E4E5', '#FFBD8F', '#E47479'],
    "bg": '#F2F5F7',
    "bg2": '#DFE6EA',
    "ink": '#24353D',
    "muted": '#7D8589',
    "seq": ['#F2F7FA', '#E3EEF3', '#D4E4EC', '#C4DAE5', '#B3CFDD', '#A2C4D6', '#92BACF', '#7FAFC7', '#6CA4BF', '#5A98B3', '#4E8AA5', '#437E98', '#38738C', '#2D667D', '#275A6F', '#204F61', '#1B4454', '#153947', '#153947'],
    "div": ['#254655', '#2D5A6E', '#346F88', '#4C839C', '#6598AF', '#83ADC1', '#A3C3D2', '#C3D7E1', '#E2EAEF', '#F4E6DE', '#F5CCB0', '#EFB185', '#E1965F', '#D07C3C', '#BA6722', '#A35207', '#84430B', '#66350D', '#66350D'],
    "flow": ['#D8EFF6', '#C4E3F1', '#B4D9ED', '#A3CEE8', '#8AC8E9', '#66C6E8', '#27C5E5', '#00BFD4', '#00BAC2', '#00B5B1', '#00B0A5', '#00AAAC', '#00A5B2', '#009FB7', '#0098BD', '#2491BE', '#4B8AB5', '#5D84AC', '#687EA2', '#717A97', '#6E718D', '#676785', '#625C7B', '#5E5172', '#614867', '#643F5B', '#64364C', '#622E3D', '#5E282E', '#5B2629'],
    "cyclic": ['#D57D7F', '#D38073', '#CE8369', '#C88760', '#C08B5A', '#B79056', '#AC9354', '#A09854', '#929B58', '#829F5F', '#70A36B', '#5AA579', '#44A788', '#2AA797', '#05A7A5', '#00A6B3', '#00A4C0', '#16A2CD', '#3D9ED4', '#5B9BD7', '#7297D7', '#8493D4', '#958ED0', '#A58ACA', '#B485C0', '#C381B3', '#CE7DA3', '#D47C93', '#D57D84', '#D57D7F'],
    "wheel": [{'i': 0, 'L': 74.3, 'C': 24.0, 'h': 239.4}, {'i': 1, 'L': 49.4, 'C': 26.9, 'h': 250.5}, {'i': 2, 'L': 60.1, 'C': 9.7, 'h': 239.0}, {'i': 3, 'L': 74.6, 'C': 1.2, 'h': 225.5}, {'i': 4, 'L': 65.6, 'C': 63.5, 'h': 60.5}, {'i': 5, 'L': 46.0, 'C': 60.6, 'h': 22.3}],
    "ramp_stats": {'seq': {'L_range': 74.9, 'L_min': 22.1, 'L_max': 96.9, 'monotonic': True, 'total_dE': 104.1, 'uniformity': 0.564}, 'div': {'L_range': 67.9, 'L_min': 27.8, 'L_max': 95.7, 'monotonic': False, 'total_dE': 154.2, 'uniformity': 0.709}, 'flow': {'L_range': 70.1, 'L_min': 22.9, 'L_max': 93.0, 'monotonic': True, 'total_dE': 138.1, 'uniformity': 0.652}, 'cyclic': {'L_range': 0.5, 'L_min': 61.8, 'L_max': 62.3, 'monotonic': True, 'total_dE': 156.3, 'uniformity': 0.692}},
    "cvd_grade": 'B',
    "safe_set": [0, 1, 2, 3, 4, 5],
    "orders": {'smooth': [0, 1, 2, 3, 4, 5], 'distinct': [0, 2, 1, 5, 4, 3], 'hue': [5, 4, 0, 1, 3, 2], 'light': [3, 0, 4, 2, 1, 5]},
    "min_de": 13.8,
    "cvd": {'protan': 12.4, 'deutan': 13.5, 'tritan': 14.0},
  },
  "ayaka-frost": {
    "slug": 'ayaka-frost',
    "zh": '神里绫华',
    "en": 'Ayaka',
    "tone_zh": '霜蓝',
    "tone_en": 'Frost Blue',
    "name_zh": '神里绫华 · 霜蓝',
    "name_en": 'Ayaka · Frost Blue',
    "family": '蓝',
    "source": '原神',
    "kind": 'cat',
    "colors": ['#73BDFD', '#B5B7B9', '#C8657D', '#A497C6', '#6C889E', '#2B5C8C'],
    "dark": ['#4095D3', '#8D8F91', '#9E3D58', '#7C709E', '#466278', '#003962'],
    "light": ['#CFE6FF', '#E2E3E5', '#E997A8', '#CFC4EA', '#9CB2C4', '#6583AB'],
    "bg": '#F2F5F9',
    "bg2": '#DFE6EF',
    "ink": '#213446',
    "muted": '#7D858E',
    "seq": ['#F2F7FE', '#E4EEFB', '#D5E4F7', '#C7DBF4', '#BAD3F1', '#ACCBED', '#9AC1E9', '#85B5E4', '#6DA9E0', '#509DDA', '#3F8ECA', '#3082BA', '#2076AC', '#07699D', '#045C8B', '#024F79', '#014368', '#003858', '#003858'],
    "div": ['#194565', '#185983', '#126DA3', '#3981B7', '#5896CA', '#7CABD9', '#9FC1E5', '#C1D5EE', '#E1EAF5', '#F1E6EB', '#F0CAD2', '#EAAEB9', '#DD92A1', '#CE778B', '#BA6176', '#A44B62', '#843F4F', '#66323E', '#66323E'],
    "flow": ['#DEEDFA', '#D3E8FB', '#C6E2FD', '#B7DBFE', '#A5D4FF', '#92CCFF', '#8BC1F8', '#8CB7EC', '#8CADE1', '#8BA4D6', '#869CCA', '#7C94BE', '#758EB3', '#6D87A6', '#67809B', '#627A93', '#5F7492', '#5D6E91', '#5C688F', '#5D618D', '#605A89', '#635485', '#654C7E', '#594A79', '#4D4772', '#42446A', '#384161', '#303D58', '#2A394E', '#29384B'],
    "cyclic": ['#CB8190', '#CC8284', '#CA8479', '#C68670', '#C08A68', '#B98D63', '#B29160', '#A8945F', '#9E9860', '#929B63', '#849E69', '#75A173', '#65A37F', '#54A48C', '#45A599', '#39A5A5', '#33A4B1', '#38A2BC', '#47A0C5', '#5A9CCA', '#6B99CC', '#7B96CC', '#8993CA', '#968FC6', '#A28CC1', '#AF88BA', '#BB85AF', '#C482A2', '#CA8194', '#CB8190'],
    "wheel": [{'i': 0, 'L': 74.3, 'C': 39.0, 'h': 262.2}, {'i': 1, 'L': 74.3, 'C': 1.3, 'h': 255.7}, {'i': 2, 'L': 55.1, 'C': 42.1, 'h': 6.9}, {'i': 3, 'L': 65.0, 'C': 26.6, 'h': 302.5}, {'i': 4, 'L': 55.3, 'C': 15.6, 'h': 253.3}, {'i': 5, 'L': 38.0, 'C': 31.4, 'h': 269.9}],
    "ramp_stats": {'seq': {'L_range': 75.0, 'L_min': 22.1, 'L_max': 97.0, 'monotonic': True, 'total_dE': 93.9, 'uniformity': 0.663}, 'div': {'L_range': 67.9, 'L_min': 27.9, 'L_max': 95.8, 'monotonic': False, 'total_dE': 146.4, 'uniformity': 0.732}, 'flow': {'L_range': 70.0, 'L_min': 23.0, 'L_max': 93.0, 'monotonic': True, 'total_dE': 107.4, 'uniformity': 0.644}, 'cyclic': {'L_range': 0.5, 'L_min': 61.8, 'L_max': 62.3, 'monotonic': True, 'total_dE': 141.4, 'uniformity': 0.638}},
    "cvd_grade": 'B',
    "safe_set": [0, 1, 4, 5],
    "orders": {'smooth': [0, 1, 2, 3, 4, 5], 'distinct': [0, 4, 5, 3, 2, 1], 'hue': [2, 4, 0, 5, 3, 1], 'light': [1, 0, 3, 4, 2, 5]},
    "min_de": 18.3,
    "cvd": {'protan': 9.2, 'deutan': 9.6, 'tritan': 8.5},
  },
  "ganyu-glacier": {
    "slug": 'ganyu-glacier',
    "zh": '甘雨',
    "en": 'Ganyu',
    "tone_zh": '冰蓝',
    "tone_en": 'Glacier Blue',
    "name_zh": '甘雨 · 冰蓝',
    "name_en": 'Ganyu · Glacier Blue',
    "family": '蓝',
    "source": '原神',
    "kind": 'cat',
    "colors": ['#5586CB', '#9BBADF', '#8A8F96', '#C34759', '#766987', '#33466E'],
    "dark": ['#2061A3', '#7292B6', '#646970', '#981836', '#514562', '#08254A'],
    "light": ['#91B0E8', '#D2E6FF', '#B6BABF', '#E37E86', '#9E93AC', '#606C8E'],
    "bg": '#F3F5FA',
    "bg2": '#E1E5EF',
    "ink": '#273347',
    "muted": '#7F848F',
    "seq": ['#F3F6FE', '#E5EBF9', '#D6DFF4', '#C8D4F0', '#B9C8EA', '#A9BCE5', '#98B0DF', '#86A4DA', '#7397D3', '#5F8BCE', '#4E7FC2', '#4273B4', '#3869A8', '#2C5F9B', '#25538A', '#204979', '#1B3E69', '#17355A', '#17355A'],
    "div": ['#334456', '#40576F', '#4E6A8A', '#637E9E', '#7993B1', '#94A9C3', '#B0BFD4', '#CAD5E3', '#E5E9F0', '#F5E5E7', '#F9C8CA', '#F6AAAE', '#EB8C93', '#DD6F7A', '#C85765', '#B24151', '#903642', '#6F2C34', '#6F2C34'],
    "flow": ['#DEECFF', '#D3E3F9', '#C5D5EB', '#BBCBE2', '#B0C3DD', '#A4BDDF', '#96B6E2', '#86ADE5', '#74A5E7', '#6C9CE8', '#7395E4', '#7B8EDF', '#8287DA', '#8980D4', '#9079CE', '#9771C6', '#9D68BE', '#A35FB4', '#9460AC', '#8460A4', '#775F9A', '#6B5D8F', '#625B84', '#5A5878', '#55566E', '#4C4E64', '#43465A', '#3A3F52', '#34394A', '#313747'],
    "cyclic": ['#CE8086', '#CD827B', '#C98571', '#C38869', '#BD8C63', '#B4905F', '#AB935D', '#A1965D', '#959A60', '#879E65', '#77A06F', '#66A37B', '#55A589', '#44A596', '#36A5A3', '#2CA4AF', '#2DA3BB', '#3DA1C5', '#519DCC', '#679ACE', '#7797CE', '#8593CD', '#9390C9', '#9F8DC5', '#AD89BE', '#B985B4', '#C482A7', '#CB8099', '#CE808B', '#CE8086'],
    "wheel": [{'i': 0, 'L': 55.4, 'C': 40.9, 'h': 275.8}, {'i': 1, 'L': 74.5, 'C': 22.0, 'h': 264.9}, {'i': 2, 'L': 59.2, 'C': 4.4, 'h': 264.9}, {'i': 3, 'L': 48.0, 'C': 53.4, 'h': 17.9}, {'i': 4, 'L': 46.6, 'C': 18.6, 'h': 307.8}, {'i': 5, 'L': 29.9, 'C': 26.0, 'h': 281.3}],
    "ramp_stats": {'seq': {'L_range': 75.0, 'L_min': 21.8, 'L_max': 96.9, 'monotonic': True, 'total_dE': 86.7, 'uniformity': 0.696}, 'div': {'L_range': 67.9, 'L_min': 27.9, 'L_max': 95.8, 'monotonic': False, 'total_dE': 152.2, 'uniformity': 0.695}, 'flow': {'L_range': 69.8, 'L_min': 23.1, 'L_max': 92.9, 'monotonic': True, 'total_dE': 109.0, 'uniformity': 0.675}, 'cyclic': {'L_range': 0.5, 'L_min': 61.8, 'L_max': 62.2, 'monotonic': True, 'total_dE': 145.1, 'uniformity': 0.657}},
    "cvd_grade": 'A',
    "safe_set": [0, 1, 2, 3, 4, 5],
    "orders": {'smooth': [0, 1, 2, 3, 4, 5], 'distinct': [0, 1, 5, 4, 3, 2], 'hue': [3, 1, 0, 5, 4, 2], 'light': [1, 2, 0, 3, 4, 5]},
    "min_de": 16.5,
    "cvd": {'protan': 14.0, 'deutan': 14.1, 'tritan': 15.5},
  },
  "link-champion": {
    "slug": 'link-champion',
    "zh": '林克',
    "en": 'Link',
    "tone_zh": '苍蓝',
    "tone_en": 'Champion Blue',
    "name_zh": '林克 · 苍蓝',
    "name_en": 'Link · Champion Blue',
    "family": '蓝',
    "source": '塞尔达传说',
    "kind": 'cat',
    "colors": ['#327EBF', '#9ABAD4', '#98958A', '#D0B560', '#7E5F40', '#354862'],
    "dark": ['#005990', '#7292AB', '#716F64', '#A58D38', '#583C1E', '#10273F'],
    "light": ['#7AA7DC', '#CDE6FB', '#C2C0B7', '#FBE29E', '#A4886F', '#616E84'],
    "bg": '#F2F5FA',
    "bg2": '#E0E6EF',
    "ink": '#233447',
    "muted": '#7E848F',
    "seq": ['#F2F7FE', '#E2EBF8', '#D2DFF2', '#C2D3ED', '#B0C6E6', '#9CB8DF', '#89ACD8', '#759FD1', '#6093CB', '#4887C4', '#307CBC', '#2572B0', '#1968A4', '#085E97', '#025488', '#054A78', '#064169', '#07375A', '#07375A'],
    "div": ['#1F4467', '#225786', '#236BA7', '#427FBB', '#5F94CE', '#81A9DC', '#A3C0E8', '#C3D5F0', '#E2E9F5', '#EBE9E2', '#DFD3B6', '#CEBC8D', '#BAA56A', '#A58F49', '#8F7A31', '#7A671B', '#645318', '#4E4115', '#4E4115'],
    "flow": ['#FDE9BA', '#EEE8B8', '#DDE5B9', '#CBE1BB', '#B9DBBF', '#ABD3C3', '#A1C9C1', '#9ABDAD', '#95B09A', '#92A48A', '#80A085', '#6A9E86', '#529A8A', '#349790', '#039398', '#008D9D', '#0086A1', '#007FA5', '#0E77A8', '#3670A2', '#486A9B', '#556492', '#5D5E89', '#64587D', '#67516E', '#5B4C65', '#4C475D', '#3F4153', '#343A47', '#313742'],
    "cyclic": ['#B78E66', '#B09163', '#A89462', '#9E9763', '#949B66', '#879D6B', '#78A074', '#6AA27F', '#5BA38B', '#4EA497', '#44A4A3', '#3EA3AE', '#41A2B9', '#4CA0C1', '#5C9CC7', '#6D9AC9', '#7B97C9', '#8893C7', '#9590C4', '#A18DBF', '#AE8AB7', '#B986AD', '#C383A1', '#C88293', '#C98387', '#C8847C', '#C58774', '#C08A6D', '#BA8D68', '#B78E66'],
    "wheel": [{'i': 0, 'L': 51.1, 'C': 40.7, 'h': 268.3}, {'i': 1, 'L': 74.0, 'C': 17.3, 'h': 253.6}, {'i': 2, 'L': 61.7, 'C': 6.3, 'h': 98.5}, {'i': 3, 'L': 74.4, 'C': 46.4, 'h': 91.1}, {'i': 4, 'L': 42.7, 'C': 24.1, 'h': 69.5}, {'i': 5, 'L': 30.1, 'C': 17.6, 'h': 271.0}],
    "ramp_stats": {'seq': {'L_range': 75.0, 'L_min': 22.0, 'L_max': 97.0, 'monotonic': True, 'total_dE': 88.2, 'uniformity': 0.718}, 'div': {'L_range': 67.9, 'L_min': 27.9, 'L_max': 95.8, 'monotonic': False, 'total_dE': 147.7, 'uniformity': 0.717}, 'flow': {'L_range': 70.0, 'L_min': 22.9, 'L_max': 92.9, 'monotonic': True, 'total_dE': 149.1, 'uniformity': 0.641}, 'cyclic': {'L_range': 0.5, 'L_min': 61.8, 'L_max': 62.3, 'monotonic': True, 'total_dE': 137.6, 'uniformity': 0.647}},
    "cvd_grade": 'A',
    "safe_set": [0, 1, 2, 3, 4, 5],
    "orders": {'smooth': [0, 1, 2, 3, 4, 5], 'distinct': [0, 1, 3, 4, 5, 2], 'hue': [4, 3, 1, 0, 5, 2], 'light': [3, 1, 2, 0, 4, 5]},
    "min_de": 21.0,
    "cvd": {'protan': 20.2, 'deutan': 20.0, 'tritan': 17.4},
  },
  "taki-night-indigo": {
    "slug": 'taki-night-indigo',
    "zh": '泷',
    "en": 'Taki',
    "tone_zh": '夜靛',
    "tone_en": 'Night Indigo',
    "name_zh": '泷 · 夜靛',
    "name_en": 'Taki · Night Indigo',
    "family": '蓝',
    "source": '你的名字',
    "kind": 'cat',
    "colors": ['#1F467E', '#5F6471', '#5B86B2', '#9DB9E5', '#96999C', '#C46E5A'],
    "dark": ['#002550', '#3C414D', '#30618B', '#7491BC', '#707275', '#994836'],
    "light": ['#586C9B', '#888C97', '#91AFD3', '#D6E5FF', '#C2C4C7', '#E79E8C'],
    "bg": '#F4F5F9',
    "bg2": '#E3E5EE',
    "ink": '#2B3245',
    "muted": '#81838D',
    "seq": ['#F4F6FD', '#E4E8F4', '#D7DCEC', '#C7CEE3', '#BAC2DC', '#AAB4D2', '#9BA6C9', '#8A98BF', '#7A8AB6', '#6B7EAE', '#5C72A6', '#4A659C', '#375892', '#305188', '#28487D', '#26406E', '#253960', '#243455', '#243455'],
    "div": ['#2D445B', '#385776', '#436B92', '#597FA7', '#7194BA', '#8EA9CB', '#ABC0DA', '#C8D5E7', '#E4E9F2', '#F2E6E6', '#F0CCC4', '#E8B1A4', '#D99686', '#C97C6B', '#B46755', '#9E5242', '#804436', '#63362B', '#63362B'],
    "flow": ['#E1ECFF', '#D3E2FB', '#C7D7EF', '#BCCCE4', '#B3C4DC', '#AFBEDE', '#AEB7DF', '#B0AFDF', '#B4A7DD', '#BA9FD9', '#C196D3', '#C88DCB', '#CB85C4', '#BB85C5', '#AB84C4', '#9C84C3', '#8E83C0', '#7F81BC', '#7180B5', '#637DAE', '#5A78A3', '#597095', '#576888', '#54607B', '#515A70', '#4C5467', '#434B60', '#3B4359', '#313A51', '#2D374E'],
    "cyclic": ['#C48778', '#C08A71', '#BA8C6B', '#B49067', '#AB9265', '#A39665', '#9A9966', '#8F9C6A', '#829E71', '#74A07A', '#66A285', '#59A391', '#4FA39C', '#47A3A7', '#46A2B2', '#4DA1BB', '#599EC2', '#689BC6', '#7698C7', '#8195C6', '#8D92C4', '#998FC0', '#A58DBB', '#B189B2', '#BB86A8', '#C2849C', '#C7838F', '#C78484', '#C5867A', '#C48778'],
    "wheel": [{'i': 0, 'L': 29.9, 'C': 36.4, 'h': 281.1}, {'i': 1, 'L': 42.4, 'C': 8.0, 'h': 277.3}, {'i': 2, 'L': 54.5, 'C': 27.8, 'h': 265.1}, {'i': 3, 'L': 74.5, 'C': 25.1, 'h': 271.5}, {'i': 4, 'L': 63.1, 'C': 2.0, 'h': 255.9}, {'i': 5, 'L': 55.7, 'C': 41.3, 'h': 39.1}],
    "ramp_stats": {'seq': {'L_range': 75.0, 'L_min': 21.9, 'L_max': 96.9, 'monotonic': True, 'total_dE': 94.3, 'uniformity': 0.617}, 'div': {'L_range': 67.9, 'L_min': 28.0, 'L_max': 95.8, 'monotonic': False, 'total_dE': 150.2, 'uniformity': 0.735}, 'flow': {'L_range': 70.0, 'L_min': 23.1, 'L_max': 93.1, 'monotonic': True, 'total_dE': 113.6, 'uniformity': 0.687}, 'cyclic': {'L_range': 0.5, 'L_min': 61.7, 'L_max': 62.3, 'monotonic': True, 'total_dE': 133.7, 'uniformity': 0.581}},
    "cvd_grade": 'A',
    "safe_set": [0, 1, 2, 3, 4, 5],
    "orders": {'smooth': [0, 1, 2, 3, 4, 5], 'distinct': [0, 2, 1, 3, 5, 4], 'hue': [5, 2, 3, 0, 4, 1], 'light': [3, 4, 5, 2, 1, 0]},
    "min_de": 16.9,
    "cvd": {'protan': 15.9, 'deutan': 15.9, 'tritan': 15.7},
  },
  "cloud-soldier": {
    "slug": 'cloud-soldier',
    "zh": '克劳德',
    "en": 'Cloud',
    "tone_zh": '军蓝',
    "tone_en": 'Soldier Blue',
    "name_zh": '克劳德 · 军蓝',
    "name_en": 'Cloud · Soldier Blue',
    "family": '蓝',
    "source": '最终幻想VII',
    "kind": 'cat',
    "colors": ['#294771', '#6B5A48', '#6882A5', '#34C3F9', '#B6B8BB', '#D0B55C'],
    "dark": ['#00264C', '#473726', '#415D7E', '#0099C8', '#8E9093', '#A58D34'],
    "light": ['#5B6D90', '#918273', '#98ACC8', '#C0E8FF', '#E3E5E7', '#FBE29B'],
    "bg": '#F4F5F8',
    "bg2": '#E3E5EC',
    "ink": '#2C3341',
    "muted": '#81848B',
    "seq": ['#F4F6FC', '#E4E8F1', '#D3D8E6', '#C1C8DA', '#B1BACF', '#9EAAC3', '#8E9BB7', '#808FAE', '#7082A5', '#62769C', '#546A93', '#435D88', '#3A557F', '#334D75', '#2E466C', '#2B3F5F', '#293A57', '#27354E', '#27354E'],
    "div": ['#354356', '#43566F', '#526989', '#677D9D', '#7D92B1', '#96A8C3', '#B2BED4', '#CCD4E2', '#E5E9EF', '#ECE9E0', '#DFD3B4', '#CFBC8B', '#BBA567', '#A68F46', '#907A2D', '#7A6716', '#645315', '#4E4113', '#4E4113'],
    "flow": ['#E1ECFB', '#D0E8FD', '#BEE6FE', '#A8E4FC', '#8DE1F7', '#73DFEE', '#5BDDE2', '#45DAD4', '#25D4D3', '#00CEDA', '#00C6DE', '#00BEE3', '#00B6E7', '#12ADEA', '#3AA4E6', '#4F98D2', '#5A8EC0', '#6084AE', '#637B9F', '#687497', '#6C6E8E', '#6E6785', '#6F6078', '#6D586A', '#67505C', '#594958', '#4B4254', '#403E50', '#32394B', '#2E3749'],
    "cyclic": ['#B68F62', '#AE9260', '#A5955F', '#9A9861', '#8E9C65', '#809F6D', '#70A277', '#60A383', '#51A490', '#43A59D', '#39A4A8', '#36A3B4', '#3DA2BE', '#4E9FC6', '#609CCA', '#7099CC', '#7E95CB', '#8D92C9', '#9A8FC5', '#A78BBE', '#B487B6', '#BF83AA', '#C7829C', '#CB818E', '#CC8283', '#C98478', '#C5876F', '#BF8A69', '#B88E63', '#B68F62'],
    "wheel": [{'i': 0, 'L': 29.8, 'C': 27.7, 'h': 276.5}, {'i': 1, 'L': 39.4, 'C': 13.6, 'h': 73.1}, {'i': 2, 'L': 53.6, 'C': 21.6, 'h': 269.1}, {'i': 3, 'L': 73.9, 'C': 41.8, 'h': 242.6}, {'i': 4, 'L': 74.7, 'C': 1.8, 'h': 265.8}, {'i': 5, 'L': 74.3, 'C': 48.3, 'h': 91.5}],
    "ramp_stats": {'seq': {'L_range': 74.8, 'L_min': 22.0, 'L_max': 96.9, 'monotonic': True, 'total_dE': 101.5, 'uniformity': 0.595}, 'div': {'L_range': 67.9, 'L_min': 28.0, 'L_max': 95.8, 'monotonic': False, 'total_dE': 152.6, 'uniformity': 0.719}, 'flow': {'L_range': 70.0, 'L_min': 23.0, 'L_max': 93.0, 'monotonic': True, 'total_dE': 136.9, 'uniformity': 0.667}, 'cyclic': {'L_range': 0.5, 'L_min': 61.8, 'L_max': 62.2, 'monotonic': True, 'total_dE': 141.2, 'uniformity': 0.642}},
    "cvd_grade": 'A',
    "safe_set": [0, 1, 2, 3, 4, 5],
    "orders": {'smooth': [0, 1, 2, 3, 4, 5], 'distinct': [0, 2, 3, 5, 1, 4], 'hue': [1, 5, 3, 2, 0, 4], 'light': [4, 5, 3, 2, 1, 0]},
    "min_de": 21.6,
    "cvd": {'protan': 17.7, 'deutan': 17.7, 'tritan': 20.8},
  },
  "ichika-leoneed": {
    "slug": 'ichika-leoneed',
    "zh": '星乃一歌',
    "en": 'Ichika',
    "tone_zh": '电光蓝',
    "tone_en": 'Leo/need Blue',
    "name_zh": '星乃一歌 · 电光蓝',
    "name_en": 'Ichika · Leo/need Blue',
    "family": '蓝',
    "source": '世界计划',
    "kind": 'cat',
    "colors": ['#3C50D7', '#0096D8', '#B4B7C1', '#31CE95', '#D9B30D', '#D64F52'],
    "dark": ['#0030A1', '#006EA1', '#8C8F99', '#00A371', '#AA8C00', '#A9212F'],
    "light": ['#7F7BE9', '#7ABFF5', '#E1E4EC', '#8DF7C8', '#FFE08F', '#F68783'],
    "bg": '#F6F4FD',
    "bg2": '#E7E3F7',
    "ink": '#302E57',
    "muted": '#858197',
    "seq": ['#F7F5FF', '#EEEBFD', '#E4DFFB', '#D9D2F9', '#CBC3F6', '#BDB5F4', '#AEA5F1', '#9F96ED', '#8F88E9', '#7F7AE5', '#6E6EE1', '#5C61DD', '#4554D8', '#344ACC', '#2841BD', '#2239A7', '#24328F', '#242C77', '#242C77'],
    "div": ['#004769', '#005A85', '#006EA1', '#2883B9', '#4398D0', '#6EADDE', '#96C3EA', '#BBD7F1', '#DFEAF6', '#EEE8DB', '#E6D2A3', '#D8BB6F', '#C3A43F', '#AC8E0D', '#947905', '#7D6600', '#675300', '#514100', '#514100'],
    "flow": ['#E6EBFB', '#E6E2FF', '#EDD9FF', '#FDCCFD', '#FFC4E2', '#FFBCC8', '#FFB4AF', '#FFAE97', '#FFA77B', '#FFA159', '#F1A245', '#DDA43B', '#C9A634', '#B3A732', '#9BA635', '#80A63E', '#62A34C', '#3CA05C', '#009B6D', '#00937C', '#008B85', '#00838C', '#007B91', '#007196', '#00679F', '#1E5DA7', '#41549F', '#46478D', '#373670', '#323166'],
    "cyclic": ['#F86667', '#F26C54', '#EA7444', '#DF7C35', '#D38428', '#C58B1C', '#B69214', '#A59814', '#919D1C', '#79A32B', '#59A840', '#24AC58', '#00AB76', '#00A98E', '#00A8A0', '#00A6B1', '#00A4C2', '#00A1D5', '#009DEE', '#3B97FF', '#6991FF', '#888AFA', '#A483F2', '#BE7AE5', '#D56FD2', '#E966B9', '#F6609E', '#FB6084', '#F9646D', '#F86667'],
    "wheel": [{'i': 0, 'L': 40.6, 'C': 80.8, 'h': 297.9}, {'i': 1, 'L': 58.8, 'C': 43.8, 'h': 257.7}, {'i': 2, 'L': 74.5, 'C': 5.5, 'h': 279.3}, {'i': 3, 'L': 74.2, 'C': 55.7, 'h': 162.0}, {'i': 4, 'L': 74.2, 'C': 75.0, 'h': 89.7}, {'i': 5, 'L': 52.4, 'C': 59.6, 'h': 26.9}],
    "ramp_stats": {'seq': {'L_range': 75.0, 'L_min': 22.0, 'L_max': 96.9, 'monotonic': True, 'total_dE': 86.7, 'uniformity': 0.684}, 'div': {'L_range': 67.5, 'L_min': 28.2, 'L_max': 95.7, 'monotonic': False, 'total_dE': 152.9, 'uniformity': 0.663}, 'flow': {'L_range': 70.0, 'L_min': 23.1, 'L_max': 93.1, 'monotonic': True, 'total_dE': 191.5, 'uniformity': 0.772}, 'cyclic': {'L_range': 0.4, 'L_min': 61.8, 'L_max': 62.2, 'monotonic': True, 'total_dE': 197.6, 'uniformity': 0.805}},
    "cvd_grade": 'A',
    "safe_set": [0, 1, 2, 3, 4, 5],
    "orders": {'smooth': [0, 1, 2, 3, 4, 5], 'distinct': [0, 1, 4, 5, 3, 2], 'hue': [5, 4, 3, 1, 0, 2], 'light': [2, 4, 3, 1, 5, 0]},
    "min_de": 25.1,
    "cvd": {'protan': 16.1, 'deutan': 16.0, 'tritan': 12.7},
  },
  "raiden-electro": {
    "slug": 'raiden-electro',
    "zh": '雷电将军',
    "en": 'Raiden',
    "tone_zh": '雷紫',
    "tone_en": 'Electro Violet',
    "name_zh": '雷电将军 · 雷紫',
    "name_en": 'Raiden · Electro Violet',
    "family": '紫',
    "source": '原神',
    "kind": 'cat',
    "colors": ['#886CD4', '#BDA5F0', '#B6B2BD', '#A16D8D', '#5C3F8E', '#484552'],
    "dark": ['#5F47AC', '#947DC7', '#8E8A95', '#7A4867', '#351D69', '#272430'],
    "light": ['#B49AEE', '#E5D7FF', '#E2DFE8', '#C59AB4', '#846AAA', '#6E6C76'],
    "bg": '#F6F4FB',
    "bg2": '#E8E3F2',
    "ink": '#372D4C',
    "muted": '#878191',
    "seq": ['#F9F5FF', '#F0E9FC', '#E6DCF8', '#DBCEF4', '#CFBFF0', '#C3B0EB', '#B6A0E6', '#A991E1', '#9C82DC', '#8F74D7', '#8368CE', '#785EC1', '#6D54B4', '#624BA7', '#574296', '#4D3A84', '#423273', '#392B63', '#392B63'],
    "div": ['#483970', '#5C4892', '#7058B5', '#866CCA', '#9C82DC', '#B39AE8', '#C8B4F2', '#DBCDF6', '#EDE6F8', '#EBE8E0', '#D6D6AF', '#BFC282', '#A5AC5A', '#8D9735', '#77821D', '#626E01', '#505A04', '#3F4606', '#3F4606'],
    "flow": ['#EEE8F8', '#EAE2F9', '#E6DAF9', '#E0D3FA', '#DACAFB', '#D3C0FB', '#CCB7FC', '#C4ACFC', '#BBA2FC', '#B297FC', '#A98DFC', '#A886EC', '#A681DB', '#A37CCA', '#9E77BB', '#9973AC', '#92709E', '#8A6A97', '#816394', '#795D91', '#6E568F', '#64508D', '#5A4B83', '#524675', '#4C4369', '#463F5D', '#413B52', '#3C3848', '#393742', '#38363F'],
    "cyclic": ['#998DCF', '#A68ACA', '#B585C1', '#C280B5', '#CD7DA6', '#D47B95', '#D67C85', '#D57E78', '#D1816B', '#CB8562', '#C3895B', '#BA8E56', '#AF9253', '#A49752', '#979B56', '#879E5C', '#74A166', '#60A474', '#48A684', '#2DA793', '#09A7A2', '#00A6AF', '#00A5BD', '#00A2CB', '#379FD4', '#579BD8', '#6F97D8', '#8393D6', '#948FD1', '#998DCF'],
    "wheel": [{'i': 0, 'L': 52.6, 'C': 60.7, 'h': 304.6}, {'i': 1, 'L': 72.2, 'C': 41.7, 'h': 304.6}, {'i': 2, 'L': 73.2, 'C': 6.2, 'h': 304.5}, {'i': 3, 'L': 52.3, 'C': 27.3, 'h': 340.5}, {'i': 4, 'L': 33.5, 'C': 50.0, 'h': 307.9}, {'i': 5, 'L': 30.0, 'C': 8.4, 'h': 300.2}],
    "ramp_stats": {'seq': {'L_range': 75.2, 'L_min': 21.9, 'L_max': 97.1, 'monotonic': True, 'total_dE': 83.3, 'uniformity': 0.676}, 'div': {'L_range': 67.6, 'L_min': 28.0, 'L_max': 95.6, 'monotonic': False, 'total_dE': 150.2, 'uniformity': 0.64}, 'flow': {'L_range': 69.7, 'L_min': 23.1, 'L_max': 92.9, 'monotonic': True, 'total_dE': 101.5, 'uniformity': 0.651}, 'cyclic': {'L_range': 0.6, 'L_min': 61.7, 'L_max': 62.3, 'monotonic': True, 'total_dE': 157.9, 'uniformity': 0.707}},
    "cvd_grade": 'A',
    "safe_set": [0, 1, 2, 3, 4, 5],
    "orders": {'smooth': [0, 1, 2, 3, 4, 5], 'distinct': [0, 1, 4, 5, 3, 2], 'hue': [0, 1, 4, 3, 2, 5], 'light': [2, 1, 0, 3, 4, 5]},
    "min_de": 17.6,
    "cvd": {'protan': 15.4, 'deutan': 15.5, 'tritan': 6.3},
  },
  "eva01-violet-lime": {
    "slug": 'eva01-violet-lime',
    "zh": '初号机',
    "en": 'EVA-01',
    "tone_zh": '紫萤',
    "tone_en": 'Violet & Lime',
    "name_zh": '初号机 · 紫萤',
    "name_en": 'EVA-01 · Violet & Lime',
    "family": '紫',
    "source": '新世纪福音战士',
    "kind": 'cat',
    "colors": ['#824CC5', '#503F64', '#A989D6', '#B9B4C0', '#7F8E4F', '#83CA20'],
    "dark": ['#58259D', '#2D1E41', '#8163AE', '#918C98', '#58682A', '#609F00'],
    "light": ['#AA7CDD', '#756785', '#D2B7F6', '#E5E1EB', '#ACB784', '#C0F478'],
    "bg": '#F8F3FB',
    "bg2": '#EBE2F3',
    "ink": '#3C2B4F',
    "muted": '#8A8093',
    "seq": ['#FAF4FF', '#F2E8FB', '#EADBF8', '#E1CCF3', '#D6BDEE', '#CBADE9', '#C09CE3', '#B48CDD', '#A97DD8', '#9D6ED2', '#915FCC', '#8651C7', '#7A46BB', '#6F3DAD', '#63349F', '#572F8B', '#4C2978', '#432568', '#432568'],
    "div": ['#523375', '#694099', '#814EBE', '#9763D3', '#AC79E4', '#C093EF', '#D3AFF7', '#E3CAFA', '#F0E5FA', '#EBE7EF', '#D5D2D9', '#BFBCC3', '#A9A5AE', '#938F99', '#7E7A84', '#6A6770', '#57535B', '#444147', '#444147'],
    "flow": ['#D4F7A0', '#E4ED9A', '#EEE399', '#F6DA9B', '#F9D1A0', '#F9CAA8', '#F2C3AF', '#E5BDB8', '#E1B2B1', '#E6A2A6', '#E98F9D', '#EA7B94', '#DF777E', '#D2746C', '#C4725D', '#B4704F', '#A46E45', '#A76543', '#AB5B46', '#AD514B', '#AE4753', '#AC3D5D', '#A6356A', '#9B3278', '#8A3386', '#6F3877', '#593865', '#493755', '#3E3547', '#3B3443'],
    "cyclic": ['#879F3F', '#73A34A', '#55A75B', '#29AA70', '#00AA87', '#00A999', '#00A7A9', '#00A5B8', '#00A3C9', '#00A0DC', '#219CF1', '#5896F1', '#7791EE', '#908CE8', '#A785E0', '#BA7FD5', '#CE77C5', '#DE71AF', '#E86D98', '#EB6E83', '#EA7170', '#E57660', '#DE7C53', '#D48247', '#C9883E', '#BD8E37', '#B09335', '#A09936', '#8E9E3B', '#879F3F'],
    "wheel": [{'i': 0, 'L': 44.2, 'C': 72.4, 'h': 310.6}, {'i': 1, 'L': 29.9, 'C': 24.7, 'h': 309.5}, {'i': 2, 'L': 62.7, 'C': 44.5, 'h': 308.1}, {'i': 3, 'L': 74.0, 'C': 6.8, 'h': 306.4}, {'i': 4, 'L': 56.5, 'C': 35.5, 'h': 116.7}, {'i': 5, 'L': 74.3, 'C': 83.0, 'h': 123.7}],
    "ramp_stats": {'seq': {'L_range': 74.9, 'L_min': 22.0, 'L_max': 96.9, 'monotonic': True, 'total_dE': 83.7, 'uniformity': 0.711}, 'div': {'L_range': 67.8, 'L_min': 28.0, 'L_max': 95.7, 'monotonic': False, 'total_dE': 147.9, 'uniformity': 0.689}, 'flow': {'L_range': 70.1, 'L_min': 23.0, 'L_max': 93.0, 'monotonic': True, 'total_dE': 168.6, 'uniformity': 0.737}, 'cyclic': {'L_range': 0.4, 'L_min': 61.8, 'L_max': 62.2, 'monotonic': True, 'total_dE': 183.7, 'uniformity': 0.754}},
    "cvd_grade": 'A',
    "safe_set": [0, 1, 2, 3, 4, 5],
    "orders": {'smooth': [0, 1, 2, 3, 4, 5], 'distinct': [0, 2, 1, 5, 4, 3], 'hue': [4, 5, 2, 1, 0, 3], 'light': [5, 3, 2, 4, 0, 1]},
    "min_de": 19.2,
    "cvd": {'protan': 17.5, 'deutan': 17.5, 'tritan': 11.7},
  },
  "howl-iridescent": {
    "slug": 'howl-iridescent',
    "zh": '哈尔',
    "en": 'Howl',
    "tone_zh": '金蓝虹',
    "tone_en": 'Iridescent Gold',
    "name_zh": '哈尔 · 金蓝虹',
    "name_en": 'Howl · Iridescent Gold',
    "family": '粉',
    "source": '哈尔的移动城堡',
    "kind": 'cat',
    "colors": ['#DF72A6', '#C0B7A5', '#977900', '#578B6C', '#77BDE0', '#346595'],
    "dark": ['#B5497F', '#988F7D', '#6B5500', '#316548', '#4A95B7', '#00426D'],
    "light": ['#FFA7CE', '#EBE4D5', '#C1A353', '#8AB39A', '#BCE7FF', '#6E8CB4'],
    "bg": '#FAF3F6',
    "bg2": '#F1E1E7',
    "ink": '#482937',
    "muted": '#907F86',
    "seq": ['#FFF3F8', '#FDE8F1', '#FBDBE8', '#F8CDDF', '#F5BFD5', '#F1AFCB', '#EC9EC0', '#E78DB6', '#E27BAB', '#D76CA0', '#C76092', '#BA5586', '#AC4A7B', '#9D406F', '#8C3762', '#7B3056', '#6B284A', '#5A203D', '#5A203D'],
    "div": ['#2C445F', '#36577B', '#416A98', '#587EAC', '#7093BF', '#8DA9CF', '#ABBFDE', '#C8D5E9', '#E4E9F2', '#EEE8DF', '#E4D2AF', '#D5BB82', '#C1A45A', '#AB8E35', '#95791D', '#7F6601', '#685204', '#514006', '#514006'],
    "flow": ['#F2EADB', '#E5E4CE', '#D5DFC4', '#C2DBBF', '#ACD6BD', '#94D2C0', '#77CDC4', '#58C7CB', '#27C2D4', '#00B9DA', '#00B0DE', '#00A7E4', '#299EE9', '#5397E2', '#6A90D9', '#7A8AD1', '#8683C7', '#917DBA', '#9976AB', '#9D6F99', '#9C6688', '#945884', '#8B497F', '#7C3E7C', '#67407A', '#534175', '#41406B', '#323D5E', '#2A3A50', '#29384B'],
    "cyclic": ['#AB9359', '#A1975A', '#949B5D', '#869E63', '#76A16C', '#64A379', '#52A587', '#40A695', '#2DA6A2', '#1CA5AF', '#1AA4BB', '#2EA2C6', '#489FCD', '#5D9BD1', '#7298D1', '#8394D0', '#9290CC', '#A18CC6', '#AF88BE', '#BC84B3', '#C780A5', '#CE7F96', '#D17F88', '#D0807C', '#CC8371', '#C78768', '#C08A61', '#B88E5D', '#AE925A', '#AB9359'],
    "wheel": [{'i': 0, 'L': 62.1, 'C': 49.0, 'h': 350.3}, {'i': 1, 'L': 74.7, 'C': 10.3, 'h': 89.4}, {'i': 2, 'L': 52.1, 'C': 57.9, 'h': 88.3}, {'i': 3, 'L': 53.6, 'C': 27.0, 'h': 155.5}, {'i': 4, 'L': 73.3, 'C': 27.5, 'h': 242.3}, {'i': 5, 'L': 41.5, 'C': 31.2, 'h': 268.6}],
    "ramp_stats": {'seq': {'L_range': 74.8, 'L_min': 22.1, 'L_max': 96.9, 'monotonic': True, 'total_dE': 82.7, 'uniformity': 0.666}, 'div': {'L_range': 67.9, 'L_min': 27.9, 'L_max': 95.8, 'monotonic': False, 'total_dE': 151.1, 'uniformity': 0.695}, 'flow': {'L_range': 69.9, 'L_min': 23.0, 'L_max': 92.9, 'monotonic': True, 'total_dE': 155.4, 'uniformity': 0.733}, 'cyclic': {'L_range': 0.4, 'L_min': 61.8, 'L_max': 62.2, 'monotonic': True, 'total_dE': 148.8, 'uniformity': 0.648}},
    "cvd_grade": 'A',
    "safe_set": [0, 1, 2, 3, 4, 5],
    "orders": {'smooth': [0, 1, 2, 3, 4, 5], 'distinct': [0, 5, 2, 4, 3, 1], 'hue': [2, 3, 4, 5, 0, 1], 'light': [1, 4, 0, 3, 2, 5]},
    "min_de": 26.5,
    "cvd": {'protan': 15.0, 'deutan': 14.9, 'tritan': 12.3},
  },
  "violet-evergarden": {
    "slug": 'violet-evergarden',
    "zh": '薇尔莉特',
    "en": 'Violet',
    "tone_zh": '紫罗兰',
    "tone_en": 'Violet Bloom',
    "name_zh": '薇尔莉特 · 紫罗兰',
    "name_en": 'Violet · Violet Bloom',
    "family": '紫',
    "source": '紫罗兰永恒花园',
    "kind": 'cat',
    "colors": ['#916F95', '#633373', '#3684D7', '#DBA1E7', '#BBB6AE', '#D7B258'],
    "dark": ['#6B4A6F', '#3E0E4F', '#005FA5', '#B179BE', '#938E86', '#AC8A2F'],
    "light": ['#B79BBA', '#865F92', '#82ADF1', '#F9D7FF', '#E7E3DC', '#FFDF9E'],
    "bg": '#F7F4F7',
    "bg2": '#E9E4E9',
    "ink": '#392F3B',
    "muted": '#888288',
    "seq": ['#F9F5F9', '#ECE5ED', '#E0D4E1', '#D3C3D4', '#C5B2C7', '#B9A2BC', '#AC92AF', '#A183A5', '#96759A', '#8C6B90', '#836287', '#7A5A7D', '#715274', '#664968', '#5C425F', '#533C56', '#4A354C', '#412F43', '#412F43'],
    "div": ['#1C4370', '#1C5692', '#166AB5', '#3D7EC9', '#5D93DB', '#81A8E7', '#A4BEF1', '#C4D4F6', '#E2E9F8', '#EDE8E2', '#E3D2B4', '#D4BB8A', '#C0A365', '#AC8D43', '#96782A', '#806511', '#685212', '#514011', '#514011'],
    "flow": ['#F3EADB', '#F3E4CC', '#F2DBBB', '#F2D3A9', '#F2C994', '#F3BE80', '#F4B576', '#F7AE77', '#F9A77A', '#FAA17C', '#FA9A80', '#F99484', '#F78D89', '#F3888F', '#EE8295', '#E87D9C', '#DE759F', '#D36EA1', '#C768A4', '#BA62A6', '#AC5FA7', '#9F5A9A', '#93578C', '#87547E', '#7A5071', '#6E4D66', '#62445D', '#553C55', '#48324C', '#443049'],
    "cyclic": ['#B19249', '#A49749', '#969B4D', '#849F54', '#6FA360', '#57A670', '#38A881', '#07A993', '#00A8A2', '#00A6B0', '#00A4BE', '#00A2CE', '#1CA0DD', '#4E9BE0', '#6B96E0', '#8192DD', '#948DD8', '#A588D1', '#B783C7', '#C57EBB', '#D279AA', '#DA7797', '#DD7785', '#DC7A76', '#D87D69', '#D2825E', '#C98755', '#C08C4E', '#B5914A', '#B19249'],
    "wheel": [{'i': 0, 'L': 51.3, 'C': 25.6, 'h': 322.8}, {'i': 1, 'L': 30.1, 'C': 43.3, 'h': 319.5}, {'i': 2, 'L': 54.2, 'C': 49.6, 'h': 275.1}, {'i': 3, 'L': 73.8, 'C': 42.8, 'h': 321.0}, {'i': 4, 'L': 74.2, 'C': 4.7, 'h': 85.9}, {'i': 5, 'L': 74.2, 'C': 50.3, 'h': 86.6}],
    "ramp_stats": {'seq': {'L_range': 74.8, 'L_min': 22.2, 'L_max': 96.9, 'monotonic': True, 'total_dE': 93.0, 'uniformity': 0.648}, 'div': {'L_range': 67.9, 'L_min': 27.9, 'L_max': 95.8, 'monotonic': False, 'total_dE': 150.6, 'uniformity': 0.697}, 'flow': {'L_range': 69.9, 'L_min': 23.1, 'L_max': 93.0, 'monotonic': True, 'total_dE': 115.1, 'uniformity': 0.584}, 'cyclic': {'L_range': 0.5, 'L_min': 61.7, 'L_max': 62.3, 'monotonic': True, 'total_dE': 167.7, 'uniformity': 0.71}},
    "cvd_grade": 'B',
    "safe_set": [0, 1, 2, 3, 4, 5],
    "orders": {'smooth': [0, 1, 2, 3, 4, 5], 'distinct': [0, 3, 1, 5, 2, 4], 'hue': [5, 2, 1, 3, 0, 4], 'light': [4, 5, 3, 2, 0, 1]},
    "min_de": 20.2,
    "cvd": {'protan': 13.0, 'deutan': 14.3, 'tritan': 10.1},
  },
  "nezuko-crimson-pink": {
    "slug": 'nezuko-crimson-pink',
    "zh": '祢豆子',
    "en": 'Nezuko',
    "tone_zh": '绯粉',
    "tone_en": 'Crimson Pink',
    "name_zh": '祢豆子 · 绯粉',
    "name_en": 'Nezuko · Crimson Pink',
    "family": '粉',
    "source": '鬼灭之刃',
    "kind": 'cat',
    "colors": ['#E93F6E', '#F1A0B9', '#C8B4A1', '#E4703C', '#903159', '#4F4449'],
    "dark": ['#B9004A', '#C77891', '#9F8C7A', '#B74815', '#680037', '#2D2328'],
    "light": ['#FF869C', '#FFDAE4', '#F2E1D2', '#FFA780', '#B0647F', '#746B6F'],
    "bg": '#FEF2F4',
    "bg2": '#F8E0E2',
    "ink": '#53232D',
    "muted": '#987D80',
    "seq": ['#FFF4F5', '#FFE9EC', '#FFDDE1', '#FFCDD3', '#FFBDC6', '#FFABB8', '#FD98A8', '#F98399', '#F46E8A', '#EE577B', '#E83E6D', '#D93363', '#CA2759', '#BA184F', '#A70D45', '#920C3C', '#7E0B33', '#6B0A2B', '#6B0A2B'],
    "div": ['#7A2038', '#9E2447', '#C42757', '#DB446B', '#EF5F80', '#F98298', '#FEA5B3', '#FFC5CC', '#FEE2E5', '#E6EAE7', '#BADBD1', '#90C9BA', '#69B4A2', '#42A08B', '#278B76', '#017663', '#056051', '#074B3F', '#074B3F'],
    "flow": ['#F7E9DC', '#F7E1D0', '#F7D8C6', '#F8CFBD', '#F9C5B4', '#F9BBAE', '#FAB1A9', '#FCA69A', '#FE9B8A', '#FF8F78', '#FE8364', '#FB7650', '#F86B50', '#F56152', '#F05754', '#EB4C57', '#E54159', '#DE375C', '#CE395D', '#BD3C5E', '#AC3D5D', '#9C3E5B', '#8B3F58', '#7B3E53', '#6C3C4E', '#5F3A49', '#543844', '#4A363F', '#42343B', '#403439'],
    "cyclic": ['#E07589', '#E07779', '#DD7A6B', '#D77F5F', '#D08455', '#C7884D', '#BC8E48', '#B09345', '#A29745', '#939C49', '#80A052', '#6AA45F', '#4EA770', '#29A982', '#00A995', '#00A7A4', '#00A6B2', '#00A4C1', '#00A2D2', '#1C9FE3', '#509AE4', '#6E95E3', '#8591E0', '#998CDA', '#AC86D2', '#BE7FC5', '#CE7AB5', '#DA76A2', '#DF758F', '#E07589'],
    "wheel": [{'i': 0, 'L': 54.0, 'C': 68.4, 'h': 11.0}, {'i': 1, 'L': 74.4, 'C': 33.4, 'h': 359.2}, {'i': 2, 'L': 74.5, 'C': 13.0, 'h': 71.7}, {'i': 3, 'L': 60.3, 'C': 64.0, 'h': 49.5}, {'i': 4, 'L': 35.7, 'C': 43.8, 'h': 357.0}, {'i': 5, 'L': 30.1, 'C': 5.8, 'h': 347.3}],
    "ramp_stats": {'seq': {'L_range': 75.0, 'L_min': 22.0, 'L_max': 97.0, 'monotonic': True, 'total_dE': 86.3, 'uniformity': 0.659}, 'div': {'L_range': 68.0, 'L_min': 27.9, 'L_max': 95.9, 'monotonic': False, 'total_dE': 153.3, 'uniformity': 0.696}, 'flow': {'L_range': 70.0, 'L_min': 23.1, 'L_max': 93.1, 'monotonic': True, 'total_dE': 109.9, 'uniformity': 0.693}, 'cyclic': {'L_range': 0.5, 'L_min': 61.8, 'L_max': 62.3, 'monotonic': True, 'total_dE': 171.9, 'uniformity': 0.743}},
    "cvd_grade": 'C',
    "safe_set": [0, 1, 3, 4],
    "orders": {'smooth': [0, 1, 2, 3, 4, 5], 'distinct': [0, 1, 3, 4, 5, 2], 'hue': [0, 3, 2, 4, 1, 5], 'light': [2, 1, 3, 0, 4, 5]},
    "min_de": 19.7,
    "cvd": {'protan': 7.2, 'deutan': 7.3, 'tritan': 7.1},
  },
  "march7-sakura-ice": {
    "slug": 'march7-sakura-ice',
    "zh": '三月七',
    "en": 'March 7th',
    "tone_zh": '樱冰',
    "tone_en": 'Sakura Ice',
    "name_zh": '三月七 · 樱冰',
    "name_en": 'March 7th · Sakura Ice',
    "family": '粉',
    "source": '崩坏：星穹铁道',
    "kind": 'cat',
    "colors": ['#DF81AA', '#A64575', '#8D7B82', '#BAB8B9', '#78BDDD', '#3E6B9E'],
    "dark": ['#B55983', '#7D1A51', '#67565D', '#929091', '#4B95B4', '#034778'],
    "light": ['#FFB4D3', '#C6789B', '#B5A6AB', '#E6E5E5', '#B9E7FF', '#7693BD'],
    "bg": '#FAF3F6',
    "bg2": '#EFE2E7',
    "ink": '#462B36',
    "muted": '#8F8085',
    "seq": ['#FEF4F8', '#FBE8F0', '#F7DCE7', '#F4CFDE', '#EFBFD3', '#EAB1C8', '#E4A0BC', '#DF90B1', '#D980A6', '#CD7299', '#BE668D', '#B15B81', '#A45076', '#96466B', '#853E5F', '#753553', '#652D47', '#55243B', '#55243B'],
    "div": ['#214757', '#265B70', '#2B6F8B', '#44839F', '#5F98B3', '#7FADC4', '#A1C3D5', '#C1D7E3', '#E1EAF0', '#F0E6EC', '#EDCAD8', '#E5AFC4', '#D893AF', '#C8789B', '#B46286', '#9F4D72', '#80405D', '#633348', '#633348'],
    "flow": ['#F9E6F0', '#F3DDED', '#EBD4EB', '#E1CDEA', '#D5C6E9', '#C9C0E9', '#C6B9E7', '#C9B1E2', '#CDA8DC', '#D19FD4', '#D596CA', '#DA8DC0', '#DD84B3', '#D57EA8', '#C57B9E', '#B67895', '#A9768D', '#9E7486', '#927180', '#8C6A7C', '#85647A', '#7D5D78', '#755776', '#6B5175', '#644A6E', '#624363', '#5E3B57', '#59344C', '#532E40', '#512B3C'],
    "cyclic": ['#46A0C4', '#579DCA', '#699ACC', '#7997CC', '#8893CA', '#9590C7', '#A28CC2', '#AF88BA', '#BB85AF', '#C482A2', '#CA8195', '#CC8187', '#CB837D', '#C88673', '#C3896B', '#BD8C65', '#B49061', '#AB935F', '#A19660', '#969962', '#8A9D67', '#7BA06F', '#6BA27A', '#5AA487', '#4BA594', '#3EA5A0', '#35A4AC', '#35A3B7', '#3FA1C1', '#46A0C4'],
    "wheel": [{'i': 0, 'L': 65.2, 'C': 41.7, 'h': 351.9}, {'i': 1, 'L': 43.7, 'C': 45.8, 'h': 350.6}, {'i': 2, 'L': 53.4, 'C': 8.3, 'h': 351.3}, {'i': 3, 'L': 75.0, 'C': 0.9, 'h': 343.7}, {'i': 4, 'L': 73.3, 'C': 26.4, 'h': 239.6}, {'i': 5, 'L': 44.2, 'C': 32.3, 'h': 271.2}],
    "ramp_stats": {'seq': {'L_range': 75.1, 'L_min': 22.0, 'L_max': 97.0, 'monotonic': True, 'total_dE': 84.1, 'uniformity': 0.639}, 'div': {'L_range': 67.7, 'L_min': 28.1, 'L_max': 95.7, 'monotonic': False, 'total_dE': 149.2, 'uniformity': 0.702}, 'flow': {'L_range': 70.0, 'L_min': 23.0, 'L_max': 93.0, 'monotonic': True, 'total_dE': 104.4, 'uniformity': 0.729}, 'cyclic': {'L_range': 0.5, 'L_min': 61.8, 'L_max': 62.3, 'monotonic': True, 'total_dE': 141.6, 'uniformity': 0.645}},
    "cvd_grade": 'C',
    "safe_set": [0, 5],
    "orders": {'smooth': [0, 1, 2, 3, 4, 5], 'distinct': [0, 2, 4, 5, 1, 3], 'hue': [4, 5, 1, 0, 3, 2], 'light': [3, 4, 0, 2, 5, 1]},
    "min_de": 19.7,
    "cvd": {'protan': 9.6, 'deutan': 6.3, 'tritan': 19.9},
  },
  "aerith-rose-sage": {
    "slug": 'aerith-rose-sage',
    "zh": '爱丽丝',
    "en": 'Aerith',
    "tone_zh": '玫粉鼠尾草',
    "tone_en": 'Rose & Sage',
    "name_zh": '爱丽丝 · 玫粉鼠尾草',
    "name_en": 'Aerith · Rose & Sage',
    "family": '粉',
    "source": '最终幻想VII',
    "kind": 'cat',
    "colors": ['#C95B7C', '#ECA8BA', '#9E9698', '#408E52', '#775D4C', '#AF212B'],
    "dark": ['#9F3257', '#C28092', '#777072', '#0E672E', '#523A2A', '#790012'],
    "light": ['#E98FA6', '#FFDFE7', '#C8C1C3', '#7BB684', '#9D8678', '#CF605A'],
    "bg": '#FBF3F5',
    "bg2": '#F2E1E5',
    "ink": '#4A2931',
    "muted": '#917F83',
    "seq": ['#FFF4F6', '#FCE7EB', '#F8D9DF', '#F3C9D2', '#EEB8C4', '#E7A7B6', '#E195A8', '#DA839A', '#D3728D', '#CB6180', '#C05475', '#B44B6C', '#A84363', '#993858', '#8A314E', '#792B45', '#6A253B', '#5B2033', '#5B2033'],
    "div": ['#214A2A', '#286035', '#2E7640', '#458A54', '#5E9F69', '#7DB385', '#9EC8A3', '#BFDBC2', '#DFECE1', '#F1E6E6', '#F2C9D1', '#EEACBB', '#E28FA4', '#D3738E', '#BF5C79', '#AA4765', '#893B52', '#6A2F40', '#6A2F40'],
    "flow": ['#FFE4EB', '#FED8E1', '#F0CCD4', '#E3C0C8', '#DFB7C0', '#E2ACB8', '#E7A0AF', '#EB92A5', '#EE829A', '#EE778B', '#E7747C', '#E1736F', '#D97262', '#D17156', '#C7714C', '#BE7143', '#B4713A', '#AA7132', '#9F712C', '#9A6A33', '#956439', '#8D5F3F', '#845A43', '#7A5647', '#6E534A', '#694A43', '#653F38', '#62352F', '#5E2A26', '#5C2623'],
    "cyclic": ['#D87995', '#DA7A85', '#D97C77', '#D57F6B', '#CF8361', '#C88759', '#BF8C53', '#B4914F', '#A8954E', '#9B9950', '#8B9D55', '#79A15E', '#64A46C', '#4BA67C', '#2DA88D', '#04A89C', '#00A7AA', '#00A6B8', '#00A4C6', '#0EA1D6', '#449DDB', '#6398DC', '#7994DA', '#8C90D7', '#9E8BD1', '#AF86C9', '#BF80BC', '#CD7CAD', '#D57A9B', '#D87995'],
    "wheel": [{'i': 0, 'L': 53.3, 'C': 47.1, 'h': 3.7}, {'i': 1, 'L': 75.7, 'C': 27.6, 'h': 1.7}, {'i': 2, 'L': 62.8, 'C': 3.3, 'h': 360.0}, {'i': 3, 'L': 53.0, 'C': 45.2, 'h': 146.6}, {'i': 4, 'L': 41.6, 'C': 16.0, 'h': 60.0}, {'i': 5, 'L': 38.5, 'C': 64.0, 'h': 29.6}],
    "ramp_stats": {'seq': {'L_range': 75.1, 'L_min': 21.9, 'L_max': 97.1, 'monotonic': True, 'total_dE': 86.2, 'uniformity': 0.663}, 'div': {'L_range': 68.0, 'L_min': 27.8, 'L_max': 95.8, 'monotonic': False, 'total_dE': 149.0, 'uniformity': 0.694}, 'flow': {'L_range': 70.0, 'L_min': 22.9, 'L_max': 92.9, 'monotonic': True, 'total_dE': 121.6, 'uniformity': 0.655}, 'cyclic': {'L_range': 0.5, 'L_min': 61.8, 'L_max': 62.3, 'monotonic': True, 'total_dE': 163.3, 'uniformity': 0.71}},
    "cvd_grade": 'B',
    "safe_set": [0, 1, 5],
    "orders": {'smooth': [0, 1, 2, 3, 4, 5], 'distinct': [0, 1, 5, 3, 4, 2], 'hue': [1, 0, 5, 4, 3, 2], 'light': [1, 2, 0, 3, 4, 5]},
    "min_de": 19.9,
    "cvd": {'protan': 9.1, 'deutan': 9.1, 'tritan': 15.7},
  },
  "acheron-magenta": {
    "slug": 'acheron-magenta',
    "zh": '黄泉',
    "en": 'Acheron',
    "tone_zh": '洋红雷',
    "tone_en": 'Nihility Magenta',
    "name_zh": '黄泉 · 洋红雷',
    "name_en": 'Acheron · Nihility Magenta',
    "family": '粉',
    "source": '崩坏：星穹铁道',
    "kind": 'cat',
    "colors": ['#C93DA1', '#4A435C', '#8C3A47', '#F09ED0', '#989699', '#D8B35B'],
    "dark": ['#9D007A', '#282239', '#641226', '#C675A7', '#727072', '#AD8B33'],
    "light": ['#E77CC3', '#706A7F', '#AD6970', '#FFDAEF', '#C3C1C4', '#FFE1A3'],
    "bg": '#FBF3F8',
    "bg2": '#F3E0EB',
    "ink": '#4C253F',
    "muted": '#937E8B',
    "seq": ['#FFF3FA', '#FDE8F4', '#FADBED', '#F6CDE7', '#F2BCDE', '#EDABD5', '#E899CC', '#E287C2', '#DB74B9', '#D562B0', '#CE4EA8', '#C63B9F', '#B73091', '#A92485', '#9A1878', '#851768', '#721559', '#61134C', '#61134C'],
    "div": ['#44404F', '#575266', '#6B657D', '#807891', '#958DA5', '#AAA3B8', '#C1BBCC', '#D6D2DD', '#EAE8ED', '#EFE8DF', '#E3D2B4', '#D3BB8B', '#C0A366', '#AC8D44', '#96782B', '#806514', '#685213', '#514012', '#514012'],
    "flow": ['#FFE8BE', '#FFE0BA', '#FFD8B6', '#FFD0B3', '#FFC7B0', '#FFBFAE', '#FFB6AD', '#FFADAD', '#F1A6AC', '#DFA0AA', '#CE9AA7', '#BD96A2', '#BD8E9E', '#C2859B', '#C77998', '#CD6C95', '#D15B92', '#D64790', '#D03A8A', '#BC3F7F', '#A94275', '#97446C', '#864463', '#77435F', '#68415C', '#5A3F58', '#4F3D52', '#443A4B', '#3C3744', '#393540'],
    "cyclic": ['#DD7784', '#DC7A75', '#D87D68', '#D1825D', '#CA8755', '#BF8C4E', '#B5914A', '#A89549', '#9A9A4B', '#899E51', '#75A25C', '#5DA56B', '#41A77D', '#15A98E', '#00A89E', '#00A6AC', '#00A5BB', '#00A3CA', '#00A0DB', '#459CE0', '#6697E0', '#7D93DD', '#918ED9', '#A389D3', '#B484C9', '#C47EBC', '#D07AAD', '#D9779C', '#DD778A', '#DD7784'],
    "wheel": [{'i': 0, 'L': 49.9, 'C': 68.8, 'h': 339.5}, {'i': 1, 'L': 30.0, 'C': 16.3, 'h': 302.8}, {'i': 2, 'L': 36.1, 'C': 37.4, 'h': 15.0}, {'i': 3, 'L': 74.5, 'C': 39.8, 'h': 341.0}, {'i': 4, 'L': 62.3, 'C': 1.9, 'h': 314.7}, {'i': 5, 'L': 74.6, 'C': 49.3, 'h': 86.4}],
    "ramp_stats": {'seq': {'L_range': 74.9, 'L_min': 22.1, 'L_max': 96.9, 'monotonic': True, 'total_dE': 83.7, 'uniformity': 0.658}, 'div': {'L_range': 67.7, 'L_min': 28.0, 'L_max': 95.7, 'monotonic': False, 'total_dE': 153.8, 'uniformity': 0.706}, 'flow': {'L_range': 69.9, 'L_min': 23.0, 'L_max': 92.9, 'monotonic': True, 'total_dE': 116.7, 'uniformity': 0.726}, 'cyclic': {'L_range': 0.5, 'L_min': 61.8, 'L_max': 62.3, 'monotonic': True, 'total_dE': 168.2, 'uniformity': 0.74}},
    "cvd_grade": 'B',
    "safe_set": [0, 1, 2, 3, 4, 5],
    "orders": {'smooth': [0, 1, 2, 3, 4, 5], 'distinct': [0, 3, 1, 4, 5, 2], 'hue': [2, 5, 1, 0, 3, 4], 'light': [5, 3, 4, 0, 2, 1]},
    "min_de": 21.6,
    "cvd": {'protan': 14.0, 'deutan': 12.9, 'tritan': 9.0},
  },
  "noface-ink-gray": {
    "slug": 'noface-ink-gray',
    "zh": '无脸男',
    "en": 'No-Face',
    "tone_zh": '墨灰',
    "tone_en": 'Ink Gray',
    "name_zh": '无脸男 · 墨灰',
    "name_en": 'No-Face · Ink Gray',
    "family": '中性',
    "source": '千与千寻',
    "kind": 'mono',
    "colors": ['#303038', '#4F4F5F', '#765D84', '#7B7B8B', '#959599', '#B6B6C5'],
    "dark": ['#111019', '#2D2D3C', '#513A5F', '#565665', '#6F6F73', '#8E8E9D'],
    "light": ['#55545B', '#767684', '#9C87A7', '#A5A5B2', '#C0C0C3', '#E3E3EF'],
    "bg": '#F5F5F5',
    "bg2": '#E5E5E6',
    "ink": '#323235',
    "muted": '#848385',
    "seq": ['#F6F6F7', '#E3E3E5', '#D1D1D4', '#C2C2C5', '#B0B0B5', '#A2A2A8', '#939399', '#85858C', '#77777F', '#6B6B73', '#5D5D66', '#54545C', '#4F4F58', '#4A4A53', '#43434B', '#3E3E45', '#39393E', '#343439', '#343439'],
    "div": ['#4B3D53', '#614E6B', '#776084', '#8B7498', '#A089AC', '#B4A0BE', '#C8B9D0', '#DBD0E0', '#ECE7EF', '#E9E9E6', '#D2D5C6', '#BAC1A7', '#A1AA89', '#8A956F', '#758059', '#616C45', '#4F583A', '#3E452E', '#3E452E'],
    "flow": ['#EAEAFA', '#E1E1F3', '#D6D7EB', '#CFCFE5', '#C8C8E0', '#BFC0D9', '#B9BAD3', '#B3B3CD', '#ADADC8', '#A6A7C2', '#A1A1BD', '#9A9AB7', '#9493B3', '#8E8BAE', '#8984A9', '#847DA5', '#7F76A0', '#797099', '#726C90', '#6B6787', '#65627F', '#5F5D77', '#59596F', '#535466', '#4E4F60', '#494A59', '#444553', '#3E3E4B', '#383843', '#363640'],
    "cyclic": ['#9093BD', '#9891BB', '#A08EB8', '#A98CB2', '#B389AA', '#BB879F', '#C08693', '#C18789', '#C08980', '#BC8A79', '#B88D73', '#B38F6F', '#AC926C', '#A6946B', '#9E976C', '#95996E', '#8B9C73', '#7F9E79', '#73A082', '#68A18D', '#5EA298', '#58A2A2', '#56A1AB', '#59A0B4', '#619EBA', '#6B9BBE', '#7799C0', '#8296C0', '#8C94BE', '#9093BD'],
    "wheel": [{'i': 0, 'L': 20.2, 'C': 5.4, 'h': 291.5}, {'i': 1, 'L': 34.1, 'C': 10.0, 'h': 291.9}, {'i': 2, 'L': 43.3, 'C': 25.3, 'h': 315.1}, {'i': 3, 'L': 52.1, 'C': 9.3, 'h': 291.3}, {'i': 4, 'L': 61.8, 'C': 2.2, 'h': 290.4}, {'i': 5, 'L': 74.5, 'C': 8.1, 'h': 290.9}],
    "ramp_stats": {'seq': {'L_range': 75.0, 'L_min': 21.9, 'L_max': 96.9, 'monotonic': True, 'total_dE': 99.0, 'uniformity': 0.442}, 'div': {'L_range': 67.7, 'L_min': 28.0, 'L_max': 95.7, 'monotonic': False, 'total_dE': 146.6, 'uniformity': 0.722}, 'flow': {'L_range': 70.1, 'L_min': 23.0, 'L_max': 93.1, 'monotonic': True, 'total_dE': 103.9, 'uniformity': 0.615}, 'cyclic': {'L_range': 0.5, 'L_min': 61.7, 'L_max': 62.2, 'monotonic': True, 'total_dE': 125.7, 'uniformity': 0.55}},
    "cvd_grade": 'B',
    "safe_set": [0, 3, 5],
    "orders": {'smooth': [0, 1, 2, 3, 4, 5], 'distinct': [0, 1, 3, 5, 4, 2], 'hue': [2, 5, 4, 3, 1, 0], 'light': [5, 4, 3, 2, 1, 0]},
    "min_de": 10.7,
    "cvd": {'protan': 9.7, 'deutan': 9.6, 'tritan': 9.0},
  },
  "2b-achromatic": {
    "slug": '2b-achromatic',
    "zh": '2B',
    "en": '2B',
    "tone_zh": '素墨',
    "tone_en": 'Achromatic Ink',
    "name_zh": '2B · 素墨',
    "name_en": '2B · Achromatic Ink',
    "family": '中性',
    "source": '尼尔：机械纪元',
    "kind": 'mono',
    "colors": ['#303035', '#5A5A67', '#81818D', '#C7C5C2', '#999487', '#83714F'],
    "dark": ['#111016', '#373744', '#5C5C67', '#9E9C99', '#726E61', '#5D4D2C'],
    "light": ['#545459', '#82828D', '#ABABB5', '#F4F2F0', '#C3BFB4', '#AB9B7F'],
    "bg": '#F5F5F5',
    "bg2": '#E5E5E6',
    "ink": '#323234',
    "muted": '#848484',
    "seq": ['#F6F6F7', '#E4E4E6', '#D4D4D6', '#C4C4C6', '#B4B4B7', '#A4A4A7', '#96969A', '#87878B', '#7A7A7E', '#6C6C71', '#5F5F65', '#54545A', '#505055', '#4B4B51', '#434347', '#3E3E42', '#3A3A3E', '#343438', '#343438'],
    "div": ['#4B412E', '#60533A', '#766647', '#8B7A5B', '#A08F71', '#B4A58B', '#C9BCA8', '#DCD2C5', '#EDE8E2', '#E6E9EB', '#C8D5E0', '#AAC1D2', '#8CAAC1', '#7095AF', '#59809B', '#446C87', '#38586D', '#2D4555', '#2D4555'],
    "flow": ['#F3EADB', '#ECE0D0', '#E5D7C5', '#DECDBB', '#D8C4B1', '#D4BDAB', '#D3B6A8', '#D1B0A6', '#CDA9A5', '#C8A2A5', '#C19CA6', '#B796A7', '#B38D9C', '#AF8590', '#AB7D84', '#A77778', '#A2726D', '#9C6C66', '#966869', '#8E636B', '#855F6D', '#7A5C6D', '#6F596C', '#65576A', '#5A5264', '#504B5B', '#484554', '#403E4B', '#393843', '#363640'],
    "cyclic": ['#A9936C', '#A2966B', '#9A986D', '#919A70', '#879D74', '#7B9F7C', '#70A085', '#66A18F', '#5DA29A', '#57A2A4', '#56A1AE', '#5A9FB5', '#639DBB', '#6E9BBF', '#7998C0', '#8496C0', '#8E93BE', '#9890BA', '#A28EB6', '#AD8BAF', '#B589A7', '#BC879C', '#C08690', '#C18787', '#BF897E', '#BC8B78', '#B78D72', '#B1906E', '#AB926C', '#A9936C'],
    "wheel": [{'i': 0, 'L': 20.0, 'C': 3.4, 'h': 291.0}, {'i': 1, 'L': 38.7, 'C': 8.0, 'h': 291.4}, {'i': 2, 'L': 54.3, 'C': 6.9, 'h': 291.0}, {'i': 3, 'L': 79.6, 'C': 1.8, 'h': 85.1}, {'i': 4, 'L': 61.4, 'C': 7.5, 'h': 93.9}, {'i': 5, 'L': 48.5, 'C': 21.6, 'h': 85.1}],
    "ramp_stats": {'seq': {'L_range': 75.1, 'L_min': 21.8, 'L_max': 96.9, 'monotonic': True, 'total_dE': 100.9, 'uniformity': 0.443}, 'div': {'L_range': 67.6, 'L_min': 28.0, 'L_max': 95.6, 'monotonic': False, 'total_dE': 156.3, 'uniformity': 0.71}, 'flow': {'L_range': 70.0, 'L_min': 23.0, 'L_max': 93.0, 'monotonic': True, 'total_dE': 117.6, 'uniformity': 0.589}, 'cyclic': {'L_range': 0.4, 'L_min': 61.8, 'L_max': 62.2, 'monotonic': True, 'total_dE': 124.6, 'uniformity': 0.537}},
    "cvd_grade": 'A',
    "safe_set": [0, 1, 2, 3, 4, 5],
    "orders": {'smooth': [0, 1, 2, 3, 4, 5], 'distinct': [0, 1, 2, 3, 4, 5], 'hue': [5, 3, 4, 2, 1, 0], 'light': [3, 4, 2, 5, 1, 0]},
    "min_de": 14.7,
    "cvd": {'protan': 14.3, 'deutan': 14.4, 'tritan': 9.6},
  },
  "kakashi-silver-navy": {
    "slug": 'kakashi-silver-navy',
    "zh": '卡卡西',
    "en": 'Kakashi',
    "tone_zh": '银藏',
    "tone_en": 'Silver & Navy',
    "name_zh": '卡卡西 · 银藏',
    "name_en": 'Kakashi · Silver & Navy',
    "family": '中性',
    "source": '火影忍者',
    "kind": 'cat',
    "colors": ['#8E98A4', '#BFC1C2', '#727578', '#516E90', '#3B475C', '#B14A3A'],
    "dark": ['#68727D', '#97999A', '#4E5153', '#2A4A6A', '#192639', '#862218'],
    "light": ['#BBC3CD', '#ECEEEF', '#9C9EA1', '#8196B2', '#646D7F', '#D37C6B'],
    "bg": '#F4F5F6',
    "bg2": '#E4E5E7',
    "ink": '#303336',
    "muted": '#828486',
    "seq": ['#F5F6F8', '#E7EAED', '#DBDEE3', '#CED2D8', '#C1C7CD', '#B2B9C1', '#A7AFB8', '#98A1AC', '#8A94A0', '#7F8994', '#737D88', '#69727D', '#5F6872', '#535C65', '#4A525A', '#424850', '#383D44', '#30353B', '#30353B'],
    "div": ['#344356', '#42566F', '#506A8A', '#657E9E', '#7B93B1', '#95A8C3', '#B1BFD4', '#CBD4E3', '#E5E9F0', '#F4E6E4', '#F6CAC1', '#F1AD9F', '#E49180', '#D57664', '#C0604E', '#AA4A3B', '#893E31', '#6A3127', '#6A3127'],
    "flow": ['#DAEEF8', '#CFE5F1', '#C4DBEA', '#B9D1E2', '#ADC6DA', '#A3BDD1', '#98B3C9', '#8EAAC0', '#85A2B8', '#7A98B2', '#7191AD', '#6888A7', '#5E80A1', '#5A799E', '#5B739D', '#5D6C9B', '#616598', '#665F94', '#6B578F', '#715089', '#764882', '#71447B', '#634476', '#564470', '#4B4369', '#424060', '#3B3F58', '#363B4E', '#333844', '#323741'],
    "cyclic": ['#C68678', '#C28870', '#BC8B69', '#B68F66', '#AD9263', '#A49562', '#9B9964', '#8F9B68', '#829E6E', '#73A177', '#65A383', '#58A38F', '#4BA49B', '#42A4A7', '#3FA3B2', '#45A1BC', '#529EC3', '#649CC7', '#7298C9', '#8095C8', '#8D92C6', '#9A8FC2', '#A68CBD', '#B288B4', '#BC85AA', '#C4839D', '#C88290', '#C98385', '#C7857B', '#C68678'],
    "wheel": [{'i': 0, 'L': 62.4, 'C': 7.6, 'h': 262.0}, {'i': 1, 'L': 77.9, 'C': 0.9, 'h': 235.8}, {'i': 2, 'L': 49.1, 'C': 2.1, 'h': 256.0}, {'i': 3, 'L': 45.5, 'C': 21.9, 'h': 267.2}, {'i': 4, 'L': 29.9, 'C': 14.0, 'h': 274.0}, {'i': 5, 'L': 45.0, 'C': 51.0, 'h': 36.6}],
    "ramp_stats": {'seq': {'L_range': 75.0, 'L_min': 21.9, 'L_max': 96.9, 'monotonic': True, 'total_dE': 125.1, 'uniformity': 0.448}, 'div': {'L_range': 68.0, 'L_min': 27.9, 'L_max': 95.8, 'monotonic': False, 'total_dE': 155.7, 'uniformity': 0.703}, 'flow': {'L_range': 70.0, 'L_min': 23.0, 'L_max': 92.9, 'monotonic': True, 'total_dE': 106.1, 'uniformity': 0.619}, 'cyclic': {'L_range': 0.5, 'L_min': 61.8, 'L_max': 62.2, 'monotonic': True, 'total_dE': 136.7, 'uniformity': 0.632}},
    "cvd_grade": 'A',
    "safe_set": [0, 1, 2, 3, 4, 5],
    "orders": {'smooth': [0, 1, 2, 3, 4, 5], 'distinct': [0, 2, 4, 3, 5, 1], 'hue': [5, 3, 4, 1, 0, 2], 'light': [1, 0, 2, 3, 5, 4]},
    "min_de": 13.3,
    "cvd": {'protan': 13.0, 'deutan': 13.3, 'tritan': 13.3},
  },
  "nyanko-fortune": {
    "slug": 'nyanko-fortune',
    "zh": '猫咪老师',
    "en": 'Nyanko-sensei',
    "tone_zh": '招财米',
    "tone_en": 'Fortune Beige',
    "name_zh": '猫咪老师 · 招财米',
    "name_en": 'Nyanko-sensei · Fortune Beige',
    "family": '中性',
    "source": '夏目友人帐',
    "kind": 'cat',
    "colors": ['#A89263', '#E6AD3F', '#BDB7AA', '#7D7364', '#4A4640', '#BD3830'],
    "dark": ['#806C3E', '#B9850A', '#958F82', '#584F40', '#292520', '#90000F'],
    "light": ['#D1BD97', '#FFDEAF', '#E9E4D9', '#A59C90', '#706C67', '#DE7162'],
    "bg": '#F7F5F2',
    "bg2": '#E9E5DE',
    "ink": '#393224',
    "muted": '#87837C',
    "seq": ['#F9F6F1', '#F1EBE2', '#E8E0D2', '#DED3BE', '#D3C6AC', '#C9B99B', '#BFAD89', '#B4A077', '#AA9466', '#9B8658', '#8E7A4E', '#806D43', '#75623A', '#665631', '#5B4C2B', '#504325', '#473A20', '#3E331B', '#3E331B'],
    "div": ['#732A23', '#95342B', '#B83E34', '#CF5447', '#E46C5D', '#F28A7A', '#FCA99B', '#FFC6BC', '#FEE3DE', '#E8E9E7', '#C0D8D8', '#99C6C7', '#75B1B2', '#529C9E', '#37878A', '#187376', '#195E60', '#18494A', '#18494A'],
    "flow": ['#F2EADB', '#F1E6CE', '#F0E0BE', '#EFDAAB', '#EED397', '#ECCB81', '#EAC268', '#E0B95E', '#D1B062', '#C4A766', '#B89F69', '#AC9769', '#A18D66', '#978564', '#8D7E61', '#86785F', '#857152', '#856B45', '#856337', '#855B2A', '#85521B', '#86480B', '#784610', '#6B4416', '#60421B', '#563F20', '#4E3D24', '#463A28', '#3E372C', '#3C362D'],
    "cyclic": ['#D87D6F', '#D38164', '#CC855A', '#C38A53', '#BA8E4E', '#AF924C', '#A3974C', '#949B50', '#839F58', '#6FA363', '#57A672', '#3AA883', '#0CA994', '#00A7A3', '#00A6B0', '#00A4BE', '#00A3CE', '#279FDB', '#529BDE', '#6D96DE', '#8292DA', '#958DD6', '#A789CF', '#B883C4', '#C77DB6', '#D37AA4', '#D97892', '#DB7981', '#D97C73', '#D87D6F'],
    "wheel": [{'i': 0, 'L': 61.5, 'C': 28.0, 'h': 87.0}, {'i': 1, 'L': 74.2, 'C': 62.7, 'h': 80.3}, {'i': 2, 'L': 74.6, 'C': 7.4, 'h': 91.3}, {'i': 3, 'L': 48.9, 'C': 9.8, 'h': 83.0}, {'i': 4, 'L': 29.9, 'C': 4.2, 'h': 83.9}, {'i': 5, 'L': 44.0, 'C': 63.4, 'h': 34.1}],
    "ramp_stats": {'seq': {'L_range': 75.1, 'L_min': 21.8, 'L_max': 97.0, 'monotonic': True, 'total_dE': 108.3, 'uniformity': 0.533}, 'div': {'L_range': 67.8, 'L_min': 27.9, 'L_max': 95.7, 'monotonic': False, 'total_dE': 152.9, 'uniformity': 0.722}, 'flow': {'L_range': 70.0, 'L_min': 23.0, 'L_max': 92.9, 'monotonic': True, 'total_dE': 125.4, 'uniformity': 0.686}, 'cyclic': {'L_range': 0.5, 'L_min': 61.8, 'L_max': 62.3, 'monotonic': True, 'total_dE': 165.4, 'uniformity': 0.726}},
    "cvd_grade": 'A',
    "safe_set": [0, 1, 2, 3, 4, 5],
    "orders": {'smooth': [0, 1, 2, 3, 4, 5], 'distinct': [0, 2, 3, 5, 1, 4], 'hue': [5, 1, 0, 2, 3, 4], 'light': [2, 1, 0, 3, 5, 4]},
    "min_de": 15.4,
    "cvd": {'protan': 13.7, 'deutan': 14.0, 'tritan': 13.6},
  },
  "tarnished-gilded": {
    "slug": 'tarnished-gilded',
    "zh": '褪色者',
    "en": 'Tarnished',
    "tone_zh": '黄金暗夜',
    "tone_en": 'Gilded Nightfall',
    "name_zh": '褪色者 · 黄金暗夜',
    "name_en": 'Tarnished · Gilded Nightfall',
    "family": '中性',
    "source": '艾尔登法环',
    "kind": 'cat',
    "colors": ['#7A674F', '#B18C35', '#C7B68D', '#948E83', '#4A4641', '#842317'],
    "dark": ['#55432C', '#876605', '#9E8E66', '#6E685D', '#292520', '#520500'],
    "light": ['#A1907C', '#DAB774', '#F1E3C2', '#BEB9B0', '#706C68', '#A65545'],
    "bg": '#F6F5F3',
    "bg2": '#E8E5E1',
    "ink": '#38322A',
    "muted": '#87837F',
    "seq": ['#F9F6F3', '#EBE5E0', '#DAD2C9', '#C8BEB2', '#B8AC9C', '#A99B89', '#998976', '#8B7964', '#7C6A52', '#74624B', '#6D5C45', '#695741', '#61503B', '#594A35', '#534432', '#4B3E2E', '#45392A', '#3D3326', '#3D3326'],
    "div": ['#6A3126', '#893E30', '#AA4B3A', '#C0604D', '#D57663', '#E4917F', '#F1AD9E', '#F8C9BE', '#FAE4DF', '#E7E9E8', '#C2D8D9', '#9DC5C7', '#7BB0B3', '#5B9B9F', '#41868A', '#287276', '#245D60', '#1F484B', '#1F484B'],
    "flow": ['#F5EAD2', '#F3E4C4', '#F1DDB6', '#EFD7A7', '#EDCF98', '#EAC787', '#E8BF76', '#DEB776', '#D4B079', '#CAAA7C', '#C0A57E', '#B69F81', '#AD9981', '#A6917A', '#A18B74', '#9A836C', '#957D67', '#8F7661', '#88705C', '#816A58', '#7A6453', '#725E4E', '#6B5749', '#645043', '#624B3E', '#604537', '#5D3E31', '#5A372B', '#562F25', '#552C23'],
    "cyclic": ['#CF8271', '#CA8568', '#C48961', '#BC8D5B', '#B39058', '#AA9456', '#9E9858', '#909B5B', '#819F63', '#6FA26E', '#5BA57C', '#46A68B', '#2FA799', '#17A6A7', '#00A5B4', '#04A4C2', '#2CA1CC', '#4C9DD2', '#6499D4', '#7895D3', '#8992D1', '#998ECC', '#A889C5', '#B785BB', '#C481AE', '#CE7D9E', '#D27D8E', '#D37F81', '#D08174', '#CF8271'],
    "wheel": [{'i': 0, 'L': 44.8, 'C': 16.8, 'h': 77.1}, {'i': 1, 'L': 60.2, 'C': 50.2, 'h': 84.5}, {'i': 2, 'L': 74.5, 'C': 23.1, 'h': 90.6}, {'i': 3, 'L': 59.2, 'C': 6.7, 'h': 88.1}, {'i': 4, 'L': 30.0, 'C': 3.7, 'h': 79.8}, {'i': 5, 'L': 29.8, 'C': 51.4, 'h': 37.8}],
    "ramp_stats": {'seq': {'L_range': 75.1, 'L_min': 21.9, 'L_max': 97.0, 'monotonic': True, 'total_dE': 116.9, 'uniformity': 0.415}, 'div': {'L_range': 67.9, 'L_min': 27.8, 'L_max': 95.8, 'monotonic': False, 'total_dE': 149.9, 'uniformity': 0.73}, 'flow': {'L_range': 69.8, 'L_min': 23.2, 'L_max': 93.0, 'monotonic': True, 'total_dE': 114.7, 'uniformity': 0.606}, 'cyclic': {'L_range': 0.5, 'L_min': 61.8, 'L_max': 62.2, 'monotonic': True, 'total_dE': 152.9, 'uniformity': 0.676}},
    "cvd_grade": 'A',
    "safe_set": [0, 1, 2, 3, 4, 5],
    "orders": {'smooth': [0, 1, 2, 3, 4, 5], 'distinct': [0, 1, 2, 5, 3, 4], 'hue': [5, 0, 1, 2, 3, 4], 'light': [2, 1, 3, 0, 4, 5]},
    "min_de": 15.6,
    "cvd": {'protan': 13.3, 'deutan': 13.7, 'tritan': 14.2},
  },
  "mario-primary": {
    "slug": 'mario-primary',
    "zh": '马力欧',
    "en": 'Mario',
    "tone_zh": '正红蓝',
    "tone_en": 'Primary Red & Blue',
    "name_zh": '马力欧 · 正红蓝',
    "name_en": 'Mario · Primary Red & Blue',
    "family": '撞色',
    "source": '超级马力欧',
    "kind": 'cat',
    "colors": ['#DD5643', '#C8B3A2', '#DDB300', '#683D17', '#46464D', '#2F56B3'],
    "dark": ['#B02A20', '#9F8B7B', '#AE8C00', '#3E1E00', '#25252C', '#003580'],
    "light": ['#FD8D78', '#F2E0D2', '#FFE19B', '#8D6546', '#6C6C72', '#6F7ECB'],
    "bg": '#FDF3F1',
    "bg2": '#F6E1DC',
    "ink": '#502720',
    "muted": '#967E79',
    "seq": ['#FFF4F2', '#FFE8E3', '#FFDBD4', '#FECEC4', '#FDBFB2', '#FAAE9E', '#F69D8B', '#F08B77', '#EA7864', '#E36652', '#DB5442', '#CD4B39', '#BD4030', '#AD3527', '#9D2C21', '#89261C', '#752117', '#631B13', '#631B13'],
    "div": ['#4B4038', '#605247', '#766557', '#8A796B', '#9F8E80', '#B3A498', '#C8BCB2', '#DBD2CC', '#ECE8E5', '#F9E4DF', '#FEC7BB', '#FCA998', '#F28A77', '#E46D59', '#CF5543', '#B83F2F', '#953527', '#732B20', '#732B20'],
    "flow": ['#FFE9B9', '#FFDCA4', '#F7D1A5', '#EAC8AA', '#DCC1AD', '#DDB9A4', '#E3AF94', '#EAA486', '#F39678', '#FA866E', '#FF7569', '#FF696E', '#FE5F77', '#F75A83', '#ED578E', '#DF559A', '#CF56A4', '#BD57AC', '#AC58AD', '#AA5197', '#A34C81', '#99496E', '#8D475E', '#7D4554', '#6E4356', '#5E4055', '#503E52', '#433B4C', '#393843', '#363640'],
    "cyclic": ['#E27864', '#DB7D58', '#D3824D', '#CA8845', '#BF8D3F', '#B2923C', '#A4973C', '#949C40', '#7FA149', '#67A557', '#47A96A', '#0FAA7E', '#00A992', '#00A7A2', '#00A6B2', '#00A4C1', '#00A2D3', '#009EE8', '#4B9AEC', '#6C94EA', '#858FE6', '#9B8AE0', '#B083D7', '#C47CC8', '#D575B6', '#E171A1', '#E7708B', '#E77279', '#E37668', '#E27864'],
    "wheel": [{'i': 0, 'L': 54.5, 'C': 64.3, 'h': 36.6}, {'i': 1, 'L': 74.3, 'C': 12.4, 'h': 67.4}, {'i': 2, 'L': 74.6, 'C': 77.0, 'h': 88.5}, {'i': 3, 'L': 30.3, 'C': 34.1, 'h': 63.2}, {'i': 4, 'L': 30.0, 'C': 4.5, 'h': 291.0}, {'i': 5, 'L': 38.7, 'C': 56.8, 'h': 289.7}],
    "ramp_stats": {'seq': {'L_range': 75.1, 'L_min': 21.9, 'L_max': 97.0, 'monotonic': True, 'total_dE': 90.8, 'uniformity': 0.705}, 'div': {'L_range': 67.7, 'L_min': 28.0, 'L_max': 95.7, 'monotonic': False, 'total_dE': 156.5, 'uniformity': 0.68}, 'flow': {'L_range': 70.1, 'L_min': 23.0, 'L_max': 93.0, 'monotonic': True, 'total_dE': 141.2, 'uniformity': 0.714}, 'cyclic': {'L_range': 0.5, 'L_min': 61.8, 'L_max': 62.3, 'monotonic': True, 'total_dE': 179.2, 'uniformity': 0.748}},
    "cvd_grade": 'A',
    "safe_set": [0, 1, 2, 3, 4, 5],
    "orders": {'smooth': [0, 1, 2, 3, 4, 5], 'distinct': [0, 5, 2, 3, 1, 4], 'hue': [0, 3, 1, 2, 5, 4], 'light': [2, 1, 0, 5, 3, 4]},
    "min_de": 22.9,
    "cvd": {'protan': 16.7, 'deutan': 16.4, 'tritan': 10.8},
  },
  "luffy-red-straw": {
    "slug": 'luffy-red-straw',
    "zh": '路飞',
    "en": 'Luffy',
    "tone_zh": '赤麦',
    "tone_en": 'Red & Straw',
    "name_zh": '路飞 · 赤麦',
    "name_en": 'Luffy · Red & Straw',
    "family": '撞色',
    "source": '海贼王',
    "kind": 'cat',
    "colors": ['#C11B1E', '#C8732E', '#D7B34E', '#A29D96', '#51443E', '#2B5FA8'],
    "dark": ['#860009', '#9C4D00', '#AB8B23', '#7B766F', '#2F231E', '#003C78'],
    "light": ['#E16352', '#EDA26B', '#FFE09A', '#CDC9C3', '#766B66', '#6C87C3'],
    "bg": '#FFF2F0',
    "bg2": '#F9E0DB',
    "ink": '#54241D',
    "muted": '#997D78',
    "seq": ['#FFF4F2', '#FFE8E4', '#FEDCD5', '#FCCCC3', '#F9BEB3', '#F6AEA1', '#F29D8E', '#ED8C7C', '#E67B6B', '#DF6A5A', '#D8594A', '#D1483B', '#C8322A', '#BD191C', '#AC0D16', '#9B010F', '#810C0F', '#6A110E', '#6A110E'],
    "div": ['#2C426B', '#36548B', '#3F68AD', '#587BC1', '#7190D3', '#8FA6E0', '#ADBDEB', '#C9D3F2', '#E5E8F7', '#EEE8E1', '#E3D2B0', '#D4BB84', '#C0A45D', '#AB8E3A', '#95791F', '#7F6601', '#685207', '#51400A', '#51400A'],
    "flow": ['#FFE9BA', '#F6DEAF', '#E8D2AE', '#DAC8AC', '#D2BFA6', '#D3B895', '#D5B080', '#D6A66A', '#D89B54', '#DA8F3C', '#D8822D', '#D57520', '#D26714', '#CF5808', '#CD4E13', '#CB4823', '#C7432F', '#C13F39', '#BA3C43', '#B03B4B', '#A43C53', '#963D58', '#873E58', '#7C3D4B', '#713C41', '#643B39', '#583934', '#4D3731', '#43352F', '#40352F'],
    "cyclic": ['#EE6F5D', '#E7754E', '#DE7C41', '#D38335', '#C7892C', '#BA9026', '#AB9624', '#989B27', '#83A032', '#68A542', '#43AA57', '#01AB70', '#00AA89', '#00A89C', '#00A6AC', '#00A5BD', '#00A2CF', '#009FE5', '#2899FD', '#6093FB', '#808DF5', '#9B87EE', '#B37FE3', '#CA77D4', '#DF6DBE', '#ED67A5', '#F4658C', '#F46876', '#F06D63', '#EE6F5D'],
    "wheel": [{'i': 0, 'L': 41.6, 'C': 75.4, 'h': 35.0}, {'i': 1, 'L': 56.8, 'C': 57.8, 'h': 60.8}, {'i': 2, 'L': 74.3, 'C': 55.0, 'h': 88.1}, {'i': 3, 'L': 65.0, 'C': 4.3, 'h': 83.0}, {'i': 4, 'L': 30.0, 'C': 7.2, 'h': 52.0}, {'i': 5, 'L': 40.4, 'C': 45.1, 'h': 281.0}],
    "ramp_stats": {'seq': {'L_range': 75.0, 'L_min': 21.9, 'L_max': 97.0, 'monotonic': True, 'total_dE': 87.4, 'uniformity': 0.697}, 'div': {'L_range': 67.7, 'L_min': 27.9, 'L_max': 95.6, 'monotonic': False, 'total_dE': 150.7, 'uniformity': 0.7}, 'flow': {'L_range': 69.9, 'L_min': 23.1, 'L_max': 93.1, 'monotonic': True, 'total_dE': 126.2, 'uniformity': 0.727}, 'cyclic': {'L_range': 0.6, 'L_min': 61.7, 'L_max': 62.3, 'monotonic': True, 'total_dE': 192.5, 'uniformity': 0.806}},
    "cvd_grade": 'B',
    "safe_set": [0, 1, 2, 3, 4, 5],
    "orders": {'smooth': [0, 1, 2, 3, 4, 5], 'distinct': [0, 2, 5, 1, 4, 3], 'hue': [0, 1, 2, 5, 3, 4], 'light': [2, 3, 1, 0, 5, 4]},
    "min_de": 22.9,
    "cvd": {'protan': 14.3, 'deutan': 12.8, 'tritan': 15.6},
  },
  "rx78-trikolor": {
    "slug": 'rx78-trikolor',
    "zh": 'RX-78-2',
    "en": 'RX-78-2',
    "tone_zh": '三色旗',
    "tone_en": 'Trikolor',
    "name_zh": 'RX-78-2 · 三色旗',
    "name_en": 'RX-78-2 · Trikolor',
    "family": '撞色',
    "source": '机动战士高达',
    "kind": 'cat',
    "colors": ['#2F5AA9', '#43474D', '#D92A3A', '#777C86', '#B4B8BB', '#E0B100'],
    "dark": ['#003879', '#22262C', '#A10020', '#525761', '#8C9093', '#B08A00'],
    "light": ['#6D82C3', '#6A6D72', '#F7716C', '#A2A6AE', '#E1E4E7', '#FFE09F'],
    "bg": '#F4F5FA',
    "bg2": '#E3E5F1',
    "ink": '#2B324B',
    "muted": '#818391',
    "seq": ['#F5F6FF', '#E8EAF9', '#DCDFF4', '#CDD1EC', '#BCC3E5', '#ADB5DD', '#9DA8D6', '#8D9ACE', '#7D8DC7', '#6C80C0', '#5D74B9', '#4B69B2', '#345DAB', '#27529E', '#1C4990', '#1C4181', '#1E3A71', '#1F3360', '#1F3360'],
    "div": ['#30416D', '#3A538E', '#4566B1', '#5E79C5', '#778ED7', '#94A4E4', '#B0BBEE', '#CCD2F4', '#E5E8F7', '#F0E7DC', '#E9D1A2', '#DBBA6D', '#C8A23C', '#B28C06', '#997802', '#816500', '#6A5200', '#534000', '#534000'],
    "flow": ['#DCEDFA', '#C1ECFE', '#9DECFB', '#75EBED', '#5AE9D7', '#52E6BB', '#5EE199', '#75DA72', '#9AD05E', '#B3C458', '#C4B959', '#D0AF60', '#D6A66A', '#D79E78', '#CF9886', '#BE9592', '#C78683', '#D3706B', '#DB564B', '#DD3C36', '#D7334A', '#CC305E', '#BA3470', '#A03E7E', '#834584', '#664983', '#4C4773', '#39415D', '#323A48', '#313741'],
    "cyclic": ['#FC6261', '#F66A4E', '#ED723D', '#E27B2D', '#D5831D', '#C78A0C', '#B79100', '#A59800', '#919E08', '#78A320', '#56A938', '#15AC53', '#00AB74', '#00A98D', '#00A8A0', '#00A6B1', '#00A4C2', '#00A1D6', '#009DF0', '#4396FF', '#6D90FF', '#8C88FF', '#AA80F5', '#C476E7', '#DD6BD2', '#F15FB6', '#FC5A9A', '#FF5B7F', '#FE6068', '#FC6261'],
    "wheel": [{'i': 0, 'L': 39.2, 'C': 48.5, 'h': 285.3}, {'i': 1, 'L': 30.0, 'C': 4.2, 'h': 267.0}, {'i': 2, 'L': 47.9, 'C': 74.8, 'h': 28.4}, {'i': 3, 'L': 51.9, 'C': 6.1, 'h': 272.5}, {'i': 4, 'L': 74.6, 'C': 2.2, 'h': 247.7}, {'i': 5, 'L': 74.4, 'C': 77.1, 'h': 86.8}],
    "ramp_stats": {'seq': {'L_range': 75.1, 'L_min': 22.0, 'L_max': 97.0, 'monotonic': True, 'total_dE': 89.3, 'uniformity': 0.691}, 'div': {'L_range': 67.5, 'L_min': 28.1, 'L_max': 95.6, 'monotonic': False, 'total_dE': 153.2, 'uniformity': 0.65}, 'flow': {'L_range': 70.0, 'L_min': 22.9, 'L_max': 92.9, 'monotonic': True, 'total_dE': 211.8, 'uniformity': 0.822}, 'cyclic': {'L_range': 0.5, 'L_min': 61.8, 'L_max': 62.3, 'monotonic': True, 'total_dE': 201.3, 'uniformity': 0.803}},
    "cvd_grade": 'A',
    "safe_set": [0, 1, 2, 3, 4, 5],
    "orders": {'smooth': [0, 1, 2, 3, 4, 5], 'distinct': [0, 2, 5, 4, 3, 1], 'hue': [2, 5, 0, 4, 3, 1], 'light': [4, 5, 3, 2, 0, 1]},
    "min_de": 19.4,
    "cvd": {'protan': 19.5, 'deutan': 19.5, 'tritan': 18.2},
  },
  "inkling-splat": {
    "slug": 'inkling-splat',
    "zh": 'Inkling',
    "en": 'Inkling',
    "tone_zh": '荧墨',
    "tone_en": 'Splat Neon',
    "name_zh": 'Inkling · 荧墨',
    "name_en": 'Inkling · Splat Neon',
    "family": '撞色',
    "source": '斯普拉遁',
    "kind": 'cat',
    "colors": ['#F32A7E', '#C65B00', '#49454F', '#008FAD', '#BBB7B0', '#5BD01F'],
    "dark": ['#B80059', '#8F3D00', '#28242D', '#00677D', '#938F88', '#3BA400'],
    "light": ['#FF86A9', '#EA8C4F', '#6F6C74', '#6EB7CF', '#E7E4DE', '#A6F978'],
    "bg": '#FEF2F5',
    "bg2": '#F9DFE5',
    "ink": '#562031',
    "muted": '#997C83',
    "seq": ['#FFF4F6', '#FFE9ED', '#FFDCE4', '#FFCED9', '#FFBDCD', '#FFAAC0', '#FF96B3', '#FD81A5', '#FA6998', '#F74F8B', '#F32D7E', '#E22174', '#D01669', '#BE095E', '#AB0052', '#970048', '#83003D', '#700033', '#700033'],
    "div": ['#074958', '#055D71', '#01728B', '#2A87A0', '#469CB5', '#6DB0C6', '#94C5D7', '#B9D8E4', '#DDEBF0', '#F5E6DD', '#FACAAD', '#F7AD80', '#EA9158', '#D97734', '#C3611C', '#AB4C01', '#8B3F04', '#6C3206', '#6C3206'],
    "flow": ['#F3EADB', '#F2E6C6', '#EBE1AC', '#DEDE90', '#C7DC75', '#A7DB5D', '#79DA4E', '#56D668', '#30D081', '#00C995', '#00C1A3', '#00B8AD', '#2CAFB2', '#00A7B9', '#009EBF', '#0094C6', '#008ACE', '#007FDE', '#0072F1', '#4768E5', '#645ED5', '#7753C4', '#8447AE', '#8D3A95', '#84347E', '#683970', '#543A60', '#453850', '#3C3644', '#39353F'],
    "cyclic": ['#FF5892', '#FF5C79', '#FF6062', '#F8684E', '#EE713C', '#E3792B', '#D7821A', '#C88A04', '#B89100', '#A69800', '#929E00', '#78A31A', '#57A834', '#16AC4F', '#00AB71', '#00AA8B', '#00A89E', '#00A6AF', '#00A4C0', '#00A2D4', '#009EED', '#3E97FF', '#6A90FF', '#8A88FF', '#A880F8', '#C375E9', '#DD6AD4', '#F15FB9', '#FE589C', '#FF5892'],
    "wheel": [{'i': 0, 'L': 54.3, 'C': 76.8, 'h': 3.0}, {'i': 1, 'L': 51.3, 'C': 71.8, 'h': 57.2}, {'i': 2, 'L': 30.0, 'C': 6.7, 'h': 306.1}, {'i': 3, 'L': 54.7, 'C': 32.6, 'h': 229.6}, {'i': 4, 'L': 74.6, 'C': 4.1, 'h': 87.9}, {'i': 5, 'L': 74.5, 'C': 91.8, 'h': 131.5}],
    "ramp_stats": {'seq': {'L_range': 74.5, 'L_min': 22.6, 'L_max': 97.1, 'monotonic': True, 'total_dE': 84.1, 'uniformity': 0.673}, 'div': {'L_range': 67.5, 'L_min': 28.1, 'L_max': 95.6, 'monotonic': False, 'total_dE': 152.7, 'uniformity': 0.66}, 'flow': {'L_range': 70.1, 'L_min': 22.9, 'L_max': 93.0, 'monotonic': True, 'total_dE': 175.2, 'uniformity': 0.785}, 'cyclic': {'L_range': 0.4, 'L_min': 61.8, 'L_max': 62.2, 'monotonic': True, 'total_dE': 202.4, 'uniformity': 0.831}},
    "cvd_grade": 'A',
    "safe_set": [0, 1, 2, 3, 4, 5],
    "orders": {'smooth': [0, 1, 2, 3, 4, 5], 'distinct': [0, 5, 1, 3, 2, 4], 'hue': [0, 1, 5, 3, 4, 2], 'light': [4, 5, 3, 0, 1, 2]},
    "min_de": 28.7,
    "cvd": {'protan': 13.7, 'deutan': 13.7, 'tritan': 6.4},
  },
  "joker-phantom": {
    "slug": 'joker-phantom',
    "zh": '雨宫莲',
    "en": 'Joker',
    "tone_zh": '怪盗红黑',
    "tone_en": 'Phantom Crimson',
    "name_zh": '雨宫莲 · 怪盗红黑',
    "name_en": 'Joker · Phantom Crimson',
    "family": '撞色',
    "source": '女神异闻录5',
    "kind": 'cat',
    "colors": ['#E50011', '#93001B', '#46464D', '#7C5F4F', '#848380', '#C1B7A8'],
    "dark": ['#A10006', '#580004', '#25252C', '#563C2D', '#5F5E5B', '#998F80'],
    "light": ['#FF6C53', '#B44C48', '#6C6C72', '#A2897B', '#AEADAB', '#ECE4D8'],
    "bg": '#FFF2EF',
    "bg2": '#FEDFD7',
    "ink": '#5A2016',
    "muted": '#9E7C74',
    "seq": ['#FFF4F2', '#FFEAE6', '#FFDFD8', '#FFD2C8', '#FFC4B7', '#FFB5A5', '#FFA490', '#FE907A', '#FB7E66', '#F76A52', '#F2543E', '#EC3A2A', '#E60E14', '#D1000E', '#BA000A', '#A10007', '#890004', '#730000', '#730000'],
    "div": ['#83170F', '#AA1310', '#D20610', '#E83828', '#FA5942', '#FF826A', '#FFA795', '#FFC6BA', '#FFE2DC', '#EAE8E6', '#C0D8D8', '#96C6C8', '#71B1B5', '#4C9DA1', '#2E888C', '#037478', '#0F5E62', '#13494C', '#13494C'],
    "flow": ['#F4EADB', '#EADDCD', '#E0D0BD', '#D6C3AF', '#DABB9F', '#E2B590', '#EBAB7E', '#F5A06F', '#FF9362', '#FF8865', '#FF7C67', '#FF6F6A', '#FE575E', '#E36265', '#CB686A', '#B56C6C', '#A36E6F', '#986D6E', '#996269', '#9A5564', '#9A4762', '#983762', '#8C3366', '#783867', '#663A64', '#553B5E', '#483B57', '#3E394D', '#383744', '#363640'],
    "cyclic": ['#DF7870', '#DB7C64', '#D5805A', '#CD8551', '#C38A4A', '#B98F45', '#AC9443', '#9E9945', '#8D9D4A', '#79A154', '#60A563', '#41A876', '#0CA988', '#00A89A', '#00A7A9', '#00A5B7', '#00A3C7', '#00A1D8', '#349DE4', '#5C98E6', '#7793E3', '#8D8FDF', '#A189D8', '#B483CE', '#C67DC0', '#D577AD', '#DE7499', '#E27586', '#E07775', '#DF7870'],
    "wheel": [{'i': 0, 'L': 47.9, 'C': 93.4, 'h': 37.6}, {'i': 1, 'L': 30.1, 'C': 61.7, 'h': 29.6}, {'i': 2, 'L': 30.0, 'C': 4.5, 'h': 291.0}, {'i': 3, 'L': 42.8, 'C': 16.6, 'h': 55.6}, {'i': 4, 'L': 54.8, 'C': 1.8, 'h': 96.9}, {'i': 5, 'L': 74.8, 'C': 8.9, 'h': 83.8}],
    "ramp_stats": {'seq': {'L_range': 74.5, 'L_min': 22.5, 'L_max': 97.0, 'monotonic': True, 'total_dE': 88.9, 'uniformity': 0.683}, 'div': {'L_range': 67.7, 'L_min': 27.9, 'L_max': 95.6, 'monotonic': False, 'total_dE': 150.9, 'uniformity': 0.735}, 'flow': {'L_range': 70.1, 'L_min': 23.0, 'L_max': 93.1, 'monotonic': True, 'total_dE': 141.3, 'uniformity': 0.73}, 'cyclic': {'L_range': 0.5, 'L_min': 61.8, 'L_max': 62.2, 'monotonic': True, 'total_dE': 172.6, 'uniformity': 0.745}},
    "cvd_grade": 'B',
    "safe_set": [0, 1, 2, 3, 4, 5],
    "orders": {'smooth': [0, 1, 2, 3, 4, 5], 'distinct': [0, 1, 2, 4, 3, 5], 'hue': [1, 0, 3, 5, 4, 2], 'light': [5, 4, 0, 3, 1, 2]},
    "min_de": 17.6,
    "cvd": {'protan': 14.2, 'deutan': 12.7, 'tritan': 17.8},
  },
}


FAMILIES = ["红", "橙", "黄", "绿", "青", "蓝", "紫", "粉", "中性", "撞色"]

_ALIAS = {}
for _s, _e in PALETTES.items():
    for _k in (_s, _s.split('-')[0], _e['zh'], _e['en'].lower(),
               _e['name_zh'], _e['name_en'].lower(), _e['tone_zh']):
        _ALIAS.setdefault(str(_k).lower(), _s)

# 作品名（一个作品对应多套配色，只用于 find()，不用于精确解析）
_SOURCE = {}
for _s, _e in PALETTES.items():
    _SOURCE.setdefault(_e['source'], []).append(_s)


CJK_FONTS = ["Noto Sans CJK SC", "Source Han Sans SC", "Microsoft YaHei",
             "PingFang SC", "Heiti SC", "SimHei", "WenQuanYi Zen Hei",
             "Noto Sans SC", "Hiragino Sans GB"]


def use_cjk_font(name: str = None) -> str:
    """让 matplotlib 能正常显示中文（自动挑一个系统里存在的中文字体）。"""
    import matplotlib
    from matplotlib import font_manager
    have = {f.name for f in font_manager.fontManager.ttflist}
    for f in ([name] if name else []) + CJK_FONTS:
        if f in have:
            matplotlib.rcParams["font.sans-serif"] = [f] + list(
                matplotlib.rcParams.get("font.sans-serif", []))
            matplotlib.rcParams["axes.unicode_minus"] = False
            return f
    return ""


def _cjk_ok() -> bool:
    import matplotlib
    from matplotlib import font_manager
    have = {f.name for f in font_manager.fontManager.ttflist}
    return bool(have & set(CJK_FONTS)) or bool(
        set(matplotlib.rcParams.get("font.sans-serif", [])) & set(CJK_FONTS))


def _resolve(name):
    k = str(name).strip().lower()
    if k in _ALIAS:
        return _ALIAS[k]
    hits = [s for a, s in _ALIAS.items() if k and k in a]
    if len(set(hits)) == 1:
        return hits[0]
    if hits:
        raise KeyError(f"'{name}' 匹配到多套配色: {sorted(set(hits))}")
    raise KeyError(f"未找到配色 '{name}'，用 anime_palettes.ls() 查看全部")


def get(name) -> dict:
    """返回该配色的完整字典。"""
    return PALETTES[_resolve(name)]


ORDERS = ("smooth", "distinct", "hue", "light")
ORDER_LABEL = {"smooth": "平滑（相邻色差最小）", "distinct": "区分度优先",
               "hue": "色相环顺序", "light": "明度浅→深"}
DEFAULT_ORDER = "smooth"


def colors(name, n: int = 6, variant: str = "main", order: str = None) -> list:
    """主色列表。

    variant : main / dark / light
    order   : smooth（默认，过渡平滑）/ distinct（区分度优先，多系列图表用）
              / hue（色相环）/ light（明度浅→深）
    """
    e = get(name)
    key = {"main": "colors", "dark": "dark", "light": "light"}[variant]
    idx = e["orders"][order or DEFAULT_ORDER]
    seq = [e[key][i] for i in idx]
    return [seq[i % len(seq)] for i in range(n)]


def order_of(name, order: str = None) -> list:
    """该排序下的颜色下标（相对 PALETTES[..]["colors"] 的规范顺序）。"""
    return get(name)["orders"][order or DEFAULT_ORDER]


def safe(name) -> list:
    """红/绿色盲下两两仍可分辨的推荐子集。"""
    e = get(name)
    return [e["colors"][i] for i in e["safe_set"]]


def neutrals(name) -> dict:
    """配套中性色：bg 纸色 / bg2 次级底 / muted 辅助灰 / ink 墨色。"""
    e = get(name)
    return {k: e[k] for k in ("bg", "bg2", "muted", "ink")}


def ls(family: str = None, grade: str = None, kind: str = None):
    """打印配色清单。"""
    rows = [e for e in PALETTES.values()
            if (family is None or e["family"] == family)
            and (grade is None or e["cvd_grade"] == grade)
            and (kind is None or e["kind"] == kind)]
    rows.sort(key=lambda e: (FAMILIES.index(e["family"]), e["slug"]))
    print(f"{'slug':<24}{'名称':<20}{'色系':<5}{'色盲':<5}{'主色'}")
    for e in rows:
        print(f"{e['slug']:<24}{e['name_zh']:<18}{e['family']:<5}"
              f"{e['cvd_grade']:<5}{' '.join(colors(e['slug']))}")
    print(f"\n共 {len(rows)} 套")
    return [e["slug"] for e in rows]


def find(q: str):
    """模糊搜索，返回匹配的 slug 列表。角色名 / 色调 / 作品名都可以。"""
    q = q.strip().lower()
    hit = {s for a, s in _ALIAS.items() if q in a}
    for src, ss in _SOURCE.items():
        if q in src.lower():
            hit.update(ss)
    out = sorted(hit)
    for s in out:
        e = PALETTES[s]
        print(f"{s:<24}{e['name_zh']} / {e['name_en']}  [{e['source']}]")
    return out


# ---------------------------------------------------------------- matplotlib

def _mpl():
    import matplotlib
    return matplotlib


RAMPS = ("seq", "flow", "div", "cyclic")
RAMP_LABEL = {
    "seq": "连续（单色相）：热图、密度、单调强度",
    "flow": "连续（多色相）：散点连续着色、需要强过渡的图",
    "div": "发散：相关系数、差值、以 0 为中心的量",
    "cyclic": "环形：相位、角度、风向、一天中的时刻",
}


def cmap(name, which: str = "seq", n: int = 256, crop=None):
    """构造 matplotlib colormap。

    which : seq / flow / div / cyclic，加 `_r` 反向
    crop  : (lo, hi)，0–1，裁掉两端。散点图上小点太浅会看不见，
            常用 crop=(0.12, 0.95)
    """
    from matplotlib.colors import LinearSegmentedColormap
    e = get(name)
    rev = which.endswith("_r")
    key = which[:-2] if rev else which
    stops = list(e[key])
    if rev:
        stops = stops[::-1]
    if crop:
        lo, hi = crop
        k = len(stops) - 1
        a, b = int(round(lo * k)), int(round(hi * k))
        stops = stops[a:b + 1] or stops
    return LinearSegmentedColormap.from_list(f"{e['slug']}_{which}", stops, N=n)


def ramp_info(name, which: str = "flow") -> dict:
    """色标体检数据：明度跨度 / 是否单调 / 感知均匀度。"""
    return get(name)["ramp_stats"][which.replace("_r", "")]


def listed(name, n: int = 6, order: str = None):
    """构造离散 ListedColormap。"""
    from matplotlib.colors import ListedColormap
    return ListedColormap(colors(name, n, order=order), name=_resolve(name))


def register(name=None):
    """把 colormap 注册到 matplotlib，之后可用字符串引用，如 cmap='miku_seq'。"""
    import matplotlib
    names = [_resolve(name)] if name else list(PALETTES)
    done = []
    for s in names:
        for w in ("seq", "seq_r", "flow", "flow_r", "div", "div_r",
                  "cyclic", "cyclic_r"):
            cm = cmap(s, w)
            cm.name = f"{s.split('-')[0]}_{w}"
            try:
                matplotlib.colormaps.register(cm, force=True)
            except AttributeError:                       # matplotlib < 3.5
                matplotlib.cm.register_cmap(cm.name, cm)
            done.append(cm.name)
    return done


import warnings as _warnings
_warnings.filterwarnings("ignore", message="Overwriting the cmap")


def rc(name, n: int = 6, order: str = None) -> dict:
    """返回该配色对应的 rcParams 字典（不直接生效）。

    画多系列图表时建议 order="distinct"。
    """
    e = get(name)
    from cycler import cycler
    return {
        "axes.prop_cycle": cycler(color=colors(name, n, order=order)),
        "figure.facecolor": "white",
        "axes.facecolor": "white",
        "axes.edgecolor": e["ink"],
        "axes.labelcolor": e["ink"],
        "axes.titlecolor": e["ink"],
        "axes.grid": True,
        "axes.axisbelow": True,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "grid.color": e["bg2"],
        "grid.linewidth": 0.8,
        "text.color": e["ink"],
        "xtick.color": e["ink"],
        "ytick.color": e["ink"],
        "xtick.direction": "out",
        "ytick.direction": "out",
        "legend.frameon": False,
        "image.cmap": f"{_resolve(name).split('-')[0]}_seq",
        "savefig.facecolor": "white",
        "savefig.dpi": 300,
        "figure.dpi": 120,
        "lines.linewidth": 2.0,
        "lines.markersize": 5,
        "font.size": 10,
    }


def use(name, n: int = 6, order: str = None):
    """全局套用该配色（颜色循环 + 坐标轴 + 默认 colormap）。

    order 默认 "smooth"（过渡平滑）。**画多系列图表时传 order="distinct"**，
    相邻系列的颜色差异会明显更大。
    """
    import matplotlib.pyplot as plt
    register(name)
    plt.rcParams.update(rc(name, n, order))
    return _resolve(name)


class using:
    """上下文管理器：with anime_palettes.using('miku'): ..."""

    def __init__(self, name, n=6, order=None):
        self.name, self.n, self.order = name, n, order

    def __enter__(self):
        import matplotlib.pyplot as plt
        self._old = dict(plt.rcParams)
        use(self.name, self.n, self.order)
        return _resolve(self.name)

    def __exit__(self, *a):
        import matplotlib.pyplot as plt
        plt.rcParams.update(self._old)
        return False


def preview(name, save: str = None, order: str = None):
    """画一张该配色的示意图（折线 / 柱状 / 散点 / 热图 / 色阶）。"""
    import numpy as np
    import matplotlib.pyplot as plt
    e = get(name)
    od = order or DEFAULT_ORDER
    use_cjk_font()
    title = (f"{e['name_zh']}  ·  {e['name_en']}   [{e['source']}]  色盲友好度 "
             f"{e['cvd_grade']}  ·  排序 {ORDER_LABEL[od]}"
             if _cjk_ok() else
             f"{e['name_en']}   CVD grade {e['cvd_grade']}   order: {od}")
    with using(name, order=od):
        use_cjk_font()
        fig, ax = plt.subplots(2, 3, figsize=(12, 6.4))
        x = np.linspace(0, 10, 120)
        for i in range(6):
            ax[0, 0].plot(x, np.sin(x + i * 0.6) + i * 0.35, label=f"S{i+1}")
        ax[0, 0].set_title("line"); ax[0, 0].legend(ncol=3, fontsize=7)
        cs = colors(name, order=od)
        ax[0, 1].bar(range(6), [5, 7, 4, 8, 6, 3], color=cs)
        ax[0, 1].set_title("bar")
        rng = np.random.default_rng(0)
        for i, c in enumerate(cs):
            ax[0, 2].scatter(rng.normal(i, .6, 40), rng.normal(i, .6, 40), s=18,
                             color=c, edgecolor="white", linewidth=.4)
        ax[0, 2].set_title("scatter")
        g = np.add.outer(np.linspace(0, 1, 40), np.linspace(0, 1, 40))
        ax[1, 0].imshow(g, cmap=cmap(name, "flow")); ax[1, 0].set_title("flow（多色相连续）")
        ax[1, 1].imshow(g - 1, cmap=cmap(name, "div"), vmin=-1, vmax=1)
        ax[1, 1].set_title("diverging（发散）")
        for a in (ax[1, 0], ax[1, 1]):
            a.grid(False)
        li = colors(name, variant="light", order=od)
        di_ = colors(name, variant="dark", order=od)
        for i, c in enumerate(cs):
            for j, v in enumerate((li[i], c, di_[i])):
                ax[1, 2].add_patch(plt.Rectangle((i, -j), 1, 1, color=v))
        for k in range(48):
            ax[1, 2].add_patch(plt.Rectangle((k / 8.0, -4.1), 1 / 8.0, .9,
                                             color=e["seq"][round(k * (len(e["seq"]) - 1) / 47)]))
            ax[1, 2].add_patch(plt.Rectangle((k / 8.0, -5.2), 1 / 8.0, .9,
                                             color=e["cyclic"][round(k * (len(e["cyclic"]) - 1) / 47)]))
        ax[1, 2].text(6.1, -3.65, "seq", fontsize=7, va="center")
        ax[1, 2].text(6.1, -4.75, "cyclic", fontsize=7, va="center")
        ax[1, 2].set_xlim(0, 6.9); ax[1, 2].set_ylim(-5.4, 1); ax[1, 2].axis("off")
        ax[1, 2].set_title("light / main / dark")
        for a in ax.ravel()[:3]:
            a.grid(alpha=.35)
        fig.suptitle(title, fontsize=12)
        fig.tight_layout()
        if save:
            fig.savefig(save, dpi=200, bbox_inches="tight")
        return fig


def wheel(name=None, ax=None, save: str = None, order: str = None, show_path: bool = True):
    """画色环：极坐标里 角度 = CIELAB 色相 h，半径 = 彩度 C，点的明暗即 L*。
    一眼看出这套配色占了色轮的哪几块、彩度够不够、有没有色相扎堆。
    name=None 时画整个色库的色相分布。"""
    import numpy as np
    import matplotlib.pyplot as plt
    use_cjk_font()
    if name is None:
        return wheel_all(save=save)
    e = get(name)
    idx = e["orders"][order or DEFAULT_ORDER]
    if ax is None:
        fig, ax = plt.subplots(figsize=(4.6, 4.6), subplot_kw=dict(projection="polar"))
    else:
        fig = ax.figure
    # 背景色轮
    TH, RR = np.meshgrid(np.linspace(0, 2 * np.pi, 217), np.linspace(0, 1, 34))
    bg = np.zeros(TH.shape + (3,))
    for i in range(TH.shape[0]):
        for j in range(TH.shape[1]):
            bg[i, j] = _lab_rgb(76.0, 66 * RR[i, j] * np.cos(TH[i, j]),
                                66 * RR[i, j] * np.sin(TH[i, j]))
    ax.pcolormesh(TH, RR * 66, bg, shading="gouraud", alpha=0.42,
                  rasterized=True, zorder=0)
    pts = [(np.radians(e["wheel"][i]["h"]), e["wheel"][i]["C"],
            e["colors"][i], e["wheel"][i]["L"]) for i in idx]
    if show_path:
        ax.plot([p[0] for p in pts], [p[1] for p in pts],
                color=e["ink"], lw=1.1, alpha=.45, zorder=2)
    for k, (th, C, col, L) in enumerate(pts):
        ax.scatter([th], [C], s=340, color=col, edgecolor="white",
                   linewidth=1.8, zorder=3)
        ax.annotate(str(k + 1), (th, C), color="#fff" if L < 62 else "#111",
                    ha="center", va="center", fontsize=8.5, zorder=4)
    ax.set_theta_zero_location("E")
    ax.set_rmax(66)
    ax.set_rticks([20, 40, 60])
    ax.set_yticklabels(["C20", "C40", "C60"], fontsize=7, color="#999")
    ax.set_xticks(np.radians([0, 60, 120, 180, 240, 300]))
    ax.set_xticklabels(["红 0°", "黄 60°", "绿 120°", "青 180°", "蓝 240°", "紫 300°"],
                       fontsize=8)
    ax.grid(color="#ddd", lw=.6)
    ax.set_title(f"{e['name_zh']}  色环（角度=色相，半径=彩度）"
                 if _cjk_ok() else f"{e['name_en']}  hue wheel", fontsize=11, pad=14)
    if save:
        fig.savefig(save, dpi=200, bbox_inches="tight", facecolor="white")
    return ax


def _lab_rgb(L, a, b):
    """Lab -> sRGB（0–1，越界按彩度收敛），仅供画色环底图用。"""
    import numpy as np
    def f_inv(t):
        return t ** 3 if t ** 3 > 216 / 24389 else (t - 4 / 29) * 108 / 841
    for scale in (1.0, .8, .65, .5, .35, .2, .1):
        fy = (L + 16) / 116
        fx, fz = fy + a * scale / 500, fy - b * scale / 200
        X, Y, Z = f_inv(fx) * .95047, f_inv(fy), f_inv(fz) * 1.08883
        r = 3.2404542 * X - 1.5371385 * Y - .4985314 * Z
        g = -.9692660 * X + 1.8760108 * Y + .0415560 * Z
        bl = .0556434 * X - .2040259 * Y + 1.0572252 * Z
        out = []
        for c in (r, g, bl):
            c = max(0.0, min(1.0, c))
            out.append(12.92 * c if c <= .0031308 else 1.055 * c ** (1 / 2.4) - .055)
        if all(0 <= v <= 1 for v in (r, g, bl)):
            return np.array(out)
    return np.array(out)


def wheel_all(save: str = None, annotate: bool = False):
    """整个色库的色相/彩度分布：看还缺哪一块色相。"""
    import numpy as np
    import matplotlib.pyplot as plt
    use_cjk_font()
    fig, ax = plt.subplots(figsize=(6.4, 6.4), subplot_kw=dict(projection="polar"))
    for s, e in PALETTES.items():
        for w, col in zip(e["wheel"], e["colors"]):
            ax.scatter([np.radians(w["h"])], [w["C"]], s=58, color=col,
                       edgecolor="white", linewidth=.7, alpha=.92)
    ax.set_theta_zero_location("E")
    ax.set_rmax(70)
    ax.set_xticks(np.radians([0, 60, 120, 180, 240, 300]))
    ax.set_xticklabels(["红 0°", "黄 60°", "绿 120°", "青 180°", "蓝 240°", "紫 300°"],
                       fontsize=9)
    ax.set_rticks([20, 40, 60])
    ax.set_yticklabels(["C20", "C40", "C60"], fontsize=7, color="#999")
    ax.grid(color="#ddd", lw=.6)
    ax.set_title(f"全库 {len(PALETTES)} 套 × 6 色的色相 / 彩度分布"
                 if _cjk_ok() else "library hue / chroma coverage", fontsize=12, pad=16)
    if save:
        fig.savefig(save, dpi=200, bbox_inches="tight", facecolor="white")
    return ax


def _most_separated(hexes, k=3):
    """从一套色里挑 k 个两两色差最大的（用于只需要少数几类的图）。"""
    import itertools as _it
    from math import inf
    def de(a, b):
        la, lb = _lab(a), _lab(b)
        return sum((x - y) ** 2 for x, y in zip(la, lb)) ** .5
    best, bs = None, -inf
    for comb in _it.combinations(range(len(hexes)), k):
        m = min(de(hexes[i], hexes[j]) for i, j in _it.combinations(comb, 2))
        if m > bs:
            best, bs = comb, m
    return list(best)


def _lab(h):
    import math as _m
    def s2l(c):
        return c / 12.92 if c <= .04045 else ((c + .055) / 1.055) ** 2.4
    r, g, b = [s2l(int(h[1:][i:i + 2], 16) / 255) for i in (0, 2, 4)]
    X = .4124564 * r + .3575761 * g + .1804375 * b
    Y = .2126729 * r + .7151522 * g + .0721750 * b
    Z = .0193339 * r + .1191920 * g + .9503041 * b
    def f(t):
        return t ** (1 / 3) if t > 216 / 24389 else (841 / 108) * t + 4 / 29
    fx, fy, fz = f(X / .95047), f(Y), f(Z / 1.08883)
    return (116 * fy - 16, 500 * (fx - fy), 200 * (fy - fz))


def scatter_guide(name, save: str = None, seed: int = 3):
    """散点图四种配色策略的对照图：
    分类散点 / 连续变量着色 / 密度大时的处理 / 双变量（类别×强度）。"""
    import numpy as np
    import matplotlib.pyplot as plt
    e = get(name)
    use_cjk_font()
    cn = _cjk_ok()
    rng = np.random.default_rng(seed)
    with using(name):
        use_cjk_font()
        fig, ax = plt.subplots(2, 2, figsize=(11, 8.6))

        # ① 分类散点：区分度优先 + 白描边 + 形状冗余
        cs = colors(name, order="distinct")
        marks = ["o", "s", "^", "D", "v", "P"]
        for i in range(5):
            x = rng.normal(i * .8, 1.05, 55)
            y = rng.normal(i * .75, 1.05, 55)
            ax[0, 0].scatter(x, y, s=46, color=cs[i], marker=marks[i],
                             edgecolor="white", linewidth=.7, alpha=.95,
                             label=f"{'组' if cn else 'G'}{i+1}")
        ax[0, 0].legend(fontsize=8, ncol=3)
        ax[0, 0].set_title("① 分类散点：order='distinct' + 白描边 + 形状冗余" if cn
                           else "1. categorical: distinct order + white edge + markers",
                           fontsize=11)

        # ② 连续变量着色：flow 色标（多色相，强过渡）
        n = 420
        x = rng.normal(0, 1, n); y = x * .75 + rng.normal(0, .75, n)
        v = x + y + rng.normal(0, .35, n)
        sc = ax[0, 1].scatter(x, y, c=v, s=42, cmap=cmap(name, "flow", crop=(.10, .93)),
                              edgecolor="white", linewidth=.35)
        fig.colorbar(sc, ax=ax[0, 1], shrink=.85, label="强度" if cn else "value")
        ax[0, 1].set_title("② 连续着色：cmap='flow' + crop 掉最浅端" if cn
                           else "2. continuous: flow cmap, cropped", fontsize=11)

        # ③ 点太多：去描边 + 降 alpha + 只用色标深段
        n = 3500
        x = rng.normal(0, 1, n); y = x * .6 + rng.normal(0, .8, n)
        v = np.hypot(x, y)
        ax[1, 0].scatter(x, y, c=v, s=9, alpha=.42, linewidth=0,
                         cmap=cmap(name, "flow", crop=(.35, 1.0)))
        ax[1, 0].set_title("③ 密度大：s↓ alpha↓ 去描边 + crop=(0.35,1) 保持可见" if cn
                           else "3. dense: smaller, alpha, dark half only", fontsize=11)

        # ④ 双变量：类别定色相，强度走该色的 light→dark
        from matplotlib.colors import LinearSegmentedColormap
        tri = _most_separated(e["colors"], 3)
        li3 = [e["light"][k] for k in tri]
        dk3 = [e["dark"][k] for k in tri]
        for i in range(3):
            base, lo, hi = e["colors"][tri[i]], li3[i], dk3[i]
            cm = LinearSegmentedColormap.from_list("t", [lo, base, hi])
            x = rng.normal(i * 1.6, .85, 90); y = rng.normal(i * .9, .85, 90)
            ax[1, 1].scatter(x, y, c=np.linspace(0, 1, 90), cmap=cm, s=42,
                             edgecolor="white", linewidth=.4)
        ax[1, 1].set_title("④ 双变量：类别定色相，强度走 light→main→dark" if cn
                           else "4. bivariate: hue = class, lightness = value", fontsize=11)

        for a in ax.ravel():
            a.grid(alpha=.3)
        fig.suptitle(f"{e['name_zh']} · 散点图配色策略" if cn
                     else f"{e['name_en']} · scatter strategies", fontsize=13)
        fig.tight_layout()
        if save:
            fig.savefig(save, dpi=180, bbox_inches="tight")
        return fig


def to_hex_block(name, order: str = None) -> str:
    """给 Origin / GraphPad / AI 直接粘贴的十六进制清单。"""
    return "\n".join(colors(name, order=order))


# ================================================================ 命令行
# 零依赖，方便 `uvx --from git+... anime-palettes ls` 直接用。

_LANGS = ("python", "python256", "r", "matlab", "origin", "css", "hex")


def _sample(stops, n):
    """在 sRGB 里线性重采样到 n 级（stops 已足够密，误差可忽略）。"""
    def hx(h):
        return [int(h[1:][i:i + 2], 16) / 255 for i in (0, 2, 4)]

    def xh(v):
        return "#" + "".join("%02X" % max(0, min(255, round(c * 255))) for c in v)
    out = []
    for i in range(n):
        t = i / (n - 1) * (len(stops) - 1)
        k = min(int(t), len(stops) - 2)
        f = t - k
        a, b = hx(stops[k]), hx(stops[k + 1])
        out.append(xh([a[j] + (b[j] - a[j]) * f for j in range(3)]))
    return out


def code(name, ramp: str = "flow", lang: str = "python") -> str:
    """生成可直接粘贴的色标代码。lang: python/python256/r/matlab/origin/css/hex"""
    e = get(name)
    ramp = ramp.replace("_r", "")
    if ramp not in RAMPS:
        raise ValueError(f"ramp 只能是 {RAMPS}")
    if lang not in _LANGS:
        raise ValueError(f"lang 只能是 {_LANGS}")
    stops = e[ramp]
    st = e["ramp_stats"][ramp]
    v = f"{e['slug'].split('-')[0]}_{ramp}"
    head = f"{e['name_zh']} / {e['name_en']} — {RAMP_LABEL[ramp]}"
    meta = (f"L* 跨度 {st['L_range']} · 明度单调 {'是' if st['monotonic'] else '否'}"
            f" · 感知均匀度 {st['uniformity']}")

    def wrap(items, per, ind):
        rows = [ind + ", ".join(items[i:i + per]) for i in range(0, len(items), per)]
        return ",\n".join(rows)

    q = [f'"{c}"' for c in stops]
    if lang == "python":
        tail = {
            "flow": f'# ax.scatter(x, y, c=v, cmap={v}, s=42, edgecolor="white", linewidth=.35)',
            "div": f"# ax.imshow(C, cmap={v}, vmin=-1, vmax=1)   # vmin/vmax 要对称",
            "cyclic": f"# ax.scatter(x, y, c=phase, cmap={v}, vmin=0, vmax=2*np.pi)",
            "seq": f"# ax.imshow(Z, cmap={v})",
        }[ramp]
        return (f"# {head}\n# {meta}\n"
                f"from matplotlib.colors import LinearSegmentedColormap\n\n"
                f'{v} = LinearSegmentedColormap.from_list("{e["slug"]}_{ramp}", [\n'
                f"{wrap(q, 4, '    ')},\n])\n\n{tail}\n")
    if lang == "python256":
        s256 = [f'"{c}"' for c in _sample(stops, 256)]
        return (f"# {head}  —  256 级查找表\n# {meta}\n"
                f"{v}_hex = [\n{wrap(s256, 6, '    ')},\n]\n\n"
                f"from matplotlib.colors import ListedColormap\n"
                f'{v} = ListedColormap({v}_hex, name="{e["slug"]}_{ramp}")\n')
    if lang == "r":
        return (f"# {head}\n# {meta}\n"
                f"{v}_stops <- c(\n{wrap(q, 4, '  ')}\n)\n"
                f'{v} <- grDevices::colorRampPalette({v}_stops, space = "Lab")\n\n'
                f"# + scale_colour_gradientn(colours = {v}(256))\n"
                f"# + scale_fill_gradientn(colours = {v}(256))\n")
    if lang == "matlab":
        rows = []
        for c in _sample(stops, 256):
            r, g, b = [int(c[1:][i:i + 2], 16) / 255 for i in (0, 2, 4)]
            rows.append(f"    {r:.4f} {g:.4f} {b:.4f}")
        return (f"% {head}\n% {meta}\n{v} = [\n" + ";\n".join(rows) + "\n];\n\n"
                f"% colormap({v}); scatter(x, y, 36, v, \"filled\"); colorbar\n")
    if lang == "origin":
        return f"# {head}  —  16 级\n# {meta}\n" + "\n".join(_sample(stops, 16)) + "\n"
    if lang == "css":
        s12 = _sample(stops, 12)
        grad = ",\n".join(f"    {c} {i * 100 / 11:.1f}%" for i, c in enumerate(s12))
        return (f"/* {head} */\n/* {meta} */\n.{e['slug']}-{ramp} {{\n"
                f"  background: linear-gradient(90deg,\n{grad}\n  );\n}}\n")
    return f"{head}\n{meta}\n\n" + "\n".join(_sample(stops, 32)) + "\n"


def _swatch(hexes, width=8):
    """终端真彩色色块（不支持真彩色的终端会退化成普通文字）。"""
    out = []
    for c in hexes:
        r, g, b = [int(c[1:][i:i + 2], 16) for i in (0, 2, 4)]
        fg = "0;0;0" if (0.299 * r + 0.587 * g + 0.114 * b) > 150 else "255;255;255"
        out.append(f"\033[48;2;{r};{g};{b}m\033[38;2;{fg}m{c.center(width)}\033[0m")
    return "".join(out)


def main(argv=None):
    """命令行入口：anime-palettes <命令> ..."""
    import argparse
    import json as _json
    p = argparse.ArgumentParser(
        prog="anime-palettes",
        description="动漫 / 游戏角色配色库 —— 36 套，面向科研配图与 PPT",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""示例:
  anime-palettes ls --family 蓝 --grade A
  anime-palettes show 胡桃 --order distinct
  anime-palettes hex miku -n 3
  anime-palettes code ganyu --ramp flow --lang python > ganyu_flow.py
  anime-palettes search 原神
  anime-palettes json miku | jq .colors
""")
    sub = p.add_subparsers(dest="cmd", required=True)

    a = sub.add_parser("ls", help="列出全部配色（带色块预览）")
    a.add_argument("--family", help="按色系筛：红 橙 黄 绿 青 蓝 紫 粉 中性 撞色")
    a.add_argument("--grade", choices=list("ABC"), help="按色盲友好度筛")
    a.add_argument("--order", choices=ORDERS, default=DEFAULT_ORDER)

    a = sub.add_parser("show", help="显示单套配色的全部细节")
    a.add_argument("name")
    a.add_argument("--order", choices=ORDERS, default=DEFAULT_ORDER)

    a = sub.add_parser("hex", help="只输出 HEX，一行一个，方便管道")
    a.add_argument("name")
    a.add_argument("-n", type=int, default=6)
    a.add_argument("--order", choices=ORDERS, default=DEFAULT_ORDER)
    a.add_argument("--variant", choices=("main", "dark", "light"), default="main")
    a.add_argument("--safe", action="store_true", help="只输出色盲安全子集")

    a = sub.add_parser("code", help="生成色标代码")
    a.add_argument("name")
    a.add_argument("--ramp", choices=RAMPS, default="flow")
    a.add_argument("--lang", choices=_LANGS, default="python")

    a = sub.add_parser("search", help="按角色 / 色调 / 作品模糊搜索")
    a.add_argument("query")

    a = sub.add_parser("json", help="输出该配色的完整 JSON")
    a.add_argument("name")

    ns = p.parse_args(argv)

    if ns.cmd == "ls":
        rows = [e for e in PALETTES.values()
                if (not ns.family or e["family"] == ns.family)
                and (not ns.grade or e["cvd_grade"] == ns.grade)]
        rows.sort(key=lambda e: (FAMILIES.index(e["family"]), e["slug"]))
        for e in rows:
            print(f"{e['name_zh']:<14}{e['family']}  {e['cvd_grade']}  "
                  f"{_swatch(colors(e['slug'], order=ns.order), 9)}  {e['slug']}")
        print(f"\n共 {len(rows)} 套 · 色盲友好度 A=全可分 B=大部分 C=只用安全子集")
        return 0

    if ns.cmd == "search":
        for s in find(ns.query):
            pass
        return 0

    e = get(ns.name)

    if ns.cmd == "json":
        print(_json.dumps(e, ensure_ascii=False, indent=1))
        return 0

    if ns.cmd == "hex":
        cs = safe(ns.name) if ns.safe else colors(
            ns.name, n=ns.n, variant=ns.variant, order=ns.order)
        print("\n".join(cs))
        return 0

    if ns.cmd == "code":
        print(code(ns.name, ns.ramp, ns.lang), end="")
        return 0

    # show
    print(f"\n  {e['name_zh']}   {e['name_en']}")
    print(f"  {e['source']} · 色系 {e['family']} · 色盲友好度 {e['cvd_grade']}"
          f" · 最小 ΔE00 {e['min_de']}\n")
    for label, variant in (("浅 light", "light"), ("主 main ", "main"), ("深 dark ", "dark")):
        print(f"  {label}  {_swatch(colors(ns.name, variant=variant, order=ns.order), 9)}")
    print(f"\n  中性色     {_swatch([e['bg'], e['bg2'], e['muted'], e['ink']], 9)}"
          f"   bg / bg2 / muted / ink")
    print(f"  色盲安全   {_swatch(safe(ns.name), 9)}")
    print(f"\n  排序 {ORDER_LABEL[ns.order]}")
    for o in ORDERS:
        if o != ns.order:
            print(f"       {ORDER_LABEL[o]:<18}{_swatch(colors(ns.name, order=o), 9)}")
    print()
    for r in RAMPS:
        st = e["ramp_stats"][r]
        print(f"  {r:<7}{_swatch(_sample(e[r], 8), 7)}  L*{st['L_range']:>5} "
              f"单调{'是' if st['monotonic'] else '否'} 均匀{st['uniformity']}  {RAMP_LABEL[r]}")
    print(f"\n  取代码: anime-palettes code {e['slug']} --ramp flow --lang python\n")
    return 0


__all__ = ["PALETTES", "FAMILIES", "ORDERS", "ORDER_LABEL", "order_of", "code", "main", "get", "colors", "safe", "neutrals", "ls",
           "find", "cmap", "listed", "register", "rc", "use", "using",
           "preview", "to_hex_block", "use_cjk_font", "wheel", "wheel_all",
           "scatter_guide", "RAMPS", "RAMP_LABEL", "ramp_info"]


if __name__ == "__main__":
    import sys as _sys
    _sys.exit(main())
