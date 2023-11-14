import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.collections import PatchCollection
from matplotlib.colors import ListedColormap
import pandas as pd

df = pd.read_csv(
    "2022_data.csv",
    # Date column is the index column
    index_col=0,
)

print(df)
