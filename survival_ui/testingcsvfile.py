import pandas as pd

data= pd.read_csv(r'Integrated Data.csv')
data =  data.dropna(axis=0)
data=data.reset_index(drop=True)
df_new = data[['Time', 'CTC count', 'Oncology Milestone']]
print(data[['Time','RBC']])