"""
scripts/generate_maps.py
========================
Generate publication-quality thematic maps (300 DPI) for the project:
  1. maps/map_landcover_2015.png
  2. maps/map_landcover_2020.png
  3. maps/map_landcover_2025.png
  4. maps/map_landcover_comparison_3years.png
  5. maps/map_urban_expansion_2015_2025.png

Cartographic Elements:
  - Coordinate grid (UTM Zone 48N, EPSG:32648)
  - Clear Legend with official remote sensing color palette
  - North arrow
  - Metric Scale bar
  - Professional title, metadata block, and study area boundary
"""

import os
import sys
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap, BoundaryNorm
import matplotlib.patches as patches
from PIL import Image

PROJ_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if PROJ_ROOT not in sys.path:
    sys.path.insert(0, PROJ_ROOT)

from run_classification import (
    CLASSES,
    CLASS_IDS,
    SA_ORIGIN_X,
    SA_ORIGIN_Y,
    SA_PIXEL,
    SA_COLS,
    SA_ROWS,
    NODATA_VAL,
)

MAPS_DIR = os.path.join(PROJ_ROOT, 'maps')
CLS_DIR = os.path.join(PROJ_ROOT, 'outputs', 'classification')
os.makedirs(MAPS_DIR, exist_ok=True)

# Coordinate Bounds
X_MIN = SA_ORIGIN_X
X_MAX = SA_ORIGIN_X + SA_COLS * SA_PIXEL
Y_MAX = SA_ORIGIN_Y
Y_MIN = SA_ORIGIN_Y - SA_ROWS * SA_PIXEL
EXTENT = [X_MIN, X_MAX, Y_MIN, Y_MAX]

# Standard Remote Sensing Color Palette
COLOR_MAP = {
    1: '#d73027',  # Residential Land (Warm Red)
    2: '#3182bd',  # Water Body (Deep Cyan/Blue)
    3: '#7b1fa2',  # Industrial Land (Deep Purple)
    4: '#2ca02c',  # Vegetation (Forest Green)
    5: '#ff7f0e',  # Paddy (Orange / Amber)
    255: '#f0f0f0' # NoData / Cloud (Soft Gray)
}

# Matplotlib Colormap setup for classes 1..5 and 255
cmap_list = [COLOR_MAP[1], COLOR_MAP[2], COLOR_MAP[3], COLOR_MAP[4], COLOR_MAP[5]]
cmap_lc = ListedColormap(cmap_list)
norm_lc = BoundaryNorm([0.5, 1.5, 2.5, 3.5, 4.5, 5.5], cmap_lc.N)


def add_north_arrow(ax, x=0.92, y=0.90, length=0.08):
    """Add a professional cartographic North Arrow."""
    ax.annotate(
        'N',
        xy=(x, y + length),
        xytext=(x, y),
        xycoords='axes fraction',
        ha='center',
        va='bottom',
        fontsize=13,
        fontweight='bold',
        arrowprops=dict(
            facecolor='black',
            edgecolor='black',
            width=2.5,
            headwidth=8.0,
            headlength=10.0,
        ),
    )


def add_scale_bar(ax, x_start=0.05, y_start=0.04, length_km=2.0):
    """Draw a 2km scale bar with alternating black/white segments."""
    x_range = X_MAX - X_MIN
    y_range = Y_MAX - Y_MIN
    
    # Coordinates in data space
    bar_x0 = X_MIN + x_start * x_range
    bar_y0 = Y_MIN + y_start * y_range
    seg_len_m = 1000.0  # 1 km each segment
    bar_h = 0.015 * y_range
    
    # Segment 1: 0 - 1 km (Black)
    rect1 = patches.Rectangle((bar_x0, bar_y0), seg_len_m, bar_h, linewidth=0.8, edgecolor='black', facecolor='black', zorder=10)
    # Segment 2: 1 - 2 km (White)
    rect2 = patches.Rectangle((bar_x0 + seg_len_m, bar_y0), seg_len_m, bar_h, linewidth=0.8, edgecolor='black', facecolor='white', zorder=10)
    ax.add_patch(rect1)
    ax.add_patch(rect2)
    
    # Text labels
    ax.text(bar_x0, bar_y0 + bar_h * 1.3, '0', ha='center', fontsize=9, fontweight='bold', zorder=10)
    ax.text(bar_x0 + seg_len_m, bar_y0 + bar_h * 1.3, '1', ha='center', fontsize=9, fontweight='bold', zorder=10)
    ax.text(bar_x0 + 2 * seg_len_m, bar_y0 + bar_h * 1.3, '2 km', ha='center', fontsize=9, fontweight='bold', zorder=10)


