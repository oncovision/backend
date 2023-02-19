import pandas as pd

pd.set_option('display.max_rows', None)
df = pd.read_csv (r'lungcancerdataset.csv')


import requests
response = requests.get("http://localhost:8000/getlungcancerdata")
print response.content