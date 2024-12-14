from datetime import datetime
import requests
from bs4 import BeautifulSoup
import pandas as pd 
import sqlite3

project_path = './5_project_bank_market'
log_file_path = '/code_log.txt'

def log_progress(message):
    with open(project_path + log_file_path, 'a') as log_file:
        log_file.write(f'{datetime.now().strftime('%Y-%h-%d %H:%M:%S')} : {message} \n')
        # print(f'{datetime.now().strftime('%Y-%h-%d %H:%M:%S')} {message}')
    
    return None

def extract(url, table_attributes, table_index=0):
    ''' Extracts table from a web page using BeautifulSoup. Converts the table to a DataFrame.

    Args:
        url (str): The url of the webpage containing the table.
        table_attributes (list): List of column names to be used in the dataframe.
        table_index (int): Index of the table in the webpage (default is 0).

    Returns:
        pandas.DataFrame: The extracted table in DataFrame format. 
    '''
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')

    tables = soup.find_all('tbody')
    if table_index >= len(tables):
        raise ValueError(f"Table index {table_index} is out of range. Found {len(tables)} <tbody> elements.")
    rows = tables[table_index].find_all('tr')

    data = []

    for row in rows:
        cols = row.find_all('td')
        
        if not cols: # If data is empty 
            continue

        data.append(
            {
                table_attributes[0]: cols[1].text.strip(),
                table_attributes[1]: float(cols[2].text.strip())
            }
        )

    df = pd.DataFrame(data, columns=table_attributes)
    return df

def transform(df, exchange_rate_csv_path, table_column_names):
    '''
    Adds new columns to the specified dataframe based on the table_column_names with
    values based on equivalent currency based on exchange rate specified in the csv.

    Args:
        df (pandas.DataFrame): The dataframe to be modified.
        exchange_rate_csv_path (str): File path of the csv for exchange rate.
        table_column_names (list): List of the resultant table names. 

    Returns:
        pandas.DataFrame: The modified DataFrame. 
    '''
    exchange_rate_df = pd.read_csv(exchange_rate_csv_path)
    exchange_rate = exchange_rate_df.set_index('Currency')['Rate'].to_dict()
    
    df[table_column_names[2]] = round(df['MC_USD_Billion'] * exchange_rate['GBP'], 2)
    df[table_column_names[3]] = round(df['MC_USD_Billion'] * exchange_rate['EUR'], 2)
    df[table_column_names[4]] = round(df['MC_USD_Billion'] * exchange_rate['INR'], 2) 
    
    print(df['MC_EUR_Billion'][4])
    return df

def load_to_csv(df, file_path):
    ''' Saves DataFrame into the specified csv filepath.

    Args:
        df (pandas.DataFrame): The dataframe to be saved.
        file_path (str): File path for the csv output.

    Returns:
        None
    '''
    df.to_csv(file_path, sep=',', encoding='utf-8', index=False)
    return None

def load_to_db(df, sql_conn, table_name):
    ''' Saves DataFrame into the specified database.

    Args:
        df (pandas.DataFrame): The dataframe to be saved.
        sql_conn (Cpnnection): SQLite3 connection object to the database.
        table_name (str): Name of the table for the dataframe in the database 

    Returns:
        None
    '''
    df.to_sql(table_name, sql_conn, if_exists='replace', index=False)
    return None

def run_query(query_statement, sql_connection):
    print(query_statement)
    return pd.read_sql(query_statement, sql_connection)

# Main Code

url = 'https://web.archive.org/web/20230908091635 /https://en.wikipedia.org/wiki/List_of_largest_banks'
exchange_rate_path_csv = '/exchange_rate.csv'
table_attributes = ['Name', 'MC_USD_Billion']
table_attributes_final = ['Name', 'MC_USD_Billion', 'MC_GBP_Billion', 'MC_EUR_Billion', 'MC_INR_Billion']

csv_path = '/Largest_banks_data.csv'
db_path = '/Banks.db'
table_name = 'largest_banks'

log_progress('Preliminaries complete. Initiating ETL process.')
df = extract(url, table_attributes)
log_progress('Data extraction complete. Initiating Transformation process')
df = transform(df, project_path+exchange_rate_path_csv, table_attributes_final)
log_progress('Data transformation complete. Initiating Loading process')
load_to_csv(df, project_path+csv_path)
log_progress('Data saved to CSV file')
conn = sqlite3.connect(project_path+db_path)
log_progress('SQL Connection initiated')
load_to_db(df, conn, table_name)
log_progress('Data loaded to Database as a table, Executing queries')
query1 = 'SELECT * FROM Largest_banks'
query2 = 'SELECT AVG(MC_GBP_Billion) FROM Largest_banks'
query3 = 'SELECT Name from Largest_banks LIMIT 5'
print(run_query(query1, conn))
print(run_query(query2, conn))
print(run_query(query3, conn))
log_progress('Process Complete')
conn.close()
log_progress('Server Connection closed')