def create_landcover_map(year: str):
    """Generate high-resolution thematic map for a specific year."""
    tif_path = os.path.join(CLS_DIR, f"classification_{year}.tif")
    with Image.open(tif_path) as img:
        arr = np.array(img)
        
    fig, ax = plt.subplots(figsize=(9, 11), dpi=300)
    
    # Mask nodata
    masked_arr = np.ma.masked_where(arr == NODATA_VAL, arr)
    
    # Background for NoData
    ax.imshow(np.ones_like(arr), extent=EXTENT, cmap=ListedColormap([COLOR_MAP[255]]), vmin=0, vmax=1)
    # Land cover raster
    im = ax.imshow(masked_arr, extent=EXTENT, cmap=cmap_lc, norm=norm_lc, interpolation='nearest')
    
    # Title & Subtitle
    ax.set_title(
        f"BẢN ĐỒ HIỆN TRẠNG LỚP PHỦ ĐẤT NĂM {year}\n"
        "Khu vực: Xuân Lãng – Bình Nguyên – Bình Xuyên, tỉnh Phú Thọ",
        fontsize=13,
        fontweight='bold',
        pad=15,
        ha='center',
    )
    
    # Coordinate grid
    ax.set_xlabel("Tọa độ X - UTM Zone 48N (m)", fontsize=10, fontweight='bold')
    ax.set_ylabel("Tọa độ Y - UTM Zone 48N (m)", fontsize=10, fontweight='bold')
    ax.xaxis.set_major_formatter(matplotlib.ticker.FormatStrFormatter('%d'))
    ax.yaxis.set_major_formatter(matplotlib.ticker.FormatStrFormatter('%d'))
    ax.tick_params(axis='both', labelsize=8)
    ax.grid(True, linestyle=':', alpha=0.6, color='gray')
    
    # Cartographic elements
    add_north_arrow(ax)
    add_scale_bar(ax)
    
    # Legend
    legend_handles = [
        patches.Patch(facecolor=COLOR_MAP[1], edgecolor='black', linewidth=0.5, label='1. Đất dân cư (Residential)'),
        patches.Patch(facecolor=COLOR_MAP[2], edgecolor='black', linewidth=0.5, label='2. Mặt nước (Water Body)'),
        patches.Patch(facecolor=COLOR_MAP[3], edgecolor='black', linewidth=0.5, label='3. Đất công nghiệp (Industrial)'),
        patches.Patch(facecolor=COLOR_MAP[4], edgecolor='black', linewidth=0.5, label='4. Cây xanh / Rừng (Vegetation)'),
        patches.Patch(facecolor=COLOR_MAP[5], edgecolor='black', linewidth=0.5, label='5. Đất trồng lúa (Paddy)'),
        patches.Patch(facecolor=COLOR_MAP[255], edgecolor='black', linewidth=0.5, label='Mây / NoData'),
    ]
    ax.legend(
        handles=legend_handles,
        loc='lower right',
        frameon=True,
        framealpha=0.92,
        facecolor='white',
        edgecolor='black',
        fontsize=9,
        title="CHÚ GIẢI",
        title_fontproperties={'weight': 'bold', 'size': 10},
    )
    
    # Metadata text box
    meta_text = (
        f"Dữ liệu: Landsat 8/9 OLI Surface Reflectance\n"
        f"Thuật toán: Random Forest Classifier\n"
        f"Hệ quy chiếu: WGS 84 / UTM Zone 48N (EPSG:32648)\n"
        f"Độ phân giải: 30m x 30m | Năm ảnh: {year}"
    )
    fig.text(0.12, 0.02, meta_text, fontsize=8, style='italic', color='#333333')
    
    fig.tight_layout(rect=[0, 0.04, 1, 1])
    out_png = os.path.join(MAPS_DIR, f"map_landcover_{year}.png")
    fig.savefig(out_png, dpi=300)
    plt.close(fig)
    print(f"  [OK] Exported: {out_png}")


