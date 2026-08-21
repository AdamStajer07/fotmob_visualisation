import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from utils.colors import (BG_COLOR, LEGIA_COLOR, LEAGUE_COLOR, OTHER_COLOR, TEXT_COLOR, SUBTITLE_TEXT,
                    COLOR_GRID, ZONE_GREEN, ZONE_RED)

df = pd.read_parquet('data/team_stats.parquet')

SEASON = '2025/2026'
TEAM = 'Legia Warszawa'

teams = df[df['season'] == SEASON].copy()

legia = teams[teams['team_name'] == TEAM].iloc[0]
others = teams[teams['team_name'] != TEAM]

plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['Segoe UI', 'Arial', 'Helvetica'],
})

fig, ax = plt.subplots(figsize=(12, 10))

median_xg = teams['expected_goals_team'].median()
median_xga = teams['expected_goals_conceded_team'].median()

x_min = teams['expected_goals_team'].min() - 3
x_max = teams['expected_goals_team'].max() + 3
y_min = teams['expected_goals_conceded_team'].min() - 3
y_max = teams['expected_goals_conceded_team'].max() + 3

median_y_norm = (median_xga - y_min) / (y_max - y_min)

ax.axvspan(median_xg, x_max, ymin=median_y_norm, ymax=1,
           facecolor=ZONE_GREEN, alpha=0.5, zorder=0)
ax.axvspan(x_min, median_xg, ymin=0, ymax=median_y_norm,
           facecolor=ZONE_RED, alpha=0.5, zorder=0)

ax.scatter(
    others['expected_goals_team'], others['expected_goals_conceded_team'],
    color=OTHER_COLOR, s=105, zorder=3,
    edgecolors=BG_COLOR, linewidths=1.2, alpha=0.7,
)

for _, row in others.iterrows():
    goals_scored = int(row['expected_goals_team_sub'])
    goals_conceded = int(row['goals_conceded_team_match_sub'])
    label = f"{row['team_name']}\n{goals_scored}:{goals_conceded}"
    ax.annotate(
        label,
        (row['expected_goals_team'], row['expected_goals_conceded_team']),
        textcoords="offset points", xytext=(6, -12),
        fontsize=9, color=SUBTITLE_TEXT,
    )

legia_goals_scored = int(legia['expected_goals_team_sub'])
legia_goals_conceded = int(legia['goals_conceded_team_match_sub'])

ax.scatter(
    legia['expected_goals_team'], legia['expected_goals_conceded_team'],
    color=LEAGUE_COLOR, s=160, zorder=5,
    edgecolors=BG_COLOR, linewidths=2.0, alpha=0.9,
)
ax.annotate(
    f"Legia Warszawa\n{legia_goals_scored}:{legia_goals_conceded}",
    (legia['expected_goals_team'], legia['expected_goals_conceded_team']),
    textcoords="offset points", xytext=(8, 10),
    fontsize=11, fontweight='bold', color='black',
    alpha=0.9,
)

ax.text(0.95, 0.95, 'Strong attack\nStrong defence',
        transform=ax.transAxes, ha='right', va='top',
        fontsize=10, fontweight='bold', color=LEGIA_COLOR, alpha=0.5)
ax.text(0.05, 0.05, 'Weak attack\nWeak defence',
        transform=ax.transAxes, ha='left', va='bottom',
        fontsize=10, fontweight='bold', color='#c0392b', alpha=0.5)
ax.text(0.05, 0.95, 'Weak attack\nStrong defence',
        transform=ax.transAxes, ha='left', va='top',
        fontsize=9, color=SUBTITLE_TEXT, alpha=0.5)
ax.text(0.95, 0.05, 'Strong attack\nWeak defence',
        transform=ax.transAxes, ha='right', va='bottom',
        fontsize=9, color=SUBTITLE_TEXT, alpha=0.5)

ax.set_title(
    'EKSTRAKLASA 2025/26 — xG vs xGA',
    fontsize=18, fontweight='bold', color=TEXT_COLOR, pad=24, loc='left',
)
ax.text(
    0.0, 1.02,
    'Expected goals vs expected goals against | quadrants split by league median',
    transform=ax.transAxes, fontsize=10, color=SUBTITLE_TEXT,
    verticalalignment='bottom',
)

ax.set_xlabel('xG (expected goals)', fontsize=12, color=TEXT_COLOR, fontweight='bold')
ax.set_ylabel('xGA (expected goals against)', fontsize=12, color=TEXT_COLOR, fontweight='bold')
ax.tick_params(axis='both', labelsize=11, colors=SUBTITLE_TEXT, length=0)
ax.set_xlim(x_min, x_max)
ax.set_ylim(y_min, y_max)

ax.invert_yaxis()

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
