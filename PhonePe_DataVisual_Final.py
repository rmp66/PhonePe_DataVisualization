import mysql.connector
import pymysql.cursors
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

# Connect to the database
cnx = pymysql.connect(user='      ',
                      password='     ',
                      host='127.0.0.1',
                      database='phonepe_db')
cursor = cnx.cursor()
#cursor = cnx.cursor()
# Config steamlit and Set the title
st.set_page_config(layout='wide')
st.title("PhonePe Data Visualization - Palaniappan Kannan")
#------------------------------------------Aggregate Transaction Data Visualization on India Map------------------------
# Query the database to get unique data for dropdown
def get_unique_values(column_name):
    query = f"SELECT DISTINCT {column_name} FROM agg_transaction ORDER BY {column_name}"
    cursor.execute(query)
    values = cursor.fetchall()
    return [value[0] for value in values]

# Function query to get display data based on selections
def get_data(transaction_type, year, quarter):
    query = """
    SELECT State, Year, Quarter, Transaction_type, Transaction_count, Transaction_amount
    FROM agg_transaction
    WHERE Transaction_type = %s AND Year = %s AND Quarter = %s
    """
    cursor.execute(query, (transaction_type, year, quarter))
    data = cursor.fetchall()
    columns = ['State', 'Year', 'Quarter', 'Transaction_type', 'Transaction_count', 'Transaction_amount']
    return pd.DataFrame(data, columns=columns)

# st.title("PhonePe Data Visualization - Palaniappan Kannan")
st.subheader("Statewise Aggregate Transaction")

# Dropdowns for State, Year, Quarter
transaction_type = get_unique_values('Transaction_type')
years = get_unique_values('Year')
quarters = get_unique_values('Quarter')

# Place select boxes(dropdowns) on the same line
col1, col2, col3 = st.columns(3)

with col1:
    selected_transaction_type = st.selectbox("Transaction_type", transaction_type)

with col2:
    selected_year = st.selectbox("Select Year", years)

with col3:
    selected_quarter = st.selectbox("Select Quarter", quarters)
# selected_transaction_type = st.selectbox("Transaction_type", transaction_type)
# selected_year = st.selectbox("Select Year", years)
# selected_quarter = st.selectbox("Select Quarter", quarters)

# Fetch data based on selections
df = get_data(selected_transaction_type, selected_year, selected_quarter)

# Round the 'Transaction_amount' column to two decimal places
df['Transaction_amount'] = df['Transaction_amount'].round(2)

# India GeoJSON link to fetch map data
geojson_url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
# Since State names between df and JSON(ST_NM) does not match, below code for changing df State name to JSON State Name
# The comparison csv file produced in Jupyter NB
df['State'] = df['State'].replace({
    'andaman-&-nicobar-islands': 'Andaman & Nicobar',
    'andhra-pradesh': 'Andhra Pradesh',
    'arunachal-pradesh': 'Arunachal Pradesh',
    'assam': 'Assam',
    'bihar': 'Bihar',
    'chandigarh': 'Chandigarh',
    'chhattisgarh': 'Chhattisgarh',
    'dadra-&-nagar-haveli-&-daman-&-diu': 'Dadra and Nagar Haveli and Daman and Diu',
    'delhi': 'Delhi',
    'goa': 'Goa',
    'gujarat': 'Gujarat',
    'haryana': 'Haryana',
    'himachal-pradesh': 'Himachal Pradesh',
    'jammu-&-kashmir': 'Jammu & Kashmir',
    'jharkhand': 'Jharkhand',
    'karnataka': 'Karnataka',
    'kerala': 'Kerala',
    'ladakh': 'Ladakh',
    'lakshadweep': 'Lakshadweep',
    'madhya-pradesh': 'Madhya Pradesh',
    'maharashtra': 'Maharashtra',
    'manipur': 'Manipur',
    'meghalaya': 'Meghalaya',
    'mizoram': 'Mizoram',
    'nagaland': 'Nagaland',
    'odisha': 'Odisha',
    'puducherry': 'Puducherry',
    'punjab': 'Punjab',
    'rajasthan': 'Rajasthan',
    'sikkim': 'Sikkim',
    'tamil-nadu': 'Tamil Nadu',
    'telangana': 'Telangana',
    'tripura': 'Tripura',
    'uttar-pradesh': 'Uttar Pradesh',
    'uttarakhand': 'Uttarakhand',
    'west-bengal': 'West Bengal'

})

