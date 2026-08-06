"""Minimal, dependency-light colour-science helpers (sRGB / CIELAB / dE2000 / CVD)."""
import itertools
import math

# ---------- basic conversions ----------

def hex2rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i + 2], 16) / 255.0 for i in (0, 2, 4))


def rgb2hex(rgb):
    return '#' + ''.join('%02X' % max(0, min(255, round(c * 255))) for c in rgb)


def _srgb2lin(c):
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def _lin2srgb(c):
    c = max(0.0, min(1.0, c))
    return 12.92 * c if c <= 0.0031308 else 1.055 * c ** (1 / 2.4) - 0.055


M_RGB2XYZ = ((0.4124564, 0.3575761, 0.1804375),
             (0.2126729, 0.7151522, 0.0721750),
             (0.0193339, 0.1191920, 0.9503041))
M_XYZ2RGB = ((3.2404542, -1.5371385, -0.4985314),
             (-0.9692660, 1.8760108, 0.0415560),
             (0.0556434, -0.2040259, 1.0572252))
WP = (0.95047, 1.00000, 1.08883)


def _mv(M, v):
    return tuple(sum(M[i][j] * v[j] for j in range(3)) for i in range(3))


def rgb2lab(rgb):
    lin = tuple(_srgb2lin(c) for c in rgb)
    X, Y, Z = _mv(M_RGB2XYZ, lin)
    def f(t):
        return t ** (1 / 3) if t > 216 / 24389 else (841 / 108) * t + 4 / 29
    fx, fy, fz = f(X / WP[0]), f(Y / WP[1]), f(Z / WP[2])
    return (116 * fy - 16, 500 * (fx - fy), 200 * (fy - fz))


def lab2rgb_raw(lab):
    L, a, b = lab
    fy = (L + 16) / 116
    fx, fz = fy + a / 500, fy - b / 200
    def fi(t):
        return t ** 3 if t ** 3 > 216 / 24389 else (t - 4 / 29) * 108 / 841
    X, Y, Z = fi(fx) * WP[0], fi(fy) * WP[1], fi(fz) * WP[2]
    lin = _mv(M_XYZ2RGB, (X, Y, Z))
    return tuple(_lin2srgb(c) for c in lin), all(-0.002 <= c <= 1.002 for c in lin)


def lab2rgb(lab):
    """Gamut-map by chroma reduction (keeps L* and hue)."""
    L, a, b = lab
    L = max(0.0, min(100.0, L))
    rgb, ok = lab2rgb_raw((L, a, b))
    if ok:
        return rgb
    lo, hi = 0.0, 1.0
    for _ in range(24):
        mid = (lo + hi) / 2
        rgb, ok = lab2rgb_raw((L, a * mid, b * mid))
        if ok:
            lo = mid
        else:
            hi = mid
    return lab2rgb_raw((L, a * lo, b * lo))[0]


def hex2lab(h):
    return rgb2lab(hex2rgb(h))


def lab2hex(lab):
    return rgb2hex(lab2rgb(lab))


def lch(h):
    L, a, b = hex2lab(h)
    return L, math.hypot(a, b), math.degrees(math.atan2(b, a)) % 360


# ---------- deltaE 2000 ----------

def delta_e00(lab1, lab2):
    L1, a1, b1 = lab1
    L2, a2, b2 = lab2
    C1, C2 = math.hypot(a1, b1), math.hypot(a2, b2)
    Cb = (C1 + C2) / 2
    G = 0.5 * (1 - math.sqrt(Cb ** 7 / (Cb ** 7 + 25 ** 7))) if Cb > 0 else 0.5
    a1p, a2p = (1 + G) * a1, (1 + G) * a2
    C1p, C2p = math.hypot(a1p, b1), math.hypot(a2p, b2)
    h1p = math.degrees(math.atan2(b1, a1p)) % 360 if (a1p or b1) else 0
    h2p = math.degrees(math.atan2(b2, a2p)) % 360 if (a2p or b2) else 0
    dLp = L2 - L1
    dCp = C2p - C1p
    if C1p * C2p == 0:
        dhp = 0.0
    elif abs(h2p - h1p) <= 180:
        dhp = h2p - h1p
    else:
        dhp = h2p - h1p - 360 * (1 if h2p > h1p else -1)
    dHp = 2 * math.sqrt(C1p * C2p) * math.sin(math.radians(dhp) / 2)
    Lbp = (L1 + L2) / 2
    Cbp = (C1p + C2p) / 2
    if C1p * C2p == 0:
        hbp = h1p + h2p
    elif abs(h1p - h2p) <= 180:
        hbp = (h1p + h2p) / 2
    else:
        hbp = (h1p + h2p + 360) / 2 if (h1p + h2p) < 360 else (h1p + h2p - 360) / 2
    T = (1 - 0.17 * math.cos(math.radians(hbp - 30)) + 0.24 * math.cos(math.radians(2 * hbp))
         + 0.32 * math.cos(math.radians(3 * hbp + 6)) - 0.20 * math.cos(math.radians(4 * hbp - 63)))
    dTh = 30 * math.exp(-(((hbp - 275) / 25) ** 2))
    Rc = 2 * math.sqrt(Cbp ** 7 / (Cbp ** 7 + 25 ** 7)) if Cbp > 0 else 0
    Sl = 1 + 0.015 * (Lbp - 50) ** 2 / math.sqrt(20 + (Lbp - 50) ** 2)
    Sc = 1 + 0.045 * Cbp
    Sh = 1 + 0.015 * Cbp * T
    Rt = -math.sin(math.radians(2 * dTh)) * Rc
    return math.sqrt((dLp / Sl) ** 2 + (dCp / Sc) ** 2 + (dHp / Sh) ** 2
                     + Rt * (dCp / Sc) * (dHp / Sh))


