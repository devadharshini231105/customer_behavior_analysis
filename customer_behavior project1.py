import pandas as pd
#import the dataset
df=pd.read_csv(r"C:\Users\Deva Dharshini\Downloads\customer_shopping_behavior.csv")
#print the top values
print(df.head())
#overview of the dataset(no.row&col,col name,datatypes,non-null values,missing values,memeory usage)
print(df.info())
#summarisation of dataset
print(df.describe(include='all'))
#checks the count of missing values
print(df.isnull().sum())
#if some row is null fill it with median value over mean bcoz mean has outliers
df['Review Rating']=df.groupby('Category')['Review Rating'].transform(lambda x: x.fillna(x.median()))
print(df.isnull().sum())
#to avoid error and easily readable change column name to lowercase
df.columns=df.columns.str.lower()
#to avoid error and easily readable change space to underscore
df.columns=df.columns.str.replace(' ','_')
print(df.columns)
#if any col has different name change that too
df=df.rename(columns={'purchase_amount_(usd)':'purchase_amount'})
print(df.columns)
#creating a column age group
labels=['young','adult','middle age','senior']
df['age_group']=pd.qcut(df['age'],q=4,labels=labels)
print(df[['age','age_group']].head(20))
#creating column purchase_frequency_days
#it is a dictionary which maps purchase_frequency words to the number of days
frequency_mapping={
    'Fortnightly':14,
    'Weekly':7,
    'Monthly':30,
    'Bi-Weekly':14,
    'Quarterly':90,
    'Annually':365,
    'Every 3 Months':90
    }
df['purchase_frequency_days']=df['frequency_of_purchases'].map(frequency_mapping)
print(df[['frequency_of_purchases','purchase_frequency_days']].head(20))
#check discount_applied and promo_code_used are same? if same remove the unwanted extra col
print(df[['discount_applied','promo_code_used']])
print((df['discount_applied']==df['promo_code_used']).all())
#remove promocode col
df=df.drop('promo_code_used',axis=1)#drop-removes row/col;axis=0:removes row,axis=1:removes col
print(df.columns)
#lets connect idle with postgresql
#pip install psycopg2-binary sqlalchemy type this in cmd
#step 1:connect to postgresql
#replace placeholders with your actual details
from sqlalchemy import create_engine
username="postgres"
password="Deva%400523"
host="localhost"
port="5432"
database="customer_behaviour"
engine=create_engine(f"postgresql+psycopg2://{username}:{password}@{host}:{port}/{database}")
#step 2 load data frame into postgresql
table_name="customer" #choose any tablename
df.to_sql(table_name,engine,if_exists="replace",index=False)
print(f"Data successfully loaded into table'{table_name}'in database'{database}'.") 




