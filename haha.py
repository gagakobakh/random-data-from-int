import pandas as pd
#merging all the dara in a single file
import os
import matplotlib.pyplot as plt


files=[file for file in os.listdir('./sales')]
all_data=pd.DataFrame()
for file in files:
    df=pd.read_csv('./sales/'+file)
    all_data=pd.concat([all_data,df])



print(all_data.to_csv('all_data.csv',index=False))
all_data=pd.read_csv('all_data.csv')
#nan_df=all_data[all_data.isna().any(axis=1)]
#print(nan_df.head())
all_data=all_data.dropna(how='all')
all_data=all_data[all_data['Order Date'].str[0:2]!='Or']



all_data['month']=all_data['Order Date'].str[0:2]
all_data['month']=all_data['month'].astype('int32')
all_data['Quantity Ordered']=pd.to_numeric(all_data['Quantity Ordered'])
all_data['Price Each']=pd.to_numeric(all_data['Price Each'])
#print(all_data.head())

all_data['sales']=all_data['Quantity Ordered']*all_data["Price Each"]
results=all_data.groupby("month").sum()['sales']
#print(results)

#print(all_data.head())
month=range(1,13)
#print(month)
plt.bar(range(1,9),results)
print(plt.show)
def getcity(adress):
    return adress.split(",")[1]
def getstate(adress):
    return adress.split(",")[2].split(" ")[1]

all_data['city']=all_data['Purchase Address'].apply(lambda x:getcity(x)+" "+getstate(x))
#print(all_data.head())

results2=all_data.groupby("city").sum()["sales"]

cities=[city for city,df in all_data.groupby('city')]
plt.bar(cities,results2)
plt.xticks(cities,rotation='vertical',size=8)
#print(plt.show)

all_data['Order Date']=pd.to_datetime(all_data['Order Date'])
all_data["hour"]=all_data["Order Date"].dt.hour

all_data["minute"]=all_data["Order Date"].dt.minute
#print(all_data.head())
hours=[hour for hour,df in all_data.groupby('hour')]
plt.plot(hours,all_data.groupby(["hour"]).count())
plt.show

df=all_data[all_data['Order ID'].duplicated(keep=False)]
df['grouped']=df.groupby('Order ID')["Product"].transform(lambda x :','.join(x))
df=df[["Order ID","grouped"]].drop_duplicates()
print(df.head())

from itertools import combinations
from collections import Counter

count=Counter()
for row in df["grouped"]:
    row_list=row.split(',')
    count.update(Counter(combinations(row_list,2)))

print(count.most_common(10))








