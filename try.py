import numpy as np
import pandas as pd


df = pd.read_csv(r'C:\Users\limzy\Downloads\AMSUN TEXAS AGREEMENT.csv')
count = 0
checked = set()
    
for index, row in df.iterrows():
    if isinstance(row['Internship Training Centre'], str) and 'Nazareth' in row['Internship Training Centre']:
        print(row['Name'], row['Phone'])
        