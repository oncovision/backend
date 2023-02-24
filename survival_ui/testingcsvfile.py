import pandas as pd
from PIL import Image

data= pd.read_csv(r'Integrated Data.csv')
data =  data.dropna(axis=0)
data=data.reset_index(drop=True)
df_new = data[['Time', 'CTC count', 'Oncology Milestone']]
#image = Image.open(df["Radiology Image"].head(1))
str= data['Radiology Image'].head(1)
image = Image.open('radiologicalImages/'+data['Radiology Image'].head(1).values[0])
#image = Image.open(str)
#print(str.values[0])