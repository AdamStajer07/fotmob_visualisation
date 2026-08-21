import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from utils.colors import (BG_COLOR, LEGIA_COLOR, TEXT_COLOR, SUBTITLE_TEXT, LEAGUE_COLOR, COLOR_AVG_CLUB)
from utils.club_info import (SEASON, TEAM)
df = pd.read_parquet('data/team_stats.parquet')


legia = df[(df['team_name'] == TEAM) & (df['season'] == SEASON)].iloc[0]

total_goals = int(legia['goals_team_match_sub'])
set_piece_goals = int(legia['_set_piece_goals_team'])
penalties_won = int(legia['penalty_won_team'])
penalty_conversion = legia['penalty_won_team_sub'] / 100
penalty_goals = int(round(penalties_won * penalty_conversion))

open_play_goals = total_goals - set_piece_goals - penalty_goals

colors_pie = [LEGIA_COLOR, LEAGUE_COLOR, COLOR_AVG_CLUB]
labels = ['Open play', 'Set pieces', 'Penalties']
values = [open_play_goals, set_piece_goals, penalty_goals]

plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['Segoe UI', 'Arial', 'Helvetica'],
})

fig, ax = plt.subplots(figsize=(10, 10))

wedges, texts, autotexts = ax.pie(
    values,
    labels=labels,
    colors=colors_pie,
    autopct=lambda pct: f'{int(round(pct / 100 * sum(values)))}\n({pct:.0f}%)',
    pctdistance=0.75,
    startangle=90,
    textprops={'fontsize': 12, 'fontweight': 'bold', 'color': TEXT_COLOR},
    wedgeprops={'edgecolor': BG_COLOR, 'linewidth': 2.5},
)

for autotext in autotexts:
    autotext.set_color(BG_COLOR)
    autotext.set_fontsize(13)
    autotext.set_fontweight('bold')

centre_circle = plt.Circle((0, 0), 0.50, fc=BG_COLOR)
ax.add_artist(centre_circle)

ax.text(0, 0.05, str(total_goals), ha='center', va='center',
        fontsize=36, fontweight='bold', color=TEXT_COLOR)
ax.text(0, -0.12, 'total goals', ha='center', va='center',
        fontsize=12, color=SUBTITLE_TEXT)

ax.set_title(
    'LEGIA WARSZAWA — GOAL TYPES',
    fontsize=18, fontweight='bold', color=TEXT_COLOR, pad=24,
)
fig.text(
    0.5, 0.88,
    f'Ekstraklasa 2025/26 | {legia["matches_played"]:.0f} matches played',
    ha='center', fontsize=10, color=SUBTITLE_TEXT,
)

fig.patch.set_facecolor(BG_COLOR)
ax.set_facecolor(BG_COLOR)

fig.tight_layout()
fm = plt.get_current_fig_manager()
fm.window.showMaximized()
plt.show()
