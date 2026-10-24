r"""
scripts/generate_comparison_charts.py
=====================================
Generate professional 300 DPI comparison charts from multi-algorithm evaluation data:
  1. chart_oa_comparison.png — Overall Accuracy grouped bar chart
  2. chart_kappa_comparison.png — Cohen's Kappa grouped bar chart
  3. chart_f1_comparison.png — Macro F1-Score grouped bar chart
  4. chart_radar_per_class.png — Multi-year radar chart per land-cover class
  5. chart_training_time.png — Training time efficiency comparison
"""

import os
import sys
import json
import csv
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

PROJ_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DATA_DIR = os.path.join(PROJ_ROOT, 'outputs', 'comparison')
CHART_DIR = os.path.join(DATA_DIR, 'charts')
os.makedirs(CHART_DIR, exist_ok=True)

# Load summary CSV
summary_path = os.path.join(DATA_DIR, 'comparison_summary.csv')
with open(summary_path, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    summary_rows = list(reader)

# Load per-class CSV
per_class_path = os.path.join(DATA_DIR, 'comparison_per_class.csv')
with open(per_class_path, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    per_class_rows = list(reader)

YEARS = ['2015', '2020', '2025']
ALGORITHMS = {
    'RF':  {'name': 'Random Forest', 'color': '#2ca02c'},
    'MLC': {'name': 'Maximum Likelihood (MLC)', 'color': '#1f77b4'},
    'NB':  {'name': 'Naive Bayes (Gaussian)', 'color': '#ff7f0e'},
    'MDC': {'name': 'Minimum Distance (MDC)', 'color': '#d62728'},
}
ALG_ORDER = ['RF', 'MLC', 'NB', 'MDC']

CLASSES = {
    1: 'Residential',
    2: 'Water Body',
    3: 'Industrial',
    4: 'Vegetation',
    5: 'Paddy',
}
CLASS_IDS = sorted(CLASSES.keys())

# Organize summary data: data[alg][year]
summary_data = {a: {} for a in ALG_ORDER}
for r in summary_rows:
    alg = r['algorithm']
    yr = r['year']
    if alg in summary_data:
        summary_data[alg][yr] = {
            'oa': float(r['overall_accuracy']) * 100,
            'kappa': float(r['kappa']),
            'f1': float(r['macro_f1']) * 100,
            'train_time': float(r['train_time_s']),
        }

# Organize per-class data: pc_data[alg][year][class_id]
pc_data = {a: {y: {} for y in YEARS} for a in ALG_ORDER}
for r in per_class_rows:
    alg = r['algorithm']
    yr = r['year']
    cid = int(r['class_id'])
    if alg in pc_data and yr in pc_data[alg]:
        pc_data[alg][yr][cid] = float(r['f1_score']) * 100

x = np.arange(len(YEARS))
width = 0.20

# ── 1. Overall Accuracy Comparison ──
fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
for i, alg in enumerate(ALG_ORDER):
    oas = [summary_data[alg][y]['oa'] for y in YEARS]
    bars = ax.bar(x + (i - 1.5) * width, oas, width,
                  label=ALGORITHMS[alg]['name'],
                  color=ALGORITHMS[alg]['color'], edgecolor='white', linewidth=0.8)
    for bar, val in zip(bars, oas):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.8,
                f'{val:.1f}%', ha='center', va='bottom', fontsize=8, fontweight='bold')

ax.set_xlabel('Mốc thời gian (Năm nghiên cứu)', fontsize=11, fontweight='bold')
ax.set_ylabel('Độ chính xác toàn thể - Overall Accuracy (%)', fontsize=11, fontweight='bold')
ax.set_title('SO SÁNH ĐỘ CHÍNH XÁC TOÀN THỂ (OA) GIỮA 4 THUẬT TOÁN PHÂN LOẠI\nKhu vực: Xuân Lãng – Bình Nguyên – Bình Xuyên, Phú Thọ (2015 – 2025)',
             fontsize=12, fontweight='bold', pad=15)
ax.set_xticks(x)
ax.set_xticklabels(YEARS, fontsize=11, fontweight='bold')
ax.legend(loc='lower left', fontsize=9, framealpha=0.95)
ax.set_ylim(0, 100)
ax.yaxis.set_major_formatter(mticker.PercentFormatter())
ax.grid(axis='y', linestyle='--', alpha=0.4)
plt.tight_layout()
p1 = os.path.join(CHART_DIR, 'chart_oa_comparison.png')
plt.savefig(p1, bbox_inches='tight')
plt.close()
print(f'  [1/5] Saved: {p1}')

# ── 2. Cohen's Kappa Comparison ──
fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
for i, alg in enumerate(ALG_ORDER):
    kappas = [summary_data[alg][y]['kappa'] for y in YEARS]
    bars = ax.bar(x + (i - 1.5) * width, kappas, width,
                  label=ALGORITHMS[alg]['name'],
                  color=ALGORITHMS[alg]['color'], edgecolor='white', linewidth=0.8)
    for bar, val in zip(bars, kappas):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.015,
                f'{val:.3f}', ha='center', va='bottom', fontsize=8, fontweight='bold')

ax.axhline(0.8, color='#388e3c', linestyle=':', linewidth=1.2, label='Rất cao (Almost Perfect ≥ 0.80)')
ax.axhline(0.6, color='#1976d2', linestyle='--', linewidth=1.2, label='Đáng kể (Substantial ≥ 0.60)')
ax.axhline(0.4, color='#f57c00', linestyle='-.', linewidth=1.2, label='Trung bình khá (Moderate ≥ 0.40)')

