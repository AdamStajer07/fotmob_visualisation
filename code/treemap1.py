import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.patheffects as pe
import squarify
from utils.colors import (BG_COLOR, TEXT_COLOR, SUBTITLE_TEXT)
from utils.club_info import (SEASON, TEAM, EXCLUDED_PLAYERS)

df = pd.read_parquet('data/ekstraklasa_all_clean.parquet')

legia = df[
    (df['team'] == TEAM) &
    (df['tournament'] == 'Ekstraklasa') &
    (df['season'] == SEASON) &
    (df['position'] != 'Keeper')
].copy()

legia = legia[~legia['player_name'].isin(EXCLUDED_PLAYERS)]

legia['goals'] = legia['goals'].fillna(0)
legia['assists'] = legia['assists'].fillna(0)
legia['contributions'] = legia['goals'].astype(int) + legia['assists'].astype(int)

legia = legia[legia['top_minutes_played'] >= 300].copy()
legia = legia[legia['contributions'] >= 1].sort_values('contributions', ascending=False).reset_index(drop=True)

names = legia['player_name'].tolist()
contributions = legia['contributions'].astype(int).tolist()
goals_list = legia['goals'].astype(int).tolist()
assists_list = legia['assists'].astype(int).tolist()
labels = [f"{name}\n{g}G + {a}A" for name, g, a in zip(names, goals_list, assists_list)]

cmap = mcolors.LinearSegmentedColormap.from_list('legia', ['#e8f5e9', '#a5d6a7'])
max_val = max(contributions)
colors = [cmap(c / max_val) for c in contributions]

plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['Segoe UI', 'Arial', 'Helvetica'],
})

fig, ax = plt.subplots(figsize=(16, 9))

squarify.plot(
    sizes=contributions,
    label=labels,
    color=colors,
    alpha=0.9,
    ax=ax,
    text_kwargs={'fontsize': 11, 'fontweight': 'bold', 'color': TEXT_COLOR,
                 'path_effects': [pe.withStroke(linewidth=3, foreground=BG_COLOR, alpha=0.8)]},
    bar_kwargs={'edgecolor': BG_COLOR, 'linewidth': 2.5},
)

ax.set_title(
    'LEGIA WARSZAWA — GOAL CONTRIBUTIONS',
    fontsize=24, fontweight='bold', color=TEXT_COLOR, pad=24, loc='left',
)
ax.text(
    0.0, 1.01, 'Ekstraklasa 2025/26 | size = goals + assists',
    transform=ax.transAxes, fontsize=16, color=SUBTITLE_TEXT,
    verticalalignment='bottom',
)

ax.axis('off')

fig.patch.set_facecolor(BG_COLOR)
ax.set_facecolor(BG_COLOR)

fig.tight_layout()
fm = plt.get_current_fig_manager()
fm.window.showMaximized()
plt.savefig('images/treemap1.png', dpi=600, bbox_inches='tight', facecolor=BG_COLOR)
plt.show()
