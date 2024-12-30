import pandas as pd
import numpy as np
#NOTE: excluded data from abroad, it was messing up the file structure

df = pd.read_csv('raw_data\\obwody_glosowania_utf8.csv', delimiter='\t', encoding='utf-8', header=0)
df = df.drop(columns=['typ_obwodu', 'typ_obszaru'])

#Creating 'Gmina' table by getting unique gminy names and id's from the set
gminy_table_df = df.drop_duplicates(subset=['gmina'])
gminy_table_df = gminy_table_df.drop(['nr_komisji', 'siedziba', 'powiat', 'wojewodztwo', 'okrag', 'mieszkancy', 'wyborcy'], axis=1)
gminy_table_df.reset_index(inplace=True, drop=True)
gminy_table_df.rename(columns={'teryt_gminy': 'id', 'gmina': 'nazwa'}, inplace=True)

#Creating table 'Okrag'
okrag_table_df = pd.read_csv('raw_data\\okregi_sejm_utf8.csv', delimiter=',', encoding='utf-8', header=0)
okrag_table_df.drop(columns={'opis_granic'}, inplace=True)

#Creating table 'Placowka' 
placowka_table_df = df.groupby('siedziba').agg({'mieszkancy': 'sum', 'wyborcy': 'sum'}).reset_index()
placowka_table_df.sort_values(by='siedziba', ascending=True, inplace=True)
placowka_table_df.rename(columns={'siedziba': 'placowka'}, inplace=True)
placowka_table_df['id'] = placowka_table_df.index + 1   
placowka_table_df = placowka_table_df[['id', 'placowka', 'mieszkancy', 'wyborcy']] 

#Extend placowka with previously dropped data
placowka_no_dupes = df.drop_duplicates('siedziba')
placowka_no_dupes.reset_index(inplace=True, drop=True)

placowka_table_df = pd.merge(placowka_table_df, placowka_no_dupes, left_on='placowka', right_on='siedziba', how='left')
placowka_table_df.drop(columns=['nr_komisji', 'siedziba', 'teryt_gminy','mieszkancy_y', 'wyborcy_y'], inplace=True)

#Rearanging columns, renaming
placowka_table_df = placowka_table_df.rename(columns={
    'placowka': 'nazwa',
    'mieszkancy_x': 'mieszkancy', 
    'wyborcy_x': 'wyborcy', 
    'powiat': 'powiat', 
    'wojewodztwo': 'wojewodztwo',
    'okrag': 'okrag_id'
})

#Adding miasto column to 'placowka_table_df' by splitting nazwa, checking if every row matches.
kod_poczt_miasto = placowka_table_df['nazwa'].str.split(',').str[-1]
condition = kod_poczt_miasto.str.contains(r'\d{2}-\d{3} .+')

# pd.options.display.max_colwidth=1000
# print(placowka_table_df[~condition])

#Only 9 rows dont match, changing them manually:
placowka_table_df.at[4518, 'nazwa'] = 'Kopalnia Kultury w Czeladzi, Czeladź ul. Stanisława Trznadla 1, 41-253 Czeladź'
placowka_table_df.at[7466, 'nazwa'] = 'Przedszkole nr 10, Czeladź ul. Stefana Żeromskiego 19, 41-253 Czeladź'
placowka_table_df.at[7602, 'nazwa'] = 'Przedszkole nr 5, Czeladź ul. Krótka 1, 41-253 Czeladź'
placowka_table_df.at[14896, 'nazwa'] = 'Szkoła Podstawowa nr 5, Czeladź ul. Lwowska 2, 41-253 Czeladź'
placowka_table_df.at[15035, 'nazwa'] = 'Szkoła Podstawowa nr 7, Czeladź ul. Spacerowa 2, 41-253 Czeladź'
placowka_table_df.at[1679, 'nazwa'] = 'Dom Katechetyczny, Katowice ul. Tadeusza Boya Żeleńskiego 34, 40-750 Katowice'
placowka_table_df.at[18824, 'nazwa'] = 'Szpital, Katowice ul. Władysława Stanisława Reymonta 8, 40-029 Katowice'
placowka_table_df.at[1580, 'nazwa'] = 'Centrum Usług Społecznych w Łapach, Łapy ul. Główna 50, 18-100 Łapy'
placowka_table_df.at[6485, 'nazwa'] = 'Powiatowy Publiczny Zakład Opieki Zdrowotnej w Rydułtowach i Wodzisławiu Śląskim z siedzibą w Wodzisławiu Śląskim, Wodzisław Śląski ul. 26 Marca 51, 44-300 Wodzisław Śląski'

