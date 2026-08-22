import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict
from utils.colors import (BG_COLOR, LEGIA_COLOR, LEAGUE_COLOR, TEXT_COLOR, SUBTITLE_TEXT,
                    COLOR_GRID, ZONE_GREEN, ZONE_RED, COLOR_AVG_LEAGUE, COLOR_AVG_CLUB)
from utils.club_info import (SEASON, TEAM, EXCLUDED_PLAYERS)

df = pd.read_parquet('data/ekstraklasa_all_clean.parquet')

MIN_MATCHES = 5
MIN_AERIALS = 10 

legia_players = df[
    (df['team'] == TEAM) &
    (df['tournament'] == 'Ekstraklasa') &
    (df['season'] == SEASON) &
    (df['position'] != 'Keeper')
].copy()
legia_players = legia_players[~legia_players['player_name'].isin(EXCLUDED_PLAYERS)]

legia_players['top_matches_uppercase'] = legia_players['top_matches_uppercase'].fillna(0)
legia_players = legia_players[legia_players['top_matches_uppercase'] >= MIN_MATCHES].copy()

legia_players['aerials_won'] = legia_players['aerials_won'].fillna(0)
legia_players['aerials_won_percent'] = legia_players['aerials_won_percent'].fillna(0)

legia_players = legia_players[legia_players['aerials_won'] >= MIN_AERIALS].copy()

all_outfield = df[
    (df['tournament'] == 'Ekstraklasa') &
    (df['season'] == SEASON) &
    (df['position'] != 'Keeper')
].copy()
all_outfield['top_matches_uppercase'] = all_outfield['top_matches_uppercase'].fillna(0)
all_outfield = all_outfield[all_outfield['top_matches_uppercase'] >= MIN_MATCHES].copy()
all_outfield['aerials_won'] = all_outfield['aerials_won'].fillna(0)
all_outfield['aerials_won_percent'] = all_outfield['aerials_won_percent'].fillna(0)
all_outfield = all_outfield[all_outfield['aerials_won'] >= MIN_AERIALS].copy()

league_avg_aerials = all_outfield['aerials_won'].mean()
league_avg_aerials_pct = all_outfield['aerials_won_percent'].mean()
club_avg_aerials = legia_players['aerials_won'].mean()
club_avg_aerials_pct = legia_players['aerials_won_percent'].mean()

legia_players['top_minutes_played'] = legia_players['top_minutes_played'].fillna(0)
min_minutes = legia_players['top_minutes_played'].min()
max_minutes = legia_players['top_minutes_played'].max()
size_min, size_max = 80, 350
if max_minutes > min_minutes:
    legia_players['dot_size'] = size_min + (legia_players['top_minutes_played'] - min_minutes) / (max_minutes - min_minutes) * (size_max - size_min)
else:
    legia_players['dot_size'] = (size_min + size_max) / 2

def shorten_names(names_list):
    surnames = {}
    for full_name in names_list:
        parts = full_name.split()
        surname = parts[-1] if parts else full_name
        surnames.setdefault(surname, []).append(full_name)

    short = {}
    for surname, fulls in surnames.items():
        if len(fulls) == 1:
            short[fulls[0]] = surname
        else:
            for full in fulls:
                parts = full.split()
                short[full] = f"{parts[0][0]}. {surname}" if len(parts) > 1 else surname
    return short

name_map = shorten_names(legia_players['player_name'].tolist())
legia_players['short_name'] = legia_players['player_name'].map(name_map)

plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['Segoe UI', 'Arial', 'Helvetica'],
})

fig, ax = plt.subplots(figsize=(18, 12))

x_min = 0
x_max = legia_players['aerials_won'].max() * 1.05
y_min = max(0, legia_players['aerials_won_percent'].min() - 10)
y_max = min(90, legia_players['aerials_won_percent'].max() + 10)

median_x = league_avg_aerials
median_y = league_avg_aerials_pct

median_y_norm = (median_y - y_min) / (y_max - y_min)
median_x_norm = (median_x - x_min) / (x_max - x_min)

ax.axvspan(median_x, x_max, ymin=median_y_norm, ymax=1,
           facecolor=ZONE_GREEN, alpha=0.5, zorder=0)
ax.axvspan(x_min, median_x, ymin=0, ymax=median_y_norm,
           facecolor=ZONE_RED, alpha=0.5, zorder=0)