# India map display code to display in Streamlit
fig = px.choropleth(
    df,
    geojson=geojson_url,
    locations='State',
    featureidkey="properties.ST_NM",
    color="Transaction_count",
    hover_data=["State", "Transaction_count", "Transaction_amount"],
    color_continuous_scale="Reds"
)
fig.update_geos(fitbounds="locations", visible=False)
fig.update_layout(width=1200, height=800)
st.plotly_chart(fig)

# Streamlit columns used to layout the dataframe and bar charts side by side
col1, col2 = st.columns(2)

with col1:
    # Display the data table
    st.dataframe(df, height=850)

with col2:
    # Top Five States by Transaction Count bar chart
    top_five_transaction_count = df.nlargest(5, 'Transaction_count')
    fig_transaction_count = px.bar(top_five_transaction_count,
                                   x='State',
                                   y='Transaction_count',
                                   title='Transaction Count - Top Five States',
                                   color='Transaction_count',
                                   labels={'Transaction_count': 'Transaction Count'})
    st.plotly_chart(fig_transaction_count)

    # Top Five States by Transaction Amount bar chart
    top_five_transaction_amount = df.nlargest(5, 'Transaction_amount')
    fig_transaction_amount = px.bar(top_five_transaction_amount,
                                    x='State',
                                    y='Transaction_amount',
                                    title='Transaction Amount(Rs.) - Top Five States',
                                    color='Transaction_amount',
                                    labels={'Transaction_amount': 'Transaction Amount(Rs.)'})
    st.plotly_chart(fig_transaction_amount)

#--------------------------Aggregate User data visulalization in INdia Map----------------------------------------------
#Transaction_type=Brand_name; Transaction_count = Brand_count; Transaction_amount = Brand_percentage; agg_transaction = agg_user
# Query the database to get unique data for dropdown
def get_unique_values_agg_user(column_name):
    query = f"SELECT DISTINCT {column_name} FROM agg_user ORDER BY {column_name}"
    cursor.execute(query)
    values = cursor.fetchall()
    return [value[0] for value in values]

# Function query to get display data based on selections
def get_data_agg_user(brand_name, year, quarter):
    query = """
    SELECT State, Year, Quarter, Brand_name, Brand_count, Brand_percentage
    FROM agg_user
    WHERE Brand_name = %s AND Year = %s AND Quarter = %s
    """
    cursor.execute(query, (brand_name, year, quarter))
    data = cursor.fetchall()
    columns = ['State', 'Year', 'Quarter', 'Brand_name', 'Brand_count', 'Brand_percentage']
    return pd.DataFrame(data, columns=columns)

# st.title("PhonePe Data Visualization - Palaniappan Kannan")
st.subheader("Statewise Aggregate User")

# Dropdowns for State, Year, Quarter
brand_name = get_unique_values_agg_user('Brand_name')
years = get_unique_values_agg_user('Year')
quarters = get_unique_values_agg_user('Quarter')

# Place select boxes(dropdowns) on the same line
col1, col2, col3 = st.columns(3)

with col1:
    selected_brand_name = st.selectbox("Brand_name", brand_name)

with col2:
    selected_year = st.selectbox("Select Year", years)

with col3:
    selected_quarter = st.selectbox("Select Quarter ", quarters)
    #selected_quarter = st.selectbox("Select Quarter", quarters)

# Fetch data based on selections
df = get_data_agg_user(selected_brand_name, selected_year, selected_quarter)

# Round the 'Brand_percentage' column to two decimal places
df['Brand_percentage'] = df['Brand_percentage'].round(2)

# India GeoJSON link to fetch map data
geojson_url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
# Since State names between df and JSON(ST_NM) does not match, below code for changing df State name to JSON State Name
# The comparison csv file produced in Jupyter NB
df['State'] = df['State'].replace({
    'andaman-&-nicobar-islands': 'Andaman & Nicobar',
    'andhra-pradesh': 'Andhra Pradesh',
    'arunachal-pradesh': 'Arunachal Pradesh',
    'assam': 'Assam',
    'bihar': 'Bihar',
    'chandigarh': 'Chandigarh',
    'chhattisgarh': 'Chhattisgarh',
    'dadra-&-nagar-haveli-&-daman-&-diu': 'Dadra and Nagar Haveli and Daman and Diu',
    'delhi': 'Delhi',
    'goa': 'Goa',
    'gujarat': 'Gujarat',
    'haryana': 'Haryana',
    'himachal-pradesh': 'Himachal Pradesh',
    'jammu-&-kashmir': 'Jammu & Kashmir',
    'jharkhand': 'Jharkhand',
    'karnataka': 'Karnataka',
    'kerala': 'Kerala',
    'ladakh': 'Ladakh',
    'lakshadweep': 'Lakshadweep',
    'madhya-pradesh': 'Madhya Pradesh',
    'maharashtra': 'Maharashtra',
    'manipur': 'Manipur',
    'meghalaya': 'Meghalaya',
    'mizoram': 'Mizoram',
    'nagaland': 'Nagaland',
    'odisha': 'Odisha',
    'puducherry': 'Puducherry',
    'punjab': 'Punjab',
    'rajasthan': 'Rajasthan',
    'sikkim': 'Sikkim',
    'tamil-nadu': 'Tamil Nadu',
    'telangana': 'Telangana',
    'tripura': 'Tripura',
    'uttar-pradesh': 'Uttar Pradesh',
    'uttarakhand': 'Uttarakhand',
    'west-bengal': 'West Bengal'

})

