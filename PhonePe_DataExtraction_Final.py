#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#Clone github data
get_ipython().system('git clone https://github.com/PhonePe/pulse.git')
#Since it threw 'updating' errors downloaded data


# In[ ]:


get_ipython().system('pip install mysql-connector-python')


# In[ ]:


get_ipython().system('pip install streamlit-option-menu')


# In[ ]:


get_ipython().system('pip install streamlit')


# In[1]:


import mysql.connector
import json
import re
import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import plotly.express as px
import json
import os
os.environ["GIT_PYTHON_REFRESH"] = "quiet"
from PIL import Image


# In[ ]:


#agreegated transaction df
path="/Users/        "

Agg_state_list=os.listdir(path)
Agg_state_list
#Agg_state_list--> to get the list of states in India

#<------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------>#

#This is to extract the data's to create a dataframe
#{"success":true,"code":"SUCCESS","data":{"from":1577817000000,"to":1585333800000,"transactionData":[{"name":"Peer-to-peer payments","paymentInstruments":[{"type":"TOTAL","count":18324,"amount":1.4233240179234773E8}]}...,{"name":"Others","paymentInstruments":[{"type":"TOTAL","count":216,"amount":332393.19201521645}]}]},"responseTimestamp":1630501491518}

clm={'State':[], 'Year':[],'Quater':[],'Transacion_type':[], 'Transacion_count':[], 'Transacion_amount':[]}

for i in Agg_state_list:
    p_i=path+i+"/"
    Agg_yr=os.listdir(p_i)
    for j in Agg_yr:
        p_j=p_i+j+"/"
        Agg_yr_list=os.listdir(p_j)
        for k in Agg_yr_list:
            p_k=p_j+k
            Data=open(p_k,'r')
            D=json.load(Data)
            #print(D)
            for z in D['data']['transactionData']:
              Name=z['name']
              count=z['paymentInstruments'][0]['count']
              amount=z['paymentInstruments'][0]['amount']
              clm['Transacion_type'].append(Name)
              clm['Transacion_count'].append(count)
              clm['Transacion_amount'].append(amount)
              clm['State'].append(i)
              clm['Year'].append(j)
              clm['Quater'].append(int(k.strip('.json')))
#Succesfully created a dataframe
df_Agg_trans=pd.DataFrame(clm)


# In[42]:


df_Agg_trans


# In[ ]:


df_Agg_trans.shape


# In[ ]:


df_Agg_trans.dtypes 
#Need to see if any encoding or datatype conversion is required
#df['seats'] = df['seats'].astype('int')
#df['mileage'] = df['mileage'].str.split(" ").str[0]
#df['mileage'] = df['mileage'].astype('float')


# In[ ]:


df_Agg_trans.isnull().sum()
#Data seems to be complete with no ull values


# In[23]:


#agreegated users df
path="/Users/   "

Agg_state_list=os.listdir(path)
Agg_state_list
#<------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------>#
#This is to extract the data's to create a dataframe
#{"success":true,"code":"SUCCESS","data":{"aggregated":{"registeredUsers":28368,"appOpens":193586},"usersByDevice":[{"brand":"Xiaomi","count":6803,"percentage":0.23981246474901297}....,{"brand":"Others","count":2257,"percentage":0.0795614777213762}]},"responseTimestamp":1630501498181}

clm={'State':[], 'Year':[],'Quater':[],'Brand_name':[], 'Brand_count':[], 'Brand_percentage':[]}

for i in Agg_state_list:
    p_i=path+i+"/"
    Agg_yr=os.listdir(p_i)
    for j in Agg_yr:
        p_j=p_i+j+"/"
        Agg_yr_list=os.listdir(p_j)
        for k in Agg_yr_list:
            p_k=p_j+k
            Data=open(p_k,'r')
            D=json.load(Data)
            #print(D)
            try:
                for z in D['data']['usersByDevice']:
                  Brand=z['brand']
                  Count=z['count']
                  Percentage=z['percentage']
                  clm['Brand_name'].append(Brand)
                  clm['Brand_count'].append(Count)
                  clm['Brand_percentage'].append(Percentage)
                  clm['State'].append(i)
                  clm['Year'].append(j)
                  clm['Quater'].append(int(k.strip('.json')))
            except:
                pass                
            