def de_hex(h1, h2):
    return delta_e00(hex2lab(h1), hex2lab(h2))


# ---------- contrast ----------

def luminance(h):
    r, g, b = hex2rgb(h)
    r, g, b = _srgb2lin(r), _srgb2lin(g), _srgb2lin(b)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(h1, h2):
    a, b = luminance(h1), luminance(h2)
    hi, lo = max(a, b), min(a, b)
    return (hi + 0.05) / (lo + 0.05)


# ---------- colour-vision deficiency (Machado et al. 2009, severity 1.0) ----------

CVD = {
    'protan': ((0.152286, 1.052583, -0.204868),
               (0.114503, 0.786281, 0.099216),
               (-0.003882, -0.048116, 1.051998)),
    'deutan': ((0.367322, 0.860646, -0.227968),
               (0.280085, 0.672501, 0.047413),
               (-0.011820, 0.042940, 0.968881)),
    'tritan': ((1.255528, -0.076749, -0.178779),
               (-0.078411, 0.930809, 0.147602),
               (0.004733, 0.691367, 0.303900)),
}


def simulate_cvd(h, kind):
    lin = tuple(_srgb2lin(c) for c in hex2rgb(h))
    out = _mv(CVD[kind], lin)
    return rgb2hex(tuple(_lin2srgb(c) for c in out))


# ---------- derivations ----------

def shift(h, dL, chroma=1.0):
    L, a, b = hex2lab(h)
    return lab2hex((L + dL, a * chroma, b * chroma))


def set_lightness(h, L, chroma=1.0):
    _, a, b = hex2lab(h)
    return lab2hex((L, a * chroma, b * chroma))


def _lerp(a, b, t):
    return a + (b - a) * t


def ramp(stops, n):
    """Piecewise-linear interpolation through Lab stops -> n hex colours."""
    labs = [hex2lab(s) for s in stops]
    out = []
    seg = len(labs) - 1
    for i in range(n):
        t = i / (n - 1) * seg
        k = min(int(t), seg - 1)
        f = t - k
        lab = tuple(_lerp(labs[k][j], labs[k + 1][j], f) for j in range(3))
        out.append(lab2hex(lab))
    return out


def sequential(base, n=256, light_L=97.0, dark_L=22.0):
    """Perceptually monotonic light->dark ramp anchored on `base`'s hue."""
    L, a, b = hex2lab(base)
    C = math.hypot(a, b)
    hue = math.atan2(b, a)
    stops = []
    # anchor lightness of the base within the ramp
    L = max(38.0, min(62.0, L))
    for LL, cf in ((light_L, 0.10), ((light_L + L) / 2, 0.55), (L, 1.00),
                   ((L + dark_L) / 2, 0.92), (dark_L, 0.62)):
        cc = C * cf
        stops.append(lab2hex((LL, cc * math.cos(hue), cc * math.sin(hue))))
    return ramp(stops, n)


def _unwrap(hues):
    """把一串 0–360 的色相角展开成连续序列（去掉跨 0° 的跳变）。"""
    out = [hues[0]]
    for h in hues[1:]:
        prev = out[-1]
        d = (h - prev + 180) % 360 - 180
        out.append(prev + d)
    return out


