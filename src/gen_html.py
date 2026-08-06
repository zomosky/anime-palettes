# -*- coding: utf-8 -*-
"""生成单文件交互色卡库 anime-palettes.html"""
import os
import json

os.makedirs('build', exist_ok=True)
lib = json.load(open('library.json'))
from marks import MARKS

def thin(seq, k=17):
    return [seq[round(i * 255 / (k - 1))] for i in range(k)]

DATA = [dict(
    slug=e['slug'], zh=e['zh'], en=e['en'], tone=e['tone_zh'], toneEn=e['tone_en'],
    nameZh=e['name_zh'], nameEn=e['name_en'], fam=e['family'], src=e['source'],
    kind=e['kind'], grade=e['cvd_grade'], safe=e['safe_set'],
    c=e['colors'], d=e['dark'], l=e['light'], ord=e['orders'],
    bg=e['bg'], bg2=e['bg2'], ink=e['ink'], muted=e['muted'],
    seq=thin(e['seq']), div=thin(e['div']),
    flw=thin(e['flow'], 25), cyc=thin(e['cyclic'], 25), wh=e['wheel'],
    rs={k: {'m': v['monotonic'], 'r': v['L_range'], 'u': v['uniformity']}
        for k, v in e['ramp_stats'].items()},
    minde=e['min_de'], cvd=e['cvd'],
) for e in lib]

HTML = r"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>动漫 / 游戏角色配色库 · 58 套</title>
<meta name="description" content="58 套取自动漫与游戏角色的配色，为科研配图与 PPT 做过色彩学调优：色相锁定、ΔE2000 区分度优化、色盲评级、四条连续色标。点色块复制 HEX，点色标条取 Python/R/MATLAB 代码。">
<meta name="theme-color" content="#f6f6f4">
<meta property="og:type" content="website">
<meta property="og:title" content="动漫 / 游戏角色配色库 · 58 套">
<meta property="og:description" content="每套 6 主色 + 深浅变体 + 4 条连续色标 + 色环，标注色盲友好度。面向科研配图与 PPT。">
<meta property="og:url" content="https://zomosky.github.io/anime-palettes/">
<meta name="twitter:card" content="summary_large_image">
<style>
:root{
  --bg:#f6f6f4; --card:#ffffff; --fg:#1d1d21; --dim:#6c6c76; --line:#e4e4e0;
  --accent:#1d1d21; --shadow:0 1px 2px rgba(0,0,0,.05),0 8px 24px rgba(0,0,0,.05);
}
html[data-theme="dark"]{
  --bg:#131316; --card:#1c1c20; --fg:#eeeef0; --dim:#9a9aa4; --line:#2c2c32;
  --accent:#eeeef0; --shadow:0 1px 2px rgba(0,0,0,.4),0 8px 24px rgba(0,0,0,.35);
}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--fg);
  font-family:-apple-system,BlinkMacSystemFont,"PingFang SC","Microsoft YaHei","Noto Sans SC",
  "Helvetica Neue",Arial,sans-serif;-webkit-font-smoothing:antialiased}
code,.mono{font-family:ui-monospace,SFMono-Regular,"SF Mono",Menlo,Consolas,monospace}
header{position:sticky;top:0;z-index:20;background:var(--bg);
  border-bottom:1px solid var(--line);backdrop-filter:blur(8px)}
.wrap{max-width:1520px;margin:0 auto;padding:0 22px}
h1{font-size:19px;margin:0;font-weight:650;letter-spacing:.2px}
h1 .gh{font-size:11.5px;font-weight:500;color:var(--dim);text-decoration:none;
  margin-left:10px;border:1px solid var(--line);border-radius:6px;padding:3px 8px;
  vertical-align:middle;white-space:nowrap}
h1 .gh:hover{color:var(--fg);border-color:var(--dim)}
.sub{font-size:12.5px;color:var(--dim);margin-top:3px;line-height:1.6}
.topbar{display:flex;align-items:flex-end;justify-content:space-between;gap:16px;padding:16px 0 12px;flex-wrap:wrap}
.controls{display:flex;gap:8px;align-items:center;flex-wrap:wrap;padding-bottom:12px}
#theme{margin-left:auto}
input[type=search]{background:var(--card);border:1px solid var(--line);color:var(--fg);
  border-radius:8px;padding:7px 11px;font-size:13px;width:210px;outline:none}
input[type=search]:focus{border-color:var(--dim)}
.seg{display:flex;background:var(--card);border:1px solid var(--line);border-radius:8px;overflow:hidden}
.seg button{background:none;border:none;color:var(--dim);padding:7px 11px;font-size:12.5px;
  cursor:pointer;font-family:inherit;white-space:nowrap}
.seg button.on{background:var(--accent);color:var(--card)}
.seg button:hover:not(.on){color:var(--fg)}
.lbl{font-size:11.5px;color:var(--dim);margin-right:2px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(430px,1fr));gap:16px;padding:20px 0 60px}
.card{background:var(--card);border:1px solid var(--line);border-radius:12px;overflow:hidden;
  box-shadow:var(--shadow)}
