import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.patches import Rectangle
from matplotlib.collections import PatchCollection
from matplotlib.colors import ListedColormap
import pandas as pd

df = pd.read_csv(
    "2022_data.csv",\
    # Date column is the index column
    index_col=0,
)

print(df)

firstdate = df.index[0]
print(firstdate)
lastdate = df.index[-1]

print(lastdate)

max = df.loc[firstdate:lastdate, 'max']
print(max)
reference = max.loc[firstdate:lastdate].mean()

# fig, ax = plt.subplots(figsize=(6, 1))
# fig.subplots_adjust(bottom=0.5)

cmap = ListedColormap([
    # Canard
    "#0E5876",
    # Bleu Sport
    "#1B3980",
    # Ultra Bleu
    "#6082B8",
    # Amande
    "#A9B19B",
    # Brindille
    "#C8DAD8",
    # Biche
    "#DCC6B2",
    # Peche
    "#ECB198",
    # Orange Sport
    "#CE5C53",
    # Rouge
    "#BC3241"
])

bounds = [0, 6, 11, 16, 21, 26, 31, 36]
norm = mpl.colors.BoundaryNorm(bounds, cmap.N, extend='both')
print(norm)

fig = plt.figure(figsize=(10, 2))

ax = fig.add_axes([0, 0, 1, 1])
ax.set_axis_off()

# create a collection with a rectangle for each date
# print(list(range(len(df.index))))
col = PatchCollection([
    Rectangle((y, 0), 1, 1)
    for y in range(4)
])

col.set_array(df.loc[firstdate:df.index[3], "max"])
col.set_cmap(cmap)
# col.set_norm(norm)
col.set_clim(-1, 37)
ax.add_collection(col)

# fig.colorbar(mpl.cm.ScalarMappable(norm=norm, cmap=cmap),
             # cax=ax, orientation='horizontal',
             # label="Discrete intervals with extend='both' keyword")

fig.savefig("result.png")
# plt.show()
