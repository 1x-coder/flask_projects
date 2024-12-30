from db_config import DB_CONFIG
import mysql.connector

connection_pool = mysql.connector.pooling.MySQLConnectionPool(
    pool_name = "main_pool",
    pool_size = 5,
    **DB_CONFIG  
)

try:
    with connection_pool.get_connection() as connection:
        with connection.cursor() as cursor:
            query = 'SELECT * FROM gmina;'

            cursor.execute(query)

            rows = cursor.fetchall()
            
            for row in rows:
                id = row[0]
                name = row[1]
                type = row[2]

                query = "UPDATE gmina SET name = %s WHERE id = %s"

                if type == 'gmina':
                    cursor.execute(query, (type + ' ' + name, id))

            connection.commit()

except mysql.connector.Error as ce:
    print(f'Database Error: {ce}')
    raise ce