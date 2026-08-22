import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from utils.colors import (BG_COLOR, LEGIA_COLOR, COLOR_AVG_CLUB, TEXT_COLOR, SUBTITLE_TEXT,
                    COLOR_GRID, COLOR_AVG_LEAGUE, LEAGUE_COLOR)
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

legia_players['fouls'] = legia_players['fouls'].fillna(0)
legia_players['fouls_won'] = legia_players['fouls_won'].fillna(0)

legia_players = legia_players[
    (legia_players['fouls'] > 0) | (legia_players['fouls_won'] > 0)
].copy()

legia_players['foul_balance'] = legia_players['fouls_won'] - legia_players['fouls']
legia_players['foul_total'] = legia_players['fouls'] + legia_players['fouls_won']
legia_players = legia_players.sort_values(
    ['foul_total', 'foul_balance'], ascending=[True, True]
).reset_index(drop=True)

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
all_outfield['fouls'] = all_outfield['fouls'].fillna(0)
all_outfield['fouls_won'] = all_outfield['fouls_won'].fillna(0)
all_outfield = all_outfield[(all_outfield['fouls'] > 0) | (all_outfield['fouls_won'] > 0)]

league_avg_fouls = all_outfield['fouls'].mean()
league_avg_fouls_won = all_outfield['fouls_won'].mean()
club_avg_fouls = legia_players['fouls'].mean()
club_avg_fouls_won = legia_players['fouls_won'].mean()

legia_players['_avg_type'] = ''
avg_rows = pd.DataFrame([
    {'short_name': 'League average', 'fouls': league_avg_fouls, 'fouls_won': league_avg_fouls_won,
     'foul_balance': league_avg_fouls_won - league_avg_fouls, '_avg_type': 'league'},
    {'short_name': 'Club average', 'fouls': club_avg_fouls, 'fouls_won': club_avg_fouls_won,
     'foul_balance': club_avg_fouls_won - club_avg_fouls, '_avg_type': 'club'},
])
plot_data = pd.concat([legia_players, avg_rows], ignore_index=True)
plot_data['foul_total'] = plot_data['foul_total'].fillna(plot_data['fouls'] + plot_data['fouls_won'])
plot_data = plot_data.sort_values(
    ['foul_total', 'foul_balance'], ascending=[True, True]
).reset_index(drop=True)

plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['Segoe UI', 'Arial', 'Helvetica'],
})

fig, ax = plt.subplots(figsize=(14, max(8, len(plot_data) * 0.5)))

bar_height = 0.7

for i, (_, row) in enumerate(plot_data.iterrows()):
    avg_type = row.get('_avg_type', '')
    if avg_type == 'league':
        color_left = COLOR_AVG_LEAGUE
        color_right = COLOR_AVG_LEAGUE
    elif avg_type == 'club':
        color_left = COLOR_AVG_CLUB
        color_right = COLOR_AVG_CLUB
    else:
        color_left = LEAGUE_COLOR
        color_right = LEGIA_COLOR

    ax.barh(i, -row['fouls'], height=bar_height, color=color_left,
            alpha=0.8, edgecolor=BG_COLOR, linewidth=0.5, zorder=3)
    ax.barh(i, row['fouls_won'], height=bar_height, color=color_right,
            alpha=0.8, edgecolor=BG_COLOR, linewidth=0.5, zorder=3)

ax.set_yticks(range(len(plot_data)))
ax.set_yticklabels(plot_data['short_name'])

for i, (_, row) in enumerate(plot_data.iterrows()):
    avg_type = row.get('_avg_type', '')
    is_avg = avg_type != ''

    if avg_type == 'league':
        color_left = COLOR_AVG_LEAGUE
        color_right = COLOR_AVG_LEAGUE
        balance_color = COLOR_AVG_LEAGUE
    elif avg_type == 'club':
        color_left = COLOR_AVG_CLUB
        color_right = COLOR_AVG_CLUB
        balance_color = COLOR_AVG_CLUB
    else:
        color_left = LEAGUE_COLOR
        color_right = LEGIA_COLOR
        balance = int(row['foul_balance'])
        balance_color = LEGIA_COLOR if balance > 0 else LEAGUE_COLOR if balance < 0 else SUBTITLE_TEXT

    if row['fouls'] > 0:
        label_left = f"{row['fouls']:.1f}" if is_avg else str(int(row['fouls']))
        ax.text(-row['fouls'] - 0.3, i, label_left,
                va='center', ha='right', fontsize=11, fontweight='bold', color=color_left)
    if row['fouls_won'] > 0:
        label_right = f"{row['fouls_won']:.1f}" if is_avg else str(int(row['fouls_won']))
        ax.text(row['fouls_won'] + 0.3, i, label_right,
                va='center', ha='left', fontsize=11, fontweight='bold', color=color_right)

ytick_labels = ax.get_yticklabels()
for label in ytick_labels:
    txt = label.get_text()
    if txt == 'League average':
        label.set_color(COLOR_AVG_LEAGUE)
        label.set_fontweight('bold')
    elif txt == 'Club average':
        label.set_color(COLOR_AVG_CLUB)
        label.set_fontweight('bold')

ax.axvline(x=0, color=TEXT_COLOR, linewidth=1.2, alpha=0.4, zorder=2)

ax.set_title(
    'LEGIA WARSZAWA — FOULS COMMITTED vs FOULS WON',
    fontsize=24, fontweight='bold', color=TEXT_COLOR, pad=30, loc='left',
)
ax.text(
    0.0, 1.02,
    f'Ekstraklasa 2025/26 | min. {MIN_MATCHES} matches | sorted by total fouls, then balance',
    transform=ax.transAxes, fontsize=16, color=SUBTITLE_TEXT,
    verticalalignment='bottom',
)

max_val = max(plot_data['fouls'].max(), plot_data['fouls_won'].max())
ticks = np.arange(-int(max_val) - 2, int(max_val) + 3, 5)
ax.set_xticks(ticks)
ax.set_xticklabels([str(abs(int(t))) for t in ticks])

ax.text(0.25, -0.04, '← Fouls committed',
        transform=ax.transAxes, fontsize=13, color=LEAGUE_COLOR,
        fontweight='bold', ha='center', va='top')
ax.text(0.75, -0.04, 'Fouls won →',
        transform=ax.transAxes, fontsize=13, color=LEGIA_COLOR,
        fontweight='bold', ha='center', va='top')

ax.tick_params(axis='y', labelsize=13, colors=TEXT_COLOR, length=0)
ax.tick_params(axis='x', labelsize=11, colors=SUBTITLE_TEXT, length=0)

for spine in ax.spines.values():
    spine.set_visible(False)

ax.grid(axis='x', linewidth=0.5, alpha=0.2, color=COLOR_GRID, zorder=0)
ax.set_axisbelow(True)

fig.patch.set_facecolor(BG_COLOR)
ax.set_facecolor(BG_COLOR)

fig.tight_layout()
fm = plt.get_current_fig_manager()
fm.window.showMaximized()
plt.savefig('images/bar3.png', dpi=600, bbox_inches='tight', facecolor=BG_COLOR)
plt.show()
