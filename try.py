import numpy as np
import pandas as pd


df = pd.read_csv(r'C:\Users\limzy\Downloads\AMSUN TEXAS AGREEMENT.csv')
count = 0
checked = set()
    
for index, row in df.iterrows():
    if count < 1 and 'Mba' not in row['Internship Training Centre']:
        print(row['Internship Training Centre'])
        
        count+=1
    else:
        break