.chead{display:flex;justify-content:space-between;align-items:flex-start;gap:10px;padding:13px 15px 10px}
.cname{font-size:15.5px;font-weight:650;letter-spacing:.2px;line-height:1.35}
.cname .tone{color:var(--dim);font-weight:500}
.cmeta{font-size:11.5px;color:var(--dim);margin-top:3px}
.badges{display:flex;gap:5px;flex-shrink:0;align-items:center}
.mark{width:44px;height:44px;flex-shrink:0;display:block}
.chead .right{display:flex;align-items:center;gap:8px}
.badge{font-size:10.5px;padding:2.5px 7px;border-radius:999px;border:1px solid var(--line);
  color:var(--dim);white-space:nowrap}
.gA{background:#1f7a4d;color:#fff;border-color:transparent}
.gB{background:#b07a12;color:#fff;border-color:transparent}
.gC{background:#9c4040;color:#fff;border-color:transparent}
.sw{display:grid;grid-template-columns:repeat(6,1fr)}
.sw .cell{position:relative;cursor:pointer;height:66px;display:flex;align-items:flex-end;
  justify-content:center;padding-bottom:6px;transition:transform .12s}
.sw.trip .cell{height:22px;padding:0}
.sw .cell span{font-size:10px;font-family:ui-monospace,Menlo,monospace;letter-spacing:.2px;
  opacity:.72;transition:opacity .12s}
.sw .cell:hover span{opacity:1}
.sw.trip .cell span{opacity:0}
.sw.trip .cell:hover span{opacity:1}
.sw .cell.unsafe::after{content:"";position:absolute;top:5px;right:5px;width:5px;height:5px;
  border-radius:50%;background:rgba(255,255,255,.75);box-shadow:0 0 0 1px rgba(0,0,0,.25)}
.ramp{height:17px;cursor:pointer;position:relative;transition:transform .12s}
.ramps:hover .ramp{opacity:.72}
.ramps .ramp:hover{opacity:1;transform:scaleY(1.45);z-index:3;
  box-shadow:0 0 0 1px var(--fg)}
.rlab span{cursor:pointer}
.rlab span:hover{color:var(--fg)}
/* ---- 代码面板 ---- */
#mask{position:fixed;inset:0;background:rgba(0,0,0,.42);backdrop-filter:blur(2px);
  display:none;z-index:60;align-items:center;justify-content:center;padding:24px}
#mask.on{display:flex}
#modal{background:var(--card);border:1px solid var(--line);border-radius:14px;
  width:min(820px,100%);max-height:88vh;display:flex;flex-direction:column;
  box-shadow:0 24px 70px rgba(0,0,0,.3);overflow:hidden}
#modal h3{margin:0;font-size:15.5px;font-weight:650}
.mhead{padding:15px 18px 11px;border-bottom:1px solid var(--line)}
.msub{font-size:11.5px;color:var(--dim);margin-top:4px;line-height:1.6}
.mbar{height:20px;border-radius:5px;margin-top:11px}
.mtabs{display:flex;gap:5px;flex-wrap:wrap;padding:11px 18px 0}
.mtabs button{background:none;border:1px solid var(--line);color:var(--dim);
  border-radius:7px;padding:4.5px 10px;font-size:11.5px;cursor:pointer;font-family:inherit}
.mtabs button.on{background:var(--accent);color:var(--card);border-color:transparent}
#code{margin:11px 18px;padding:13px 15px;background:var(--bg);border:1px solid var(--line);
  border-radius:9px;font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;
  font-size:11.5px;line-height:1.62;white-space:pre;overflow:auto;flex:1 1 auto;
  min-height:150px;color:var(--fg);tab-size:2}
.mfoot{display:flex;gap:8px;padding:0 18px 16px;flex-wrap:wrap;align-items:center}
.mfoot button{border:1px solid var(--line);background:none;color:var(--fg);
  border-radius:8px;padding:7px 14px;font-size:12.5px;cursor:pointer;font-family:inherit}
.mfoot button.primary{background:var(--accent);color:var(--card);border-color:transparent}
.mfoot button:hover{border-color:var(--dim)}
.mfoot .sp{flex:1 1 auto}
.mstat{font-size:11px;color:var(--dim);font-family:ui-monospace,Menlo,monospace}
.chartrow{display:flex;align-items:center;gap:6px;padding:6px 12px 2px;background:var(--card)}
.wheel{flex:0 0 92px;width:92px;height:92px}
.chart{flex:1 1 auto;min-width:0}
.ramps{display:grid;grid-template-columns:repeat(4,1fr);gap:1px;background:var(--line)}
.rlab{display:grid;grid-template-columns:repeat(4,1fr);font-size:9.5px;color:var(--dim);
  padding:4px 12px 0;gap:1px}
.rlab span{text-align:center}
.foot{display:flex;justify-content:space-between;align-items:center;gap:8px;
  padding:8px 13px 12px;font-size:11px;color:var(--dim);flex-wrap:wrap}
.copy{display:flex;gap:5px;flex-wrap:wrap}
.copy button{background:none;border:1px solid var(--line);color:var(--dim);border-radius:6px;
  padding:3.5px 8px;font-size:11px;cursor:pointer;font-family:inherit}
