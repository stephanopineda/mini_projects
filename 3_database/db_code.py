import sqlite3
import pandas as pd 

# Database
conn = sqlite3.connect('./3_database/STAFF.db')
table_name = "INSTRUCTOR"

# Column Names
attribute_list = ['ID', 'FNAME', 'LNAME', 'CITY', 'CCODE']
file_path = './3_database/INSTRUCTOR.csv'
df = pd.read_csv(file_path, names=attribute_list)

# Transfer to Database
# if_exists parameters: 'fail', 'replace', 'append'
df.to_sql(table_name, conn, if_exists='replace', index=False)

# Access the database
query_statement = f"SELECT * FROM {table_name}"
query_output = pd.read_sql(query_statement, conn)

print(query_statement)
print(query_output)

query_statement = f"SELECT COUNT(*) FROM {table_name}"
query_output = pd.read_sql(query_statement, conn)
print(query_statement)
print(query_output)

data_dict = {
    'ID' : [100],
    'FNAME' : ['John'],
    'LNAME' : ['Doe'],
    'CITY' : ['Paris'],
    'CCODE' : ['FR']
}
data_append = pd.DataFrame(data_dict)

data_append.to_sql(table_name, conn, if_exists='append', index=False)
print('Data appended successfully')

query_statement = f"SELECT * FROM {table_name}"
query_output = pd.read_sql(query_statement, conn)
print(query_statement)
print(query_output)

conn.close()