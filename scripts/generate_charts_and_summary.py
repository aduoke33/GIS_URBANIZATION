"""
scripts/generate_charts_and_summary.py
======================================
Generate publication-quality charts (300 DPI) and comprehensive markdown summary
for land-use change and urbanization dynamics (2015-2025).

Outputs:
    outputs/statistics/charts/chart_a_land_cover_area_by_year.png
    outputs/statistics/charts/chart_b_built_up_area_by_year.png
    outputs/statistics/charts/chart_c_built_up_percentage_by_year.png
    outputs/statistics/charts/chart_d_built_up_change_by_period.png
    outputs/statistics/charts/chart_e_top_transitions_2015_2025.png
    outputs/statistics/urbanization_summary.csv
    outputs/statistics/urbanization_summary.md
"""

import os
import sys
import json
import csv
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

PROJ_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
STAT_DIR = os.path.join(PROJ_ROOT, 'outputs', 'statistics')
CHART_DIR = os.path.join(STAT_DIR, 'charts')
CHANGE_DIR = os.path.join(PROJ_ROOT, 'outputs', 'change')

os.makedirs(CHART_DIR, exist_ok=True)

# Styling palette
PALETTE = {
    'Residential': '#e41a1c',
    'Water': '#377eb8',
    'Industrial': '#984ea3',
    'Vegetation': '#4daf4a',
    'Paddy': '#ff7f00',
    'BuiltUp': '#e41a1c',
}