.copy button:hover{color:var(--fg);border-color:var(--dim)}
.stat{font-family:ui-monospace,Menlo,monospace;font-size:10.5px}
#toast{position:fixed;left:50%;bottom:26px;transform:translateX(-50%) translateY(20px);
  background:var(--accent);color:var(--card);padding:9px 16px;border-radius:8px;font-size:13px;
  opacity:0;pointer-events:none;transition:all .18s;z-index:99;max-width:80vw;
  overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
#toast.on{opacity:1;transform:translateX(-50%) translateY(0)}
.empty{padding:60px 0;text-align:center;color:var(--dim);font-size:14px}
.note{font-size:11.5px;color:var(--dim);line-height:1.7;padding:0 0 18px;max-width:1000px}
kbd{border:1px solid var(--line);border-radius:4px;padding:1px 5px;font-size:11px;
  font-family:ui-monospace,Menlo,monospace}
</style>
</head>
<body>
<header>
 <div class="wrap">
  <div class="topbar">
   <div>
    <h1>动漫 / 游戏角色配色库<a class="gh" href="https://github.com/zomosky/anime-palettes"
       target="_blank" rel="noopener" title="项目主页：Python 模块 / Excel / PPT 取色板 / 色板文件">项目主页 ↗</a></h1>
    <div class="sub">58 套 · 每套 6 主色 + 深/浅变体 + 连续与发散色标 · 面向 PPT 与科研配图 ·
      点击色块复制 HEX，点击底部色标条取 colormap 代码 · 右上「排序」可切换 4 种排列</div>
   </div>
  </div>
  <div class="controls">
   <input type="search" id="q" placeholder="搜角色 / 色调 / 作品…">
   <span class="lbl">色系</span>
   <div class="seg" id="fam"></div>
   <span class="lbl">排序</span>
   <div class="seg" id="order">
    <button data-o="smooth" class="on" title="相邻色差最小，过渡最顺滑">平滑</button>
    <button data-o="distinct" title="前几色差异最大，画多系列图表用这个">区分度</button>
    <button data-o="hue" title="红→橙→黄→绿→青→蓝→紫">色相环</button>
    <button data-o="light" title="L* 由高到低，也最适合灰度打印">明度</button>
   </div>
   <span class="lbl">色盲</span>
   <div class="seg" id="grade">
    <button data-g="" class="on">全部</button><button data-g="A">A</button>
    <button data-g="B">B</button><button data-g="C">C</button>
   </div>
   <span class="lbl">模拟</span>
   <div class="seg" id="cvd">
    <button data-v="none" class="on">正常</button><button data-v="protan">红色盲</button>
    <button data-v="deutan">绿色盲</button><button data-v="tritan">蓝色盲</button>
    <button data-v="gray">灰度</button>
   </div>
   <div class="seg" id="view">
    <button data-w="main" class="on">主色</button><button data-w="trip">含深浅</button>
   </div>
   <div class="seg" id="mark"><button id="mkbtn" title="显示每套配色的标志物图形">标志物</button></div>
   <div class="seg" id="theme"><button id="tbtn">深色界面</button></div>
  </div>
 </div>
</header>
<div class="wrap">
 <div class="note" id="note"></div>
 <div class="grid" id="grid"></div>
</div>
<div id="toast"></div>
<div id="mask">
 <div id="modal">
  <div class="mhead">
   <h3 id="mtitle"></h3>
   <div class="msub" id="mdesc"></div>
   <div class="mbar" id="mbar"></div>
  </div>
  <div class="mtabs" id="mtabs"></div>
  <div id="code"></div>
  <div class="mfoot">
   <button class="primary" id="mcopy">复制代码</button>
   <button id="mdl">下载文件</button>
   <button id="mdlall">下载整套 .py</button>
   <span class="sp"></span>
   <span class="mstat" id="mstat"></span>
   <button id="mclose">关闭</button>
  </div>
 </div>
</div>
<script>
const DATA = __DATA__;
const MK=__MARKS__;
const FAMS = ["红","橙","黄","绿","青","蓝","紫","粉","中性","撞色"];
let state = {q:"", fam:"", grade:"", cvd:"none", view:"main", order:"smooth", mark:false};
const ORDER_LABEL={smooth:"平滑",distinct:"区分度优先",hue:"色相环",light:"明度浅→深"};
const ord = (p,key) => p.ord[state.order].map(i=>p[key][i]);

