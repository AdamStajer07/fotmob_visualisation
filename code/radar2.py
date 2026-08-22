import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from utils.colors import (BG_COLOR, LEGIA_COLOR, LEAGUE_COLOR, TEXT_COLOR, SUBTLE_TEXT,
                    RING_COLOR_1, RING_COLOR_2, RING_EDGE)
from utils.club_info import (SEASON)
from mplsoccer import Radar
df = pd.read_parquet('data/ekstraklasa_all_clean.parquet')

SEASON = '2025/2026'
PLAYER1 = 'Ottó Hindrich'
PLAYER2 = 'Kacper Tobiasz'

COLOR_TOBIASZ = '#e67e22'

hindrich = df[
    (df['player_name'] == PLAYER1) &
    (df['tournament'] == 'Ekstraklasa') &
    (df['season'] == SEASON)
].iloc[0]

tobiasz = df[
    (df['player_name'] == PLAYER2) &
    (df['tournament'] == 'Ekstraklasa') &
    (df['season'] == SEASON)
].iloc[0]

stat_cols = [
    'saves_per90',
    'save_percentage_per90',
    'goals_conceded_per90',
    'goals_prevented_per90',
    'clean_sheet_team_title_per90',
    'keeper_sweeper_per90',
    'keeper_high_claim_per90',
    'long_ball_succeeeded_accuracy_per90',
    'successful_passes_per90',
    'error_led_to_goal_per90',
]

params = [
    'Saves\n/90',
    'Save %',
    'Goals conceded\n/90 (fewer=better)',
    'Goals\nprevented /90',
    'Clean sheets\n/90',
    'Sweeper\nactions /90 (fewer=better)',
    'High\nclaims /90',
    'Long ball\naccuracy %',
    'Passes\n/90',
    'Errors to goal\n/90 (fewer=better)',
]

INVERT = [False, False, True, False, False, True, False, False, False, True]

keepers = df[
    (df['tournament'] == 'Ekstraklasa') &
    (df['season'] == SEASON) &
    (df['position'] == 'Keeper') &
    (df['top_matches_uppercase'] >= 5)
].copy()

low = np.array([keepers[col].min() for col in stat_cols])
high = np.array([keepers[col].max() for col in stat_cols])

hindrich_values = np.array([hindrich[col] if pd.notna(hindrich[col]) else 0 for col in stat_cols])
tobiasz_values = np.array([tobiasz[col] if pd.notna(tobiasz[col]) else 0 for col in stat_cols])
mean_values = np.array([keepers[col].mean() for col in stat_cols])

lower_is_better_params = [params[i] for i, inv in enumerate(INVERT) if inv]

plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['Segoe UI', 'Arial', 'Helvetica'],
})

radar = Radar(
    params, low, high,
    lower_is_better=lower_is_better_params,
    num_rings=5,
    ring_width=1,
    center_circle_radius=1,
)

fig, ax = radar.setup_axis(facecolor=BG_COLOR, figsize=(10, 10))
fig.patch.set_facecolor(BG_COLOR)

rings_inner = radar.draw_circles(
    ax=ax, inner=True,
    facecolor=RING_COLOR_1, edgecolor=RING_EDGE, linewidth=0.8,
)
rings_outer = radar.draw_circles(
    ax=ax, inner=False,
    facecolor=RING_COLOR_2, edgecolor=RING_EDGE, linewidth=0.8,
)

radar1, radar2, vertices1, vertices2 = radar.draw_radar_compare(
    hindrich_values, tobiasz_values, ax=ax,
    kwargs_radar={'facecolor': LEGIA_COLOR, 'alpha': 0.45, 'edgecolor': LEGIA_COLOR, 'linewidth': 2.5},
    kwargs_compare={'facecolor': COLOR_TOBIASZ, 'alpha': 0.35, 'edgecolor': COLOR_TOBIASZ, 'linewidth': 2.5},
)

radar3, rings3, vertices3 = radar.draw_radar(
    mean_values, ax=ax,
    kwargs_radar={'facecolor': 'none', 'edgecolor': LEAGUE_COLOR, 'linewidth': 1.5, 'linestyle': '--', 'alpha': 0.7},
    kwargs_rings={'facecolor': 'none', 'edgecolor': 'none'},
)

