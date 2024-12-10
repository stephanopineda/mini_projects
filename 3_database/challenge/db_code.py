import sqlite3
import pandas as pd 

# 1. Prepare to connect and select the table
conn = sqlite3.connect('./3_database/STAFF.db')
table_name = "Departments"

# Convert csv to dataframe and ready the column names
attribute_list = ['DEPT_ID', 'DEP_NAME', 'MANAGER_ID', 'LOC_ID']
file_path = './3_database/Departments.csv'
df = pd.read_csv(file_path, names=attribute_list)

# 2. Convert data from df to database
# if_exists parameters: 'fail', 'replace', 'append'
df.to_sql(table_name, conn, if_exists='replace', index=False)

# 3. Append data as per instructions
data_dict = {
    'DEPT_ID' : [9],
    'DEP_NAME' : ['Quality Assurance'],
    'MANAGER_ID' : [30010],
    'LOC_ID' : ['L0010']
}
data_append = pd.DataFrame(data_dict)
data_append.to_sql(table_name, conn, if_exists='append', index=False)
print('Data appended successfully')

# 4a. View all entries in database
query_statement = f"SELECT * FROM {table_name}"
query_output = pd.read_sql(query_statement, conn)

print(query_statement)
print(query_output)

# 4b. View only department stores
query_statement = f"SELECT DISTINCT DEP_NAME FROM {table_name}"
query_output = pd.read_sql(query_statement, conn)
print(query_statement)
print(query_output)

# 4c. Count the total entries
query_statement = f"SELECT COUNT(*) FROM {table_name}"
query_output = pd.read_sql(query_statement, conn)
print(query_statement)
print(query_output)

conn.close()