/* ---------- 色觉模拟（Machado et al. 2009, severity 1.0） ---------- */
const M = {
 protan:[[0.152286,1.052583,-0.204868],[0.114503,0.786281,0.099216],[-0.003882,-0.048116,1.051998]],
 deutan:[[0.367322,0.860646,-0.227968],[0.280085,0.672501,0.047413],[-0.011820,0.042940,0.968881]],
 tritan:[[1.255528,-0.076749,-0.178779],[-0.078411,0.930809,0.147602],[0.004733,0.691367,0.303900]]
};
const s2l = c => c<=0.04045 ? c/12.92 : Math.pow((c+0.055)/1.055,2.4);
const l2s = c => {c=Math.max(0,Math.min(1,c)); return c<=0.0031308?12.92*c:1.055*Math.pow(c,1/2.4)-0.055;};
function hx(h){h=h.replace('#','');return [0,2,4].map(i=>parseInt(h.substr(i,2),16)/255);}
function xh(v){return '#'+v.map(c=>Math.round(Math.max(0,Math.min(1,c))*255).toString(16).padStart(2,'0')).join('').toUpperCase();}
const cache = {};
function sim(h){
  const m = state.cvd; if(m==="none") return h;
  const k = m+h; if(cache[k]) return cache[k];
  const lin = hx(h).map(s2l); let out;
  if(m==="gray"){const y=0.2126*lin[0]+0.7152*lin[1]+0.0722*lin[2]; out=[y,y,y];}
  else {const A=M[m]; out=A.map(r=>r[0]*lin[0]+r[1]*lin[1]+r[2]*lin[2]);}
  return cache[k]=xh(out.map(l2s));
}
function lum(h){const l=hx(h).map(s2l);return 0.2126*l[0]+0.7152*l[1]+0.0722*l[2];}
const readable = h => lum(h)>0.42 ? '#111' : '#fff';

/* ---------- 复制 ---------- */
function toast(msg){const t=document.getElementById('toast');t.textContent=msg;t.classList.add('on');
  clearTimeout(t._t);t._t=setTimeout(()=>t.classList.remove('on'),1500);}
function copy(text,msg){
  const done=()=>toast(msg);
  if(navigator.clipboard&&window.isSecureContext){navigator.clipboard.writeText(text).then(done,()=>fb());}
  else fb();
  function fb(){const ta=document.createElement('textarea');ta.value=text;ta.style.position='fixed';
    ta.style.opacity=0;document.body.appendChild(ta);ta.select();
    try{document.execCommand('copy');done();}catch(e){toast('复制失败，请手动选取');}
    document.body.removeChild(ta);}
}

/* ---------- 迷你示意图 ---------- */
function chart(p){
  const C = ord(p,"c").map(sim);
  const W=406,H=76,pad=4;
  let s=`<svg viewBox="0 0 ${W} ${H}" width="100%" height="${H}" style="display:block">`;
  // 折线
  const n=44;
  for(let i=0;i<6;i++){
    let d="";
    for(let j=0;j<n;j++){
      const x=pad+j*(W*0.45-2*pad)/(n-1);
      const y=H/2 + Math.sin(j/5.2+i*0.75)*(H*0.16) - (i-2.5)*4.4;
      d+=(j?"L":"M")+x.toFixed(1)+" "+y.toFixed(1);
    }
    s+=`<path d="${d}" fill="none" stroke="${C[i]}" stroke-width="2" stroke-linecap="round"/>`;
  }
  // 柱状
  const bv=[.62,.9,.44,1,.72,.34], bx=W*0.48, bw=(W*0.24)/6;
  for(let i=0;i<6;i++)
    s+=`<rect x="${(bx+i*bw+1).toFixed(1)}" y="${(H-4-bv[i]*(H-14)).toFixed(1)}" width="${(bw-2).toFixed(1)}" height="${(bv[i]*(H-14)).toFixed(1)}" fill="${C[i]}" rx="1.5"/>`;
  // 散点
  const sx=W*0.755;
  let seed=7; const rnd=()=>{seed=(seed*16807)%2147483647;return seed/2147483647;};
  for(let i=0;i<6;i++)for(let j=0;j<9;j++){
    const x=sx+ (i*1.0+rnd()*3.6)*((W*0.235)/9.2);
    const y=H-6-(i*1.0+rnd()*3.6)*((H-14)/9.2);
    s+=`<circle cx="${x.toFixed(1)}" cy="${y.toFixed(1)}" r="2.6" fill="${C[i]}" fill-opacity=".92"/>`;
  }
  return s+"</svg>";
}
const grad = arr => `linear-gradient(90deg,${arr.map(sim).join(',')})`;

