"""Calculates the average floor height from data estimates taken from FIgure 1
in Vish 2005. I used a graphical tool to attempt to select as many data points
on the figure and extract the data from figure, as they were not tabulated in
the paper, so the numbers are rough estimates."""
import os
import pandas as pd

PATH_TO_THIS_FILE = os.path.abspath(__file__)
DIR_OF_THIS_FILE = os.path.dirname(PATH_TO_THIS_FILE)
PROJECT_ROOT = os.path.abspath(os.path.join(DIR_OF_THIS_FILE, '..'))

ft2m = lambda x: 0.3048*x

data = pd.read_csv(os.path.join(PROJECT_ROOT, 'data',
                                'fig-1-data-vish-2005.csv'),
                   comment="#")

# .round(1) ensures it rounds up and down to closest integer
data['floor number'] = data['floor number'].round(0).astype(int)

print('Count of data points for each floor:')
print(data.groupby('floor number').count())
print('Mean of data points for each floor [meters]:')
print(data.groupby('floor number').mean().apply(ft2m).round(1))