# India map display code to display in Streamlit
fig = px.choropleth(
    df,
    geojson=geojson_url,
    locations='State',
    featureidkey="properties.ST_NM",
    color="Brand_count",
    hover_data=["State", "Brand_count", "Brand_percentage"],
    color_continuous_scale="Reds"
)
fig.update_geos(fitbounds="locations", visible=False)
fig.update_layout(width=1200, height=800)
st.plotly_chart(fig)

# Streamlit columns used to layout the dataframe and bar charts side by side
col1, col2 = st.columns(2)

with col1:
    # Display the data table
    st.dataframe(df, height=850)

with col2:
    # Top Five States by Transaction Count bar chart
    top_five_brand_count = df.nlargest(5, 'Brand_count')
    fig_brand_count = px.bar(top_five_brand_count,
                                   x='State',
                                   y='Brand_count',
                                   title='Brand Count - Top Five States',
                                   color='Brand_count',
                                   labels={'Brand_count': 'Brand_count'})
    st.plotly_chart(fig_brand_count)

    # Top Five States by Transaction Amount bar chart
    top_five_brand_percentage = df.nlargest(5, 'Brand_percentage')
    fig_brand_percentage = px.bar(top_five_brand_percentage,
                                    x='State',
                                    y='Brand_percentage',
                                    title='Brand Percentage(%) - Top Five States',
                                    color='Brand_percentage',
                                    labels={'Brand_percentage': 'Brand Percentage(%)'})
    st.plotly_chart(fig_brand_percentage)

#------------------Show brand usage in pie chart from agg-user table----------------------------------------------------
def get_data_agg_user1(state, year, quarter):
    query = """
    SELECT State, Year, Quarter, Brand_name, Brand_count, Brand_percentage
    FROM agg_user
    WHERE State = %s AND Year = %s AND Quarter = %s
    """
    cursor.execute(query, (state, year, quarter))
    data = cursor.fetchall()
    columns = ['State', 'Year', 'Quarter', 'Brand_name', 'Brand_count', 'Brand_percentage']
    return pd.DataFrame(data, columns=columns)

# Streamlit subheader
st.subheader("Statewise Brand Usage Pie Chart")

# Dropdowns for State, Year, Quarter
states = get_unique_values_agg_user('State')
years = get_unique_values_agg_user('Year')
quarters = get_unique_values_agg_user('Quarter')

# Place select boxes(dropdowns) on the same line
col1, col2, col3 = st.columns(3)

with col1:
    selected_state = st.selectbox("Select State", states)

with col2:
    selected_year = st.selectbox("Select Year ", years)

with col3:
    selected_quarter = st.selectbox("Select Quarter  ", quarters)

# Fetch data based on selections
df = get_data_agg_user1(selected_state, selected_year, selected_quarter)

# Display pie charts if data is available
if not df.empty:
    # Pie chart for Brand_count
    #fig_count = px.pie(df, names='Brand_name', values='Brand_count', title='Brand Count')
    fig_count = px.pie(df, names='Brand_name', values='Brand_count', title='Brand Count')
    fig_count.update_traces(textinfo='value')

    # Pie chart for Brand_percentage
    fig_percentage = px.pie(df, names='Brand_name', values='Brand_percentage', title='Brand Percentage')

    # Use columns to display pie charts side by side
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(fig_count)
    with col2:
        st.plotly_chart(fig_percentage)
else:
    st.write("No data available for the selected criteria.")

#------------------Show Transaction_count Vs Transaction_amount in regression plot from map_transaction table----------------------------------------------------
# Function to query unique values for 'State'
def get_unique_states_map_transaction():
    cursor.execute("SELECT DISTINCT State FROM map_transaction ORDER BY State")
    states = cursor.fetchall()
    return [state[0] for state in states]
