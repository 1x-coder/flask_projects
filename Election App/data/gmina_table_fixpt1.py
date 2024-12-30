import pandas as pd
from sqlalchemy import create_engine
from db_config import DB_CONFIG

df = pd.read_csv('.\\raw_data\\final_committee_table.csv').applymap(lambda x: x.rstrip() if isinstance(x, str) else x)

gmina_df = pd.DataFrame({'id': range(1, len(df['gmina'].unique()) + 1), 'name': df['gmina'].unique()})

# Adding 'type' column:
def determine_type(name):
    if name.startswith('m. '):
        return 'miasto'
    elif name.startswith('gm. '):
        return 'gmina'
    else:
        return 'dzielnica'

gmina_df['type'] = gmina_df['name'].apply(determine_type)

# Removing the 'gm. ' or 'm. ' prefixes
def remove_prefix(name):
    if name.startswith('m. '):
        return name[3:]
    elif name.startswith('gm. '):
        return name[4:]
    else:
        return name

gmina_df['name'] = gmina_df['name'].apply(remove_prefix)

# Removing records where type == 'miasto'
gmina_df = gmina_df[gmina_df['type'] != 'miasto']

# Dropping the type column
gmina_df = gmina_df.drop('type', axis=1)

connection_string = f"mysql+mysqlconnector://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:3306/{DB_CONFIG['database']}"
db_engine = create_engine(connection_string)

gmina_df.to_sql('gmina', con=db_engine, if_exists='replace', index=False)

db_engine.dispose()