#Adding miasto_nazwa column: 
placowka_table_df['miasto'] = placowka_table_df['nazwa'].str.split(',').str[-1]
placowka_table_df['miasto'] = placowka_table_df['miasto'].str.strip()

#Getting rid of post codes:
for index, row in placowka_table_df.iterrows():
    split = row['miasto'].split(' ')
    new_name = ''
    for i, element in enumerate(split):
        if i == 0:
            continue
        if i == len(split) - 1:
            new_name += element
        else:
            new_name += (element + ' ')
    placowka_table_df.at[index, 'miasto'] = new_name

#Cleaning some invalid data:
placowka_table_df['miasto'] = placowka_table_df['miasto'].str.replace(r'\s\d+', '', regex=True)

#Decided to drop columns wyborcy and mieszkancy
placowka_table_df.drop(columns=['mieszkancy', 'wyborcy'], inplace=True)

#Final column rearrangement
placowka_table_df = placowka_table_df[['id', 'nazwa', 'miasto', 'gmina', 'powiat', 'wojewodztwo', 'okrag_id']]

#Creating 'Komitet' table manually
komitet_table_data =  {
    'id': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
    'nazwa': [
        'Bezpartyjni Samorządowcy',
        'Trzecia Droga Polska 2050 Szymona Hołowni - Polskie Stronnictwo Ludowe',
        'Nowa Lewica',
        'Prawo i Sprawiedliwość',
        'Konfederacja Wolność i Niepodległość',
        'Koalicja Obywatelska',
        'Polska Jest Jedna',
        'Ruch Dobrobytu i Pokoju',
        'Normalny Kraj',
        'Antypartia',
        'Ruch Naprawy Polski',
        'Mniejszość Niemiecka'
    ],
    'skrot': [
        'BS',
        '3D', 
        'NL',
        'PiS',
        'Konfederacja',
        'KO',
        'PJJ',
        'DiP',
        'NK',
        'AP',
        'RNP',
        'MN'
    ]
}

komitet_table_df = pd.DataFrame(komitet_table_data)

#Creating placowka_wyniki_df
placowka_wyniki_df = pd.read_csv('raw_data\\wyniki_gl_na_listy_po_obwodach_sejm_utf8.csv', delimiter='\t', encoding='utf-8', header=0)
placowka_wyniki_df = placowka_wyniki_df.drop(['nr_komisji', 'teryt_gminy', 'gmina', 'powiat', 'wojewodztwo', 'okrag'], axis=1)
placowka_wyniki_df.reset_index(inplace=True, drop=True)
placowka_wyniki_df.rename(columns={'siedziba': 'placowka'}, inplace=True)

#Changing NaN's to zeros.
placowka_wyniki_df.fillna(0, inplace=True)

#Changing columns where dtype is float64 to int
for column in placowka_wyniki_df.columns:
    if placowka_wyniki_df[column].dtype == np.float64:
        placowka_wyniki_df[column] = placowka_wyniki_df[column].astype(int)

#Grouping by 'placowka', summing every other column
placowka_wyniki_df = placowka_wyniki_df.groupby('placowka').agg({
    'bezpartyjni_sam': 'sum', 
    '2050_trzecia_droga': 'sum',
    'nowa_lewica': 'sum',
    'pis': 'sum',
    'konfa': 'sum',
    'ko': 'sum',
    'polska_jest_jedna': 'sum',
    'dobrobyt_i_pokoj': 'sum',
    'normalny_kraj': 'sum',
    'antypartia': 'sum',
    'ruch_naprawy_polski': 'sum',
    'mniejszosc_niemiecka': 'sum'
}).reset_index()