/* ---------- 色环：角度=CIELAB 色相，半径=彩度 ---------- */
function wheelSVG(p){
  const S=92, c=S/2, R=S/2-4, CMAX=64;
  let s=`<svg class="wheel" viewBox="0 0 ${S} ${S}">`;
  // 参考色轮（低透明度扇区）
  for(let k=0;k<36;k++){
    const a0=k*10*Math.PI/180, a1=(k*10+10.4)*Math.PI/180;
    const x0=c+R*Math.cos(a0), y0=c-R*Math.sin(a0);
    const x1=c+R*Math.cos(a1), y1=c-R*Math.sin(a1);
    const hue=k*10;
    s+=`<path d="M${c} ${c}L${x0.toFixed(2)} ${y0.toFixed(2)}A${R} ${R} 0 0 0 ${x1.toFixed(2)} ${y1.toFixed(2)}Z" fill="${labHex(78,52,hue)}" opacity=".26"/>`;
  }
  s+=`<circle cx="${c}" cy="${c}" r="${R}" fill="none" stroke="rgba(128,128,128,.35)" stroke-width=".8"/>`;
  s+=`<circle cx="${c}" cy="${c}" r="${R*20/CMAX}" fill="none" stroke="rgba(128,128,128,.22)" stroke-width=".7"/>`;
  s+=`<circle cx="${c}" cy="${c}" r="${R*40/CMAX}" fill="none" stroke="rgba(128,128,128,.22)" stroke-width=".7"/>`;
  const idx=p.ord[state.order];
  const pt=i=>{const w=p.wh[i], r=Math.min(1,w.C/CMAX)*R, a=w.h*Math.PI/180;
    return [c+r*Math.cos(a), c-r*Math.sin(a)];};
  let d="";
  idx.forEach((i,k)=>{const [x,y]=pt(i); d+=(k?"L":"M")+x.toFixed(2)+" "+y.toFixed(2);});
  s+=`<path d="${d}" fill="none" stroke="rgba(90,90,100,.55)" stroke-width="1.1"/>`;
  idx.forEach(i=>{const [x,y]=pt(i);
    s+=`<circle cx="${x.toFixed(2)}" cy="${y.toFixed(2)}" r="5.4" fill="${sim(p.c[i])}" stroke="#fff" stroke-width="1.3"/>`;});
  return s+"</svg>";
}
/* 极简 Lab(L,C,h)->hex，仅供色轮底图 */
function labHex(L,C,h){
  const r=h*Math.PI/180, a=C*Math.cos(r), b=C*Math.sin(r);
  const fy=(L+16)/116, fx=fy+a/500, fz=fy-b/200;
  const fi=t=>t*t*t>0.008856?t*t*t:(t-4/29)*108/841;
  const X=fi(fx)*0.95047, Y=fi(fy), Z=fi(fz)*1.08883;
  let R=3.2404542*X-1.5371385*Y-0.4985314*Z,
      G=-0.9692660*X+1.8760108*Y+0.0415560*Z,
      B=0.0556434*X-0.2040259*Y+1.0572252*Z;
  return xh([R,G,B].map(l2s));
}

/* ---------- 卡片 ---------- */
function card(p){
  const trip = state.view==="trip";
  const idx = p.ord[state.order];
  const rows = trip ? [ord(p,"l"),ord(p,"c"),ord(p,"d")] : [ord(p,"c")];
  let sw = rows.map((row,ri)=>
    `<div class="sw${trip?' trip':''}">`+row.map((c,i)=>{
      const v=sim(c);
      const unsafe = ri===(trip?1:0) && !p.safe.includes(idx[i]) && p.grade!=="A";
      return `<div class="cell${unsafe?' unsafe':''}" style="background:${v}" data-hex="${c}"
        title="${c}${unsafe?'  · 色盲下与其它色接近':''}"><span style="color:${readable(v)}">${c.slice(1)}</span></div>`;
    }).join('')+`</div>`).join('');
  return `<div class="card" data-slug="${p.slug}">
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
   ${sw}
   <div class="chartrow">${wheelSVG(p)}<div class="chart">${chart(p)}</div></div>
   <div class="rlab">
     <span data-r="seq" title="单色相，热图/密度">连续 seq ↓</span>
     <span data-r="flow" title="多色相、明度单调 —— 散点连续着色首选">强过渡 flow ↓</span>
     <span data-r="div" title="以 0 为中心的量">发散 div ↓</span>
     <span data-r="cyclic" title="相位/角度/时刻">环形 cyclic ↓</span>
   </div>
   <div class="ramps">
     <div class="ramp" data-r="seq" style="background:${grad(p.seq)}" title="点击取代码 · 单色相连续 · L*跨度 ${p.rs.seq.r}"></div>
     <div class="ramp" data-r="flow" style="background:${grad(p.flw)}" title="点击取代码 · 多色相强过渡 · L*跨度 ${p.rs.flow.r} · 明度单调 ${p.rs.flow.m?'是':'否'} · 均匀度 ${p.rs.flow.u}"></div>
     <div class="ramp" data-r="div" style="background:${grad(p.div)}" title="点击取代码 · 发散 · L*跨度 ${p.rs.div.r}"></div>
     <div class="ramp" data-r="cyclic" style="background:${grad(p.cyc)}" title="点击取代码 · 环形 · 首尾闭合"></div>
   </div>
   <div class="foot">
     <span class="stat">ΔE₀₀ ${p.minde} · 色盲ΔE ${Math.min(p.cvd.protan,p.cvd.deutan).toFixed(1)} · 安全 ${p.safe.length}/6</span>
     <span class="copy">
       <button data-a="hex">HEX</button>
       <button data-a="py">Python</button>
       <button data-a="r">R</button>
       <button data-a="mpl">rcParams</button>
       <button data-a="safe">安全子集</button>
       <button data-a="flow" title="散点连续着色用的多色相色标（11 级）">flow 色标</button>
     </span>
   </div>
  </div>`;
}

