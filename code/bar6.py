import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import matplotlib.patheffects as pe
import numpy as np
from utils.colors import (BG_COLOR, COLOR_AVG_CLUB, TEXT_COLOR, SUBTITLE_TEXT,
                    COLOR_GRID, COLOR_AVG_LEAGUE, COLOR_ACCURATE, COLOR_INACCURATE)
from utils.club_info import (SEASON, TEAM, EXCLUDED_PLAYERS)

df = pd.read_parquet('data/ekstraklasa_all_clean.parquet')

MIN_MATCHES = 5
MIN_LONG_BALLS = 14 

COL_ACCURATE = 'long_balls_accurate'
COL_ACCURACY = 'long_ball_succeeeded_accuracy'



legia_players = df[
    (df['team'] == TEAM) &
    (df['tournament'] == 'Ekstraklasa') &
    (df['season'] == SEASON) &
    (df['position'] != 'Keeper')
].copy()
legia_players = legia_players[~legia_players['player_name'].isin(EXCLUDED_PLAYERS)]

legia_players['top_matches_uppercase'] = legia_players['top_matches_uppercase'].fillna(0)
legia_players = legia_players[legia_players['top_matches_uppercase'] >= MIN_MATCHES].copy()

legia_players[COL_ACCURATE] = legia_players[COL_ACCURATE].fillna(0)
legia_players[COL_ACCURACY] = legia_players[COL_ACCURACY].fillna(0)

legia_players['long_balls_total'] = legia_players.apply(
    lambda r: round(r[COL_ACCURATE] / (r[COL_ACCURACY] / 100)) if r[COL_ACCURACY] > 0 else 0,
    axis=1
)
legia_players['long_balls_inaccurate'] = legia_players['long_balls_total'] - legia_players[COL_ACCURATE]

legia_players = legia_players[legia_players[COL_ACCURATE] >= MIN_LONG_BALLS].copy()
legia_players = legia_players.sort_values(COL_ACCURATE, ascending=False).reset_index(drop=True)

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

all_outfield = df[
    (df['tournament'] == 'Ekstraklasa') &
    (df['season'] == SEASON) &
    (df['position'] != 'Keeper')
].copy()

all_outfield['top_matches_uppercase'] = all_outfield['top_matches_uppercase'].fillna(0)
all_outfield = all_outfield[all_outfield['top_matches_uppercase'] >= MIN_MATCHES].copy()
all_outfield[COL_ACCURATE] = all_outfield[COL_ACCURATE].fillna(0)
all_outfield[COL_ACCURACY] = all_outfield[COL_ACCURACY].fillna(0)
all_outfield['long_balls_total'] = all_outfield.apply(
    lambda r: round(r[COL_ACCURATE] / (r[COL_ACCURACY] / 100)) if r[COL_ACCURACY] > 0 else 0,
    axis=1
)
all_outfield['long_balls_inaccurate'] = all_outfield['long_balls_total'] - all_outfield[COL_ACCURATE]
all_outfield = all_outfield[all_outfield[COL_ACCURATE] >= MIN_LONG_BALLS]

league_avg_accurate = all_outfield[COL_ACCURATE].mean()
league_avg_total = all_outfield['long_balls_total'].mean()
league_avg_inaccurate = league_avg_total - league_avg_accurate
league_avg_accuracy = (league_avg_accurate / league_avg_total * 100) if league_avg_total > 0 else 0

club_avg_accurate = legia_players[COL_ACCURATE].mean()
club_avg_total = legia_players['long_balls_total'].mean()
club_avg_inaccurate = club_avg_total - club_avg_accurate
club_avg_accuracy = (club_avg_accurate / club_avg_total * 100) if club_avg_total > 0 else 0

legia_players['_avg_type'] = ''
avg_rows = pd.DataFrame([
    {'short_name': 'League avg', COL_ACCURATE: league_avg_accurate,
     'long_balls_inaccurate': league_avg_inaccurate, 'long_balls_total': league_avg_total,
     COL_ACCURACY: league_avg_accuracy, '_avg_type': 'league'},
    {'short_name': 'Club avg', COL_ACCURATE: club_avg_accurate,
     'long_balls_inaccurate': club_avg_inaccurate, 'long_balls_total': club_avg_total,
     COL_ACCURACY: club_avg_accuracy, '_avg_type': 'club'},
])
plot_data = pd.concat([legia_players, avg_rows], ignore_index=True)
plot_data = plot_data.sort_values(COL_ACCURATE, ascending=False).reset_index(drop=True)

plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['Segoe UI', 'Arial', 'Helvetica'],
})

fig, ax = plt.subplots(figsize=(max(14, len(plot_data) * 0.9), 10))