def _smooth_hue(hues, strength=0.6):
    """把色相序列往「单调旋转」的方向拉，压掉来回摆动，保留角色色相。"""
    u = _unwrap(hues)
    n = len(u)
    if n < 3:
        return u
    lo, hi = u[0], u[-1]
    target = [lo + (hi - lo) * i / (n - 1) for i in range(n)]
    return [a * (1 - strength) + b * strength for a, b in zip(u, target)]


def uniformize(ramp_hexes, n=None):
    """按 ΔE2000 弧长重采样，使相邻步长的色差尽量一致（感知均匀化）。"""
    n = n or len(ramp_hexes)
    labs = [hex2lab(c) for c in ramp_hexes]
    acc = [0.0]
    for i in range(1, len(labs)):
        acc.append(acc[-1] + max(delta_e00(labs[i - 1], labs[i]), 1e-6))
    total = acc[-1]
    out = []
    j = 0
    for i in range(n):
        t = total * i / (n - 1)
        while j < len(acc) - 2 and acc[j + 1] < t:
            j += 1
        span = acc[j + 1] - acc[j]
        f = 0.0 if span <= 0 else (t - acc[j]) / span
        lab = tuple(_lerp(labs[j][k], labs[j + 1][k], f) for k in range(3))
        out.append(lab2hex(lab))
    return out


def ramp_lch(stops, n):
    """在 LCh 里插值（色相走角度、彩度走径向），跨色相时中段不会掉成灰。
    stops = [(L, C, h_unwrapped), ...]"""
    out = []
    seg = len(stops) - 1
    for i in range(n):
        t = i / (n - 1) * seg
        k = min(int(t), seg - 1)
        f = t - k
        L = _lerp(stops[k][0], stops[k + 1][0], f)
        C = _lerp(stops[k][1], stops[k + 1][1], f)
        h = _lerp(stops[k][2], stops[k + 1][2], f)
        r = math.radians(h)
        out.append(lab2hex((L, C * math.cos(r), C * math.sin(r))))
    return out


def flow(colors, n=256, L_hi=93.0, L_lo=23.0, chroma=1.05, min_C=16.0):
    """多色相连续色标（viridis 式）：用整套配色自己的色相搭一条
    **明度严格单调** 的通路 —— 强过渡场景（散点连续着色、密度图）用这个。
    在 LCh 里插值并设彩度下限，保证中段不掉成灰。"""
    info = sorted((lch(c) for c in colors), key=lambda t: -t[0])   # 浅 → 深
    hues = _smooth_hue([t[2] for t in info], 0.55)
    k = len(info)
    stops = []
    for i in range(k):
        u = i / (k - 1)
        L = L_hi + (L_lo - L_hi) * u
        # 两端天然容不下高彩度，中段撑住
        cap = 0.42 + 0.58 * math.sin(math.pi * min(1.0, max(0.0, u * 0.94 + 0.06)))
        C = max(min_C * cap, info[i][1] * chroma * cap)
        stops.append((L, C, hues[i]))
    return uniformize(ramp_lch(stops, 128), n)


def cyclic(colors, n=256, L=62.0, min_C=24.0):
    """环形色标：按色相排成闭环、明度基本恒定 ——
    相位、角度、风向、一天中的时刻这类首尾相接的量用它。"""
    info = sorted((lch(c) for c in colors if lch(c)[1] >= 8), key=lambda t: t[2])
    if len(info) < 3:
        base = sorted((lch(c) for c in colors), key=lambda t: -t[1])[0]
        info = [(base[0], max(base[1], min_C), (base[2] + 120 * i) % 360) for i in range(3)]
    Cm = max(min_C, sum(t[1] for t in info) / len(info))
    # 已按色相升序，直接顺时针走一圈；不能用 _unwrap（它取最短有向差，
    # 遇到 >180° 的间隔会把方向反过来，路径就会先倒着走再折回来）
    hs = [t[2] for t in info]
    hs = hs + [hs[0] + 360]
    return uniformize(ramp_lch([(L, Cm, h) for h in hs], 180), n)


def ramp_stats(hexes):
    """色标体检：明度跨度 / 是否单调 / 相邻色差的均匀度 / 灰度可分性。"""
    Ls = [lch(c)[0] for c in hexes]
    labs = [hex2lab(c) for c in hexes]
    ds = [delta_e00(labs[i], labs[i + 1]) for i in range(len(labs) - 1)]
    mean = sum(ds) / len(ds)
    var = sum((d - mean) ** 2 for d in ds) / len(ds)
    drops = sum(1 for i in range(len(Ls) - 1) if Ls[i + 1] - Ls[i] > 0.35)
    return dict(
        L_range=round(max(Ls) - min(Ls), 1),
        L_min=round(min(Ls), 1), L_max=round(max(Ls), 1),
        monotonic=(drops == 0),
        total_dE=round(sum(ds), 1),
        uniformity=round(1 - (var ** 0.5) / mean, 3) if mean else 0.0,
    )


