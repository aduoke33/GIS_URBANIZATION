r"""
scripts/generate_study_area_map.py
==================================
Generate high-resolution (300 DPI) Study Area Location & Overview Map:
  - Satellite backdrop (Landsat False Color B5-B4-B3)
  - Boundary overlay (Study area bounding box and vector geometry)
  - Coordinate grid (UTM Zone 48N / EPSG:32648)
  - Inset map showing regional context (Northern Vietnam / Phu Tho province)
  - Complete cartographic elements: North Arrow, Scale Bar, Legend, Metadata

Output:
  maps/map_study_area_location.png
"""

import os
import sys
import math
import sqlite3
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from shapely.wkb import loads as wkb_loads

PROJ_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
MAPS_DIR = os.path.join(PROJ_ROOT, 'maps')
PROC_DIR = os.path.join(PROJ_ROOT, 'data', 'processed', '2025')
SA_GPKG = os.path.join(PROJ_ROOT, 'data', 'study_area', 'study_area.gpkg')
OUT_PATH = os.path.join(MAPS_DIR, 'map_study_area_location.png')

SA_ORIGIN_X = 561150.0
SA_ORIGIN_Y = 2361060.0
SA_PIXEL = 30.0
SA_COLS = 349
SA_ROWS = 482

X_MIN = SA_ORIGIN_X
X_MAX = SA_ORIGIN_X + SA_COLS * SA_PIXEL
Y_MAX = SA_ORIGIN_Y
Y_MIN = SA_ORIGIN_Y - SA_ROWS * SA_PIXEL
EXTENT = [X_MIN, X_MAX, Y_MIN, Y_MAX]

def parse_blob(blob):
    data = bytes(blob)
    if data[:2] != b'GP':
        try:
            return wkb_loads(data)
        except Exception:
            return None
    flags = data[3]
    env_flag = (flags & 0b00001110) >> 1
    env_sizes = {0: 0, 1: 32, 2: 48, 3: 48, 4: 64}
    env_size = env_sizes.get(env_flag, 0)
    wkb_bytes = data[8 + env_size:]
    try:
        return wkb_loads(wkb_bytes)
    except Exception:
        return None

# Load Landsat bands for backdrop
b5 = np.load(os.path.join(PROC_DIR, 'SR_B5.npy')).astype(np.float32)  # NIR
b4 = np.load(os.path.join(PROC_DIR, 'SR_B4.npy')).astype(np.float32)  # Red
b3 = np.load(os.path.join(PROC_DIR, 'SR_B3.npy')).astype(np.float32)  # Green
qa = np.load(os.path.join(PROC_DIR, 'qa_mask.npy'))

def stretch(arr):
    valid = arr[np.isfinite(arr) & (arr > 0)]
    p2, p98 = np.percentile(valid, (2, 98))
    norm = np.clip((arr - p2) / (p98 - p2 + 1e-6), 0, 1)
    return norm

rgb = np.stack([stretch(b5), stretch(b4), stretch(b3)], axis=-1)
# Dim invalid
rgb[~qa] = 0.92

# Load vector boundary
conn = sqlite3.connect(SA_GPKG)
cur = conn.cursor()
cur.execute("SELECT geometry FROM study_area")
rows = cur.fetchall()
conn.close()

boundary_geoms = [parse_blob(r[0]) for r in rows if r[0] is not None]

# Create Figure
fig = plt.figure(figsize=(14, 11), dpi=300)
ax = fig.add_axes([0.08, 0.08, 0.68, 0.84])

# Plot Landsat False Color Backdrop
ax.imshow(rgb, extent=EXTENT, origin='upper', alpha=0.92)

