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