function payload(p,kind){
  const q = a => a.map(x=>`"${x}"`).join(", ");
  const C = ord(p,"c");
  if(kind==="hex") return C.join("\n");
  if(kind==="safe") return p.safe.map(i=>p.c[i]).join("\n");
  if(kind==="py") return `${p.slug.split('-')[0]} = [${q(C)}]`;
  if(kind==="r") return `${p.slug.split('-')[0]} <- c(${q(C)})`;
  if(kind==="flow"){
    const st=[]; for(let i=0;i<11;i++) st.push(p.flw[Math.round(i*(p.flw.length-1)/10)]);
    return `# 散点/密度图连续着色：明度单调、跨色相，过渡最强\n`+
      `from matplotlib.colors import LinearSegmentedColormap\n`+
      `${p.slug.split('-')[0]}_flow = LinearSegmentedColormap.from_list(\n`+
      `    "${p.slug}_flow", [${st.map(x=>`"${x}"`).join(", ")}])\n`+
      `# ax.scatter(x, y, c=v, cmap=${p.slug.split('-')[0]}_flow, s=42, edgecolor="white", lw=.35)`;
  }
  if(kind==="mpl") return `import matplotlib as mpl\nmpl.rcParams["axes.prop_cycle"] = mpl.cycler(color=[${q(C)}])\n# bg=${p.bg}  ink=${p.ink}  muted=${p.muted}`;
}

function render(){
  const q=state.q.trim().toLowerCase();
  const rows=DATA.filter(p=>
    (!state.fam||p.fam===state.fam) && (!state.grade||p.grade===state.grade) &&
    (!q||[p.zh,p.en,p.tone,p.toneEn,p.src,p.slug,p.nameZh,p.nameEn].join(' ').toLowerCase().includes(q)));
  rows.sort((a,b)=>FAMS.indexOf(a.fam)-FAMS.indexOf(b.fam)||a.slug.localeCompare(b.slug));
  document.getElementById('grid').innerHTML = rows.length
    ? rows.map(card).join('') : '<div class="empty">没有匹配的配色</div>';
  const tip = {
    smooth:"当前「平滑」排序：相邻两色的 ΔE₀₀ 之和最小，过渡最顺滑，适合色带、装饰、整体配图协调。<b>画多系列折线/柱状/散点时请切到「区分度」</b>。",
    distinct:"当前「区分度」排序：前几个颜色彼此差异最大，<b>多系列图表用这个</b>——只画 2–3 条线时直接取前 2–3 色即可。",
    hue:"当前「色相环」排序：红→橙→黄→绿→青→蓝→紫，规律性最强、最好预测，但明度会跳。",
    light:"当前「明度」排序：L* 由浅到深，适合表达强弱/多少的有序数据，也最适合灰度打印。"
  }[state.order];
  document.getElementById('note').innerHTML =
    `当前显示 <b>${rows.length}</b> / ${DATA.length} 套。${tip}`+
    ` 色块右上角的小圆点＝该色在红/绿色盲下与同套其它色接近，多系列图建议避开或改用「安全子集」。`;
}


/* ================= 色标代码生成 ================= */
const RAMP_KEY = {seq:"seq", flow:"flw", div:"div", cyclic:"cyc"};
const RAMP_NAME = {seq:"连续 seq（单色相）", flow:"强过渡 flow（多色相）",
                   div:"发散 div", cyclic:"环形 cyclic"};
const RAMP_USE = {
  seq:"热图、密度图、等高线填充、单调强度。单色相最“素”，不抢主体。",
  flow:"散点连续着色、需要强过渡的图。多色相 + 明度严格单调，小点也分得开，灰度打印仍成立。",
  div:"相关系数、差值、以 0 为中心的量。中点近白，两侧对称发散。",
  cyclic:"相位、角度、风向、一天中的时刻。首尾闭合，明度恒定 —— 不要用它表示大小。"
};
const FORMATS = ["Python", "Python 256", "R", "MATLAB", "Origin", "CSS", "HEX"];
let MST = {p:null, r:"flow", fmt:"Python"};

function rampStops(p, r){ return p[RAMP_KEY[r]]; }

/* sRGB 线性插值取 N 级（stop 已足够密，误差可忽略） */
function sampleRamp(stops, N){
  const out=[];
  for(let i=0;i<N;i++){
    const t=i/(N-1)*(stops.length-1), k=Math.min(Math.floor(t), stops.length-2), f=t-k;
    const a=hx(stops[k]), b=hx(stops[k+1]);
    out.push(xh([0,1,2].map(j=>a[j]+(b[j]-a[j])*f)));
  }
  return out;
}

function varName(p, r){ return `${p.slug.split('-')[0]}_${r}`; }

