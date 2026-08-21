import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.patheffects as pe
import squarify
from utils.colors import (BG_COLOR, TEXT_COLOR, SUBTITLE_TEXT)
from utils.club_info import (SEASON, TEAM)

df = pd.read_parquet('data/ekstraklasa_all_clean.parquet')

legia = df[
    (df['team'] == TEAM) &
    (df['tournament'] == 'Ekstraklasa') &
    (df['season'] == SEASON) &
    (df['position'] != 'Keeper') &
    (df['chances_created'] >= 5)
].copy()

legia['chances_created'] = legia['chances_created'].fillna(0)
legia['big_chance_created_team_title'] = legia['big_chance_created_team_title'].fillna(0)

legia = legia[legia['top_minutes_played'] >= 300].copy()
legia = legia[legia['chances_created'] >= 1].sort_values('chances_created', ascending=False).reset_index(drop=True)

names = legia['player_name'].tolist()
chances = legia['chances_created'].astype(int).tolist()
big_chances = legia['big_chance_created_team_title'].astype(int).tolist()
labels = [f"{name}\n{c} chances ({bc} big)" for name, c, bc in zip(names, chances, big_chances)]

cmap = mcolors.LinearSegmentedColormap.from_list('legia', ['#e8f5e9', '#a5d6a7'])
max_val = max(chances)
colors = [cmap(c / max_val) for c in chances]

plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['Segoe UI', 'Arial', 'Helvetica'],
})

fig, ax = plt.subplots(figsize=(16, 9))

squarify.plot(
    sizes=chances,
    label=labels,
    color=colors,
    alpha=0.9,
    ax=ax,
    text_kwargs={'fontsize': 11, 'fontweight': 'bold', 'color': TEXT_COLOR,
                 'path_effects': [pe.withStroke(linewidth=3, foreground=BG_COLOR, alpha=0.8)]},
    bar_kwargs={'edgecolor': BG_COLOR, 'linewidth': 2.5},
)

ax.set_title(
    'LEGIA WARSZAWA — CHANCES CREATED',
    fontsize=18, fontweight='bold', color=TEXT_COLOR, pad=20, loc='left',
)
ax.text(
    0.0, 1.01, 'Ekstraklasa 2025/26 | size = chances created | min. 5 chances',
    transform=ax.transAxes, fontsize=10, color=SUBTITLE_TEXT,
    verticalalignment='bottom',
)

ax.axis('off')

fig.patch.set_facecolor(BG_COLOR)
ax.set_facecolor(BG_COLOR)

fig.tight_layout()
fm = plt.get_current_fig_manager()
fm.window.showMaximized()
plt.show()
