'''
This code is an ETL code for webscraping specifically a webpage from wikipedia.
This will extract a table, transform the data, and store it in csv and database.
This is a project in coursera course "Python Project for Data Engineering by IBM."
'''
from datetime import datetime
import sqlite3
import requests
from bs4 import BeautifulSoup
import pandas as pd

PROJECT_PATH = './5_project_bank_market'
LOG_FILE_PATH = '/code_log.txt'

def log_progress(message):
    ''' Saves message to a text log specified in the log path.
    
    Args:
        message (str): The message to be logged.
    Returns:
        None
    '''
    with open(PROJECT_PATH + LOG_FILE_PATH, 'a', encoding="utf-8") as log_file:
        log_file.write(f'{datetime.now().strftime('%Y-%h-%d %H:%M:%S')} : {message} \n')
        # print(f'{datetime.now().strftime('%Y-%h-%d %H:%M:%S')} {message}')

def extract(url, table_attributes, table_index=0):
    ''' Extracts table from a web page using BeautifulSoup. Converts the table to a DataFrame.

    Args:
        url (str): The url of the webpage containing the table.
        table_attributes (list): List of column names to be used in the dataframe.
        table_index (int): Index of the table in the webpage (default is 0).

    Returns:
        pandas.DataFrame: The extracted table in DataFrame format. 
    '''
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')

    tables = soup.find_all('tbody')
    if table_index >= len(tables):
        raise ValueError(f"Index {table_index} is out of range. Found {len(tables)} <tbody>.")
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

def run_query(query_statement, sql_connection):
    '''Prints the passed SQL query and the output on the terminal.
    
    Args:
        query_statement (str): SQL Query to be executed.
        sql_connection (Connection): Connection to the selected database.

    Returns:
        pandas.DataFrame: the query output as DataFrame 
    '''
    print(query_statement)
    return pd.read_sql(query_statement, sql_connection)

# Main Code

BANKS_URL = 'https://web.archive.org/web/20230908091635/\
https://en.wikipedia.org/wiki/List_of_largest_banks'
EXCHANGE_RATE_CSV_PATH = '/exchange_rate.csv'
BANK_TABLE_ATTRIBS = ['Name', 'MC_USD_Billion']
BANK_TABLE_ATTRIBS_FINAL = ['Name',
                            'MC_USD_Billion', 
                            'MC_GBP_Billion',
                            'MC_EUR_Billion', 
                            'MC_INR_Billion']

BANK_CSV_PATH = '/Largest_banks_data.csv'
BANK_DB_PATH = '/Banks.db'
BANK_TABLE_NAME = 'largest_banks'

log_progress('Preliminaries complete. Initiating ETL process.')
banks_df = extract(BANKS_URL, BANK_TABLE_ATTRIBS)
log_progress('Data extraction complete. Initiating Transformation process')
banks_df = transform(banks_df, PROJECT_PATH+EXCHANGE_RATE_CSV_PATH, BANK_TABLE_ATTRIBS_FINAL)
log_progress('Data transformation complete. Initiating Loading process')
load_to_csv(banks_df, PROJECT_PATH+BANK_CSV_PATH)
log_progress('Data saved to CSV file')
conn = sqlite3.connect(PROJECT_PATH+BANK_DB_PATH)
log_progress('SQL Connection initiated')
load_to_db(banks_df, conn, BANK_TABLE_NAME)
log_progress('Data loaded to Database as a table, Executing queries')
QUERY1 = 'SELECT * FROM Largest_banks'
QUERY2 = 'SELECT AVG(MC_GBP_Billion) FROM Largest_banks'
QUERY3 = 'SELECT Name from Largest_banks LIMIT 5'
print(run_query(QUERY1, conn))
print(run_query(QUERY2, conn))
print(run_query(QUERY3, conn))
log_progress('Process Complete')
conn.close()
log_progress('Server Connection closed')