# Plot Study Area Boundaries
for geom in boundary_geoms:
    if geom is None:
        continue
    if geom.geom_type == 'Polygon':
        x_pts, y_pts = geom.exterior.xy
        ax.plot(x_pts, y_pts, color='#ffeb3b', linewidth=2.5, label='Ranh giới khu vực nghiên cứu')
        ax.plot(x_pts, y_pts, color='#d32f2f', linewidth=1.2, linestyle='--')
    elif geom.geom_type == 'MultiPolygon':
        for poly in geom.geoms:
            x_pts, y_pts = poly.exterior.xy
            ax.plot(x_pts, y_pts, color='#ffeb3b', linewidth=2.5)
            ax.plot(x_pts, y_pts, color='#d32f2f', linewidth=1.2, linestyle='--')

# Landmarks and annotations
landmarks = [
    ('KCN Bình Xuyên', 568500, 2355500),
    ('KCN Bá Thiện', 569800, 2358200),
    ('TT. Hương Canh', 566200, 2352800),
    ('Xuân Lãng', 563500, 2358000),
    ('Sông Cà Lồ', 564800, 2348500),
]
for name, lx, ly in landmarks:
    ax.plot(lx, ly, marker='s', color='#d32f2f', markersize=6, markeredgecolor='white', markeredgewidth=1)
    ax.annotate(name, (lx, ly), textcoords="offset points", xytext=(8, 5),
                bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="#333", alpha=0.85, lw=0.6),
                fontsize=8, fontweight='bold', color='#111')

# Gridlines & Coordinates
ax.set_xlim(X_MIN, X_MAX)
ax.set_ylim(Y_MIN, Y_MAX)
ax.set_xlabel('Tọa độ X (Easting - mét) [UTM Zone 48N]', fontsize=10, fontweight='bold')
ax.set_ylabel('Tọa độ Y (Northing - mét) [UTM Zone 48N]', fontsize=10, fontweight='bold')
ax.grid(True, linestyle=':', alpha=0.6, color='white', linewidth=0.8)

# Title Header
fig.text(0.42, 0.94, 'BẢN ĐỒ VỊ TRÍ ĐỊA LÝ KHU VỰC NGHIÊN CỨU',
         fontsize=15, fontweight='bold', ha='center', va='center')
fig.text(0.42, 0.915, 'Cụm liên xã Xuân Lãng – Bình Nguyên – Bình Xuyên, tỉnh Phú Thọ & Vĩnh Phúc (Landsat 9 False Color B5-B4-B3)',
         fontsize=10, style='italic', ha='center', va='center', color='#333')

# ── Scale Bar ──
sb_x = X_MIN + 800
sb_y = Y_MIN + 800
sb_len = 3000  # 3 km
ax.add_patch(patches.Rectangle((sb_x, sb_y), sb_len, 180, facecolor='black', edgecolor='white', lw=1, zorder=10))
ax.add_patch(patches.Rectangle((sb_x + 1500, sb_y), 1500, 180, facecolor='white', edgecolor='black', lw=1, zorder=11))
ax.text(sb_x, sb_y - 250, '0', fontsize=8, fontweight='bold', ha='center', zorder=12,
        bbox=dict(boxstyle='round,pad=0.1', fc='white', ec='none', alpha=0.7))
ax.text(sb_x + 1500, sb_y - 250, '1.5', fontsize=8, fontweight='bold', ha='center', zorder=12,
        bbox=dict(boxstyle='round,pad=0.1', fc='white', ec='none', alpha=0.7))
ax.text(sb_x + 3000, sb_y - 250, '3 km', fontsize=8, fontweight='bold', ha='center', zorder=12,
        bbox=dict(boxstyle='round,pad=0.1', fc='white', ec='none', alpha=0.7))

# ── North Arrow ──
na_x = X_MAX - 1000
na_y = Y_MAX - 1200
ax.annotate('BẮC\n(N)', xy=(na_x, na_y + 400), xytext=(na_x, na_y - 300),
            arrowprops=dict(facecolor='black', edgecolor='white', width=3, headwidth=10),
            ha='center', va='center', fontsize=8, fontweight='bold', zorder=10,
            bbox=dict(boxstyle='circle,pad=0.3', fc='white', ec='black', alpha=0.8))