#Succesfully created a dataframe
df_Agg_user=pd.DataFrame(clm)


# In[24]:


df_Agg_user


# In[ ]:


df_Agg_user.shape


# In[ ]:


df_Agg_user.dtypes 


# In[ ]:


df_Agg_user.isnull().sum()


# In[26]:


#map transaction df
path="/Users/     "

Agg_state_list=os.listdir(path)
Agg_state_list
#Agg_state_list--> to get the list of states in India

#<------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------>#

#This is to extract the data's to create a dataframe
#{"success":true,"code":"SUCCESS","data":{"hoverDataList":[{"name":"north and middle andaman district","metric":[{"type":"TOTAL","count":5674,"amount":1.4697371617857102E7}]},........"responseTimestamp":1630502911249}
clm={'State':[], 'Year':[],'Quater':[],'District_name':[], 'Transacion_count':[], 'Transacion_amount':[]}

for i in Agg_state_list:
    p_i=path+i+"/"
    Agg_yr=os.listdir(p_i)
    for j in Agg_yr:
        p_j=p_i+j+"/"
        Agg_yr_list=os.listdir(p_j)
        for k in Agg_yr_list:
            p_k=p_j+k
            Data=open(p_k,'r')
            D=json.load(Data)
            #print(D)
            try:
                for z in D['data']['hoverDataList']:
                  Name=z['name']
                  Count=z['metric'][0]['count']
                  Amount=z['metric'][0]['amount']
                  clm['District_name'].append(Name)
                  clm['Transacion_count'].append(Count)
                  clm['Transacion_amount'].append(Amount)
                  clm['State'].append(i)
                  clm['Year'].append(j)
                  clm['Quater'].append(int(k.strip('.json')))
            except:
                pass                            
#Succesfully created a dataframe
df_Map_trans=pd.DataFrame(clm)            


# In[27]:


df_Map_trans


# In[ ]:


df_Map_trans.shape


# In[ ]:


df_Map_trans.dtypes


# In[ ]:


df_Map_trans.isnull().sum()


# In[28]:


#map user df
path="/Users/     "

Agg_state_list=os.listdir(path)
Agg_state_list
#Agg_state_list--> to get the list of states in India

#<------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------>#

#This is to extract the data's to create a dataframe
#{"success":true,"code":"SUCCESS","data":{"hoverData":{"north and middle andaman district":{"registeredUsers":3315,"appOpens":30444},...."responseTimestamp":1630502911838}
clm={'State':[], 'Year':[],'Quater':[],'District_name':[], 'User_count':[], 'Application_open':[]}

for i in Agg_state_list:
    p_i=path+i+"/"
    Agg_yr=os.listdir(p_i)
    for j in Agg_yr:
        p_j=p_i+j+"/"
        Agg_yr_list=os.listdir(p_j)
        for k in Agg_yr_list:
            p_k=p_j+k
            Data=open(p_k,'r')
            D=json.load(Data)
            #print(D)
            try:
                for z in D['data']['hoverData'].items():
                  Name=z[0]
                  #print(Name)  
                  Count=z[1]['registeredUsers']
                  Appopen=z[1]['appOpens']
                  clm['District_name'].append(Name)
                  clm['User_count'].append(Count)
                  clm['Application_open'].append(Appopen)
                  clm['State'].append(i)
                  clm['Year'].append(j)
                  clm['Quater'].append(int(k.strip('.json')))
            except:
                pass                            
#Succesfully created a dataframe
df_Map_user=pd.DataFrame(clm)                     


# In[29]:


df_Map_user


# In[ ]:


df_Map_user.shape


# In[ ]:


df_Map_user.dtypes


# In[ ]:


df_Map_user.isnull().sum()


# In[30]:


#top transaction df
path="/Users/      "

Agg_state_list=os.listdir(path)
Agg_state_list
#Agg_state_list--> to get the list of states in India

#<------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------>#

#This is to extract the data's to create a dataframe
#{"success":true,"code":"SUCCESS","data":{"states":null,"districts":[{"entityName":"south andaman","metric":{"type":"TOTAL","count":32713,"amount":1.3467939690582758E8}},...."responseTimestamp":1630501491517}
clm={'State':[], 'Year':[],'Quater':[],'District_name':[], 'Transacion_count':[], 'Transacion_amount':[]}

for i in Agg_state_list:
    p_i=path+i+"/"
    Agg_yr=os.listdir(p_i)
    for j in Agg_yr:
        p_j=p_i+j+"/"
        Agg_yr_list=os.listdir(p_j)
        for k in Agg_yr_list:
            p_k=p_j+k
            Data=open(p_k,'r')
            D=json.load(Data)
            #print(D)
            try:
                for z in D['data']['districts']:
                  Name=z['entityName']
                  Count=z['metric']['count']
                  Amount=z['metric']['amount']
                  clm['District_name'].append(Name)
                  clm['Transacion_count'].append(Count)
                  clm['Transacion_amount'].append(Amount)
                  clm['State'].append(i)
                  clm['Year'].append(j)
                  clm['Quater'].append(int(k.strip('.json')))
            except:
                pass                            
#Succesfully created a dataframe
df_Top_trans=pd.DataFrame(clm)     


# In[31]:


df_Top_trans


# In[ ]:


df_Top_trans.dtypes


# In[ ]:


df_Top_trans.isnull().sum()


# In[32]:


#top users dist df
path="/Users/    "

Agg_state_list=os.listdir(path)
Agg_state_list
#Agg_state_list--> to get the list of states in India

#<------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------>#

#This is to extract the data's to create a dataframe
#{"success":true,"code":"SUCCESS","data":{"states":null,"districts":[{"entityName":"south andaman","metric":{"type":"TOTAL","count":32713,"amount":1.3467939690582758E8}},...."responseTimestamp":1630501491517}
#"success":true,"code":"SUCCESS","data":{"states":null,"districts":[{"name":"south andaman","registeredUsers":24174},..{"name":"nicobars","registeredUsers":879}], "pincodes":[{"name":"744103","registeredUsers":6108},...{"name":"744301","registeredUsers":669}]},"responseTimestamp":1630501498181}
clm={'State':[], 'Year':[],'Quater':[],'District_name':[], 'Registered_users':[]}

for i in Agg_state_list:
    p_i=path+i+"/"
    Agg_yr=os.listdir(p_i)
    for j in Agg_yr:
        p_j=p_i+j+"/"
        Agg_yr_list=os.listdir(p_j)
        for k in Agg_yr_list:
            p_k=p_j+k
            Data=open(p_k,'r')
            D=json.load(Data)
            #print(D)
            try:
                for z in D['data']['districts']:
                  Name=z['name']
                  Count=z['registeredUsers']
                  clm['District_name'].append(Name)
                  clm['Registered_users'].append(Count)
                  clm['State'].append(i)
                  clm['Year'].append(j)
                  clm['Quater'].append(int(k.strip('.json')))
            except:
                pass                            
#Succesfully created a dataframe
df_Top_user_dist=pd.DataFrame(clm)     


# In[33]:


df_Top_user_dist


# In[ ]:


df_Top_user_dist.isnull().sum()


# In[34]:


#top users pincode df
path="/Users/      "

Agg_state_list=os.listdir(path)
Agg_state_list
#Agg_state_list--> to get the list of states in India

#<------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------>#

