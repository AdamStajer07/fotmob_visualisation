import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import matplotlib.patheffects as pe
import numpy as np
from utils.colors import (BG_COLOR, COLOR_AVG_CLUB, TEXT_COLOR, SUBTITLE_TEXT,
                    COLOR_GRID, COLOR_AVG_LEAGUE, COLOR_RED, COLOR_YELLOW, COLOR_PENALTY)
from utils.club_info import (SEASON, TEAM, EXCLUDED_PLAYERS)

df = pd.read_parquet('data/ekstraklasa_all_clean.parquet')
MIN_MATCHES = 5



legia_players = df[
    (df['team'] == TEAM) &
    (df['tournament'] == 'Ekstraklasa') &
    (df['season'] == SEASON) &
    (df['position'] != 'Keeper')
].copy()
legia_players = legia_players[~legia_players['player_name'].isin(EXCLUDED_PLAYERS)]

legia_players['top_matches_uppercase'] = legia_players['top_matches_uppercase'].fillna(0)
legia_players = legia_players[legia_players['top_matches_uppercase'] >= MIN_MATCHES].copy()

legia_players['yellow_cards'] = legia_players['yellow_cards'].fillna(0)
legia_players['red_cards'] = legia_players['red_cards'].fillna(0)
legia_players['penalty_conceded_title'] = legia_players['penalty_conceded_title'].fillna(0)

legia_players = legia_players[
    (legia_players['yellow_cards'] > 0) |
    (legia_players['red_cards'] > 0) |
    (legia_players['penalty_conceded_title'] > 0)
].copy()

legia_players['total_disciplinary'] = (
    legia_players['yellow_cards'] +
    legia_players['red_cards'] +
    legia_players['penalty_conceded_title']
)
legia_players = legia_players[legia_players['total_disciplinary'] > 1]
legia_players = legia_players.sort_values('total_disciplinary', ascending=False).reset_index(drop=True)

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
all_outfield['yellow_cards'] = all_outfield['yellow_cards'].fillna(0)
all_outfield['red_cards'] = all_outfield['red_cards'].fillna(0)
all_outfield['penalty_conceded_title'] = all_outfield['penalty_conceded_title'].fillna(0)
all_outfield = all_outfield[
    (all_outfield['yellow_cards'] > 0) |
    (all_outfield['red_cards'] > 0) |
    (all_outfield['penalty_conceded_title'] > 0)
]

league_avg_yellow = all_outfield['yellow_cards'].mean()
league_avg_red = all_outfield['red_cards'].mean()
league_avg_penalty = all_outfield['penalty_conceded_title'].mean()
league_avg_total = league_avg_yellow + league_avg_red + league_avg_penalty

club_avg_yellow = legia_players['yellow_cards'].mean()
club_avg_red = legia_players['red_cards'].mean()
club_avg_penalty = legia_players['penalty_conceded_title'].mean()
club_avg_total = club_avg_yellow + club_avg_red + club_avg_penalty

legia_players['_avg_type'] = ''
avg_rows = pd.DataFrame([
    {'short_name': 'League avg', 'yellow_cards': league_avg_yellow,
     'red_cards': league_avg_red, 'penalty_conceded_title': league_avg_penalty,
     'total_disciplinary': league_avg_total, '_avg_type': 'league'},
    {'short_name': 'Club avg', 'yellow_cards': club_avg_yellow,
     'red_cards': club_avg_red, 'penalty_conceded_title': club_avg_penalty,
     'total_disciplinary': club_avg_total, '_avg_type': 'club'},
])
plot_data = pd.concat([legia_players, avg_rows], ignore_index=True)
plot_data = plot_data.sort_values('total_disciplinary', ascending=False).reset_index(drop=True)

plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['Segoe UI', 'Arial', 'Helvetica'],
})

fig, ax = plt.subplots(figsize=(max(14, len(plot_data) * 0.8), 10))

bar_width = 0.65
x = np.arange(len(plot_data))

avg_mask = plot_data['_avg_type'] != ''

for i, (_, row) in enumerate(plot_data.iterrows()):
    is_avg = row['_avg_type'] != ''
    alpha = 1.0 if is_avg else 0.85

    ax.bar(i, row['yellow_cards'], width=bar_width,
           color=COLOR_YELLOW, alpha=alpha, edgecolor=BG_COLOR,
           linewidth=0.5, zorder=3)
    ax.bar(i, row['red_cards'], bottom=row['yellow_cards'], width=bar_width,
           color=COLOR_RED, alpha=alpha, edgecolor=BG_COLOR,
           linewidth=0.5, zorder=3)
    ax.bar(i, row['penalty_conceded_title'],
           bottom=row['yellow_cards'] + row['red_cards'], width=bar_width,
           color=COLOR_PENALTY, alpha=alpha, edgecolor=BG_COLOR,
           linewidth=0.5, zorder=3)

legend_elements = [
    Patch(facecolor=COLOR_YELLOW, alpha=0.7, edgecolor=BG_COLOR, label='Yellow cards'),
    Patch(facecolor=COLOR_RED, alpha=0.7, edgecolor=BG_COLOR, label='Red cards'),
    Patch(facecolor=COLOR_PENALTY, alpha=0.7, edgecolor=BG_COLOR, label='Penalties conceded'),
]

stroke_white = [pe.withStroke(linewidth=3, foreground=BG_COLOR, alpha=0.8)]
stroke_dark = [pe.withStroke(linewidth=3, foreground='#333333', alpha=0.5)]

for i, (_, row) in enumerate(plot_data.iterrows()):
    is_avg = row['_avg_type'] != ''
    bottom = 0

    val = row['yellow_cards']
    if val >= 1:
        label = f'{val:.1f}' if is_avg else str(int(val))
        ax.text(i, bottom + val / 2, label,
                ha='center', va='center', fontsize=10, fontweight='bold', color=TEXT_COLOR,
                path_effects=stroke_white)
    bottom += val

    val = row['red_cards']
    if val >= 1:
        label = f'{val:.1f}' if is_avg else str(int(val))
        ax.text(i, bottom + val / 2, label,
                ha='center', va='center', fontsize=10, fontweight='bold', color='white',
                path_effects=stroke_dark)
    bottom += val

    val = row['penalty_conceded_title']
    if val >= 1:
        label = f'{val:.1f}' if is_avg else str(int(val))
        ax.text(i, bottom + val / 2, label,
                ha='center', va='center', fontsize=10, fontweight='bold', color='white',
                path_effects=stroke_dark)

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
    'LEGIA WARSZAWA — DISCIPLINARY RECORD',
    fontsize=24, fontweight='bold', color=TEXT_COLOR, pad=40, loc='left',
)
ax.text(
    0.0, 1.03,
    f'Ekstraklasa 2025/26 | min. {MIN_MATCHES} matches | stacked: yellows + reds + penalties conceded',
    transform=ax.transAxes, fontsize=16, color=SUBTITLE_TEXT,
    verticalalignment='bottom',
)

ax.tick_params(axis='x', labelsize=12, colors=TEXT_COLOR, length=0)
ax.tick_params(axis='y', labelsize=11, colors=SUBTITLE_TEXT, length=0)

for spine in ax.spines.values():
    spine.set_visible(False)

ax.grid(axis='y', linewidth=0.5, alpha=0.2, color=COLOR_GRID, zorder=0)
ax.set_axisbelow(True)

legend = ax.legend(handles=legend_elements, loc='upper right', fontsize=12,
                   framealpha=0.9, edgecolor=COLOR_GRID, fancybox=True, shadow=False)
legend.get_frame().set_facecolor(BG_COLOR)

fig.patch.set_facecolor(BG_COLOR)
ax.set_facecolor(BG_COLOR)

fig.tight_layout()
fm = plt.get_current_fig_manager()
fm.window.showMaximized()
plt.savefig('images/bar4.png', dpi=600, bbox_inches='tight', facecolor=BG_COLOR)
plt.show()
