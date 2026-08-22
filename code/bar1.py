import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from utils.colors import (BG_COLOR, LEGIA_COLOR, OTHER_COLOR, TEXT_COLOR, SUBTITLE_TEXT,
                    COLOR_GRID, COLOR_AVG_LEAGUE)
from utils.club_info import (SEASON)

df = pd.read_parquet('data/ekstraklasa_all_clean.parquet')

SEASON = '2025/2026'
LEGIA_KEEPERS = ['Kacper Tobiasz', 'Ottó Hindrich']
MIN_MATCHES = 5

keepers = df[
    (df['position'] == 'Keeper') &
    (df['tournament'] == 'Ekstraklasa') &
    (df['season'] == SEASON) &
    (df['top_matches_uppercase'] >= MIN_MATCHES)
].dropna(subset=['goals_prevented']).copy()

keepers = keepers.sort_values('goals_prevented', ascending=True).reset_index(drop=True)

keepers = keepers.drop_duplicates(subset='player_name', keep='last').reset_index(drop=True)

avg_goals_prevented = keepers['goals_prevented'].mean()
avg_saves = keepers['saves'].mean()

avg_row = pd.DataFrame([{
    'player_name': 'League average',
    'goals_prevented': avg_goals_prevented,
    'saves': avg_saves,
    'top_matches_uppercase': 0,
}])
keepers = pd.concat([keepers, avg_row], ignore_index=True)
keepers = keepers.sort_values('goals_prevented', ascending=True).reset_index(drop=True)

colors = []
for name in keepers['player_name']:
    if name in LEGIA_KEEPERS:
        colors.append(LEGIA_COLOR)
    elif name == 'League average':
        colors.append(COLOR_AVG_LEAGUE)
    else:
        colors.append(OTHER_COLOR)

plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['Segoe UI', 'Arial', 'Helvetica'],
})

fig, ax = plt.subplots(figsize=(12, max(8, len(keepers) * 0.45)))

bars = ax.barh(
    keepers['player_name'], keepers['goals_prevented'],
    color=colors, edgecolor=BG_COLOR, linewidth=0.5, zorder=3,
    height=0.7, alpha=0.85,
)

ax.axvline(x=0, color=TEXT_COLOR, linewidth=0.8, alpha=0.4, zorder=2)

for i, (val, name, saves) in enumerate(zip(keepers['goals_prevented'], keepers['player_name'], keepers['saves'])):
    saves_str = f" ({int(saves)} saves)" if pd.notna(saves) else ""
    if val >= 0:
        x_pos = val + 0.15
        ha = 'left'
    else:
        x_pos = 0.15
        ha = 'left'
    if name in LEGIA_KEEPERS:
        color = LEGIA_COLOR
    elif name == 'League average':
        color = COLOR_AVG_LEAGUE
    else:
        color = TEXT_COLOR
    ax.text(x_pos, i, f'{val:.1f}{saves_str}', va='center', ha=ha,
            fontsize=12, fontweight='bold', color=color)

ax.set_title(
    'GOALS PREVENTED — EKSTRAKLASA GOALKEEPERS',
    fontsize=24, fontweight='bold', color=TEXT_COLOR, pad=30, loc='left',
)
ax.text(
    0.0, 1.02,
    f'2025/26 | min. {MIN_MATCHES} matches | positive = saved more than expected',
    transform=ax.transAxes, fontsize=16, color=SUBTITLE_TEXT,
    verticalalignment='bottom',
)

ax.tick_params(axis='y', labelsize=12, colors=TEXT_COLOR, length=0)
ax.tick_params(axis='x', labelsize=10, colors=SUBTITLE_TEXT, length=0)

ytick_labels = ax.get_yticklabels()
for label in ytick_labels:
    if label.get_text() in LEGIA_KEEPERS:
        label.set_color(LEGIA_COLOR)
        label.set_fontweight('bold')
        label.set_fontsize(12)
    elif label.get_text() == 'League average':
        label.set_color(COLOR_AVG_LEAGUE)
        label.set_fontweight('bold')
        label.set_fontsize(12)

for spine in ax.spines.values():
    spine.set_visible(False)

ax.grid(axis='x', linewidth=0.5, alpha=0.3, color=COLOR_GRID, zorder=0)
ax.set_axisbelow(True)

fig.patch.set_facecolor(BG_COLOR)
ax.set_facecolor(BG_COLOR)

fig.tight_layout()
fm = plt.get_current_fig_manager()
fm.window.showMaximized()
plt.savefig('images/bar1.png', dpi=600, bbox_inches='tight', facecolor=BG_COLOR)
plt.show()
