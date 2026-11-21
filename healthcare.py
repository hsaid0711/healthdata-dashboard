# Python script to transfer the WHO CSV data to and SQLITE3 db table
import pandas as pd

import sqlite3
# importing pycountry so I can validate all country codes are valid
import pycountry

# Load WHO CSV 
csv_path = 'data/WHO-COVID-19-global-daily-data.csv'
# specifying encoding as country names with special characters weren't displaying correctly
df = pd.read_csv(csv_path, encoding="utf-8")

# Save all country names to a file to help debug special character issue
# with open("countries.txt", "w", encoding="utf-8") as f:
#    for country in df['Country'].unique():
#        f.write(f"{country}\n")

# Rename columns
df = df.rename(columns={
    'Date_reported': 'date',
    'Country': 'country',
    'Country_code': 'country_code',
    'WHO_region': 'who_region',
    'New_cases': 'new_cases',
    'Cumulative_cases': 'cum_cases',
    'New_deaths': 'new_deaths',
    'Cumulative_deaths': 'cum_deaths'
})

# check the country codes against those listed in pycountry to filter out international conveyances etc

valid_codes = {c.alpha_2 for c in pycountry.countries}

df = df[df['country_code'].isin(valid_codes)]

# Exclude territories causing display issues in demo environment (for demonstration only)

df = df[
    (df['country_code'] != 'RE') &
    (df['country_code'] != 'CW')
]

# Connect to SQLite DB
conn = sqlite3.connect('covid_global.db')
cur = conn.cursor()

# Create table
cur.execute('''
CREATE TABLE IF NOT EXISTS covid_global (
    id INTEGER PRIMARY KEY,
    date TEXT,
    country TEXT,
    country_code TEXT,
    who_region TEXT,
    new_cases INTEGER,
    cum_cases INTEGER,
    new_deaths INTEGER,
    cum_deaths INTEGER
)
''')

# Insert data, AI used to check the syntax
for _, row in df.iterrows():
    cur.execute('''
        INSERT INTO covid_global (date, country, country_code, who_region, new_cases, cum_cases, new_deaths, cum_deaths)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        row['date'], row['country'], row['country_code'], row['who_region'],
        row['new_cases'], row['cum_cases'], row['new_deaths'], row['cum_deaths']
    ))

conn.commit()
conn.close()
