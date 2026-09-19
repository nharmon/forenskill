"""Regenerate docs/phase-flowchart.jpg (needs matplotlib and Pillow).

Usage: python3 docs/make_flowchart.py
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Polygon, Rectangle, FancyArrowPatch

import pathlib
OUT = str(pathlib.Path(__file__).resolve().parent / "phase-flowchart.jpg")

W, H = 204, 162
fig = plt.figure(figsize=(20.4, 16.2), dpi=100)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, W); ax.set_ylim(0, H); ax.axis("off")
fig.patch.set_facecolor("white")

INK = "#1f2933"
LINE = "#52606d"

# stage palette: (band fill, box fill, box edge)
PAL = {
    "intake":  ("#eef4fb", "#d6e6f7", "#2b6cb0"),
    "base":    ("#edf7f5", "#cfeae5", "#2c7a7b"),
    "sweep":   ("#f3effa", "#e2d8f4", "#6b46c1"),
    "content": ("#fdf6e7", "#f9e6bd", "#b7791f"),
    "synth":   ("#eef7ee", "#d2ebd3", "#2f855a"),
}
RED_F, RED_E = "#fde2e2", "#c53030"

def box(x, y, w, h, title, sub, stage, dashed=False):
    _, fill, edge = PAL[stage]
    p = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=1.6",
                       fc=fill, ec=edge, lw=2.0, ls=(0, (5, 3)) if dashed else "-", zorder=3)
    ax.add_patch(p)
    ax.text(x + w / 2, y + h - 3.6, title, ha="center", va="center", fontsize=13,
            fontweight="bold", color=INK, zorder=4)
    ax.text(x + w / 2, y + h / 2 - 2.2, sub, ha="center", va="center", fontsize=10.5,
            color=INK, zorder=4, linespacing=1.25)

def arrow(p0, p1, color=LINE, lw=2.0, dashed=False, head=True):
    ax.add_patch(FancyArrowPatch(p0, p1, arrowstyle="-|>" if head else "-", mutation_scale=16,
                                 lw=lw, color=color, ls=(0, (4, 3)) if dashed else "-",
                                 shrinkA=0, shrinkB=0, zorder=2))

def poly(pts, color=LINE, lw=2.0, dashed=False, head_last=True):
    for a, b in zip(pts[:-2], pts[1:-1]):
        arrow(a, b, color, lw, dashed, head=False)
    arrow(pts[-2], pts[-1], color, lw, dashed, head=head_last)

# ---------- title ----------
ax.text(W / 2, 157.6, "forenskill — Forensic Disk Image Analysis: Phase Flow", ha="center",
        fontsize=24, fontweight="bold", color=INK)
ax.text(W / 2, 152.6, "Phases run in numeric order 0 → 19. Each phase is a file the skill reads only when it reaches it.",
        ha="center", fontsize=12.5, color=LINE)

# ---------- rows ----------
X0, X1 = 24, 200
BH = 14
row_top = [143, 115, 87, 59, 31]         # top y of each row
row_stage = ["intake", "base", "sweep", "content", "synth"]
row_label = ["STAGE 1 · INTAKE & INTEGRITY",
             "STAGE 2 · VOLUMES, BASELINE & FILE SYSTEM",
             "STAGE 3 · ARTIFACT SWEEPS",
             "STAGE 4 · PROTECTED DATA & CONTENT",
             "STAGE 5 · SYNTHESIS & REPORT"]

def slots(n, gap=9):
    w = (X1 - X0 - gap * (n - 1)) / n
    return [(X0 + i * (w + gap), w) for i in range(n)]

# bands (behind everything)
for top, st, lab in zip(row_top, row_stage, row_label):
    band = PAL[st][0]
    ax.add_patch(Rectangle((X0 - 2, top - BH - 6), X1 - X0 + 4, BH + 12.5, fc=band, ec="none", zorder=0))
    ax.text(X1 + 1, top + 4.8, lab, ha="right", va="center", fontsize=9.5, color=LINE,
            fontweight="bold", zorder=1)

centers = {}   # name -> (cx, top_y, bottom_y, left, right)
def place(name, i, n, row, title, sub, dashed=False):
    x, w = slots(n)[i]
    top = row_top[row]
    box(x, top - BH, w, BH, title, sub, row_stage[row], dashed)
    centers[name] = (x + w / 2, top, top - BH, x, x + w)

# Row 1: P0, P1, decision, STOP
place("p0", 0, 4, 0, "Phase 0", "Setup, legal scope,\nchain of custody")
place("p1", 1, 4, 0, "Phase 1", "Evidence identification\n& integrity (hashing)")

dx, dw = slots(4)[2]
dcy = row_top[0] - BH / 2
dia = Polygon([(dx, dcy), (dx + dw / 2, dcy + BH / 2 + 1.5), (dx + dw, dcy), (dx + dw / 2, dcy - BH / 2 - 1.5)],
              closed=True, fc="#fff8dc", ec="#b7791f", lw=2.0, zorder=3)
ax.add_patch(dia)
ax.text(dx + dw / 2, dcy + 1.2, "Hashes match?", ha="center", va="center", fontsize=12.5,
        fontweight="bold", color=INK, zorder=4)
ax.text(dx + dw / 2, dcy - 2.6, "image / hash sheet /\nacquisition log", ha="center", va="center",
        fontsize=9, color=INK, zorder=4, linespacing=1.2)
centers["dia"] = (dx + dw / 2, dcy + BH / 2 + 1.5, dcy - BH / 2 - 1.5, dx, dx + dw)

sx, sw = slots(4)[3]
ax.add_patch(FancyBboxPatch((sx, row_top[0] - BH), sw, BH, boxstyle="round,pad=0,rounding_size=1.6",
                            fc=RED_F, ec=RED_E, lw=2.4, zorder=3))
ax.text(sx + sw / 2, row_top[0] - 3.6, "STOP", ha="center", va="center", fontsize=14,
        fontweight="bold", color=RED_E, zorder=4)
ax.text(sx + sw / 2, row_top[0] - BH / 2 - 2.2, "Flag in anomalies.md,\ntell the user, wait", ha="center",
        va="center", fontsize=10.5, color=INK, zorder=4, linespacing=1.25)

# Row 2
place("p3", 0, 4, 1, "Phase 3", "Partition / volume\nlayout")
place("p4", 1, 4, 1, "Phase 4", "System baseline &\ntime zone")
place("p6", 2, 4, 1, "Phase 6", "File system contents\n(allocated + deleted)")
place("p7", 3, 4, 1, "Phase 7", "OS artifacts: Windows,\nmacOS or Linux")

# Row 3
place("p8", 0, 4, 2, "Phase 8", "Volatile / memory\nevidence", dashed=True)
place("p9", 1, 4, 2, "Phase 9", "Browser, email, chat,\ncloud-sync artifacts")
place("p10", 2, 4, 2, "Phase 10", "Virtual machine &\ncontainer evidence", dashed=True)
place("p11", 3, 4, 2, "Phase 11", "Anti-forensics\nindicators")

# Row 4
place("p12", 0, 5, 3, "Phase 12", "Encrypted / protected\nvolumes", dashed=True)
place("p13", 1, 5, 3, "Phase 13", "Document & image\ncontent analysis")
place("p14", 2, 5, 3, "Phase 14", "Photo EXIF / GPS\ngeolocation", dashed=True)
place("p15", 3, 5, 3, "Phase 15", "Unallocated-space\ncarving")
place("p16", 4, 5, 3, "Phase 16", "Password / encryption\nrecovery", dashed=True)

# Row 5
place("p17", 0, 4, 4, "Phase 17", "Cross-correlation\n& timeline")
place("p18", 1, 4, 4, "Phase 18", "Exhibit / items-\nrecovered tracking")
place("p19", 2, 4, 4, "Phase 19", "Report generation\n(follows template.txt)")
tx, tw = slots(4)[3]
ax.add_patch(FancyBboxPatch((tx, row_top[4] - BH), tw, BH, boxstyle="round,pad=0,rounding_size=7",
                            fc="#2f855a", ec="#22543d", lw=2.0, zorder=3))
ax.text(tx + tw / 2, row_top[4] - BH / 2 + 1.6, "findings_report.txt", ha="center", va="center",
        fontsize=13, fontweight="bold", color="white", zorder=4)
ax.text(tx + tw / 2, row_top[4] - BH / 2 - 2.6, "re-hash image first", ha="center", va="center",
        fontsize=10.5, color="white", zorder=4)

# ---------- arrows within rows ----------
def mid_y(name):
    c = centers[name]; return (c[1] + c[2]) / 2

def h_arrow(a, b):
    ca, cb = centers[a], centers[b]
    arrow((ca[4], mid_y(a)), (cb[3], mid_y(b)))

for a, b in [("p0", "p1"), ("p1", "dia"), ("p3", "p4"), ("p4", "p6"), ("p6", "p7"),
             ("p8", "p9"), ("p9", "p10"), ("p10", "p11"),
             ("p12", "p13"), ("p13", "p14"), ("p14", "p15"), ("p15", "p16"),
             ("p17", "p18"), ("p18", "p19")]:
    h_arrow(a, b)

# decision -> STOP (No)
arrow((centers["dia"][4], dcy), (sx, dcy), color=RED_E, lw=2.4)
ax.text((centers["dia"][4] + sx) / 2, dcy + 2.2, "No", ha="center", fontsize=12, fontweight="bold", color=RED_E)
# p19 -> terminal
arrow((centers["p19"][4], mid_y("p19")), (tx, row_top[4] - BH / 2))

# ---------- row-to-row channels ----------
def channel(last, first, row_next, dx_exit=0, label=None):
    cl, cf = centers[last], centers[first]
    y_exit = cl[2]
    y_gap = y_exit - 6.6
    poly([(cl[0] + dx_exit, y_exit), (cl[0] + dx_exit, y_gap), (cf[0], y_gap), (cf[0], row_top[row_next])])
    if label:
        ax.text(cl[0] + dx_exit + 1.6, y_gap + 2.6, label, ha="left", va="center", fontsize=11,
                fontweight="bold", color="#2f855a")

channel("dia", "p3", 1, label="Yes")
channel("p7", "p8", 2)
channel("p11", "p12", 3)
channel("p16", "p17", 4, dx_exit=8)

# ---------- P12 -> P16 bypass (no key found) ----------
c12, c16 = centers["p12"], centers["p16"]
yb = c12[2] - 3.4
poly([(c12[0] + 8, c12[2]), (c12[0] + 8, yb), (c16[0] - 8, yb), (c16[0] - 8, c16[2])],
     color=RED_E, dashed=True)
ax.text((c12[0] + c16[0]) / 2, yb + 1.9, "key not found in image / memory  →  cracking fallback (needs the user's go-ahead first)",
        ha="center", va="center", fontsize=10.5, color=RED_E, fontweight="bold",
        bbox=dict(fc=PAL["content"][0], ec="none", pad=1.5), zorder=5)

# ---------- decrypted-volume loop (left margin) ----------
lx = 20.6
c3 = centers["p3"]
poly([(c12[3], mid_y("p12")), (lx, mid_y("p12")), (lx, mid_y("p3")), (c3[3], mid_y("p3"))],
     color="#6b46c1", dashed=True)
ax.text(lx - 1.5, (mid_y("p12") + mid_y("p3")) / 2, "decrypted volume re-enters Phases 3 and 6–11",
        rotation=90, ha="center", va="center", fontsize=10, color="#6b46c1", fontweight="bold",
        bbox=dict(fc="white", ec="none", pad=1.2), zorder=5)

# ---------- continuous phases (left bars) ----------
def vbar(x, w, title, sub):
    ax.add_patch(FancyBboxPatch((x, 17), w, 126, boxstyle="round,pad=0,rounding_size=1.6",
                                fc="#e4e7eb", ec="#616e7c", lw=2.0, zorder=3))
    ax.text(x + w / 2, 80, title, rotation=90, ha="center", va="center", fontsize=13,
            fontweight="bold", color=INK, zorder=4)
    ax.text(x + w / 2 - 2.4, 80, sub, rotation=90, ha="center", va="center", fontsize=9.6,
            color=INK, zorder=4)

vbar(0.8, 7.6, "Phase 2 — runs throughout", "")
vbar(9.2, 7.6, "Phase 5 — runs throughout", "")
# re-place text in two lines: bold title + sub (side by side, rotated)
for t in list(ax.texts):
    if t.get_rotation() == 90 and t.get_text() in ("Phase 2 — runs throughout", "Phase 5 — runs throughout"):
        t.set_position((t.get_position()[0] + 1.6, 80))
        t.set_fontsize(12.5)
ax.text(0.8 + 3.8 - 2.0, 80, "Methodology log · tool versions · corroboration", rotation=90, ha="center",
        va="center", fontsize=10, color=INK, zorder=4)
ax.text(9.2 + 3.8 - 2.0, 80, "Names · addresses · phones · IDs → cross-links", rotation=90, ha="center",
        va="center", fontsize=10, color=INK, zorder=4)

# ---------- legend ----------
ly = 8.6
ax.text(2, ly + 3.6, "Legend", fontsize=12, fontweight="bold", color=INK, va="center")
def leg_box(x, dashed, label, fill="#d6e6f7", edge="#2b6cb0"):
    ax.add_patch(FancyBboxPatch((x, ly - 1.7), 8, 3.4, boxstyle="round,pad=0,rounding_size=0.8",
                                fc=fill, ec=edge, lw=1.8, ls=(0, (5, 3)) if dashed else "-", zorder=3))
    ax.text(x + 10, ly, label, va="center", fontsize=10.5, color=INK)
leg_box(2, False, "Always performed")
leg_box(38, True, "Conditional — mark N/A with a reason if the evidence isn't present")
leg_box(112, False, "STOP: ask the user", fill=RED_F, edge=RED_E)
ax.text(2, 2.6, "Ask the user before continuing on: hash mismatch or acquisition error (P1) · unclear legal scope (P0) · "
                "any large password-cracking attack (P16) · any destructive action outside the working directory.",
        fontsize=10, color=INK, va="center")

fig.savefig(OUT, format="jpeg", dpi=100, pil_kwargs={"quality": 93})
print("saved", OUT)
