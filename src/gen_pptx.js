// 生成 PPT 取色板：1 张封面 + 58 张配色页（含原生图表示例，可直接取色器吸色）
const fs = require('fs');
const PptxGenJS = require('pptxgenjs');

const lib = JSON.parse(fs.readFileSync('library.json', 'utf8'));
const hx = c => c.replace('#', '').toUpperCase();
const CN = 'Microsoft YaHei';
const EN = 'Arial';

function lum(h) {
  const v = [0, 2, 4].map(i => parseInt(h.slice(1).substr(i, 2), 16) / 255)
    .map(c => c <= 0.04045 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4));
  return 0.2126 * v[0] + 0.7152 * v[1] + 0.0722 * v[2];
}
const onColor = h => lum(h) > 0.42 ? '111111' : 'FFFFFF';

const pres = new PptxGenJS();
pres.layout = 'LAYOUT_WIDE';           // 13.333 x 7.5 in
pres.author = 'anime-palettes';
pres.title = '动漫 / 游戏角色配色库';

const W = 13.333, M = 0.55;

// ---------------- 封面 ----------------
let s = pres.addSlide();
s.background = { color: 'F7F7F5' };
s.addText('动漫 / 游戏角色配色库', {
  x: M, y: 1.5, w: W - 2 * M, h: 0.85, fontSize: 40, bold: true,
  color: '1D1D21', fontFace: CN,
});
s.addText('58 套 · 每套 6 主色 + 深/浅变体 · 面向 PPT 与科研配图', {
  x: M, y: 2.35, w: W - 2 * M, h: 0.5, fontSize: 17, color: '6C6C76', fontFace: CN,
});
s.addText([
  { text: '用法：', options: { bold: true } },
  { text: '① 直接用取色器（吸管）从色块取色　② 或把 ppt-theme-colors/*.xml 放进 ' },
  { text: 'Document Themes\\Theme Colors', options: { fontFace: 'Consolas' } },
  { text: ' 后，从「设计 → 变体 → 颜色」里整套切换。\n' },
  { text: '色盲等级 A：6 色在红/绿色盲下全部可分；B：大部分可分；C：角色本身同色系，多系列时请只用标了 ✓ 的颜色。\n' },
  { text: '色块默认按「平滑」排列（相邻色差最小，过渡最顺滑）；每页右侧另给出「区分度优先」顺序，画多系列图表时用它。' },
], { x: M, y: 3.1, w: W - 2 * M, h: 1.7, fontSize: 12.5, color: '4A4A52', fontFace: CN, lineSpacing: 22 });

// 封面色带
let bx = M;
const bw = (W - 2 * M) / lib.length;
lib.forEach(e => {
  e.colors.slice(0, 6).forEach((c, i) => {
    s.addShape(pres.ShapeType.rect, {
      x: bx, y: 4.85 + i * 0.28, w: bw - 0.02, h: 0.27, fill: { color: hx(c) }, line: { width: 0 },
    });
  });
  bx += bw;
});
s.addText('每一竖列 = 一套配色', { x: M, y: 6.6, w: 6, h: 0.3, fontSize: 11, color: '9A9AA4', fontFace: CN });