function genCode(p, r, fmt){
  const stops = rampStops(p, r);
  const st = p.rs[r];
  const v = varName(p, r);
  const head = `${p.nameZh} / ${p.nameEn} — ${RAMP_NAME[r]}`;
  const meta = `L* ${st.r} · 明度单调 ${st.m?'是':'否'} · 感知均匀度 ${st.u}`;
  const q = a => a.map(x=>`"${x}"`);
  const wrap = (arr, per, ind) => {
    const rows=[]; for(let i=0;i<arr.length;i+=per) rows.push(ind+arr.slice(i,i+per).join(", "));
    return rows.join(",\n");
  };
  if(fmt==="Python")
    return `# ${head}\n# ${meta}\n`+
      `# ${RAMP_USE[r]}\n`+
      `from matplotlib.colors import LinearSegmentedColormap\n\n`+
      `${v} = LinearSegmentedColormap.from_list("${p.slug}_${r}", [\n`+
      wrap(q(stops), 4, "    ")+`,\n])\n\n`+
      (r==="flow"
        ? `# 散点连续着色（crop 掉最浅端，否则小点在白底上看不见）\n`+
          `# ax.scatter(x, y, c=v, cmap=${v}, s=42, edgecolor="white", linewidth=.35,\n`+
          `#            vmin=v.min(), vmax=v.max())\n`
        : r==="div"
        ? `# ax.imshow(C, cmap=${v}, vmin=-1, vmax=1)   # 记得对称设 vmin/vmax\n`
        : r==="cyclic"
        ? `# ax.scatter(x, y, c=phase, cmap=${v}, vmin=0, vmax=2*np.pi)\n`
        : `# ax.imshow(Z, cmap=${v})\n`);
  if(fmt==="Python 256")
    return `# ${head}  —  256 级查找表\n# ${meta}\n`+
      `${v}_hex = [\n`+wrap(q(sampleRamp(stops,256)), 6, "    ")+`,\n]\n\n`+
      `from matplotlib.colors import ListedColormap\n${v} = ListedColormap(${v}_hex, name="${p.slug}_${r}")\n`;
  if(fmt==="R")
    return `# ${head}\n# ${meta}\n`+
      `${v}_stops <- c(\n`+wrap(q(stops), 4, "  ")+`\n)\n`+
      `${v} <- grDevices::colorRampPalette(${v}_stops, space = "Lab")\n\n`+
      `# ggplot2:\n`+
      `# + scale_colour_gradientn(colours = ${v}(256))\n`+
      `# + scale_fill_gradientn(colours = ${v}(256))\n`;
  if(fmt==="MATLAB"){
    const rows = sampleRamp(stops,256).map(c=>{
      const [r0,g0,b0]=hx(c); return `    ${r0.toFixed(4)} ${g0.toFixed(4)} ${b0.toFixed(4)}`;});
    return `% ${head}\n% ${meta}\n`+
      `${v} = [\n${rows.join(";\n")}\n];\n\n`+
      `% colormap(${v});  scatter(x, y, 36, v, "filled"); colorbar\n`;
  }
  if(fmt==="Origin")
    return `# ${head}  —  16 级取样，逐行粘进 Origin 自定义色阶\n# ${meta}\n`+
      sampleRamp(stops,16).join("\n")+"\n";
  if(fmt==="CSS")
    return `/* ${head} */\n/* ${meta} */\n`+
      `.${p.slug}-${r} {\n  background: linear-gradient(90deg,\n`+
      sampleRamp(stops,12).map((c,i,a)=>`    ${c} ${(i*100/(a.length-1)).toFixed(1)}%`).join(",\n")+
      `\n  );\n}\n\n:root { --${p.slug}-${r}: ${sampleRamp(stops,3)[1]}; }\n`;
  return `${head}\n${meta}\n\n`+sampleRamp(stops,32).join("\n")+"\n";
}

const FILE_EXT = {"Python":"py","Python 256":"py","R":"R","MATLAB":"m",
                  "Origin":"txt","CSS":"css","HEX":"txt"};

function genWhole(p){
  const q = a => a.map(x=>`"${x}"`).join(", ");
  const cs = ord(p,"c");
  let out = `# -*- coding: utf-8 -*-\n`+
    `# ${p.nameZh} / ${p.nameEn}  [${p.src}]\n`+
    `# 色系 ${p.fam} · 色盲友好度 ${p.grade} · 排序 ${ORDER_LABEL[state.order]}\n`+
    `from matplotlib.colors import LinearSegmentedColormap, ListedColormap\n\n`+
    `# 6 主色（当前排序）\n${p.slug.split('-')[0]} = [${q(cs)}]\n`+
    `# 深 / 浅变体\n${p.slug.split('-')[0]}_dark  = [${q(ord(p,"d"))}]\n`+
    `${p.slug.split('-')[0]}_light = [${q(ord(p,"l"))}]\n`+
    `# 中性色\nbg, bg2, muted, ink = "${p.bg}", "${p.bg2}", "${p.muted}", "${p.ink}"\n`+
    `# 色盲下仍两两可分的子集\nsafe = [${q(p.safe.map(i=>p.c[i]))}]\n\n`;
  for(const r of ["seq","flow","div","cyclic"]){
    out += `# ${RAMP_NAME[r]} — ${RAMP_USE[r]}\n`+
      `${varName(p,r)} = LinearSegmentedColormap.from_list(\n    "${p.slug}_${r}", [${
        rampStops(p,r).map(x=>`"${x}"`).join(", ")}])\n\n`;
  }
  out += `# 一次性套用到 matplotlib\n`+
    `def use():\n    import matplotlib as mpl\n`+
    `    mpl.rcParams.update({\n`+
    `        "axes.prop_cycle": mpl.cycler(color=${p.slug.split('-')[0]}),\n`+
    `        "axes.edgecolor": ink, "axes.labelcolor": ink, "text.color": ink,\n`+
    `        "xtick.color": ink, "ytick.color": ink, "grid.color": bg2,\n`+
    `        "axes.grid": True, "axes.axisbelow": True,\n`+
    `        "axes.spines.top": False, "axes.spines.right": False,\n`+
    `        "legend.frameon": False, "savefig.dpi": 300,\n    })\n`;
  return out;
}

