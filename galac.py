import pandas as pd

data = pd.read_excel("plantilla.xslx", sheet_name='Orders', header=3 index_col='Row_10')

data.describe()