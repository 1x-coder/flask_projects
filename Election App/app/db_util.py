import json
import mysql.connector
from db_config import DB_CONFIG

connection_pool = mysql.connector.pooling.MySQLConnectionPool(
    pool_name = "main_pool",
    pool_size = 5,
    **DB_CONFIG  
)

# Returns select query based on table name.
def get_select_query(keyword, table_name):
    if table_name == 'committee':
        return '''
            SELECT committee.id, CONCAT(committee.name, ', ', address, ', ', city.name, ', ', post_code)
            FROM committee
            INNER JOIN city ON committee.city_id = city.id
            WHERE CONCAT(committee.name, ', ', address, ', ', city.name, ', ', post_code) LIKE '%{}%'
            LIMIT 10;
        '''.format(keyword)
    else:
        return '''
            SELECT id, name 
            FROM {} 
            WHERE name LIKE '%{}%'
            LIMIT 10;
        '''.format(table_name, keyword)

# Returns matching records for the specified category and keyword.        
def get_matching_records(keyword, category):
    result = []

    try:
        with connection_pool.get_connection() as connection:
            with connection.cursor() as cursor:
                table_name = map_table_name(category)
                query = get_select_query(keyword, table_name)

                cursor.execute(query)

                result = cursor.fetchall()

                result = [{'id': item[0], 'body': item[1]} for item in result]

    except mysql.connector.Error as ce:
        print(f'Database Error: {ce}')
        raise ce

    except ValueError as ve:
        print(f'Value Error: {ve}')
        raise ve
    return json.dumps(result, ensure_ascii=False)

# Returns list with voting results for queried args.
def get_voting_results(id, category):
    results = []

    try:
        with connection_pool.get_connection() as connection:
            with connection.cursor() as cursor:
                table_name = map_table_name(category)
                
                if table_name == 'committee':
                    column_name = 'committee.id'
                else:
                    column_name = table_name + '_id'

                query = '''
                    SELECT party.name, party.shortname, party.color, SUM(num_of_votes) AS votes
                    FROM party 
                    INNER JOIN results ON results.party_id = party.id
                    INNER JOIN committee ON committee.id = results.committee_id
                    WHERE {} = {}
                    GROUP BY party.shortname, party.name, party.color
                    ORDER BY votes DESC;
                '''.format(column_name, id)

                cursor.execute(query)
            
                # Parsing the query result, casting num of votes to int, removing records where num_of_votes == 0.
                result = [{'name': name, 'shortname': shortname, 'color': color, 'num_of_votes': int(num_of_votes)}
                    for name, shortname, color, num_of_votes in cursor.fetchall() if num_of_votes != 0
                ]

                total_votes = sum(item['num_of_votes'] for item in result)

                # Extending the result list by assigning 'party_img_uri' and 'votes_percentage' to each item.
                result = [{
                    **item, 
                    'votes_percentage': round((item['num_of_votes'] / total_votes) * 100.00, 2),
                    'party_img_uri': 'static/img/' + item['shortname'] + '.png' 
                } for item in result]

    except mysql.connector.Error as ce:
        print(f'Database Error: {ce}')
        raise ce

    return json.dumps(result, ensure_ascii=False)

def map_table_name(category_id):
    if category_id == '1':
        return 'committee'
    elif category_id == '2':
        return 'city'
    elif category_id == '3':
        return 'gmina'
    elif category_id == '4':
        return 'powiat'
    elif category_id == '5':
        return 'wojewodztwo'
    else:
        raise ValueError(f'Invalid category_id: {category_id}')
    
# TODO: moze zrobic jakies lepsze wyszukiwanie niz prosty LIKE na kolumnie bazy.