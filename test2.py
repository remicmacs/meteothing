#! /usr/bin/env python

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.collections import PatchCollection
from matplotlib.colors import ListedColormap
import pandas as pd

FIRST = 1850
LAST = 2023  # inclusive


# Reference period for the center of the color scale

FIRST_REFERENCE = 1971
LAST_REFERENCE = 2000
LIM = 0.7 # degrees

# data from

# https://www.metoffice.gov.uk/hadobs/hadcrut4/data/current/time_series/HadCRUT.4.6.0.0.annual_ns_avg.txt
#
# df = pd.read_fwf(
#     'HadCRUT.4.6.0.0.annual_ns_avg.txt',
#     index_col=0,
#     usecols=(0, 1),
#     names=['year', 'anomaly'],
#     header=None,
# )

df = pd.read_csv(
    "HadCRUT.5.0.1.0.analysis.summary_series.global.annual.csv",
    # Year column is the index column
    index_col=0,
    # Use only year and anomaly column
    usecols=(0, 1, 2),
    names=['year', 'anomaly', 'other'],
    # There is a header in this CSV file, skip it and use names arg
    header=0
)

anomaly = df.loc[FIRST:LAST, 'anomaly'].dropna()
reference = anomaly.loc[FIRST_REFERENCE:LAST_REFERENCE].mean()

other = df.loc[FIRST:LAST, 'other'].dropna()
other_reference = other.loc[FIRST_REFERENCE:LAST_REFERENCE].mean()

# the colors in this colormap come from http://colorbrewer2.org

# the 8 more saturated colors from the 9 blues / 9 reds

cmap = ListedColormap([
    '#08306b', '#08519c', '#2171b5', '#4292c6',
    '#6baed6', '#9ecae1', '#c6dbef', '#deebf7',
    '#fee0d2', '#fcbba1', '#fc9272', '#fb6a4a',
    '#ef3b2c', '#cb181d', '#a50f15', '#67000d',
])

fig = plt.figure(figsize=(10, 2))

ax = fig.add_axes([0, 0, 1, 1])
ax.set_axis_off()

# create a collection with a rectangle for each year

col = PatchCollection([
    Rectangle((y, 0), 1, 1)
    for y in range(FIRST, LAST + 1)
])

# set data, colormap and color limits

col.set_array(anomaly)
col.set_cmap(cmap)
col.set_clim(reference - LIM, reference + LIM)
ax.add_collection(col)

upper_col = PatchCollection([
    Rectangle((y, 1), 1, 1)
    for y in range(FIRST, LAST + 1)
])
upper_col.set_array(other)
upper_col.set_cmap(cmap)
upper_col.set_clim(other_reference - LIM, other_reference + LIM)
ax.add_collection(upper_col)

ax.set_ylim(0, 2)
ax.set_xlim(FIRST, LAST + 1)

fig.savefig('warming-stripes.png')
