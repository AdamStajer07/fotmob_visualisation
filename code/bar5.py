import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import numpy as np
from utils.colors import (BG_COLOR, COLOR_AVG_CLUB, TEXT_COLOR, SUBTITLE_TEXT,
                    COLOR_GRID, COLOR_AVG_LEAGUE, COLOR_TACKLES, COLOR_INTERCEPT)
from utils.club_info import (SEASON, TEAM, EXCLUDED_PLAYERS)

df = pd.read_parquet('data/ekstraklasa_all_clean.parquet')

MIN_MATCHES = 5
MIN_TOTAL = 20

COL_TACKLES = 'matchstats.headers.tackles'
COL_INTERCEPT = 'interceptions'



legia_players = df[
    (df['team'] == TEAM) &
    (df['tournament'] == 'Ekstraklasa') &
    (df['season'] == SEASON) &
    (df['position'] != 'Keeper')
].copy()
legia_players = legia_players[~legia_players['player_name'].isin(EXCLUDED_PLAYERS)]

legia_players['top_matches_uppercase'] = legia_players['top_matches_uppercase'].fillna(0)
legia_players = legia_players[legia_players['top_matches_uppercase'] >= MIN_MATCHES].copy()

legia_players[COL_TACKLES] = legia_players[COL_TACKLES].fillna(0)
legia_players[COL_INTERCEPT] = legia_players[COL_INTERCEPT].fillna(0)
legia_players['total_def'] = legia_players[COL_TACKLES] + legia_players[COL_INTERCEPT]

legia_players = legia_players[legia_players['total_def'] >= MIN_TOTAL].copy()
legia_players = legia_players.sort_values('total_def', ascending=False).reset_index(drop=True)

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
all_outfield[COL_TACKLES] = all_outfield[COL_TACKLES].fillna(0)
all_outfield[COL_INTERCEPT] = all_outfield[COL_INTERCEPT].fillna(0)
all_outfield['total_def'] = all_outfield[COL_TACKLES] + all_outfield[COL_INTERCEPT]
all_outfield = all_outfield[all_outfield['total_def'] >= MIN_TOTAL]

league_avg_tackles = all_outfield[COL_TACKLES].mean()
league_avg_intercept = all_outfield[COL_INTERCEPT].mean()
league_avg_total = league_avg_tackles + league_avg_intercept

club_avg_tackles = legia_players[COL_TACKLES].mean()
club_avg_intercept = legia_players[COL_INTERCEPT].mean()
club_avg_total = club_avg_tackles + club_avg_intercept

legia_players['_avg_type'] = ''
avg_rows = pd.DataFrame([
    {'short_name': 'League avg', COL_TACKLES: league_avg_tackles,
     COL_INTERCEPT: league_avg_intercept, 'total_def': league_avg_total, '_avg_type': 'league'},
    {'short_name': 'Club avg', COL_TACKLES: club_avg_tackles,
     COL_INTERCEPT: club_avg_intercept, 'total_def': club_avg_total, '_avg_type': 'club'},
])
plot_data = pd.concat([legia_players, avg_rows], ignore_index=True)
plot_data = plot_data.sort_values('total_def', ascending=False).reset_index(drop=True)

plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['Segoe UI', 'Arial', 'Helvetica'],
})

fig, ax = plt.subplots(figsize=(max(14, len(plot_data) * 0.9), 10))

bar_width = 0.35
x = np.arange(len(plot_data))

for i, (_, row) in enumerate(plot_data.iterrows()):
    avg_type = row.get('_avg_type', '')

    if avg_type == 'league':
        c_tackles = COLOR_AVG_LEAGUE
        c_intercept = COLOR_AVG_LEAGUE
        alpha = 0.7
    elif avg_type == 'club':
        c_tackles = COLOR_AVG_CLUB
        c_intercept = COLOR_AVG_CLUB
        alpha = 0.7
    else:
        c_tackles = COLOR_TACKLES
        c_intercept = COLOR_INTERCEPT
        alpha = 0.85

    ax.bar(i - bar_width / 2, row[COL_TACKLES], width=bar_width,
           color=c_tackles, alpha=alpha, edgecolor=BG_COLOR, linewidth=0.5, zorder=3)
    ax.bar(i + bar_width / 2, row[COL_INTERCEPT], width=bar_width,
           color=c_intercept, alpha=alpha, edgecolor=BG_COLOR, linewidth=0.5, zorder=3)

    is_avg = avg_type != ''
    t_val = row[COL_TACKLES]
    i_val = row[COL_INTERCEPT]
    t_label = f'{t_val:.1f}' if is_avg else str(int(t_val))
    i_label = f'{i_val:.1f}' if is_avg else str(int(i_val))

    ax.text(i - bar_width / 2, t_val + 0.3, t_label,
            ha='center', va='bottom', fontsize=10, fontweight='bold',
            color=c_tackles if is_avg else TEXT_COLOR)
    ax.text(i + bar_width / 2, i_val + 0.3, i_label,
            ha='center', va='bottom', fontsize=10, fontweight='bold',
            color=c_intercept if is_avg else TEXT_COLOR)

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
    'LEGIA WARSZAWA — TACKLES & INTERCEPTIONS',
    fontsize=24, fontweight='bold', color=TEXT_COLOR, pad=40, loc='left',
)
ax.text(
    0.0, 1.03,
    f'Ekstraklasa 2025/26 | min. {MIN_MATCHES} matches, min. {MIN_TOTAL} combined | sorted by total',
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
    Patch(facecolor=COLOR_TACKLES, alpha=0.85, edgecolor=BG_COLOR, label='Tackles'),
    Patch(facecolor=COLOR_INTERCEPT, alpha=0.85, edgecolor=BG_COLOR, label='Interceptions'),
]
legend = ax.legend(handles=legend_elements, loc='upper right', fontsize=12,
                   framealpha=0.9, edgecolor=COLOR_GRID, fancybox=True, shadow=False)
legend.get_frame().set_facecolor(BG_COLOR)

fig.patch.set_facecolor(BG_COLOR)
ax.set_facecolor(BG_COLOR)

fig.tight_layout()
fm = plt.get_current_fig_manager()
fm.window.showMaximized()
plt.savefig('images/bar5.png', dpi=600, bbox_inches='tight', facecolor=BG_COLOR)
plt.show()