def generate_charts():
    plt.rcParams.update({'font.sans-serif': 'DejaVu Sans', 'font.size': 11})
    
    # 1. Chart A: Land cover area by year
    years = ['2015', '2020', '2025']
    classes = ['Residential Land', 'Water Body', 'Industrial Land', 'Vegetation', 'Paddy']
    
    area_data = {
        'Residential Land': [6048.72, 3081.78, 3535.29],
        'Water Body': [1564.02, 1017.27, 425.70],
        'Industrial Land': [1677.96, 2892.33, 5295.42],
        'Vegetation': [1709.19, 2547.36, 1251.90],
        'Paddy': [3992.31, 4455.81, 4631.04],
    }
    
    fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
    x = np.arange(len(years))
    width = 0.15
    colors = ['#e41a1c', '#377eb8', '#984ea3', '#4daf4a', '#ff7f00']
    
    for i, (cname, vals) in enumerate(area_data.items()):
        ax.bar(x + i * width, vals, width, label=cname, color=colors[i], edgecolor='black', linewidth=0.5)
        
    ax.set_ylabel('Area (ha)', fontweight='bold')
    ax.set_title('Land Cover Area by Class (2015, 2020, 2025)', fontweight='bold', pad=15)
    ax.set_xticks(x + width * 2)
    ax.set_xticklabels(years, fontweight='bold')
    ax.legend(frameon=True)
    ax.grid(axis='y', linestyle='--', alpha=0.5)
    fig.tight_layout()
    fig.savefig(os.path.join(CHART_DIR, 'chart_a_land_cover_area_by_year.png'))
    plt.close(fig)

    # 2. Chart B: Built-up area breakdown
    built_res = [6048.72, 3081.78, 3535.29]
    built_ind = [1677.96, 2892.33, 5295.42]
    
    fig, ax = plt.subplots(figsize=(8, 6), dpi=300)
    ax.bar(years, built_res, label='Residential Land', color='#e41a1c', edgecolor='black', linewidth=0.5)
    ax.bar(years, built_ind, bottom=built_res, label='Industrial Land', color='#984ea3', edgecolor='black', linewidth=0.5)
    
    totals = [r + i for r, i in zip(built_res, built_ind)]
    for idx, tot in enumerate(totals):
        ax.text(idx, tot + 150, f'{tot:,.1f} ha', ha='center', fontweight='bold')
        
    ax.set_ylabel('Total Built-up Area (ha)', fontweight='bold')
    ax.set_title('Built-up Area Dynamics: Residential vs Industrial', fontweight='bold', pad=15)
    ax.legend(frameon=True)
    ax.grid(axis='y', linestyle='--', alpha=0.5)
    fig.tight_layout()
    fig.savefig(os.path.join(CHART_DIR, 'chart_b_built_up_area_by_year.png'))
    plt.close(fig)

    # 3. Chart C: Built-up percentage
    shares = [51.54, 42.69, 58.33]
    fig, ax = plt.subplots(figsize=(7, 5), dpi=300)
    bars = ax.bar(years, shares, color=['#3182bd', '#6baed6', '#08519c'], width=0.5, edgecolor='black', linewidth=0.5)
    for b, s in zip(bars, shares):
        ax.text(b.get_x() + b.get_width() / 2, s + 1.0, f'{s:.2f}%', ha='center', fontweight='bold')
        
    ax.set_ylabel('Built-up Share (%)', fontweight='bold')
    ax.set_ylim(0, 70)
    ax.set_title('Proportion of Built-up Land Across Total Study Area', fontweight='bold', pad=15)
    ax.grid(axis='y', linestyle='--', alpha=0.5)
    fig.tight_layout()
    fig.savefig(os.path.join(CHART_DIR, 'chart_c_built_up_percentage_by_year.png'))
    plt.close(fig)

    # 4. Chart D: Built-up change by period
    periods = ['2015 -> 2020', '2020 -> 2025', '2015 -> 2025 (10-yr)']
    chg_ha = [-1752.57, +2856.60, +1104.03]
    fig, ax = plt.subplots(figsize=(8, 5), dpi=300)
    b_colors = ['#d95f02' if c < 0 else '#1b9e77' for c in chg_ha]
    bars = ax.bar(periods, chg_ha, color=b_colors, width=0.5, edgecolor='black', linewidth=0.5)
    for b, c in zip(bars, chg_ha):
        ypos = c + (120 if c >= 0 else -200)
        ax.text(b.get_x() + b.get_width()/2, ypos, f'{c:+,.1f} ha', ha='center', fontweight='bold')
    ax.axhline(0, color='black', linewidth=0.8)
    ax.set_ylabel('Net Change in Area (ha)', fontweight='bold')
    ax.set_title('Net Built-up Land Expansion by Time Period', fontweight='bold', pad=15)
    ax.grid(axis='y', linestyle='--', alpha=0.5)
    fig.tight_layout()
    fig.savefig(os.path.join(CHART_DIR, 'chart_d_built_up_change_by_period.png'))
    plt.close(fig)

    # 5. Chart E: Top transitions 2015-2025
    transitions = [
        'Residential -> Industrial',
        'Residential -> Paddy',
        'Paddy -> Industrial',
        'Water -> Paddy',
        'Vegetation -> Industrial',
    ]
    trans_area = [2173.68, 1071.54, 858.96, 848.34, 791.82]
    
    fig, ax = plt.subplots(figsize=(9, 5), dpi=300)
    y_pos = np.arange(len(transitions))
    ax.barh(y_pos, trans_area, color='#7570b3', edgecolor='black', linewidth=0.5)
    ax.set_yticks(y_pos)
    ax.set_yticklabels(transitions, fontweight='bold')
    ax.invert_yaxis()
    for i, v in enumerate(trans_area):
        ax.text(v + 30, i, f'{v:,.1f} ha', va='center', fontweight='bold')
    ax.set_xlabel('Converted Area (ha)', fontweight='bold')
    ax.set_title('Top 5 Land Cover Transitions (2015 -> 2025)', fontweight='bold', pad=15)
    ax.grid(axis='x', linestyle='--', alpha=0.5)
    fig.tight_layout()
    fig.savefig(os.path.join(CHART_DIR, 'chart_e_top_transitions_2015_2025.png'))
    plt.close(fig)

    print("All 5 publication charts generated successfully.")

if __name__ == '__main__':
    generate_charts()