ax.scatter(
    vertices1[:, 0], vertices1[:, 1],
    c=LEGIA_COLOR, edgecolors=BG_COLOR, linewidths=1.5,
    s=70, zorder=5,
)
ax.scatter(
    vertices2[:, 0], vertices2[:, 1],
    c=COLOR_TOBIASZ, edgecolors=BG_COLOR, linewidths=1.5,
    s=70, zorder=5,
)
ax.scatter(
    vertices3[:, 0], vertices3[:, 1],
    c=LEAGUE_COLOR, edgecolors=BG_COLOR, linewidths=1.5,
    s=50, zorder=3,
)

param_labels = radar.draw_param_labels(
    ax=ax, fontsize=13, color=TEXT_COLOR, fontweight='bold', offset=2.5,
)

range_labels = radar.draw_range_labels(
    ax=ax, fontsize=10, color=SUBTLE_TEXT, alpha=0.7,
)

fig.text(
    0.5, 0.95,
    'HINDRICH vs TOBIASZ — GOALKEEPER COMPARISON',
    ha='center', va='center',
    fontsize=24, fontweight='bold', color=TEXT_COLOR,
    fontfamily='sans-serif',
)
fig.text(
    0.5, 0.91,
    'Ekstraklasa 2025/26 | per 90 min | range based on league keepers (min. 5 matches)',
    ha='center', va='center',
    fontsize=16, color=SUBTLE_TEXT,
    fontfamily='sans-serif',
)

legend_y = 0.06
fig.patches.append(plt.Rectangle((0.18, legend_y), 0.025, 0.018,
                                  facecolor=LEGIA_COLOR, alpha=0.7,
                                  transform=fig.transFigure, zorder=10))
fig.text(0.215, legend_y + 0.007, 'Ottó Hindrich', fontsize=13,
         color=TEXT_COLOR, va='center', fontfamily='sans-serif')

fig.patches.append(plt.Rectangle((0.40, legend_y), 0.025, 0.018,
                                  facecolor=COLOR_TOBIASZ, alpha=0.7,
                                  transform=fig.transFigure, zorder=10))
fig.text(0.435, legend_y + 0.007, 'Kacper Tobiasz', fontsize=13,
         color=TEXT_COLOR, va='center', fontfamily='sans-serif')

fig.patches.append(plt.Rectangle((0.62, legend_y), 0.025, 0.018,
                                  facecolor=LEAGUE_COLOR, alpha=0.4,
                                  transform=fig.transFigure, zorder=10))
fig.text(0.655, legend_y + 0.007, 'League keepers avg', fontsize=13,
         color=TEXT_COLOR, va='center', fontfamily='sans-serif')

for i, ((x1, y1), (x2, y2)) in enumerate(zip(vertices1, vertices2)):
    val1 = hindrich_values[i]
    label1 = f"{val1:.1f}" if val1 != int(val1) else f"{int(val1)}"
    ax.annotate(
        label1, (x1, y1),
        textcoords="offset points", xytext=(0, 10),
        ha='center', va='bottom',
        fontsize=9, fontweight='bold', color='white',
        bbox=dict(boxstyle='round,pad=0.15', facecolor=LEGIA_COLOR, alpha=0.85, edgecolor='none'),
    )
    val2 = tobiasz_values[i]
    label2 = f"{val2:.1f}" if val2 != int(val2) else f"{int(val2)}"
    ax.annotate(
        label2, (x2, y2),
        textcoords="offset points", xytext=(0, -12),
        ha='center', va='top',
        fontsize=9, fontweight='bold', color='white',
        bbox=dict(boxstyle='round,pad=0.15', facecolor=COLOR_TOBIASZ, alpha=0.85, edgecolor='none'),
    )

plt.tight_layout(rect=[0, 0.08, 1, 0.88])
plt.savefig('images/radar2.png', dpi=600, bbox_inches='tight', facecolor=BG_COLOR)
plt.show()