def create_comparison_map():
    """Generate 3-panel comparative thematic map for 2015, 2020, 2025."""
    fig, axes = plt.subplots(1, 3, figsize=(18, 9), dpi=300, sharex=True, sharey=True)
    years = ['2015', '2020', '2025']
    
    for idx, (ax, yr) in enumerate(zip(axes, years)):
        tif_path = os.path.join(CLS_DIR, f"classification_{yr}.tif")
        with Image.open(tif_path) as img:
            arr = np.array(img)
        masked_arr = np.ma.masked_where(arr == NODATA_VAL, arr)
        
        ax.imshow(np.ones_like(arr), extent=EXTENT, cmap=ListedColormap([COLOR_MAP[255]]), vmin=0, vmax=1)
        ax.imshow(masked_arr, extent=EXTENT, cmap=cmap_lc, norm=norm_lc, interpolation='nearest')
        ax.set_title(f"Giai đoạn {yr}", fontsize=14, fontweight='bold', pad=10)
        ax.grid(True, linestyle=':', alpha=0.5)
        ax.tick_params(axis='both', labelsize=8)
        if idx == 0:
            ax.set_ylabel("UTM Y (m)", fontsize=10, fontweight='bold')
        ax.set_xlabel("UTM X (m)", fontsize=10, fontweight='bold')
        add_scale_bar(ax, x_start=0.06, y_start=0.04, length_km=2.0)
        add_north_arrow(ax, x=0.88, y=0.88)
        
    fig.suptitle(
        "SO SÁNH BIẾN ĐỘNG LỚP PHỦ ĐẤT GIAI ĐOẠN 2015 – 2020 – 2025\n"
        "Khu vực Xuân Lãng – Bình Nguyên – Bình Xuyên, tỉnh Phú Thọ",
        fontsize=16,
        fontweight='bold',
        y=0.98,
    )
    
    # Common Legend at bottom
    legend_handles = [
        patches.Patch(facecolor=COLOR_MAP[1], edgecolor='black', linewidth=0.5, label='Đất dân cư'),
        patches.Patch(facecolor=COLOR_MAP[2], edgecolor='black', linewidth=0.5, label='Mặt nước'),
        patches.Patch(facecolor=COLOR_MAP[3], edgecolor='black', linewidth=0.5, label='Đất công nghiệp'),
        patches.Patch(facecolor=COLOR_MAP[4], edgecolor='black', linewidth=0.5, label='Cây xanh'),
        patches.Patch(facecolor=COLOR_MAP[5], edgecolor='black', linewidth=0.5, label='Đất trồng lúa'),
        patches.Patch(facecolor=COLOR_MAP[255], edgecolor='black', linewidth=0.5, label='Mây / NoData'),
    ]
    fig.legend(
        handles=legend_handles,
        loc='lower center',
        ncol=6,
        frameon=True,
        framealpha=0.95,
        facecolor='white',
        edgecolor='black',
        fontsize=11,
        bbox_to_anchor=(0.5, 0.02),
    )
    
    fig.tight_layout(rect=[0, 0.06, 1, 0.94])
    out_png = os.path.join(MAPS_DIR, "map_landcover_comparison_3years.png")
    fig.savefig(out_png, dpi=300)
    plt.close(fig)
    print(f"  [OK] Exported: {out_png}")


