import pandas as pd 
from sqlalchemy import create_engine
df = pd.read_csv("customer_shopping_behavior.csv")

# Taking null values of rating as median of rating category wise
df['Review Rating'] = df.groupby('Category')['Review Rating'].transform(lambda x:x.fillna(x.median()))


#Replacing the space with _ and transforming the columns name to lower case
df.columns = df.columns.str.lower()
df.columns = df.columns.str.replace(' ','_')
df = df.rename(columns={'purchase_amount_(usd)':'purchase_amount'})



#create a column age_group
labels = ['Yound Adult','Adult','Middle-aged','Senior']
df['age_group'] = pd.qcut(df['age'],q=4,labels=labels)

#create column purchase_frequency_days
frequency_mapping = {
    'Fortnightly':14,
    'Weekly':7,
    'Monthly':30,
    'Quarterly':90,
    'Bi-Weekly':14,
    'Annually':365,
    'Every 3 months':90
}
print(df.columns)
df['purchase_frequency_days'] = df['frequency_of_purchases'].map(frequency_mapping)
 
df = df.drop('promo_code_used',axis=1)

#Loading dataset to mysql

engine = create_engine("mysql+pymysql://root:Anurag@localhost/new")

df.to_sql("customer", engine, if_exists="replace", index=False)