bar_width = 0.65
x = np.arange(len(plot_data))

stroke = [pe.withStroke(linewidth=3, foreground=BG_COLOR, alpha=0.8)]

for i, (_, row) in enumerate(plot_data.iterrows()):
    avg_type = row.get('_avg_type', '')
    accurate = row[COL_ACCURATE]
    inaccurate = row['long_balls_inaccurate']
    total = row['long_balls_total']
    accuracy = row[COL_ACCURACY]

    if avg_type == 'league':
        c_accurate = COLOR_AVG_LEAGUE
        c_inaccurate = '#a8c4da'
        alpha = 0.8
    elif avg_type == 'club':
        c_accurate = COLOR_AVG_CLUB
        c_inaccurate = '#8fadc5'
        alpha = 0.8
    else:
        c_accurate = COLOR_ACCURATE
        c_inaccurate = COLOR_INACCURATE
        alpha = 0.85

    ax.bar(i, accurate, width=bar_width,
           color=c_accurate, alpha=alpha, edgecolor=BG_COLOR, linewidth=0.5, zorder=3)
    ax.bar(i, inaccurate, bottom=accurate, width=bar_width,
           color=c_inaccurate, alpha=0.5, edgecolor=BG_COLOR, linewidth=0.5, zorder=3)

    is_avg = avg_type != ''
    pct_label = f'{accuracy:.1f}%'
    ax.text(i, total + 1, pct_label,
            ha='center', va='bottom', fontsize=11, fontweight='bold',
            color=c_accurate if is_avg else TEXT_COLOR,
            path_effects=stroke if not is_avg else [])

    if accurate >= 5:
        acc_label = f'{accurate:.0f}' if is_avg else str(int(accurate))
        ax.text(i, accurate / 2, acc_label,
                ha='center', va='center', fontsize=10, fontweight='bold',
                color='white', path_effects=[pe.withStroke(linewidth=3, foreground=c_accurate, alpha=0.6)])

    if inaccurate >= 5:
        inacc_label = f'{inaccurate:.0f}' if is_avg else str(int(inaccurate))
        ax.text(i, accurate + inaccurate / 2, inacc_label,
                ha='center', va='center', fontsize=10, fontweight='bold',
                color=TEXT_COLOR, alpha=0.8,
                path_effects=[pe.withStroke(linewidth=3, foreground=c_inaccurate, alpha=0.6)])

ax.set_xticks(x)
ax.set_xticklabels(plot_data['short_name'], rotation=45, ha='right')

xtick_labels = ax.get_xticklabels()
for label in xtick_labels:
    txt = label.get_text()
    if txt == 'League avg':
        label.set_color(COLOR_AVG_LEAGUE)
        label.set_fontweight('bold')
    elif txt == 'Club avg':
        label.set_color(COLOR_AVG_CLUB)
        label.set_fontweight('bold')

ax.set_title(
    'LEGIA WARSZAWA — ACCURATE LONG BALLS',
    fontsize=24, fontweight='bold', color=TEXT_COLOR, pad=40, loc='left',
)
ax.text(
    0.0, 1.03,
    f'Ekstraklasa 2025/26 | min. {MIN_MATCHES} matches, min. {MIN_LONG_BALLS} accurate long balls | sorted by accurate count',
    transform=ax.transAxes, fontsize=16, color=SUBTITLE_TEXT,
    verticalalignment='bottom',
)

ax.tick_params(axis='x', labelsize=12, colors=TEXT_COLOR, length=0)
ax.tick_params(axis='y', labelsize=11, colors=SUBTITLE_TEXT, length=0)

for spine in ax.spines.values():
    spine.set_visible(False)

ax.grid(axis='y', linewidth=0.5, alpha=0.2, color=COLOR_GRID, zorder=0)
ax.set_axisbelow(True)

legend_elements = [
    Patch(facecolor=COLOR_ACCURATE, alpha=0.85, edgecolor=BG_COLOR, label='Accurate long balls'),
    Patch(facecolor=COLOR_INACCURATE, alpha=0.5, edgecolor=BG_COLOR, label='Inaccurate long balls'),
]
legend = ax.legend(handles=legend_elements, loc='upper right', fontsize=12,
                   framealpha=0.9, edgecolor=COLOR_GRID, fancybox=True, shadow=False)
legend.get_frame().set_facecolor(BG_COLOR)

fig.patch.set_facecolor(BG_COLOR)
ax.set_facecolor(BG_COLOR)

fig.tight_layout()
fm = plt.get_current_fig_manager()
fm.window.showMaximized()
plt.savefig('images/bar6.png', dpi=600, bbox_inches='tight', facecolor=BG_COLOR)
plt.show()
