import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict
from utils.colors import (BG_COLOR, LEGIA_COLOR, LEAGUE_COLOR, TEXT_COLOR, SUBTITLE_TEXT,
                    COLOR_GRID, ZONE_GREEN, ZONE_RED, COLOR_TOP20_AVG, COLOR_STRIKERS_AVG)

df = pd.read_parquet('data/ekstraklasa_all_clean.parquet')

SEASON = '2025/2026'
TEAM = 'Legia Warszawa'
MIN_SHOTS_ON_TARGET = 3

legia_players = df[
    (df['team'] == TEAM) &
    (df['tournament'] == 'Ekstraklasa') &
    (df['season'] == SEASON) &
    (df['position'] != 'Keeper') &
    (df['ShotsOnTarget'] >= MIN_SHOTS_ON_TARGET)
].dropna(subset=['ShotsOnTarget', 'goals']).copy()

legia_players['conversion'] = legia_players['goals'] / legia_players['ShotsOnTarget']

all_outfield = df[
    (df['tournament'] == 'Ekstraklasa') &
    (df['season'] == SEASON) &
    (df['position'] != 'Keeper') &
    (df['ShotsOnTarget'] >= MIN_SHOTS_ON_TARGET)
].dropna(subset=['ShotsOnTarget', 'goals']).copy()

all_outfield['conversion'] = all_outfield['goals'] / all_outfield['ShotsOnTarget']

league_median_shots = all_outfield['ShotsOnTarget'].median()
league_median_conv = all_outfield['conversion'].median()

top20_league = all_outfield.sort_values('goals', ascending=False).head(20).copy()

STRIKER_POSITIONS = ['Striker', 'forward']
strikers_league = all_outfield[all_outfield['position'].isin(STRIKER_POSITIONS)].copy()

top20_avg_shots = top20_league['ShotsOnTarget'].mean()
top20_avg_conv = top20_league['conversion'].mean()
strikers_avg_shots = strikers_league['ShotsOnTarget'].mean()
strikers_avg_conv = strikers_league['conversion'].mean()

plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['Segoe UI', 'Arial', 'Helvetica'],
})

fig, ax = plt.subplots(figsize=(12, 10))

x_min, x_max = 0, legia_players['ShotsOnTarget'].max() + 2
y_min, y_max = -0.05, min(legia_players['conversion'].max() + 0.1, 1.0)

median_y_norm = (league_median_conv - y_min) / (y_max - y_min)

ax.axvspan(league_median_shots, x_max, ymin=median_y_norm, ymax=1,
           facecolor=ZONE_GREEN, alpha=0.5, zorder=0)
ax.axvspan(x_min, league_median_shots, ymin=0, ymax=median_y_norm,
           facecolor=ZONE_RED, alpha=0.5, zorder=0)

COLOR_TOP20_AVG = "#8b5cf6"
COLOR_STRIKERS_AVG = "#1e3a5f"

ax.scatter(
    top20_avg_shots, top20_avg_conv,
    color=COLOR_TOP20_AVG, s=120, zorder=4,
    edgecolors=BG_COLOR, linewidths=1.5, alpha=0.85,
    marker='D',
)
ax.annotate(
    'Top 20 strikers avg',
    (top20_avg_shots, top20_avg_conv),
    textcoords="offset points", xytext=(8, 8),
    fontsize=9, fontweight='bold', color=COLOR_TOP20_AVG,
    alpha=0.85,
)

ax.scatter(
    strikers_avg_shots, strikers_avg_conv,
    color=COLOR_STRIKERS_AVG, s=120, zorder=4,
    edgecolors=BG_COLOR, linewidths=1.5, alpha=0.85,
    marker='D',
)
ax.annotate(
    'All strikers avg',
    (strikers_avg_shots, strikers_avg_conv),
    textcoords="offset points", xytext=(8, 8),
    fontsize=9, fontweight='bold', color=COLOR_STRIKERS_AVG,
    alpha=0.85,
)

ax.scatter(
    legia_players['ShotsOnTarget'], legia_players['conversion'],
    color=LEGIA_COLOR, s=100, zorder=4,
    edgecolors=BG_COLOR, linewidths=1.5, alpha=0.85,
)

groups = defaultdict(list)
for _, row in legia_players.iterrows():
    key = (row['ShotsOnTarget'], round(row['conversion'], 4))
    groups[key].append(row['player_name'])

for (x, y), names in groups.items():
    label = ',\n'.join(names)
    ax.annotate(
        label,
        (x, y),
        textcoords="offset points", xytext=(8, 8),
        fontsize=9, fontweight='bold', color=TEXT_COLOR,
        alpha=0.85,
    )

ax.text(0.95, 0.95, 'Effective\nFinishers',
        transform=ax.transAxes, ha='right', va='top',
        fontsize=11, fontweight='bold', color=LEGIA_COLOR, alpha=0.6)
ax.text(0.05, 0.05, 'Low\nOutput',
        transform=ax.transAxes, ha='left', va='bottom',
        fontsize=11, fontweight='bold', color=LEAGUE_COLOR, alpha=0.6)
ax.text(0.95, 0.05, 'Many chances\nLow conversion',
        transform=ax.transAxes, ha='right', va='bottom',
        fontsize=9, color=SUBTITLE_TEXT, alpha=0.7)
ax.text(0.05, 0.95, 'Few chances\nHigh conversion',
        transform=ax.transAxes, ha='left', va='top',
        fontsize=9, color=SUBTITLE_TEXT, alpha=0.7)

ax.set_title(
    'LEGIA WARSZAWA — SHOTS ON TARGET vs CONVERSION RATE',
    fontsize=18, fontweight='bold', color=TEXT_COLOR, pad=24, loc='left',
)
ax.text(
    0.0, 1.02,
    f'Ekstraklasa 2025/26 | min. {MIN_SHOTS_ON_TARGET} shots on target',
    transform=ax.transAxes, fontsize=10, color=SUBTITLE_TEXT,
    verticalalignment='bottom',
)

ax.set_xlabel('Shots on target', fontsize=12, color=TEXT_COLOR, fontweight='bold')
ax.set_ylabel('Conversion rate (goals / shots on target)', fontsize=12, color=TEXT_COLOR, fontweight='bold')
ax.tick_params(axis='both', labelsize=11, colors=SUBTITLE_TEXT, length=0)
ax.set_xlim(x_min, x_max)
ax.set_ylim(y_min, y_max)
ax.set_xticks(np.arange(0, int(x_max) + 1, 2))
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x:.0%}'))

for spine in ax.spines.values():
    spine.set_visible(False)

ax.grid(linewidth=0.5, alpha=0.2, color=COLOR_GRID, zorder=0)
ax.set_axisbelow(True)

fig.patch.set_facecolor(BG_COLOR)
ax.set_facecolor(BG_COLOR)

ax.margins(x=0.05, y=0.05)

fig.tight_layout()
fm = plt.get_current_fig_manager()
fm.window.showMaximized()
plt.show()