# Function to query unique 'District_name' for a given 'State'
def get_districts_for_state_map_transaction(state):
    cursor.execute("SELECT DISTINCT District_name FROM map_transaction WHERE State = %s ORDER BY District_name", (state,))
    districts = cursor.fetchall()
    return [district[0] for district in districts]
# Function to get data based on 'State' and 'District_name'
def get_data_map_transaction(state, district_name):
    cursor.execute("""
        SELECT Year, Transaction_count, Transaction_amount 
        FROM map_transaction 
        WHERE State = %s AND District_name = %s 
        ORDER BY Year
    """, (state, district_name))
    data = cursor.fetchall()
    return pd.DataFrame(data, columns=['Year', 'Transaction_count', 'Transaction_amount'])
# Streamlit subheader
st.subheader("Districtwise Transaction Count Vs Transaction Amount")
# # Dropdowns for State
states = get_unique_states_map_transaction()
selected_state = st.selectbox("Select State MT", states)
# Dropdown for 'District_name', dynamically updated based on 'State'
districts = get_districts_for_state_map_transaction(selected_state)
selected_district_name = st.selectbox("Select District Name", districts)

# Get and display data
df = get_data_map_transaction(selected_state, selected_district_name)

# Create a regression plot
fig = px.scatter(df, x='Transaction_count', y='Transaction_amount', color='Year',
                 trendline="ols", labels={"Transaction_count": "Transaction Count", "Transaction_amount": "Transaction Amount"},
                 title="Transaction Count vs Transaction Amount by Year")
st.plotly_chart(fig)

#-Show Districtwise multi table of Transaction_count Vs Transaction_amount in regression plot from map_transaction table-
# Function to query unique values for 'State'
def get_unique_states_map_transaction_dw():
    cursor.execute("SELECT DISTINCT State FROM map_transaction ORDER BY State")
    states = cursor.fetchall()
    return [state[0] for state in states]
    #return states
# Function to rest of the data for a given 'State'
def get_data_by_state(state):
    cursor.execute("""
        SELECT District_name, Year, Transaction_count, Transaction_amount
        FROM map_transaction
        WHERE State = %s
        ORDER BY District_name, Year
    """, (state,))
    data = cursor.fetchall()
    return pd.DataFrame(data, columns=['District_name', 'Year', 'Transaction_count', 'Transaction_amount'])
#Streamlit UI
st.subheader("Statewise Transaction Count Vs Transaction Amount")
# Dropdown for 'State'
states = get_unique_states_map_transaction_dw()
selected_state = st.selectbox("Select State MT DW", states)

# Fetch data for the selected state
df = get_data_by_state(selected_state)
# Convert 'Year' to string for categorical coloring
#df['Year'] = df['Year'].astype(str)
# Get unique districts within the selected state
districts = df['District_name'].unique()

# Number of plots per row
plots_per_row = 5
# Calculate the number of rows needed
num_rows = len(districts) // plots_per_row + (1 if len(districts) % plots_per_row > 0 else 0)
for i in range(num_rows):
    # Create a new row
    cols = st.columns(plots_per_row)
    for j in range(plots_per_row):
        # Calculate district index
        district_index = i * plots_per_row + j
        if district_index < len(districts):
            # Get the current district name
            district_name = districts[district_index]
            # Filter data for the current district
            district_df = df[df['District_name'] == district_name]
            #Plot
            fig = px.scatter(district_df, x='Transaction_count', y='Transaction_amount',
                             color='Year', trendline="ols",
                             title=f"{district_name}",
                             labels={"Transaction_count": "Transaction Count",
                                     "Transaction_amount": "Transaction Amount"},
                             height=450, width=450)  # Adjust height as needed
            # Display plot in the corresponding column
            with cols[j]:
                st.plotly_chart(fig)

#------------------Show User_count Vs Application_open in scatter tendline plot from map_user table----------------------------------------------------
# Function to query unique values for 'State'
def get_unique_states_map_user():
    cursor.execute("SELECT DISTINCT State FROM map_user ORDER BY State")
    states = cursor.fetchall()
    return [state[0] for state in states]
# Function to query unique 'District_name' for a given 'State'
def get_districts_for_state_map_user(state):
    cursor.execute("SELECT DISTINCT District_name FROM map_user WHERE State = %s ORDER BY District_name", (state,))
    districts = cursor.fetchall()
    return [district[0] for district in districts]
# Function to get data based on 'State' and 'District_name'
def get_data_map_user(state, district_name):
    cursor.execute("""
        SELECT Year, User_count, Application_open 
        FROM map_user 
        WHERE State = %s AND District_name = %s 
        ORDER BY Year
    """, (state, district_name))
    data = cursor.fetchall()
    return pd.DataFrame(data, columns=['Year', 'User_count', 'Application_open'])
