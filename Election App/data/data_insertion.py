import pymysql
import traceback
from db_config import DB_CONFIG
from data_parser import placowka_table_df, placowka_wyniki_df, komitet_table_df, okrag_table_df

connection = pymysql.connect(
    host = DB_CONFIG['host'],
    user = DB_CONFIG['user'],
    password = DB_CONFIG['password'],
    database = DB_CONFIG['database'],
    charset='utf8mb4'
)

try:    
    cursor = connection.cursor()

    #Insert Okrag table  
    query = '''INSERT INTO okrag (id, liczba_mandatow, liczba_mieszkancow, liczba_wyborcow, siedziba_okw) VALUES (%s, %s, %s, %s, %s);'''
    for index, row in okrag_table_df.iterrows():
        values = (row['id'], row['liczba_mandatow'], row['liczba_mieszkancow'], row['liczba_wyborcow'], row['siedziba_okw'])
        cursor.execute(query, values)
    
    #Insert Placowka table
    query = '''INSERT INTO placowka (id, nazwa_adres, miasto, gmina, powiat, wojewodztwo, okrag_id) VALUES (%s, %s, %s, %s, %s, %s, %s);'''
    for index, row in placowka_table_df.iterrows():
        values = (row['id'], row['nazwa'], row['miasto'], row['gmina'], row['powiat'], row['wojewodztwo'], row['okrag_id'])
        cursor.execute(query, values)
    
    #Insert Komitet table
    query = '''INSERT INTO komitet (id, nazwa, skrot) VALUES (%s, %s, %s);'''
    for index, row in komitet_table_df.iterrows():
        values = (row['id'], row['nazwa'], row['skrot'])
        cursor.execute(query, values)

    #Insert Placowka_Wyniki table
    query = '''INSERT INTO placowka_wyniki (placowka_id, komitet_id, liczba_glosow) VALUES (%s, %s, %s);'''
    for index, row in placowka_wyniki_df.iterrows():
        values = (row['placowka_id'], row['komitet_id'], row['glosow'])
        cursor.execute(query, values)

    connection.commit()

except Exception as e:
    traceback.print_exc()
    print(f"Error: {str(e)}")
finally:
    cursor.close()
    connection.close()