ax.scatter(
    league_avg_aerials, league_avg_aerials_pct,
    color=COLOR_AVG_LEAGUE, s=140, zorder=5,
    edgecolors=BG_COLOR, linewidths=1.5, alpha=0.9,
    marker='D',
)
ax.annotate(
    'League average',
    (league_avg_aerials, league_avg_aerials_pct),
    textcoords="offset points", xytext=(8, 8),
    fontsize=13, fontweight='bold', color=COLOR_AVG_LEAGUE,
    alpha=0.9,
)

ax.scatter(
    club_avg_aerials, club_avg_aerials_pct,
    color=COLOR_AVG_CLUB, s=140, zorder=1,
    edgecolors=BG_COLOR, linewidths=1.5, alpha=0.9,
    marker='D',
)
ax.annotate(
    'Club average',
    (club_avg_aerials, club_avg_aerials_pct),
    textcoords="offset points", xytext=(8, 8),
    fontsize=13, fontweight='bold', color=COLOR_AVG_CLUB,
    alpha=0.9,
)

ax.scatter(
    legia_players['aerials_won'],
    legia_players['aerials_won_percent'],
    s=legia_players['dot_size'],
    color=LEGIA_COLOR,
    zorder=1,
    edgecolors=BG_COLOR,
    linewidths=1.5,
    alpha=0.85,
)

positions = []
for _, row in legia_players.iterrows():
    positions.append({
        'x': row['aerials_won'],
        'y': row['aerials_won_percent'],
        'name': row['short_name'],
    })

positions.sort(key=lambda p: (p['y'], p['x']))

used_offsets = []
for i, pos in enumerate(positions):
    collision = False
    for prev in used_offsets:
        if abs(pos['y'] - prev['y']) < 3 and abs(pos['x'] - prev['x']) < (x_max - x_min) * 0.08:
            collision = True
            break

    if collision:
        xytext = (8, -8)
        va = 'top'
    else:
        xytext = (8, 8)
        va = 'bottom'

    ax.annotate(
        pos['name'],
        (pos['x'], pos['y']),
        textcoords="offset points", xytext=xytext,
        fontsize=13, fontweight='bold', color=TEXT_COLOR,
        alpha=0.85, va=va, zorder=2
    )
    used_offsets.append(pos)

ax.text(0.95, 0.95, 'Aerial\nDominators',
        transform=ax.transAxes, ha='right', va='top',
        fontsize=14, fontweight='bold', color=LEGIA_COLOR, alpha=0.5)
ax.text(0.05, 0.05, 'Weak\nin the air',
        transform=ax.transAxes, ha='left', va='bottom',
        fontsize=14, fontweight='bold', color=LEAGUE_COLOR, alpha=0.5)
ax.text(0.95, 0.05, 'Many duels\nLow win rate',
        transform=ax.transAxes, ha='right', va='bottom',
        fontsize=12, color=SUBTITLE_TEXT, alpha=0.6)
ax.text(0.05, 0.95, 'Few duels\nHigh win rate',
        transform=ax.transAxes, ha='left', va='top',
        fontsize=12, color=SUBTITLE_TEXT, alpha=0.6)

ax.set_title(
    'LEGIA WARSZAWA — AERIAL DUELS: VOLUME vs EFFICIENCY',
    fontsize=24, fontweight='bold', color=TEXT_COLOR, pad=30, loc='left',
)
ax.text(
    0.0, 1.02,
    f'Ekstraklasa 2025/26 | min. {MIN_MATCHES} matches, min. {MIN_AERIALS} aerial duels won | dot size = minutes played',
    transform=ax.transAxes, fontsize=16, color=SUBTITLE_TEXT,
    verticalalignment='bottom',
)

ax.set_xlabel('Aerial Duels Won (total)', fontsize=15, color=TEXT_COLOR, fontweight='bold')
ax.set_ylabel('Aerial Duels Won %', fontsize=15, color=TEXT_COLOR, fontweight='bold')
ax.tick_params(axis='both', labelsize=11, colors=SUBTITLE_TEXT, length=0)
ax.set_xlim(x_min, x_max)
ax.set_ylim(y_min, y_max)
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x:.0f}%'))

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
plt.savefig('images/scatter3.png', dpi=600, bbox_inches='tight', facecolor=BG_COLOR)
plt.show()
