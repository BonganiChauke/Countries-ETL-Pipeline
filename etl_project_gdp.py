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