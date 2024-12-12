# You have to complete the following tasks for this project
# 1. Write a data extraction function to retrieve the relevant information from the required URL.
# 2. Transform the available GDP information into 'Billion USD' from 'Million USD'.
# 3. Load the transformed information to the required CSV file and as a database file.
# 4. Run the required query on the database.
# 5. Log the progress of the code with appropriate timestamps.

# Code for ETL operations on Country-GDP data
# Importing the required libraries
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime
import requests
import sqlite3

def extract_1(url, table_attribs, table_index=2, start_row=1, first_col_index=0, second_col_index=1):
    ''' Extracts and processes a table from a webpage into a DataFrame. 
    
    Args: 
        url (str): The URL of the webpage containing the table.
        table_attribs (list): List of column names to assign to the DataFrame.
        table_index (int): Index of the table in the HTML to extract (default is 3).
        start_row (int): Starting row index to exclude any non-data rows (default is 1). 

    Returns:
        pandas.DataFrame: The extracted data in DataFrame format.
    '''

    # Read all the tables from the URL
    tables = pd.read_html(url)
    print(tables)

    # Ensure table index is valid
    if table_index >= len(tables):
        raise ValueError(f"Table index {table_index} is out of range. Only {len(tables)} are found.")

    # Extract specified table
    df = tables[table_index]

    # Select only the required rows and columns
    df = df.iloc[start_row:,[first_col_index,second_col_index]]

    # Ensure table_attribs has same length as the number of columns (df.shape[1]) of the selected table
    if len(table_attribs) != df.shape[1]:
        raise ValueError(f"Table attributes does not have the same number of colummns in the table.")
    
    # Change table header based on table attribs
    df.columns = table_attribs

    # Clean the data by removing null values in column 2
    df = df[df[table_attribs[1]] != '—']
    
    df.reset_index(inplace = True, drop = True)
    return df

def extract_2(url, table_attribs, table_index=2, first_col_index=0, second_col_index=1):
    ''' Extracts and processes a table from an HTML page using BeautifulSoup. 
    
    Args: 
        url (str): The URL of the webpage containing the table.
        table_attribs (list): List of column names to assign to the DataFrame.
        table_index (int): Index of the table in the HTML to extract (default is 2).

    Returns:
        pandas.DataFrame: The extracted data in DataFrame format.
    '''
    response = requests.get(url)
    response.raise_for_status()  # Raise an exception for HTTP errors
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the specified table body (tbody)
    tables = soup.find_all('tbody')
    if table_index >= len(tables):
        raise ValueError(f"Table index {table_index} is out of range. Found {len(tables)} <tbody> elements.")
    rows = tables[table_index].find_all('tr')

    # Initialize an empty list for the rows to be added to the DataFrame
    data = []

    # Loop through each row
    for row in rows:
        cols = row.find_all('td')
        
        # Skip rows without data or rows missing required columns
        if not cols or cols[first_col_index].find('a') is None or '—' in cols[second_col_index].text:
            continue
        
        # Extract data into a dictionary
        data.append({
            table_attribs[0]: cols[first_col_index].a.text.strip(),
            table_attribs[1]: cols[second_col_index].text.strip()
        })

    # Convert the collected data into a DataFrame
    df = pd.DataFrame(data, columns=table_attribs)
    return df
    

def transform(df, column_name, new_column_name=None):
    ''' 
    Converts the desired column (column_name) into float. 
    Divides it by 1000 and rounds it to 2 decimal places.
    Renames desired column with new_column_name.
    
    Args:
        df (pandas.DataFrame): The dataframe to be transformed.
        column_name (str): The column of the df to be transformed.
        new_column_name (str): New name for the transformed column.
    
    Returns:
        pandas.DataFrame: The transformed dataframe.
    '''
    
    # Determine the column name to use
    target_column = new_column_name if new_column_name else column_name

    # Remove commas, convert to float, divide by 1000, and round to 2 decimal places
    df[target_column] = (
        df[column_name]
        .str.replace(',', '', regex=True) # Remove commas
        .astype(float)                    # Convert to float
        .div(1000)                        # Convert to billions
        .round(2)                         # Round to 2 decimal places
    )
    
    # Drop the original column if a new column name is provided
    if new_column_name:
        df.drop(columns=[column_name], inplace=True)
    
    return df 

def load_to_csv(df, csv_path):
    ''' This function saves the final dataframe as a `CSV` file
    in the provided path. Function returns nothing.'''
    df.to_csv(csv_path, sep=',', encoding='utf-8', index=False)
    return None

def load_to_db(df, sql_connection, table_name):
    ''' This function saves the final dataframe as a database table 
    with the provided name. Function returns nothing.'''
    
    df.to_sql(table_name, sql_connection, if_exists='replace', index=False)
    
    return None
 
def run_query(query_statement, sql_connection):
    ''' This function runs the stated query on the database table and 
    prints the output on the terminal. Function returns nothing.
    Args:
        query_statement (str): SQL Query
        sql_connection (Connection): Database connection
        '''
    print(query_statement)
    return pd.read_sql(query_statement, sql_connection)


def _log_progress(message):
    ''' This function logs the mentioned message at a given 
    stage of the code execution to a log file. Function returns nothing.'''
    timestamp_format = '%Y-%h-%d %H:%M:%S' # Year-MonthName-Day-Hour-Minute-Second
    log_file_path = './4_project/log_file.txt'
    with open(log_file_path, 'a') as log_file:
        log_file.write(f'{datetime.now().strftime(timestamp_format)} {message} \n')
        # print(f'{datetime.now().strftime(timestamp_format)} {message} \n')


''' Here, you define the required entities and call the relevant 
functions in the correct order to complete the project. Note that this
portion is not inside any function.'''

_log_progress('Declaring known values.')

# url = 'https://web.archive.org/web/20230902185326/https://en.wikipedia.org/wiki/List_of_countries_by_GDP_%28nominal%29'
url = 'https://en.wikipedia.org/wiki/List_of_countries_by_GDP_%28nominal%29'
table_attribs = ['Country', 'GDP_USD_Millions']
db_name = './4_project/World_Economies.db'
table_name = 'Countries_by_GDP'
csv_path = './4_project/Countries_by_GDP.csv' 

_log_progress('Preliminaries complete. Initiating ETL process.')

df = extract_1(url, table_attribs)
print(df)

_log_progress('Data extraction complete. Initiating Transformation process.')

new_column_name = 'GDP_USD_Billions'
df = transform(df, table_attribs[1], new_column_name)
print(df)

_log_progress("Data transformation complete. Initiating loading process.")

load_to_csv(df, csv_path)

_log_progress("Data saved to CSV file.")

conn = sqlite3.connect(db_name)

_log_progress("SQL Connection initiated.")

load_to_db(df, conn, table_name)

_log_progress("Data loaded to Database as table. Running the query.")

query = f"SELECT * FROM {table_name} WHERE {new_column_name} >= 100"
print(run_query(query, conn))

_log_progress("Process Complete.")

conn.close()
