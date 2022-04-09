import pandas as pd
import re
df = pd.read_csv('Data/convertcsv .csv')
df['rentPrice/0'] = df['rentPrice/0'].map(lambda x: re.sub(r'\W+', '', x))
print(df.iloc[:,0])
# df.to_csv('cleaned.csv')