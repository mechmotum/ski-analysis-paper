import os
import pandas as pd

PATH_TO_THIS_FILE = os.path.abspath(__file__)
DIR_OF_THIS_FILE = os.path.dirname(PATH_TO_THIS_FILE)
PROJECT_ROOT = os.path.abspath(os.path.join(DIR_OF_THIS_FILE, '..'))

data = pd.read_csv(os.path.join(PROJECT_ROOT, 'data',
                                'fig-1-data-vish-2005.csv'),
                   comment="#")

data['floor number'] = data['floor number'].astype(int)

print('Count of data points for each floor:')
print(data.groupby('floor number').count())
print('Mean of data points for each floor:')
print(data.groupby('floor number').mean())