placowka_wyniki_df.rename(columns={
    'bezpartyjni_sam': 'BS', 
    '2050_trzecia_droga': '3D', 
    'nowa_lewica': 'NL', 
    'pis': 'PiS', 
    'konfa': 'Konfederacja', 
    'ko': 'KO',
    'polska_jest_jedna': 'PJJ', 
    'dobrobyt_i_pokoj': 'DiP', 
    'normalny_kraj': 'NK',
    'antypartia': 'AP',
    'ruch_naprawy_polski': 'RNP',
    'mniejszosc_niemiecka': 'MN'
}, inplace=True)

#Applying same changes here as in placowka_table_df, to join the two later
placowka_wyniki_df.at[4518, 'placowka'] = 'Kopalnia Kultury w Czeladzi, Czeladź ul. Stanisława Trznadla 1, 41-253 Czeladź'
placowka_wyniki_df.at[7466, 'placowka'] = 'Przedszkole nr 10, Czeladź ul. Stefana Żeromskiego 19, 41-253 Czeladź'
placowka_wyniki_df.at[7602, 'placowka'] = 'Przedszkole nr 5, Czeladź ul. Krótka 1, 41-253 Czeladź'
placowka_wyniki_df.at[14896, 'placowka'] = 'Szkoła Podstawowa nr 5, Czeladź ul. Lwowska 2, 41-253 Czeladź'
placowka_wyniki_df.at[15035, 'placowka'] = 'Szkoła Podstawowa nr 7, Czeladź ul. Spacerowa 2, 41-253 Czeladź'
placowka_wyniki_df.at[1679, 'placowka'] = 'Dom Katechetyczny, Katowice ul. Tadeusza Boya Żeleńskiego 34, 40-750 Katowice'
placowka_wyniki_df.at[18824, 'placowka'] = 'Szpital, Katowice ul. Władysława Stanisława Reymonta 8, 40-029 Katowice'
placowka_wyniki_df.at[1580, 'placowka'] = 'Centrum Usług Społecznych w Łapach, Łapy ul. Główna 50, 18-100 Łapy'
placowka_wyniki_df.at[6485, 'placowka'] = 'Powiatowy Publiczny Zakład Opieki Zdrowotnej w Rydułtowach i Wodzisławiu Śląskim z siedzibą w Wodzisławiu Śląskim, Wodzisław Śląski ul. 26 Marca 51, 44-300 Wodzisław Śląski'

#Applying melt, changing the df format from wide to long
placowka_wyniki_df = pd.melt(placowka_wyniki_df, id_vars=['placowka'], var_name='komitet', value_name='glosow')
placowka_wyniki_df.sort_values(by='placowka', inplace=True)
placowka_wyniki_df.reset_index(inplace=True, drop=True)

#Changing 'komitet' names to their respective id's from komitet_table_df
placowka_wyniki_df = placowka_wyniki_df.merge(komitet_table_df, left_on='komitet', right_on='skrot', how='left')
placowka_wyniki_df = placowka_wyniki_df.drop(['komitet', 'nazwa', 'skrot'], axis=1)
placowka_wyniki_df = placowka_wyniki_df[['placowka', 'id', 'glosow']]
placowka_wyniki_df.rename(columns={'id': 'komitet_id'}, inplace=True)

#Merging placowka_table_df with placowka_wyniki_df, changing to id's
placowka_wyniki_df = pd.merge(placowka_wyniki_df, placowka_table_df, left_on='placowka', right_on='nazwa', how='left')
placowka_wyniki_df.drop(columns=['placowka', 'nazwa', 'miasto', 'gmina', 'powiat', 'wojewodztwo', 'okrag_id'], inplace=True)
placowka_wyniki_df.rename(columns={'id': 'placowka_id'}, inplace=True)
placowka_wyniki_df = placowka_wyniki_df[['placowka_id', 'komitet_id', 'glosow']]