def diverging(low, high, n=256, mid_L=96.0):
    la, aa, ba = hex2lab(low)
    lb, ab, bb = hex2lab(high)
    ca, cb = math.hypot(aa, ba), math.hypot(ab, bb)
    ha, hb = math.atan2(ba, aa), math.atan2(bb, ab)
    def arm(hue, C, dark_L, mid_first):
        pts = []
        for LL, cf in ((28.0, 0.60), (45.0, 0.95), (62.0, 0.85), (80.0, 0.50), (mid_L, 0.06)):
            pts.append(lab2hex((LL, C * cf * math.cos(hue), C * cf * math.sin(hue))))
        return pts if mid_first is False else pts
    left = arm(ha, ca, 28.0, False)
    right = list(reversed(arm(hb, cb, 28.0, False)))
    return ramp(left + right[1:], n)


def pick_diverging_pair(cs):
    """自动选发散色标两端：彩度足够 & 色相相距最远的一对；
    整套配色色相跨度过小（单色系）时，从彩度最高的那色旋转 165° 派生对端。
    冷色（130°-310°）放低值端、暖色放高值端，是发散色标的通用惯例。

    返回 (a, b, mode)：mode='auto' 时 a、b 都是 cs 的下标；
    mode='derived' 时 a 是下标、b 是派生出的新 hex（不在 cs 里）。
    这个不对称的返回形状是刻意保留的 —— 调用方（derive.build_one）
    本来就要把「选中原配色里的第几个」和「凭空派生了一个新颜色」区分开。

    这段是 derive.py:pick_diverging() 的色彩学核心（不含 slug -> 人工
    override 那层业务规则），搬到这儿是为了让 propose.py 的预览页跟正式
    产物用同一份选端算法，不能各写一份、迟早走岔。原先 propose.py 里
    简化成「彩度 >= 16 的原始顺序首尾」，选出来的两端经常同冷暖、
    根本不发散，这就是要共用这份实现的原因。"""
    info = [lch(c) for c in cs]           # (L, C, h)
    def cool(h):
        return 130 <= h <= 310
    best = None
    for i, j in itertools.combinations(range(len(cs)), 2):
        Ci, Cj = info[i][1], info[j][1]
        if Ci < 16 or Cj < 16:
            continue
        dh = abs((info[i][2] - info[j][2] + 180) % 360 - 180)
        w = dh + 0.30 * min(Ci, Cj) + (25 if cool(info[i][2]) != cool(info[j][2]) else 0)
        if best is None or w > best[0]:
            best = (w, dh, i, j)
    if best and best[1] >= 80:
        _, _, i, j = best
        # 惯例：冷色在低值端，暖色在高值端
        if cool(info[j][2]) and not cool(info[i][2]):
            i, j = j, i
        return i, j, 'auto'
    # 单色系：派生对端
    k = max(range(len(cs)), key=lambda t: info[t][1])
    L, C, h = info[k]
    other = lab2hex((max(38.0, min(62.0, L)),
                     max(C, 18) * math.cos(math.radians(h + 165)),
                     max(C, 18) * math.sin(math.radians(h + 165))))
    return k, other, 'derived'


# ---------- 色盲友好度 ----------
# 这三个函数原先住在 derive.py，但 derive 的模块级有 tuned/data 指纹校验，
# 仓库处于「改了 data.py 还没 tune」时 import 就 SystemExit。它们是纯色彩科学、
# 只用本文件的原语，放这儿 propose.py 才能在那种状态下照常用。

def cvd_min(hexes, kinds=('protan', 'deutan', 'tritan')):
    out = {}
    for k in kinds:
        labs = [hex2lab(simulate_cvd(c, k)) for c in hexes]
        out[k] = min(delta_e00(labs[i], labs[j])
                     for i, j in itertools.combinations(range(len(hexes)), 2))
    return out


def safe_set(hexes, thr=12.0):
    """按顺序贪心挑出在红/绿色盲下仍两两可分的最大子集（返回索引）。"""
    keep = [0]
    for i in range(1, len(hexes)):
        sub = [hexes[k] for k in keep] + [hexes[i]]
        if min(cvd_min(sub, ('protan', 'deutan')).values()) >= thr:
            keep.append(i)
    return keep


def grade(hexes):
    m = min(cvd_min(hexes, ('protan', 'deutan')).values())
    if m >= 13:
        return 'A'
    if m >= 9:
        return 'B'
    return 'C'
