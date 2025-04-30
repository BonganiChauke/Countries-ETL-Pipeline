# importing required libraries
import requests
import sqlite3
import pandas as pd
from bs4 import BeautifulSoup # type: ignore
import numpy as np
from datetime import datetime

# defining required entities
url = 'https://web.archive.org/web/20230902185326/https://en.wikipedia.org/wiki/List_of_countries_by_GDP_%28nominal%29'
table_attribs = ['Country', 'GDP_USD_millions']
db_name = 'World_Economies.db'
table_name = 'Countries_by_GDP'
csv_path = './Countries_by_GDP.csv'

# this function extracts the required information from the website and saves into a pandas dataframe. 
# The function returns a dataframe
def extract(url, table_attribs):
    # parsing html page into Beautiful Soup as text
    page = requests.get(url).text
    data = BeautifulSoup(page,'html.parser')
    df = pd.DataFrame(columns=table_attribs)
    
    # extracting html table information
    tables = data.find_all('tbody')
    rows = tables[2].find_all('tr')
    
    # to retrieve data all at once
    for row in rows:
        col = row.find_all('td')
        if len(col)!=0:
            if col[0].find('a') is not None and '—' not in col[2]:
                data_dict = {"Country": col[0].a.contents[0],
                             "GDP_USD_millions": col[2].contents[0]}
                # appending data into dataframe
                df1 = pd.DataFrame(data_dict, index=[0])
                df = pd.concat([df,df1], ignore_index=True)
    return df

# this function to convert GDP information from currency to float value
def transform(df):
    GDP_list = df["GDP_USD_millions"].tolist()
    GDP_list = [float("".join(x.split(','))) for x in GDP_list]
    GDP_list = [np.round(x/1000,2) for x in GDP_list]
    df["GDP_USD_millions"] = GDP_list
    df=df.rename(columns = {"GDP_USD_millions":"GDP_USD_billions"})
    return df

# loading data frame into a csv file
def load_to_csv(df, csv_path):
    df.to_csv(csv_path)
    
# loading data frame into sql database 
def load_to_db(df, sql_connection, table_name):
    df.to_sql(table_name, sql_connection, if_exists='replace', index=False)  

# function to query and print from the database
def run_query(query_statement, sql_connection):
    print(query_statement)
    query_output = pd.read_sql(query_statement, sql_connection)
    print(query_output) 


# function to log progress of each function 
def log_progress(message): 
    timestamp_format = '%Y-%h-%d-%H:%M:%S' # Year-Monthname-Day-Hour-Minute-Second 
    now = datetime.now() # get current timestamp 
    timestamp = now.strftime(timestamp_format) 
    with open("./etl_project_log.txt","a") as f: 
        f.write(timestamp + ' : ' + message + '\n')

# logging the extract function entry
log_progress('Initiating ETL process.')
df = extract(url, table_attribs)

# once extraction method complete log the transformation process
log_progress('Data extraction complete. Initiating Transformation process.')
df = transform(df) 

# once transformation method complete log the loading method to csv
log_progress('Data transformation complete. Initiating loading process')
load_to_csv(df, csv_path)       