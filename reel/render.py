"""A small flat-shaded SVG renderer for manifolds: orthographic, painter's order, with
labels and dimension lines drawn in world coordinates. Good enough to review a shape."""

import math
from pathlib import Path

import cairosvg
import numpy as np
from manifold3d import Manifold

COL = {
    "chassis": "#d58ee6", "wheel": "#3f72dd", "axle_tube": "#6aa84f", "lock_pin": "#f0a030", "hinge_pin": "#e07b20",
    "cross_pin": "#f0a030", "hanger_shaft": "#b06ad0", "crank": "#e0c040", "board": "#c9a36b",
    "line": "#222222", "load": "#777777",
}
SEE_THROUGH = ("board",)
UNCUT = ("board", "line", "load")


def mesh_of(m: Manifold):
    mm = m.to_mesh()
    return np.asarray(mm.vert_properties)[:, :3].astype(float), np.asarray(mm.tri_verts).astype(int)


def shade(hexcol, k):
    h = hexcol.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    return "#%02x%02x%02x" % tuple(max(0, min(255, int(c * k))) for c in (r, g, b))


def mix(hexcol, t):
    """Blend toward white: the colour of a cut face."""
    h = hexcol.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    return "#%02x%02x%02x" % tuple(int(c + (255 - c) * t) for c in (r, g, b))


def camera(az, el):
    """Rotation taking world to view (x right, y up, z toward viewer). az about world z, el up."""
    a, e = math.radians(az), math.radians(el)
    # view direction pointing from camera to scene
    fwd = np.array([-math.cos(e) * math.cos(a), -math.cos(e) * math.sin(a), -math.sin(e)])
    up0 = np.array([0, 0, 1.0])
    if abs(fwd @ up0) > 0.99:
        up0 = np.array([0, 1.0, 0]) if fwd[2] < 0 else np.array([0, -1.0, 0])
    right = np.cross(fwd, up0)
    right /= np.linalg.norm(right)
    up = np.cross(right, fwd)
    return np.stack([right, up, -fwd])