ax.set_xlabel('Mốc thời gian (Năm nghiên cứu)', fontsize=11, fontweight='bold')
ax.set_ylabel("Hệ số Cohen's Kappa (κ)", fontsize=11, fontweight='bold')
ax.set_title("SO SÁNH HỆ SỐ ĐỒNG THUẬN KAPPA GIỮA CÁC THUẬT TOÁN (2015 – 2025)",
             fontsize=12, fontweight='bold', pad=15)
ax.set_xticks(x)
ax.set_xticklabels(YEARS, fontsize=11, fontweight='bold')
ax.legend(loc='lower left', fontsize=8, framealpha=0.95)
ax.set_ylim(0, 1.0)
ax.grid(axis='y', linestyle='--', alpha=0.4)
plt.tight_layout()
p2 = os.path.join(CHART_DIR, 'chart_kappa_comparison.png')
plt.savefig(p2, bbox_inches='tight')
plt.close()
print(f'  [2/5] Saved: {p2}')

# ── 3. Macro F1-Score Comparison ──
fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
for i, alg in enumerate(ALG_ORDER):
    f1s = [summary_data[alg][y]['f1'] for y in YEARS]
    bars = ax.bar(x + (i - 1.5) * width, f1s, width,
                  label=ALGORITHMS[alg]['name'],
                  color=ALGORITHMS[alg]['color'], edgecolor='white', linewidth=0.8)
    for bar, val in zip(bars, f1s):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.8,
                f'{val:.1f}%', ha='center', va='bottom', fontsize=8, fontweight='bold')

ax.set_xlabel('Mốc thời gian (Năm nghiên cứu)', fontsize=11, fontweight='bold')
ax.set_ylabel('Chỉ số Macro F1-Score (%)', fontsize=11, fontweight='bold')
ax.set_title('SO SÁNH MACRO F1-SCORE GIỮA 4 THUẬT TOÁN (CÂN BẰNG PRECISION & RECALL)',
             fontsize=12, fontweight='bold', pad=15)
ax.set_xticks(x)
ax.set_xticklabels(YEARS, fontsize=11, fontweight='bold')
ax.legend(loc='lower left', fontsize=9, framealpha=0.95)
ax.set_ylim(0, 100)
ax.yaxis.set_major_formatter(mticker.PercentFormatter())
ax.grid(axis='y', linestyle='--', alpha=0.4)
plt.tight_layout()
p3 = os.path.join(CHART_DIR, 'chart_f1_comparison.png')
plt.savefig(p3, bbox_inches='tight')
plt.close()
print(f'  [3/5] Saved: {p3}')

# ── 4. Radar Chart: F1 per Class by Algorithm across 3 years ──
fig, axes = plt.subplots(1, 3, figsize=(18, 6), subplot_kw=dict(polar=True), dpi=300)
categories = [CLASSES[cid] for cid in CLASS_IDS]
N = len(categories)
angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
angles += angles[:1]

for idx, yr in enumerate(YEARS):
    ax = axes[idx]
    for alg in ALG_ORDER:
        vals = [pc_data[alg][yr][cid] for cid in CLASS_IDS]
        vals += vals[:1]
        ax.plot(angles, vals, 'o-', linewidth=1.8, label=ALGORITHMS[alg]['name'],
                color=ALGORITHMS[alg]['color'], markersize=4)
        ax.fill(angles, vals, alpha=0.06, color=ALGORITHMS[alg]['color'])

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories, fontsize=9, fontweight='bold')
    ax.set_ylim(0, 100)
    ax.set_title(f'Năm {yr}', fontsize=13, fontweight='bold', pad=18)
    ax.grid(True, linestyle='--', alpha=0.5)

axes[-1].legend(loc='upper right', bbox_to_anchor=(1.35, 1.15), fontsize=9)
fig.suptitle('SO SÁNH ĐỘ CHÍNH XÁC F1-SCORE TỪNG LỚP PHỦ ĐẤT THEO 4 THUẬT TOÁN',
             fontsize=14, fontweight='bold', y=1.03)
plt.tight_layout()
p4 = os.path.join(CHART_DIR, 'chart_radar_per_class.png')
plt.savefig(p4, bbox_inches='tight')
plt.close()
print(f'  [4/5] Saved: {p4}')

# ── 5. Training Time Efficiency ──
fig, ax = plt.subplots(figsize=(10, 5), dpi=300)
avg_times = [np.mean([summary_data[alg][y]['train_time'] for y in YEARS]) for alg in ALG_ORDER]
bars = ax.barh(ALG_ORDER[::-1], avg_times[::-1], color=[ALGORITHMS[a]['color'] for a in ALG_ORDER[::-1]],
               edgecolor='white', height=0.5)

for bar, val in zip(bars, avg_times[::-1]):
    ax.text(bar.get_width() + 0.05, bar.get_y() + bar.get_height()/2,
            f'{val:.3f} s', va='center', ha='left', fontsize=9, fontweight='bold')

ax.set_xlabel('Thời gian huấn luyện trung bình (giây)', fontsize=11, fontweight='bold')
ax.set_ylabel('Thuật toán phân loại', fontsize=11, fontweight='bold')
ax.set_title('SO SÁNH HIỆU NĂNG TÍNH TOÁN & THỜI GIAN HUẤN LUYỆN (TRAINING TIME)',
             fontsize=12, fontweight='bold', pad=15)
ax.set_xlim(0, max(avg_times) * 1.25)
ax.grid(axis='x', linestyle='--', alpha=0.4)
plt.tight_layout()
p5 = os.path.join(CHART_DIR, 'chart_training_time.png')
plt.savefig(p5, bbox_inches='tight')
plt.close()
print(f'  [5/5] Saved: {p5}')

print('\nAll 5 comparison charts generated successfully in 300 DPI!')