# Streamlit subheader
st.subheader("Districtwise User_count Vs Application Open")
# # Dropdowns for State
states = get_unique_states_map_user()
selected_state = st.selectbox("Select State MU", states)
# Dropdown for 'District_name', dynamically updated based on 'State'
districts = get_districts_for_state_map_user(selected_state)
selected_district_name = st.selectbox("Select District Name MU", districts)

# Get and display data
df = get_data_map_user(selected_state, selected_district_name)
# Convert 'Year' to a string to ensure distinct coloring
df['Year'] = df['Year'].astype(str)
# Create a scatter trendline plot
fig = px.scatter(df, x='User_count', y='Application_open', color='Year',
                 trendline="lowess", labels={"User_count": "User_count", "Application_open": "Application Open"},
                 title="User_count vs Application Open by Year")
st.plotly_chart(fig)

#---------------Show District Vs Registered_users in stacked bar chart from top_user_dist table-----------------------
# Function to get unique states
def get_unique_states_tud():
    cursor.execute("SELECT DISTINCT State FROM top_user_dist ORDER BY State")
    states = cursor.fetchall()
    return [state[0] for state in states]

def get_unique_years_tud():
    cursor.execute("SELECT DISTINCT Year FROM top_user_dist ORDER BY Year")
    years = cursor.fetchall()
    return [year[0] for year in years]

# Function to fetch data for a given state and year
def get_data_tud(state, year):
    cursor.execute("""
        SELECT District_name, Quarter, Registered_users
        FROM top_user_dist
        WHERE State = %s AND Year = %s
        ORDER BY District_name, Quarter
    """, (state, year))
    data = cursor.fetchall()
    return pd.DataFrame(data, columns=['District_name', 'Quarter', 'Registered_users'])

# Streamlit UI
st.subheader("District-wise Registered Users Analysis")
# Dropdown for 'State'
states = get_unique_states_tud()
selected_state = st.selectbox("Select State TUD", states)
# Dropdown for 'Year'
years = get_unique_years_tud()
selected_year = st.selectbox("Select Year TUD", years)
# Fetch data for the selected state and year
df = get_data_tud(selected_state, selected_year) #int(selected_year))

# Pivot the DataFrame for stacked bar chart
df_pivot = df.pivot_table(index='District_name', columns='Quarter', values='Registered_users',
                          fill_value=0).reset_index()
# Plotly stacked bar chart
fig = px.bar(df_pivot, x='District_name', y=[1, 2, 3, 4],
             title=f"Registered Users in {selected_state}, {selected_year}",
             labels={'value': 'Registered Users', 'District_name': 'District'},
             text_auto=True)
st.plotly_chart(fig)

#---------------Show Registered_users as Distribution based on Pincode in stacked top_user_pincode table-----------------------
def get_unique_values_tup(column_name):
    query = f"SELECT DISTINCT {column_name} FROM top_user_pincode ORDER BY {column_name}"
    cursor.execute(query)
    values = cursor.fetchall()
    return [value[0] for value in values]

def get_data_tup(state, year, quarter):
    query = """
        SELECT Pincode, Registered_users
        FROM top_user_pincode
        WHERE State = %s AND Year = %s AND Quarter = %s
        ORDER BY Pincode
    """
    #SELECT Pincode, Registered_users
    #ORDER BYPincode
    cursor.execute(query, (state, year, quarter))
    data = cursor.fetchall()
    return pd.DataFrame(data, columns=['Pincode', 'Registered_users'])
    #return pd.DataFrame(data, columns=['Registered_users'])

# Streamlit UI
st.subheader("Pincode-wise Distribution of Registered Users")
# Dropdowns for 'State', 'Year', and 'Quarter'
states = get_unique_values_tup('State')
selected_state = st.selectbox("Select State TUP", states)
years = get_unique_values_tup('Year')
selected_year = st.selectbox("Select Year TUP", years)
quarters = get_unique_values_tup('Quarter')
selected_quarter = st.selectbox("Select Quarter TUP", quarters)
# Get data based on above selections
df = get_data_tup(selected_state, selected_year, selected_quarter)
st.write(df)
#Display Dist plot
fig = px.histogram(df, x='Registered_users',
                   title=f"Distribution of Registered Users - {selected_state}, {selected_year} Q{selected_quarter}",
                   labels={"Registered_users": "Registered Users"},
                   marginal="rug", nbins=10)
st.plotly_chart(fig)

cursor.close()
cnx.close()

