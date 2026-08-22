import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from utils.colors import (BG_COLOR, LEGIA_COLOR, COLOR_AVG_CLUB, TEXT_COLOR, SUBTITLE_TEXT,
                    COLOR_GRID, COLOR_AVG_LEAGUE)
from utils.club_info import (EXCLUDED_PLAYERS)

df = pd.read_parquet('data/ekstraklasa_all_clean.parquet')

SEASON = '2025/2026'
TEAM = 'Legia Warszawa'
STAT = 'poss_won_att_3rd_team_title'
MIN_MATCHES = 5
MIN_STAT = 5

OFFENSIVE_POSITIONS = ['Striker', 'forward', 'Left Winger', 'Right Winger',
                       'Attacking Midfielder']

legia_players = df[
    (df['team'] == TEAM) &
    (df['tournament'] == 'Ekstraklasa') &
    (df['season'] == SEASON) &
    (df['position'] != 'Keeper')
].copy()
legia_players = legia_players[~legia_players['player_name'].isin(EXCLUDED_PLAYERS)]

legia_players[STAT] = legia_players[STAT].fillna(0)
legia_players['top_matches_uppercase'] = legia_players['top_matches_uppercase'].fillna(0)
legia_players = legia_players[
    (legia_players['top_matches_uppercase'] >= MIN_MATCHES) &
    (legia_players[STAT] >= MIN_STAT)
].copy()

legia_players = legia_players.sort_values(STAT, ascending=True).reset_index(drop=True)

all_outfield = df[
    (df['tournament'] == 'Ekstraklasa') &
    (df['season'] == SEASON) &
    (df['position'] != 'Keeper')
].copy()
all_outfield[STAT] = all_outfield[STAT].fillna(0)
all_outfield['top_matches_uppercase'] = all_outfield['top_matches_uppercase'].fillna(0)
all_outfield = all_outfield[
    (all_outfield['top_matches_uppercase'] >= MIN_MATCHES) &
    (all_outfield[STAT] >= MIN_STAT)
]
league_avg = all_outfield[STAT].mean()

top20_avg = all_outfield.sort_values(STAT, ascending=False).head(20)[STAT].mean()

club_avg = legia_players[STAT].mean()

avg_rows = pd.DataFrame([
    {'player_name': 'League average', STAT: league_avg, '_avg_type': 'league'},
    {'player_name': 'Top 20 average', STAT: top20_avg, '_avg_type': 'top20'},
    {'player_name': 'Club average', STAT: club_avg, '_avg_type': 'club'},
])
legia_players['_avg_type'] = ''
plot_data = pd.concat([legia_players, avg_rows], ignore_index=True)
plot_data = plot_data.sort_values(STAT, ascending=True).reset_index(drop=True)

colors = []
for _, row in plot_data.iterrows():
    if row['_avg_type'] == 'league':
        colors.append(COLOR_AVG_LEAGUE)
    elif row['_avg_type'] == 'club':
        colors.append(COLOR_AVG_CLUB)
    elif row['_avg_type'] == 'top20':
        colors.append('#8b5cf6')
    else:
        colors.append(LEGIA_COLOR)

plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['Segoe UI', 'Arial', 'Helvetica'],
})

fig, ax = plt.subplots(figsize=(14, max(8, len(plot_data) * 0.45)))

ax.barh(
    plot_data['player_name'], plot_data[STAT],
    color=colors, edgecolor=BG_COLOR, linewidth=0.5, zorder=3,
    height=0.7, alpha=0.85,
)

for i, (val, name, avg_type) in enumerate(zip(plot_data[STAT], plot_data['player_name'], plot_data['_avg_type'])):
    label = f'{val:.1f}' if avg_type else f'{int(val)}'
    if avg_type == 'league':
        color = COLOR_AVG_LEAGUE
    elif avg_type == 'club':
        color = COLOR_AVG_CLUB
    elif avg_type == 'top20':
        color = '#8b5cf6'
    else:
        color = TEXT_COLOR
    ax.text(val + 0.2, i, label, va='center', ha='left',
            fontsize=12, fontweight='bold', color=color)

ax.set_title(
    'LEGIA WARSZAWA — POSSESSION WON IN ATTACKING 3RD',
    fontsize=24, fontweight='bold', color=TEXT_COLOR, pad=30, loc='left',
)
ax.text(
    0.0, 1.02, 'Ekstraklasa 2025/26 | total recoveries in final third',
    transform=ax.transAxes, fontsize=16, color=SUBTITLE_TEXT,
    verticalalignment='bottom',
)

ax.tick_params(axis='y', labelsize=13, colors=TEXT_COLOR, length=0)
ax.tick_params(axis='x', labelsize=13, colors=SUBTITLE_TEXT, length=0)

ytick_labels = ax.get_yticklabels()
for label in ytick_labels:
    txt = label.get_text()
    if txt == 'League average':
        label.set_color(COLOR_AVG_LEAGUE)
        label.set_fontweight('bold')
    elif txt == 'Club average':
        label.set_color(COLOR_AVG_CLUB)
        label.set_fontweight('bold')
    elif txt == 'Top 20 average':
        label.set_color('#8b5cf6')
        label.set_fontweight('bold')

for spine in ax.spines.values():
    spine.set_visible(False)

ax.grid(axis='x', linewidth=0.5, alpha=0.3, color=COLOR_GRID, zorder=0)
ax.set_axisbelow(True)

fig.patch.set_facecolor(BG_COLOR)
ax.set_facecolor(BG_COLOR)

fig.tight_layout()
fm = plt.get_current_fig_manager()
fm.window.showMaximized()
plt.savefig('images/bar2.png', dpi=600, bbox_inches='tight', facecolor=BG_COLOR)
plt.show()
