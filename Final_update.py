
# coding: utf-8

# In[404]:


# Connecting to postgresql 
import psycopg2

import json
try:
    conn = psycopg2.connect("dbname= 'pyapp' user = 'root' password = 'dev123'")
    print ("connected to database.")
except:
    print("unable to connect")
    


# In[405]:


import sys
import pandas as pd
import pandas_compat as pdc
import plotly.offline as py
from keras.models import Sequential
import requests
from keras.layers import Dense
cf.set_config_file(offline=True, world_readable=True, theme='pearl')
from keras.layers import LSTM
from matplotlib import pyplot
py.init_notebook_mode(connected=True)
from math import sqrt
import plotly.graph_objs as go
import pandas.compat as compat
import numpy as np
#from sqlalchemy import create_engine
#engine = create_engine('postgresql://root@192.168.1.144:9999/pyapp')

import sklearn
import matplotlib
from tensorflow.contrib import learn
from sklearn.metrics import mean_squared_error, mean_absolute_error
import matplotlib.pyplot as plt 
from matplotlib import pyplot as plt
from seaborn import FacetGrid
from numpy import median
from numpy import genfromtxt
from sklearn import datasets
import time
from datetime import datetime
import seaborn as sns
from seaborn import FacetGrid
get_ipython().magic('matplotlib inline')
from numpy import median
import tensorflow as tf
import itertools
#import seaborn as sns


# In[406]:


# Fetch the data from the database 
cur = conn.cursor()
cur.execute("SELECT * FROM tb_api_reports")
data= cur.fetchall()
print(data)


# In[408]:


df = pd.DataFrame(data, columns = ['Report_id_integer' ,'Report_file_name', 'Report_file_path','Report_file_size','User_id ','Testcase_id','Testset_id','Created_at_timestamp_without_Time_Zone','Module_id','Datasets_status','Report_result','Report_type','Pass_count','Fail_count']) 
print(df)


# In[409]:


df.isna().sum()


# In[410]:


# df.shape


# In[411]:


df.drop(['Datasets_status','Report_result','Report_file_name','Report_file_path'],axis = 1, inplace = True, errors = 'ignore')
print(df.count)


# In[412]:


df = df.convert_objects(convert_numeric= True)


# In[414]:


df['Report_type'].unique().tolist()


# In[415]:


def Report_type_numeric(x):
    if x=='api':
        return 1
    if x=='web':
        return 2
    if x=='Android':
        return 3
    if x=='iOS':
        return 4
df['Report_type_num'] = df['Report_type'].apply(Report_type_numeric)
print(df)
df['Report_type_num'].unique().tolist()


# In[416]:


df['Report_type_num'].value_counts(sort=True,ascending=False)


# In[417]:


# df.drop(['Report_type'], axis = 1, inplace = True, errors = 'ignore')


# In[418]:


df['Created_at_timestamp_without_Time_Zone'] = pd.to_datetime(df['Created_at_timestamp_without_Time_Zone']).dt.date
print(df)


# In[419]:


# df['Created_at_timestamp_without_Time_Zone'] = pd.DatetimeIndex (df.Created_at_timestamp_without_Time_Zone ).astype ( np.int64 )//10**9   
# print(df)


# In[420]:


# df.drop(['Created_at_timestamp_without_Time_Zone'], axis = 1, inplace = True, errors = 'ignore')


# In[421]:


# import json
# df_json= df.to_json(orient='columns',force_ascii='')


# In[422]:


# df_json


# In[423]:


# y = json.dumps(df_json)
# print(y)


# In[424]:


# from urllib.parse import urlencode
# from urllib.request import Request, urlopen

# url = 'http://pastebin.com/api/api_post.php' # Set destination URL here
# #post_fields = {'foo': 'bar'}     # Set POST fields here

# r = requests.post(url, data=json.dumps(df_json))
# print(r)


# In[425]:


df['Testcase_id'].value_counts(sort=True,ascending=False)


# In[426]:


df['Created_at_timestamp_without_Time_Zone'].min(), df['Created_at_timestamp_without_Time_Zone'].max()


# In[427]:


#df= df.set_index('Created_at_timestamp_without_Time_Zone')


# In[428]:


df_1 = pd.DataFrame([df.Testcase_id, df.Pass_count, df.Fail_count, df.Report_type]).transpose()
df_1


# In[429]:


#df_1.Module_id= df_1.Module_id.astype(int)
df_1.Pass_count= df_1.Pass_count.astype(int)
df_1.Fail_count= df_1.Fail_count.astype(int)
df_1.Testcase_id= df_1.Testcase_id.astype(int)


# In[430]:


df_1.dtypes


# In[431]:


import matplotlib
import matplotlib.pyplot as plt 
from matplotlib import pyplot as plt
import seaborn as sns
from seaborn import FacetGrid
get_ipython().magic('matplotlib inline')
from numpy import median


# In[432]:


# bar = sns.barplot(x="Module_id",y="Pass_count",data= df_1,color="b")
# bar.set_xticklabels(bar.get_xticklabels(),rotation=90)
# bar.set_title("Average prices of the Suites")


# In[433]:


df_tableset= df_1.pivot_table(index='Testset_id', columns=['Report_type'], aggfunc='size', fill_value=0, margins=False)

# In[434]:


df_tableset


# In[435]:


df_tableset_1= df_1.pivot_table(index='Testset_id', columns=['Report_type'],values=['Fail_count','Pass_count'], aggfunc=np.sum,fill_value=0, margins=False) 


# In[436]:


results_2= pd.concat([df_tableset, df_tableset_1], axis=1, sort=False)


# In[437]:


results_2


# In[438]:


finalset_df = pd.DataFrame(results_2.to_records())


# In[440]:


finalset_df = finalset_df.set_index('Testset_id')
finalset_df.index


# In[441]:


finalset_df= finalset_df.rename(columns={"('Fail_count', 'Android')":"FC_Android", "('Fail_count', 'api')":"FC_api","('Fail_count', 'iOS')":"FC_iOS","('Fail_count', 'web')":"FC_Web","('Pass_count', 'Android')":"PC_Android", "('Pass_count', 'api')":"PC_api","('Pass_count', 'iOS')":"PC_iOS","('Pass_count', 'web')":"PC_Web"})

# In[442]:


finalset_df


# In[447]:


finalset_df.query('Testset_id== [45]')


# In[395]:


import plotly 
import plotly.plotly as py
import plotly.graph_objs as go
#plotly.tools.set_credentials_file(username='DemoAccount', api_key='44nLnWejMDJkTZUcR0H6')


# In[454]:


finalset_df.iplot(kind='histogram',labels='Testset_id', subplots=True, filename='cufflinks/histogram-subplots', theme='pearl')
