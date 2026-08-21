import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from mplsoccer import Radar
from utils.colors import (BG_COLOR, LEGIA_COLOR, LEAGUE_COLOR, TEXT_COLOR, SUBTLE_TEXT,
                    RING_COLOR_1, RING_COLOR_2, RING_EDGE)     

df = pd.read_parquet('data/team_stats.parquet')

legia = df[df['team_name'] == 'Legia Warszawa'].iloc[0]

stat_cols = [
    'expected_goals_team',
    'ontarget_scoring_att_team',
    'touches_in_opp_box_team',
    'big_chance_team',
    'big_chance_missed_team',
    '_set_piece_goals_team',
]

params = [
    'xG\n(season)',
    'Shots on target\n/ match',
    'Touches in\nopp. box',
    'Big chances\ncreated',
    'Big chances\nmissed',
    'Set piece\ngoals',
]

low = np.array([df[col].min() for col in stat_cols])
high = np.array([df[col].max() for col in stat_cols])
mean_values = np.array([df[col].mean() for col in stat_cols])
legia_values = np.array([legia[col] for col in stat_cols])

radar = Radar(
    params, low, high,
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
    legia_values, mean_values, ax=ax,
    kwargs_radar={'facecolor': LEGIA_COLOR, 'alpha': 0.55, 'edgecolor': LEGIA_COLOR, 'linewidth': 2.5},
    kwargs_compare={'facecolor': LEAGUE_COLOR, 'alpha': 0.3, 'edgecolor': LEAGUE_COLOR, 'linewidth': 1.5, 'linestyle': '--'},
)

ax.scatter(
    vertices1[:, 0], vertices1[:, 1],
    c=LEGIA_COLOR, edgecolors=BG_COLOR, linewidths=1.5,
    s=80, zorder=5,
)

param_labels = radar.draw_param_labels(
    ax=ax, fontsize=11, color=TEXT_COLOR, fontweight='bold', offset=2.5,
)

range_labels = radar.draw_range_labels(
    ax=ax, fontsize=8, color=SUBTLE_TEXT, alpha=0.7,
)

fig.text(
    0.5, 0.95,
    'LEGIA WARSZAWA — OFFENSIVE PROFILE',
    ha='center', va='center',
    fontsize=18, fontweight='bold', color=TEXT_COLOR,
    fontfamily='sans-serif',
)
fig.text(
    0.5, 0.91,
    'Ekstraklasa 2025/26 | vs league average',
    ha='center', va='center',
    fontsize=12, color=SUBTLE_TEXT,
    fontfamily='sans-serif',
)

legend_y = 0.06
fig.patches.append(plt.Rectangle((0.30, legend_y), 0.025, 0.018,
                                  facecolor=LEGIA_COLOR, alpha=0.7,
                                  transform=fig.transFigure, zorder=10))
fig.text(0.335, legend_y + 0.007, 'Legia Warszawa', fontsize=11,
         color=TEXT_COLOR, va='center', fontfamily='sans-serif')

fig.patches.append(plt.Rectangle((0.55, legend_y), 0.025, 0.018,
                                  facecolor=LEAGUE_COLOR, alpha=0.5,
                                  transform=fig.transFigure, zorder=10))
fig.text(0.585, legend_y + 0.007, 'League average', fontsize=11,
         color=TEXT_COLOR, va='center', fontfamily='sans-serif')

float_indices = {0, 1}
for i, (x, y) in enumerate(vertices1):
    val = legia_values[i]
    label = f"{val:.1f}" if i in float_indices else f"{int(val)}"
    ax.annotate(
        label, (x, y),
        textcoords="offset points", xytext=(0, 12),
        ha='center', va='bottom',
        fontsize=9, fontweight='bold', color='white',
        bbox=dict(boxstyle='round,pad=0.2', facecolor=LEGIA_COLOR, alpha=0.85, edgecolor='none'),
    )

plt.tight_layout(rect=[0, 0.08, 1, 0.88])
plt.show()