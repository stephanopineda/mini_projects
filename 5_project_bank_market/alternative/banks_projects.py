from datetime import datetime
import requests
from bs4 import BeautifulSoup
import pandas as pd 
import sqlite3

project_path = './5_project_bank_market/alternative'
log_file_path = '/code_log.txt'

def log_progress(message):
    with open(project_path + log_file_path, 'a') as log_file:
        log_file.write(f'[LOG] {message} \n')
        # print(f'{datetime.now().strftime('%Y-%h-%d %H:%M:%S')} {message}')
    
    return None

def extract(url, table_attributes, table_index=0):
    log_progress('Extracting data...')
    response = requests.get(url)
    if response.status_code == 200:
        page_content = BeautifulSoup(response.content, 'html.parser')
        table = page_content.find_all('table', attrs=table_attributes)
        if table:
            df = pd.read_html(str(table))[0]
            log_progress('Data extraction successful.')
        else:
            log_progress('No table found with the same attribs.')
            return pd.DataFrame()
    else:
        log_progress('Failed to fetch webpage.')
        return pd.DataFrame()



# Main Code

url = 'https://web.archive.org/web/20230908091635 /https://en.wikipedia.org/wiki/List_of_largest_banks'
exchange_rate_path_csv = '/exchange_rate.csv'
table_attributes = ['Rank', 'Bank name', 'Market cap (US$ billion)']
table_attributes_final = ['Name', 'MC_USD_Billion', 'MC_GBP_Billion', 'MC_EUR_Billion', 'MC_INR_Billion']

csv_path = '/Largest_banks_data.csv'
db_path = '/Banks.db'
table_name = 'largest_banks'

log_progress('Preliminaries complete. Initiating ETL process.')
df = extract(url, table_attributes)
