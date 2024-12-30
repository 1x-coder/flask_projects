import pandas as pd
from db_config import DB_CONFIG
import mysql.connector

#Reading placowka table to then parse it
df = None

try:
    connection = mysql.connector.connect(**DB_CONFIG)
    cursor = connection.cursor()

    query = "SELECT * FROM placowka;"

    df = pd.read_sql_query(query, connection)

except mysql.connector.Error as e:
    print(f"Error: {e}")

finally:
    connection.close()

#Adding 'post_code' column
df['post_code'] = df['nazwa_adres'].str.extract(r'(\d{2}-\d{3})')

#Removing post code and city name from name / address column
df['nazwa_adres'] = df['nazwa_adres'].str.replace(r', \d{2}-\d{3}.*$', '', regex=True)

#Splitting the address column by ',' and exporting the df to csv to parse it by hand in excel
df[['col1', 'col2', 'col3', 'col4', 'col5']] = df['nazwa_adres'].str.split(',', expand=True)
df.to_csv('db_restructure.csv', index=False)