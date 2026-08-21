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

total_conceded = int(legia['goals_conceded_team_match_sub'])
set_piece_conceded = int(legia['_set_piece_goals_conceded_team'])
penalties_conceded = int(legia['penalty_conceded_team'])
penalty_goals_conceded = int(legia['penalty_conceded_team_sub'])
open_play_conceded = total_conceded - set_piece_conceded - penalty_goals_conceded

colors_pie = [LEGIA_COLOR, LEAGUE_COLOR, COLOR_AVG_CLUB]
labels_scored = ['Open play', 'Set pieces', 'Penalties']
values_scored = [open_play_goals, set_piece_goals, penalty_goals]

labels_conceded = ['Open play', 'Set pieces', 'Penalties']
values_conceded = [open_play_conceded, set_piece_conceded, penalty_goals_conceded]

plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['Segoe UI', 'Arial', 'Helvetica'],
})

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 9))

wedges1, texts1, autotexts1 = ax1.pie(
    values_scored,
    labels=labels_scored,
    colors=colors_pie,
    autopct=lambda pct: f'{int(round(pct / 100 * sum(values_scored)))}\n({pct:.0f}%)',
    pctdistance=0.75,
    startangle=90,
    textprops={'fontsize': 12, 'fontweight': 'bold', 'color': TEXT_COLOR},
    wedgeprops={'edgecolor': BG_COLOR, 'linewidth': 2.5},
)

for autotext in autotexts1:
    autotext.set_color(BG_COLOR)
    autotext.set_fontsize(13)
    autotext.set_fontweight('bold')

centre1 = plt.Circle((0, 0), 0.50, fc=BG_COLOR)
ax1.add_artist(centre1)

ax1.text(0, 0.05, str(total_goals), ha='center', va='center',
         fontsize=36, fontweight='bold', color=TEXT_COLOR)
ax1.text(0, -0.12, 'scored', ha='center', va='center',
         fontsize=12, color=SUBTITLE_TEXT)

ax1.set_title('Goals scored', fontsize=14, fontweight='bold', color=TEXT_COLOR, pad=16)

wedges2, texts2, autotexts2 = ax2.pie(
    values_conceded,
    labels=labels_conceded,
    colors=colors_pie,
    autopct=lambda pct: f'{int(round(pct / 100 * sum(values_conceded)))}\n({pct:.0f}%)',
    pctdistance=0.75,
    startangle=90,
    textprops={'fontsize': 12, 'fontweight': 'bold', 'color': TEXT_COLOR},
    wedgeprops={'edgecolor': BG_COLOR, 'linewidth': 2.5},
)

for autotext in autotexts2:
    autotext.set_color(BG_COLOR)
    autotext.set_fontsize(13)
    autotext.set_fontweight('bold')

centre2 = plt.Circle((0, 0), 0.50, fc=BG_COLOR)
ax2.add_artist(centre2)

ax2.text(0, 0.05, str(total_conceded), ha='center', va='center',
         fontsize=36, fontweight='bold', color=TEXT_COLOR)
ax2.text(0, -0.12, 'conceded', ha='center', va='center',
         fontsize=12, color=SUBTITLE_TEXT)

ax2.set_title('Goals conceded', fontsize=14, fontweight='bold', color=TEXT_COLOR, pad=16)

fig.suptitle(
    'LEGIA WARSZAWA — GOAL TYPES',
    fontsize=18, fontweight='bold', color=TEXT_COLOR, y=0.96,
)
fig.text(
    0.5, 0.91,
    f'Ekstraklasa 2025/26 | {legia["matches_played"]:.0f} matches played',
    ha='center', fontsize=10, color=SUBTITLE_TEXT,
)

fig.patch.set_facecolor(BG_COLOR)
ax1.set_facecolor(BG_COLOR)
ax2.set_facecolor(BG_COLOR)

fig.add_artist(plt.Line2D([0.5, 0.5], [0.05, 0.85], transform=fig.transFigure,
               color=SUBTITLE_TEXT, linewidth=1.2, linestyle='--', alpha=0.4))

fig.tight_layout(rect=[0, 0, 1, 0.90])
fm = plt.get_current_fig_manager()
fm.window.showMaximized()
plt.show()