// ---------------- 每套一页 ----------------
const CATS = ['A', 'B', 'C', 'D', 'E', 'F'];
lib.forEach(e => {
  const sl = pres.addSlide();
  sl.background = { color: 'FFFFFF' };

  sl.addText([
    { text: e.zh, options: { bold: true, color: '1D1D21' } },
    { text: '  ·  ' + e.tone_zh, options: { color: '6C6C76' } },
  ], { x: M, y: 0.3, w: 8, h: 0.5, fontSize: 26, fontFace: CN });
  sl.addText(`${e.name_en}   |   ${e.source}   |   色系 ${e.family}`, {
    x: M, y: 0.85, w: 9, h: 0.35, fontSize: 12, color: '6C6C76', fontFace: CN,
  });
  const gcol = { A: '1F7A4D', B: 'B07A12', C: '9C4040' }[e.cvd_grade];
  sl.addShape(pres.ShapeType.roundRect, {
    x: W - M - 1.7, y: 0.35, w: 1.7, h: 0.42, rectRadius: 0.2,
    fill: { color: gcol }, line: { width: 0 },
  });
  sl.addText('色盲友好度 ' + e.cvd_grade, {
    x: W - M - 1.7, y: 0.35, w: 1.7, h: 0.42, fontSize: 11.5, color: 'FFFFFF',
    align: 'center', valign: 'middle', fontFace: CN, margin: 0,
  });

  // 浅 / 主 / 深 三行（默认「平滑」排序）
  const sw = (W - 2 * M) / 6;
  const dist = e.orders.distinct;
  e.light.forEach((c, i) => sl.addShape(pres.ShapeType.rect, {
    x: M + i * sw, y: 1.32, w: sw - 0.04, h: 0.3, fill: { color: hx(c) }, line: { width: 0 },
  }));
  e.colors.forEach((c, i) => {
    sl.addShape(pres.ShapeType.rect, {
      x: M + i * sw, y: 1.64, w: sw - 0.04, h: 1.25, fill: { color: hx(c) }, line: { width: 0 },
    });
    const safe = e.safe_set.includes(i);
    sl.addText([
      { text: c.toUpperCase() + '\n', options: { bold: true, fontSize: 13 } },
      { text: `${CATS[i]}${safe ? '  ✓' : ''}`, options: { fontSize: 10 } },
    ], {
      x: M + i * sw, y: 1.64, w: sw - 0.04, h: 1.25, color: onColor(c),
      align: 'center', valign: 'middle', fontFace: 'Consolas', margin: 0,
    });
  });
  e.dark.forEach((c, i) => sl.addShape(pres.ShapeType.rect, {
    x: M + i * sw, y: 2.91, w: sw - 0.04, h: 0.3, fill: { color: hx(c) }, line: { width: 0 },
  }));
  sl.addText('浅色 light  /  主色 main  /  深色 dark　（排序：平滑，相邻色差最小）', {
    x: M, y: 3.24, w: 7.2, h: 0.26, fontSize: 9.5, color: '9A9AA4', fontFace: CN,
  });
  // 右侧：区分度优先顺序的小色条（下方图表用的就是这个顺序）
  const qx = W - M - 2.55;
  sl.addText('图表用顺序（区分度优先）', {
    x: qx - 1.95, y: 3.22, w: 1.9, h: 0.26, fontSize: 9.5, color: '9A9AA4',
    fontFace: CN, align: 'right', margin: 0,
  });
  dist.forEach((idx, k) => sl.addShape(pres.ShapeType.rect, {
    x: qx + k * 0.42, y: 3.22, w: 0.40, h: 0.26,
    fill: { color: hx(e.colors[idx]) }, line: { width: 0 },
  }));

  // 四条连续色标
  const RAMPS = [['seq','连续 seq'],['flow','强过渡 flow'],['div','发散 div'],['cyclic','环形 cyclic']];
  const rw = (W - 2 * M - 3 * 0.22) / 4;
  RAMPS.forEach(([key, label], ri) => {
    const rx = M + ri * (rw + 0.22);
    const arr = e[key];
    const N = 64;
    for (let t = 0; t < N; t++) {
      sl.addShape(pres.ShapeType.rect, {
        x: rx + t * (rw / N), y: 3.62, w: rw / N + 0.004, h: 0.24,
        fill: { color: hx(arr[Math.round(t * 255 / (N - 1))]) }, line: { width: 0 },
      });
    }
    sl.addText(label, { x: rx, y: 3.86, w: rw, h: 0.22, fontSize: 9,
      color: '9A9AA4', fontFace: CN, margin: 0 });
  });

  // 原生图表示例
  const cc = e.orders.distinct.map(i => hx(e.colors[i]));
  const cats = ['组1', '组2', '组3', '组4', '组5'];
  const bars = [0, 1, 2, 3].map(k => ({
    name: `系列${k + 1}`,
    labels: cats,
    values: [[5.2, 6.8, 4.1, 7.5, 5.9], [3.4, 4.9, 6.2, 3.1, 4.4],
             [6.1, 3.2, 5.5, 4.8, 6.6], [2.6, 5.4, 3.3, 5.9, 3.7]][k],
  }));
  sl.addChart(pres.ChartType.bar, bars, {
    x: M, y: 4.12, w: 6.0, h: 2.9, barDir: 'col', barGrouping: 'clustered',
    chartColors: cc, showLegend: true, legendPos: 'b', legendFontSize: 9,
    showTitle: true, title: '分组柱状图', titleFontSize: 12, titleColor: '4A4A52',
    catAxisLabelColor: '6C6C76', valAxisLabelColor: '6C6C76',
    catAxisLabelFontSize: 9, valAxisLabelFontSize: 9,
    valGridLine: { color: 'EAEAE6', size: 1 }, catGridLine: { style: 'none' },
    border: { pt: 0, color: 'FFFFFF' },
  });

  const xs = Array.from({ length: 24 }, (_, i) => `${i}`);
  const lines = [0, 1, 2, 3, 4, 5].map(k => ({
    name: `S${k + 1}`,
    labels: xs,
    values: xs.map((_, i) => +(Math.sin(i / 3.6 + k * 0.75) * 1.6 + k * 0.9 + 5).toFixed(2)),
  }));
  sl.addChart(pres.ChartType.line, lines, {
    x: M + 6.35, y: 4.12, w: 6.0, h: 2.9,
    chartColors: cc, lineSize: 2.5, lineSmooth: true, showLegend: true, legendPos: 'b',
    legendFontSize: 9, showTitle: true, title: '多系列折线图', titleFontSize: 12,
    titleColor: '4A4A52', catAxisLabelColor: '6C6C76', valAxisLabelColor: '6C6C76',
    catAxisLabelFontSize: 8, valAxisLabelFontSize: 9,
    valGridLine: { color: 'EAEAE6', size: 1 }, catGridLine: { style: 'none' },
    border: { pt: 0, color: 'FFFFFF' },
  });

  sl.addNotes(`${e.name_zh} / ${e.name_en}\n出处：${e.source}\n`
    + `主色（平滑序）：${e.colors.join('  ')}\n`
    + `区分度优先序：${e.orders.distinct.map(i => e.colors[i]).join('  ')}\n`
    + `纸色 ${e.bg}  次级底 ${e.bg2}  辅助灰 ${e.muted}  墨色 ${e.ink}\n`
    + `最小 ΔE00 ${e.min_de}；红色盲 ΔE ${e.cvd.protan}，绿色盲 ΔE ${e.cvd.deutan}\n`
    + `flow 色标：明度跨度 ${e.ramp_stats.flow.L_range}，单调 ${e.ramp_stats.flow.monotonic ? '是' : '否'}，均匀度 ${e.ramp_stats.flow.uniformity}\n`
    + `色盲安全子集（✓）：${e.safe_set.map(i => e.colors[i]).join('  ')}`);
});

pres.writeFile({ fileName: 'build/anime-palettes-picker.pptx' })
  .then(f => console.log('wrote', f));