#This is to extract the data's to create a dataframe
#{"success":true,"code":"SUCCESS","data":{"states":null,"districts":[{"entityName":"south andaman","metric":{"type":"TOTAL","count":32713,"amount":1.3467939690582758E8}},...."responseTimestamp":1630501491517}
#"success":true,"code":"SUCCESS","data":{"states":null,"districts":[{"name":"south andaman","registeredUsers":24174},..{"name":"nicobars","registeredUsers":879}], "pincodes":[{"name":"744103","registeredUsers":6108},...{"name":"744301","registeredUsers":669}]},"responseTimestamp":1630501498181}
clm={'State':[], 'Year':[],'Quater':[],'Pincode':[], 'Registered_users':[]}

for i in Agg_state_list:
    p_i=path+i+"/"
    Agg_yr=os.listdir(p_i)
    for j in Agg_yr:
        p_j=p_i+j+"/"
        Agg_yr_list=os.listdir(p_j)
        for k in Agg_yr_list:
            p_k=p_j+k
            Data=open(p_k,'r')
            D=json.load(Data)
            #print(D)
            try:
                for z in D['data']['pincodes']:
                  Name=z['name']
                  Count=z['registeredUsers']
                  clm['Pincode'].append(Name)
                  clm['Registered_users'].append(Count)
                  clm['State'].append(i)
                  clm['Year'].append(j)
                  clm['Quater'].append(int(k.strip('.json')))
            except:
                pass                            
#Succesfully created a dataframe
df_Top_user_pincode=pd.DataFrame(clm)    


# In[35]:


df_Top_user_pincode


# In[ ]:


df_Top_user_pincode.isnull().sum()


# In[ ]:


#Convert df to csv files - No need
df_Agg_trans.to_csv('Agg_trans.csv',index=False)
df_Agg_user.to_csv('Agg_user.csv',index=False)
df_Map_trans.to_csv('Map_trans.csv',index=False)
df_Map_user.to_csv('Map_user.csv',index=False)
df_Top_trans.to_csv('Top_trans.csv',index=False)
df_Top_user_dist.to_csv('Top_user_dist.csv',index=False)
df_Top_user_pincode.to_csv('Top_trans_pincode.csv',index=False)


# In[36]:


# Create new schema ‘phonepe_db’ from Workbench.
# Connect to mysql dB
cnx = mysql.connector.connect(
    user='    ',
    password='     ',
    host='127.0.0.1',
    database='phonepe_db'
)
cursor = cnx.cursor(buffered=True)


# In[37]:


print(cnx)


# In[ ]:





# In[38]:


#create agg_transaction table
#cursor.execute("CREATE TABLE IF NOT EXISTS agg_transaction (State VARCHAR(255), Year INT, Quarter INT, Transaction_type VARCHAR(255), Transaction_count INT, Transaction_amount DOUBLE)")


# In[39]:


#insert data to agg_transaction table from the df_Agg_trans df
for i,row in df_Agg_trans.iterrows():
    sql = "INSERT IGNORE INTO agg_transaction VALUES (%s,%s,%s,%s,%s,%s)" #No IGNORE used as there are no keys
    cursor.execute(sql, tuple(row))
    cnx.commit()
#checked count in workbench to confirm all 4314 rows committed


# In[40]:


#create agg_user table
#cursor.execute("CREATE TABLE IF NOT EXISTS agg_user (State VARCHAR(255), Year INT, Quarter INT, Brand_name VARCHAR(255), Brand_count INT, Brand_percentage DOUBLE)")


# In[41]:


#insert data to agg_user table from the df_Agg_user df
for i,row in df_Agg_user.iterrows():
    sql = "INSERT INTO agg_user VALUES (%s,%s,%s,%s,%s,%s)" 
    cursor.execute(sql, tuple(row))
    cnx.commit()
#checked count in workbench to confirm all 6732 rows committed


# In[43]:


#cursor.execute("CREATE TABLE IF NOT EXISTS map_transaction (State VARCHAR(255), Year INT, Quarter INT, District_name VARCHAR(255), Transaction_count INT, Transaction_amount DOUBLE)")


# In[44]:


#insert data to map_transaction table from the df_Map_trans df
for i,row in df_Map_trans.iterrows():
    sql = "INSERT INTO map_transaction VALUES (%s,%s,%s,%s,%s,%s)" 
    cursor.execute(sql, tuple(row))
    cnx.commit()
#checked count in workbench to confirm all '17564' rows committed


# In[45]:


#cursor.execute("CREATE TABLE IF NOT EXISTS map_user (State VARCHAR(255), Year INT, Quarter INT, District_name VARCHAR(255), User_count INT, Application_open DOUBLE)")


# In[46]:


#insert data to map_user table from the df_Map_user df
for i,row in df_Map_user.iterrows():
    sql = "INSERT INTO map_user VALUES (%s,%s,%s,%s,%s,%s)" 
    cursor.execute(sql, tuple(row))
    cnx.commit()
#checked count in workbench to confirm all '17568' rows committed


# In[47]:


#cursor.execute("CREATE TABLE IF NOT EXISTS top_transaction (State VARCHAR(255), Year INT, Quarter INT, District_name VARCHAR(255), Transaction_count INT, Transaction_amount DOUBLE)")
                   


# In[48]:


#insert data to top_transaction table from the df_Top_trans df
for i,row in df_Top_trans.iterrows():
    sql = "INSERT INTO top_transaction VALUES (%s,%s,%s,%s,%s,%s)" 
    cursor.execute(sql, tuple(row))
    cnx.commit()
#checked count in workbench to confirm all 7104 rows committed


# In[49]:


#cursor.execute("CREATE TABLE IF NOT EXISTS top_user_dist (State VARCHAR(255), Year INT, Quarter INT, District_name VARCHAR(255), Registered_users DOUBLE)") 


# In[50]:


#insert data to top_user_dist table from the df_Top_user_dist df
for i,row in df_Top_user_dist.iterrows():
    sql = "INSERT INTO top_user_dist VALUES (%s,%s,%s,%s,%s)" 
    cursor.execute(sql, tuple(row))
    cnx.commit()
#checked count in workbench to confirm all 7104 rows committed


# In[51]:


#cursor.execute("CREATE TABLE IF NOT EXISTS top_user_pincode (State VARCHAR(255), Year INT, Quarter INT, Pincode INT, Registered_users DOUBLE)")    


# In[52]:


#insert data to top_user_pincode table from the df_Top_user_pincode df
for i,row in df_Top_user_pincode.iterrows():
    sql = "INSERT INTO top_user_pincode VALUES (%s,%s,%s,%s,%s)" 
    cursor.execute(sql, tuple(row))
    cnx.commit()
#checked count in workbench to confirm all '8568' rows committed


# In[ ]:


#The India map was not showing in Streamlit. 
#So the codes below is executed to compare the if Stae names match by generating the comparision csv file
# Unique sates in df
unique_states_df = pd.DataFrame(df_Agg_trans['State'].unique(), columns=['State'])
unique_states_df.sort_values('State', inplace=True)


# In[ ]:


get_ipython().system('pip install requests')


# In[ ]:





# In[ ]:




import requests

# URL of the GeoJSON file
geojson_url = 'https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson'

# Requests to fetch the content of the GeoJSON file
response = requests.get(geojson_url)

# Check if the request was successful
if response.status_code == 200:
    # Load GeoJSON data
    geojson_data = json.loads(response.content)
    
    # Extract state names ST_NM from the GeoJSON
    states_geojson = [feature['properties']['ST_NM'] for feature in geojson_data['features']]
    unique_states_geojson = pd.DataFrame(sorted(set(states_geojson)), columns=['ST_NM'])
else:
    print(f"Failed to retrieve GeoJSON data. Status code: {response.status_code}")

# In[ ]:


# Combine both DataFrames for comparison
comparison_df = unique_states_df.merge(unique_states_geojson, left_on='State', right_on='ST_NM', how='outer', indicator=True)

# Save to CSV
comparison_df.to_csv('state_comparison.csv', index=False)


# In[ ]:





# In[ ]:




