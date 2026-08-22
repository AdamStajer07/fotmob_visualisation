import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import matplotlib.patheffects as pe
import numpy as np
from utils.colors import (BG_COLOR, LEGIA_COLOR, LEAGUE_COLOR, TEXT_COLOR, SUBTITLE_TEXT,
                    COLOR_GRID, COLOR_OVERPERFORM, COLOR_UNDERPERFORM,
                    COLOR_AVG_LEAGUE, COLOR_AVG_CLUB)
from utils.club_info import (SEASON, TEAM, EXCLUDED_PLAYERS)

df = pd.read_parquet('data/ekstraklasa_all_clean.parquet')

legia_players = df[
    (df['team'] == TEAM) &
    (df['tournament'] == 'Ekstraklasa') &
    (df['season'] == SEASON) &
    (df['position'] != 'Keeper')
].copy()

legia_players = legia_players[~legia_players['player_name'].isin(EXCLUDED_PLAYERS)]

# xG > 0.5 or min. 1 goal
legia_players = legia_players[
    (legia_players['goals'] >= 1) | (legia_players['expected_goals'] >= 1)
].copy()

legia_players = legia_players.sort_values('goals', ascending=False)
legia_players = legia_players[::-1]

all_outfield = df[
    (df['tournament'] == 'Ekstraklasa') &
    (df['season'] == SEASON) &
    (df['position'] != 'Keeper')
].copy()

all_outfield = all_outfield[
    (all_outfield['goals'] >= 1) | (all_outfield['expected_goals'] >= 1)
]

league_avg_goals = all_outfield['goals'].mean()
league_avg_xg = all_outfield['expected_goals'].mean()

legia_avg_goals = legia_players['goals'].mean()
legia_avg_xg = legia_players['expected_goals'].mean()

avg_rows = pd.DataFrame([
    {'player_name': 'League average', 'goals': league_avg_goals, 'expected_goals': league_avg_xg, 'avg_type': 'league'},
    {'player_name': 'Club average', 'goals': legia_avg_goals, 'expected_goals': legia_avg_xg, 'avg_type': 'club'},
])

legia_players['avg_type'] = ''
plot_data = pd.concat([legia_players, avg_rows], ignore_index=True)
plot_data = plot_data.sort_values('goals', ascending=False)
plot_data = plot_data[::-1].reset_index(drop=True)

plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['Segoe UI', 'Arial', 'Helvetica'],
})

fig, ax = plt.subplots(figsize=(14, max(8, len(plot_data) * 0.5 + 2)))

for _, row in plot_data.iterrows():
    goals = row['goals'] if pd.notna(row['goals']) else 0
    xg = row['expected_goals'] if pd.notna(row['expected_goals']) else 0
    diff = goals - xg
    is_avg = row['avg_type']

    if is_avg == 'league':
        line_color = COLOR_AVG_LEAGUE
        dot_goals_color = COLOR_AVG_LEAGUE
        dot_xg_color = COLOR_AVG_LEAGUE
        name_color = COLOR_AVG_LEAGUE
        val_color = COLOR_AVG_LEAGUE
        line_alpha = 0.8
        linewidth = 3.0
    elif is_avg == 'club':
        line_color = COLOR_AVG_CLUB
        dot_goals_color = COLOR_AVG_CLUB
        dot_xg_color = COLOR_AVG_CLUB
        name_color = COLOR_AVG_CLUB
        val_color = COLOR_AVG_CLUB
        line_alpha = 0.8
        linewidth = 3.0
    else:
        line_color = COLOR_OVERPERFORM if diff > 0 else COLOR_UNDERPERFORM
        dot_goals_color = LEGIA_COLOR
        dot_xg_color = LEAGUE_COLOR
        name_color = TEXT_COLOR
        val_color = LEGIA_COLOR
        line_alpha = 0.6
        linewidth = 2.5

    ax.plot(
        [goals, xg],
        [row['player_name'], row['player_name']],
        color=line_color,
        linewidth=linewidth,
        alpha=line_alpha,
        solid_capstyle='round',
        zorder=1,
    )

    ax.scatter(goals, row['player_name'], color=dot_goals_color, s=70, zorder=3,
               edgecolors=BG_COLOR, linewidths=1.5)
    ax.scatter(xg, row['player_name'], color=dot_xg_color, s=70, zorder=3,
               edgecolors=BG_COLOR, linewidths=1.5)

    goals_label = f"{goals:.1f}" if is_avg else str(int(goals))
    xg_label = f"{xg:.1f}" if is_avg else ""

    if diff >= 0:
        ax.text(
            goals + 0.2, row['player_name'],
            s=goals_label,
            fontsize=13, fontweight='bold', color=val_color,
            verticalalignment='center',
        )
        ax.text(
            xg - 0.2, row['player_name'],
            s=row['player_name'],
            fontsize=13, fontweight='bold', color=name_color,
            verticalalignment='center', horizontalalignment='right',
        )
    else:
        ax.text(
            goals - 0.3, row['player_name'],
            s=goals_label,
            fontsize=13, fontweight='bold', color=val_color,
            verticalalignment='center',
        )
        ax.text(
            xg + 0.2, row['player_name'],
            s=row['player_name'],
            fontsize=13, fontweight='bold', color=name_color,
            verticalalignment='center', horizontalalignment='left',
        )

    if abs(diff) >= 0.25:
        sign = '+' if diff > 0 else ''
        diff_label = f"{sign}{diff:.1f}"
        ax.text(
            (goals + xg) / 2,
            row['player_name'],
            s=diff_label,
            fontsize=11, fontweight='bold', color=line_color,
            horizontalalignment='center',
            verticalalignment='bottom',
            path_effects=[
                pe.withStroke(linewidth=2, foreground=BG_COLOR, alpha=0.9),
            ],
        )

ax.set_title(
    'LEGIA WARSZAWA — Goals vs xG',
    fontsize=24, fontweight='bold', color=TEXT_COLOR, pad=30, loc='left',
)
ax.text(
    0.0, 1.02, 'Ekstraklasa 2025/26 | overperformance in green, underperformance in red',
    transform=ax.transAxes, fontsize=16, color=SUBTITLE_TEXT,
    verticalalignment='bottom',
)

ax.tick_params(axis='x', labelsize=12, colors=SUBTITLE_TEXT, length=0)
max_val = max(plot_data['goals'].max(), plot_data['expected_goals'].max())
ax.set_xticks(np.arange(0, int(max_val) + 2, 1))
ax.set_xlabel('', visible=False)
ax.get_yaxis().set_visible(False)

for spine in ax.spines.values():
    spine.set_visible(False)

ax.axhline(y=-0.5, color=COLOR_GRID, linewidth=1, alpha=0.5)

ax.grid(axis='x', linewidth=0.6, alpha=0.3, color=COLOR_GRID, zorder=0)
ax.set_axisbelow(True)

legend_elements = [
    Line2D([0], [0], marker='o', color='w', markerfacecolor=LEGIA_COLOR,
           markersize=10, markeredgecolor=BG_COLOR, markeredgewidth=1.2, label='Goals'),
    Line2D([0], [0], marker='o', color='w', markerfacecolor=LEAGUE_COLOR,
           markersize=10, markeredgecolor=BG_COLOR, markeredgewidth=1.2, label='xG'),
    Line2D([0], [0], color=COLOR_OVERPERFORM, linewidth=3, alpha=0.6, label='Overperformance'),
    Line2D([0], [0], color=COLOR_UNDERPERFORM, linewidth=3, alpha=0.6, label='Underperformance'),
    Line2D([0], [0], color=COLOR_AVG_CLUB, linewidth=3, alpha=0.8, label='Club average'),
    Line2D([0], [0], color=COLOR_AVG_LEAGUE, linewidth=3, alpha=0.8, label='League average'),
]
legend = ax.legend(
    handles=legend_elements, loc='lower right',
    fontsize=13, framealpha=0.9, edgecolor=COLOR_GRID,
    fancybox=True, shadow=False,
)
legend.get_frame().set_facecolor(BG_COLOR)

fig.patch.set_facecolor(BG_COLOR)
ax.set_facecolor(BG_COLOR)

ax.margins(x=0.05, y=0.02)

fig.tight_layout()

fm = plt.get_current_fig_manager()
fm.window.showMaximized()
plt.savefig('images/dumbbell1.png', dpi=600, bbox_inches='tight', facecolor=BG_COLOR)
plt.show()