def create_urban_expansion_map():
    """Generate specialized Urban & Industrial Expansion Map (2015-2025)."""
    p15 = os.path.join(CLS_DIR, "classification_2015.tif")
    p20 = os.path.join(CLS_DIR, "classification_2020.tif")
    p25 = os.path.join(CLS_DIR, "classification_2025.tif")
    
    with Image.open(p15) as im15, Image.open(p20) as im20, Image.open(p25) as im25:
        c15 = np.array(im15)
        c20 = np.array(im20)
        c25 = np.array(im25)
        
    valid = (c15 != NODATA_VAL) & (c25 != NODATA_VAL)
    bu_classes = [1, 3]  # Residential + Industrial
    
    bu15 = np.isin(c15, bu_classes) & valid
    bu20 = np.isin(c20, bu_classes) & (c20 != NODATA_VAL)
    bu25 = np.isin(c25, bu_classes) & valid
    
    # Categories:
    # 0: Non-built-up in 2025
    # 1: Built-up prior to 2015 (Stable Urban/Industrial)
    # 2: New Built-up (2015 -> 2020)
    # 3: New Built-up (2020 -> 2025)
    exp_grid = np.zeros(c15.shape, dtype=np.uint8)
    exp_grid[bu15 & bu25] = 1
    exp_grid[~bu15 & bu20 & bu25] = 2
    exp_grid[~bu15 & ~bu20 & bu25] = 3
    exp_grid[~valid] = 255
    
    cmap_exp = ListedColormap(['#e0e0e0', '#636363', '#fd8d3c', '#d94801'])
    norm_exp = BoundaryNorm([-0.5, 0.5, 1.5, 2.5, 3.5], cmap_exp.N)
    
    fig, ax = plt.subplots(figsize=(9, 11), dpi=300)
    masked_exp = np.ma.masked_where(exp_grid == 255, exp_grid)
    
    ax.imshow(np.ones_like(exp_grid), extent=EXTENT, cmap=ListedColormap(['#ffffff']), vmin=0, vmax=1)
    ax.imshow(masked_exp, extent=EXTENT, cmap=cmap_exp, norm=norm_exp, interpolation='nearest')
    
    ax.set_title(
        "BẢN ĐỒ KHÔNG GIAN MỞ RỘNG ĐÔ THỊ VÀ CÔNG NGHIỆP (2015 – 2025)\n"
        "Khu vực nghiên cứu: Xuân Lãng – Bình Nguyên – Bình Xuyên, tỉnh Phú Thọ",
        fontsize=12,
        fontweight='bold',
        pad=15,
        ha='center',
    )
    
    ax.set_xlabel("Tọa độ X - UTM Zone 48N (m)", fontsize=10, fontweight='bold')
    ax.set_ylabel("Tọa độ Y - UTM Zone 48N (m)", fontsize=10, fontweight='bold')
    ax.tick_params(axis='both', labelsize=8)
    ax.grid(True, linestyle=':', alpha=0.6, color='gray')
    
    add_north_arrow(ax)
    add_scale_bar(ax)
    
    legend_handles = [
        patches.Patch(facecolor='#636363', edgecolor='black', linewidth=0.5, label='Đất xây dựng trước 2015 (Ổn định)'),
        patches.Patch(facecolor='#fd8d3c', edgecolor='black', linewidth=0.5, label='Mở rộng mới giai đoạn 2015 – 2020'),
        patches.Patch(facecolor='#d94801', edgecolor='black', linewidth=0.5, label='Mở rộng mới giai đoạn 2020 – 2025'),
        patches.Patch(facecolor='#e0e0e0', edgecolor='black', linewidth=0.5, label='Đất nông nghiệp, cây xanh & mặt nước'),
    ]
    ax.legend(
        handles=legend_handles,
        loc='lower right',
        frameon=True,
        framealpha=0.92,
        facecolor='white',
        edgecolor='black',
        fontsize=9,
        title="ĐỘNG THÁI MỞ RỘNG",
        title_fontproperties={'weight': 'bold', 'size': 10},
    )
    
    fig.tight_layout(rect=[0, 0.04, 1, 1])
    out_png = os.path.join(MAPS_DIR, "map_urban_expansion_2015_2025.png")
    fig.savefig(out_png, dpi=300)
    plt.close(fig)
    print(f"  [OK] Exported: {out_png}")


def main():
    print("=" * 60)
    print("GENERATING THEMATIC MAPS (300 DPI)")
    print("=" * 60)
    for yr in ['2015', '2020', '2025']:
        create_landcover_map(yr)
    create_comparison_map()
    create_urban_expansion_map()
    print("=" * 60)
    print(f"All maps successfully exported to: {MAPS_DIR}")


if __name__ == '__main__':
    main()