# ── Regional Inset Map (Right panel) ──
ax_inset = fig.add_axes([0.77, 0.52, 0.20, 0.38])
ax_inset.set_title('VỊ TRÍ TRONG KHU VỰC\n(Miền Bắc Việt Nam)', fontsize=9, fontweight='bold', pad=8)
ax_inset.set_xlim(104.5, 106.5)
ax_inset.set_ylim(20.8, 22.2)

# Approximate Northern provinces schematic
provinces = {
    'Phú Thọ': (105.15, 21.35),
    'Vĩnh Phúc': (105.55, 21.35),
    'Hà Nội': (105.85, 21.02),
    'Tuyên Quang': (105.22, 21.82),
    'Thái Nguyên': (105.84, 21.60),
}
for pname, (px, py) in provinces.items():
    ax_inset.plot(px, py, 'o', color='#555', markersize=4)
    ax_inset.text(px, py + 0.04, pname, fontsize=7, ha='center', fontweight='bold', color='#333')

# Study Area box in Inset (UTM 561150, 2346600 -> lat/lon approx 21.22N, 105.62E)
sa_lon = 105.62
sa_lat = 21.25
rect = patches.Rectangle((sa_lon - 0.06, sa_lat - 0.07), 0.12, 0.14,
                         linewidth=2, edgecolor='red', facecolor='yellow', alpha=0.45)
ax_inset.add_patch(rect)
ax_inset.annotate('Vùng NC', (sa_lon, sa_lat), xytext=(sa_lon - 0.55, sa_lat + 0.35),
                  arrowprops=dict(arrowstyle="->", color="red", lw=1.5),
                  fontsize=8, fontweight='bold', color='red',
                  bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="red", lw=1))

ax_inset.set_xlabel('Kinh độ Đông (°E)', fontsize=7)
ax_inset.set_ylabel('Vĩ độ Bắc (°N)', fontsize=7)
ax_inset.grid(True, linestyle=':', alpha=0.5)

# ── Information & Metadata Block (Right panel bottom) ──
ax_info = fig.add_axes([0.77, 0.08, 0.20, 0.40])
ax_info.axis('off')

meta_text = (
    "THÔNG TIN ĐỒ HỌA & GIS\n"
    "───────────────────────\n"
    "• Đề tài: GeoAI & Urbanization\n"
    "• Địa bàn: Bình Xuyên, Phú Thọ\n"
    "• Diện tích: 15,139.35 ha (151 km²)\n"
    "• Hệ quy chiếu: WGS 84 / UTM 48N\n"
    "• Mã EPSG: 32648\n"
    "• Độ phân giải: 30m × 30m\n"
    "• Kích thước lưới: 482 × 349 px\n"
    "• Nền ảnh: Landsat 9 (25/03/2025)\n"
    "  Tổ hợp màu giả B5-B4-B3\n"
    "• Tọa độ bao khung (BBox):\n"
    "  X: 561,150 m → 571,620 m\n"
    "  Y: 2,346,600 m → 2,361,060 m\n\n"
    "CHÚ GIẢI (LEGEND):\n"
    "───────────────────────\n"
    "▬ Ranh giới khu vực nghiên cứu\n"
    "■ Điểm mốc kinh tế / công nghiệp\n"
    "■ Đỏ tươi: Thực vật, vườn đồi, lúa\n"
    "■ Xanh dương/Đen: Nước tự nhiên\n"
    "■ Xám lơ/Tím: Mái tôn, KCN, bê tông\n"
)
ax_info.text(0.0, 1.0, meta_text, transform=ax_info.transAxes,
             fontsize=7.8, verticalalignment='top', fontfamily='monospace',
             bbox=dict(boxstyle='round,pad=0.5', facecolor='#f8f9fa', edgecolor='#bbb', linewidth=0.8))

plt.savefig(OUT_PATH, dpi=300, bbox_inches='tight')
plt.close()
print(f'Study Area Location Map generated successfully: {OUT_PATH}')