function download(text, filename){
  const blob = new Blob([text], {type:"text/plain;charset=utf-8"});
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url; a.download = filename; document.body.appendChild(a); a.click();
  document.body.removeChild(a); setTimeout(()=>URL.revokeObjectURL(url), 1500);
  toast("已下载 "+filename);
}

function renderModal(){
  const {p, r, fmt} = MST;
  document.getElementById("mtitle").textContent = `${p.nameZh} · ${RAMP_NAME[r]}`;
  document.getElementById("mdesc").textContent = RAMP_USE[r];
  document.getElementById("mbar").style.background = grad(rampStops(p, r));
  const st = p.rs[r];
  document.getElementById("mstat").textContent =
    `L* 跨度 ${st.r} · 明度单调 ${st.m?"是":"否"} · 均匀度 ${st.u}`;
  document.getElementById("mtabs").innerHTML =
    FORMATS.map(f=>`<button data-f="${f}"${f===fmt?' class="on"':''}>${f}</button>`).join("");
  document.getElementById("code").textContent = genCode(p, r, fmt);
}

function openModal(p, r){
  MST.p = p; MST.r = r;
  renderModal();
  document.getElementById("mask").classList.add("on");
}
function closeModal(){ document.getElementById("mask").classList.remove("on"); }

document.getElementById("mtabs").addEventListener("click", e=>{
  const b=e.target.closest("button"); if(!b) return;
  MST.fmt=b.dataset.f; renderModal();
});
document.getElementById("mcopy").addEventListener("click", ()=>
  copy(document.getElementById("code").textContent, "已复制代码"));
document.getElementById("mdl").addEventListener("click", ()=>
  download(document.getElementById("code").textContent,
           `${MST.p.slug}_${MST.r}.${FILE_EXT[MST.fmt]}`));
document.getElementById("mdlall").addEventListener("click", ()=>
  download(genWhole(MST.p), `${MST.p.slug}.py`));
document.getElementById("mclose").addEventListener("click", closeModal);
document.getElementById("mask").addEventListener("click", e=>{
  if(e.target.id==="mask") closeModal();
});
document.addEventListener("keydown", e=>{
  if(e.key==="Escape") closeModal();
});

/* ---------- 事件 ---------- */
const famBox=document.getElementById('fam');
famBox.innerHTML='<button data-f="" class="on">全部</button>'+FAMS.map(f=>`<button data-f="${f}">${f}</button>`).join('');
function segHandler(box,key,fn){
  box.addEventListener('click',e=>{
    const b=e.target.closest('button'); if(!b)return;
    [...box.children].forEach(x=>x.classList.remove('on')); b.classList.add('on');
    state[key]=b.dataset[fn]; render();
  });
}
segHandler(famBox,'fam','f');
segHandler(document.getElementById('grade'),'grade','g');
segHandler(document.getElementById('cvd'),'cvd','v');
segHandler(document.getElementById('view'),'view','w');
segHandler(document.getElementById('order'),'order','o');
document.getElementById('q').addEventListener('input',e=>{state.q=e.target.value;render();});
document.getElementById('grid').addEventListener('click',e=>{
  const rp=e.target.closest('.ramp, .rlab span');
  if(rp && rp.dataset.r){
    const p=DATA.find(x=>x.slug===rp.closest('.card').dataset.slug);
    openModal(p, rp.dataset.r); return;
  }
  const cell=e.target.closest('.cell');
  if(cell){copy(cell.dataset.hex, '已复制 '+cell.dataset.hex); return;}
  const btn=e.target.closest('.copy button');
  if(btn){
    const p=DATA.find(x=>x.slug===btn.closest('.card').dataset.slug);
    const txt=payload(p,btn.dataset.a);
    copy(txt, '已复制 '+p.zh+' · '+btn.textContent);
  }
});
document.getElementById('mkbtn').addEventListener('click',e=>{
  state.mark=!state.mark;
  e.target.classList.toggle('on',state.mark);
  render();
});
document.getElementById('tbtn').addEventListener('click',()=>{
  const h=document.documentElement;
  const dark=h.getAttribute('data-theme')==='dark';
  h.setAttribute('data-theme',dark?'light':'dark');
  document.getElementById('tbtn').textContent=dark?'深色界面':'浅色界面';
});
render();
</script>
</body>
</html>
"""

out = HTML.replace('__DATA__', json.dumps(DATA, ensure_ascii=False, separators=(',', ':')))
out = out.replace('__MARKS__', json.dumps(MARKS, ensure_ascii=False, separators=(',', ':')))
open('build/anime-palettes.html', 'w', encoding='utf-8').write(out)
print('wrote build/anime-palettes.html  %.0f KB' % (len(out.encode()) / 1024))