def render(parts, az, el, title, size=(900, 700), cut=None, annotate=None, light=(0.4, -0.5, 0.8)):
    """parts: list of (name, Manifold). cut: plane normal/offset; faces on the plane are hatched darker."""
    R = camera(az, el)
    L = np.array(light, dtype=float)
    L /= np.linalg.norm(L)
    Lv = R @ L
    polys = []
    all_pts = []
    for name, m in parts:
        cutplane = None
        if cut is not None and name not in UNCUT:
            n, off = cut
            m = m.trim_by_plane(n, off)
            cutplane = (np.array(n, float), off)
        if m.is_empty():
            continue
        V, F = mesh_of(m)
        P = V @ R.T
        all_pts.append(P[:, :2])
        tri = P[F]
        nrm = np.cross(tri[:, 1] - tri[:, 0], tri[:, 2] - tri[:, 0])
        ln = np.linalg.norm(nrm, axis=1)
        ok = ln > 1e-9
        nrm[ok] /= ln[ok][:, None]
        vis = (nrm[:, 2] > 1e-6) & ok
        oncut = np.zeros(len(F), bool)
        if cutplane is not None:
            d = V[F] @ cutplane[0] - cutplane[1]
            oncut = np.all(np.abs(d) < 1e-3, axis=1)
        for i in np.nonzero(vis)[0]:
            lam = max(0.0, float(nrm[i] @ Lv))
            k = 0.55 + 0.6 * lam
            col = shade(COL[name], k)
            if oncut[i]:
                col = mix(COL[name], 0.45)
            polys.append((tri[i, :, 2].max() * 0.3 + tri[i, :, 2].mean() * 0.7 + (1e3 if oncut[i] else 0), tri[i, :, :2], col, name))
    polys.sort(key=lambda p: p[0])
    pts = np.concatenate(all_pts)
    lo, hi = pts.min(0), pts.max(0)
    W, H = size
    pad = 40
    top_pad = 50
    s = min((W - 2 * pad) / (hi[0] - lo[0]), (H - pad - top_pad) / (hi[1] - lo[1]))
    cx = (lo[0] + hi[0]) / 2
    cy = (lo[1] + hi[1]) / 2

    def xy(p):
        return (W / 2 + (p[0] - cx) * s, top_pad + (H - pad - top_pad) / 2 - (p[1] - cy) * s)

    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
           f'<rect width="{W}" height="{H}" fill="#fbfaf7"/>',
           f'<text x="20" y="32" font-family="Helvetica, Arial, sans-serif" font-size="20" font-weight="bold" fill="#222">{title}</text>']
    for _, t, col, name in polys:
        d = " ".join("%.1f,%.1f" % xy(p) for p in t)
        if name in SEE_THROUGH:
            out.append(f'<polygon points="{d}" fill="{col}" fill-opacity="0.4"/>')
        else:
            out.append(f'<polygon points="{d}" fill="{col}" stroke="{col}" stroke-width="0.6" stroke-linejoin="round"/>')
    if annotate:
        for kind, *args in annotate:
            if kind == "dim":
                a3, b3, text, offset = args
                a2 = xy((R @ np.array(a3, float))[:2])
                b2 = xy((R @ np.array(b3, float))[:2])
                ox, oy = offset
                A = (a2[0] + ox, a2[1] + oy)
                B = (b2[0] + ox, b2[1] + oy)
                out.append(f'<line x1="{a2[0]:.1f}" y1="{a2[1]:.1f}" x2="{A[0]:.1f}" y2="{A[1]:.1f}" stroke="#666" stroke-width="0.8" stroke-dasharray="3,2"/>')
                out.append(f'<line x1="{b2[0]:.1f}" y1="{b2[1]:.1f}" x2="{B[0]:.1f}" y2="{B[1]:.1f}" stroke="#666" stroke-width="0.8" stroke-dasharray="3,2"/>')
                out.append(f'<line x1="{A[0]:.1f}" y1="{A[1]:.1f}" x2="{B[0]:.1f}" y2="{B[1]:.1f}" stroke="#111" stroke-width="1.2" marker-start="url(#ar)" marker-end="url(#ar)"/>')
                mx, my = (A[0] + B[0]) / 2, (A[1] + B[1]) / 2
                out += halo(mx + 4, my - 4, text, "start")
            elif kind == "label":
                p3, text, (dx, dy) = args
                p = xy((R @ np.array(p3, float))[:2])
                q = (p[0] + dx, p[1] + dy)
                out.append(f'<line x1="{p[0]:.1f}" y1="{p[1]:.1f}" x2="{q[0]:.1f}" y2="{q[1]:.1f}" stroke="#111" stroke-width="1"/>')
                out.append(f'<circle cx="{p[0]:.1f}" cy="{p[1]:.1f}" r="2.5" fill="#111"/>')
                anchor = "start" if dx >= 0 else "end"
                tx = q[0] + (4 if dx >= 0 else -4)
                for j, line_ in enumerate(text.split("\n")):
                    out += halo(tx, q[1] + 5 + 16 * j, line_, anchor)
    out.insert(2, '<defs><marker id="ar" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,1 L9,5 L0,9 z" fill="#111"/></marker></defs>')
    out.append("</svg>")
    return "\n".join(out)


def halo(x, y, text, anchor):
    base = f'x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}" font-family="Helvetica, Arial, sans-serif" font-size="15"'
    return [f'<text {base} fill="#fbfaf7" stroke="#fbfaf7" stroke-width="5" stroke-linejoin="round">{text}</text>',
            f'<text {base} fill="#111">{text}</text>']


def save(out: Path, name, svg):
    cairosvg.svg2png(bytestring=svg.encode(), write_to=str(out / f"{name}.png"), output_width=1350)

