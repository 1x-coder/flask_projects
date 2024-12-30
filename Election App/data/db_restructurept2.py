import pandas as pd
from sqlalchemy import create_engine
from db_config import DB_CONFIG
from data_parser import komitet_table_df, placowka_wyniki_df

#Reading table from csv, removing trailing whitespaces from every column.
df = pd.read_csv('final_committee_table.csv').applymap(lambda x: x.rstrip() if isinstance(x, str) else x)

#Merging cities_df with df to change city names for their id's
cities_df = pd.DataFrame({'id': range(1, len(df['city'].unique()) + 1), 'name': df['city'].unique()})
df = pd.merge(df, cities_df, left_on='city', right_on='name', how='left')
df.drop(['city', 'name_y'], axis=1, inplace=True)
df.rename(columns={'id_y': 'city_id'}, inplace=True)

#Doing the same thing for powiat, gmina, wojewodztwo.
gmina_df = pd.DataFrame({'id': range(1, len(df['gmina'].unique()) + 1), 'name': df['gmina'].unique()})
df = pd.merge(df, gmina_df, left_on='gmina', right_on='name', how='left')
df.drop(['name', 'gmina'], axis=1, inplace=True)
df.rename(columns={'id': 'gmina_id'}, inplace=True)

powiat_df = pd.DataFrame({'id': range(1, len(df['powiat'].unique()) + 1), 'name': df['powiat'].unique()})
df = pd.merge(df, powiat_df, left_on='powiat', right_on='name', how='left')
df.drop(['name', 'powiat'], axis=1, inplace=True)
df.rename(columns={'id': 'powiat_id'}, inplace=True)

wojewodztwo_df = pd.DataFrame({'id': range(1, len(df['wojewodztwo'].unique()) + 1), 'name': df['wojewodztwo'].unique()})
df = pd.merge(df, wojewodztwo_df, left_on='wojewodztwo', right_on='name', how='left')
df.drop(['name', 'wojewodztwo'], axis=1, inplace=True)
df.rename(columns={'id': 'wojewodztwo_id'}, inplace=True)

df.rename(columns={'id_x': 'id', 'name_x': 'name'}, inplace=True)

komitet_table_df.rename(columns={'nazwa': 'name', 'skrot': 'shortname'}, inplace=True)
placowka_wyniki_df.rename(columns={'placowka_id': 'committee_id', 'komitet_id': 'party_id', 'glosow': 'num_of_votes'}, inplace=True)

#Inserting the modified tables after dropping the existing ones in mysql, using SQLAlchemy
connection_string = f"mysql+mysqlconnector://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:3306/{DB_CONFIG['database']}"
db_engine = create_engine(connection_string)

cities_df.to_sql('city', con=db_engine, if_exists='replace', index=False)
wojewodztwo_df.to_sql('wojewodztwo', con=db_engine, if_exists='replace', index=False)
gmina_df.to_sql('gmina', con=db_engine, if_exists='replace', index=False)
powiat_df.to_sql('powiat', con=db_engine, if_exists='replace', index=False)
komitet_table_df.to_sql('party', con=db_engine, if_exists='replace', index=False)
df.to_sql('committee', con=db_engine, if_exists='replace', index=False)
placowka_wyniki_df.to_sql('results', con=db_engine, if_exists='replace', index=False)

db_engine.dispose()