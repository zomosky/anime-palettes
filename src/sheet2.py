import os
import sys
import json, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

# 中文字体：走 anime_palettes.use_cjk_font() 自动挑一个系统里真的装了的。
# 别再在这里手写字体名单 —— 原来写死的 ['WenQuanYi Zen Hei','Noto Sans CJK SC','DejaVu Sans']
# 全是 Linux 字体，在 macOS 上一个都没有，matplotlib 会**静默**退到 DejaVu Sans，
# 而它没有中文字形，于是整张图的中文全变成方框（tofu）。这张图是要放进 README 的，
# 坏了没有任何测试会红 —— CI 的 build 关不比对 PNG 字节。所以下面挑不到就直接报错退出，
# 宁可 make docs 失败，也不要悄悄产出一张中文全是方框的图。
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import anime_palettes as ap  # noqa: E402

_font = ap.use_cjk_font()
if not _font:
    raise SystemExit(
        "找不到任何中文字体，生成出来的图中文会全变成方框。\n"
        f"在 {', '.join(ap.CJK_FONTS)} 里装一个再跑。\n"
        "（macOS 自带 PingFang SC / Heiti SC；Linux 可装 fonts-noto-cjk）"
    )

os.makedirs('build', exist_ok=True)
lib=json.load(open('library.json'))
n=len(lib)
fig,axes=plt.subplots(n,1,figsize=(13,n*0.58))
GC={'A':'#1F7A4D','B':'#B07A12','C':'#9C4040'}
for ax,e in zip(axes,lib):
    for i,c in enumerate(e['colors']):
        ax.add_patch(Rectangle((i,0),1,1,color=c))
        ax.text(i+.5,.5,c[1:],ha='center',va='center',fontsize=6.2,family='monospace',
                color='#fff' if sum(int(c[1:][k:k+2],16) for k in (0,2,4))<330 else '#111')
    for i in range(30):
        ax.add_patch(Rectangle((6.4+i*0.14,0),0.14,1,color=e['seq'][int(i*255/29)]))
    for i in range(30):
        ax.add_patch(Rectangle((11.0+i*0.14,0),0.14,1,color=e['div'][int(i*255/29)]))
    ax.set_xlim(-6.2,15.4); ax.set_ylim(0,1); ax.axis('off')
    ax.text(-6.1,.5,f"{e['zh']} · {e['tone_zh']}",fontsize=8.5,va='center')
    ax.text(-2.5,.5,e['name_en'],fontsize=6.5,va='center',color='#777')
    ax.text(15.35,.5,e['cvd_grade'],fontsize=7,va='center',ha='right',
            color=GC[e['cvd_grade']],fontweight='bold')
fig.suptitle('动漫 / 游戏角色配色库 · 58 套 —— 主色 6 / 连续色标 / 发散色标',fontsize=13,y=0.998)
plt.tight_layout(rect=[0,0,1,0.995])
plt.savefig('build/配色总览.png',dpi=140,facecolor='white',bbox_inches='tight')
print('ok')
