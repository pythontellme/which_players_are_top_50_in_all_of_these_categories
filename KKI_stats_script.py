"""
A script for loading txt file with basketball stats
into dataframe and cleaning data
"""

import pandas as pd
import numpy as np

# Dataframe settings
pd.set_option('display.max_rows', 200)
pd.options.display.max_columns = 50

# Define column headers for dataframe
column_headers = ['Number','Player','Minutes','2m/2a','2%','3m/3a','3%','Fgm/Fga','Fg%','Fta/Ftm','Ft%','Off reb','Def reb','Tot reb','Assists','Fouls comm','Fouls against','Turnovers','Steals','Blocked shots','Blocked shot attempt','Efficiency','+/-','Pts','Unnamed: 24']

# Put txt file into dataframe
df = pd.read_csv('game_data.txt', sep='\t', names = column_headers)

# Add 'Home Team' column with empty rows
df['Home team'] = np.nan

# Add 'Gestalið' column with empty rows
df['Guest team'] = np.nan

# Call search_for_substring function which
# will result in home and away teams being
# added to appropriate columns.
ksm.search_for_substring(df, 'Number', 'Leikur:')

# Add player/team column
df['Team'] = np.nan

# Call function to add info about whether players are on 
# home or away team. String above first player in 'home team' 
# is always 'H/R' in data.
ksm.search_for_beginning_of_teams(df, 'Number','H/R', 'Lið')

# Add game_id column
df['Game number'] = np.nan

# Call function to insert number to count
# number of games
ksm.insert_game_id(df, 'Team')

# Delete rows empty rows and reset index
df.drop(df[pd.isnull(df['Team'])].index, inplace = True)
df = df.reset_index(drop=True)

# Add 'Starter column'
df['Starter'] = np.nan

# Call function to Remove star from names
# and mark starters in 'starter' column.
ksm.mark_remove_star(df)

# Minutes column: change minutes to decimal value
for row in range(len(df.index)):
    if (df.loc[row, 'Minutes'] == "-"):
        df.loc[row, 'Minutes'] = 0
    else:
        min = int(df.loc[row, 'Minutes'][:2])
        sec = int(df.loc[row, 'Minutes'][3:])
        df.loc[row, 'Minutes'] = min + sec/60

# Create new columns to hold data on attempts and made
# shots
df['2m'] = np.nan
df['2a'] = np.nan
df['3m'] = np.nan
df['3a'] = np.nan
df['Fgm'] = np.nan
df['Fga'] = np.nan
df['Ftm'] = np.nan
df['Fta'] = np.nan

# Call funtion to split data in columns with 'made and
# 'missed' shots into two seperate columns
ksm.split_fraction(df, '2m/2a', '2m', '2a')
ksm.split_fraction(df, '3m/3a', '3m', '3a')
ksm.split_fraction(df, 'Fgm/Fga', 'Fgm', 'Fga')
ksm.split_fraction(df, 'Fta/Ftm', 'Ftm', 'Fta')

# Convert columns to numeric data type
df['2m'] = pd.to_numeric(df['2m'])
df['2a'] = pd.to_numeric(df['2a'])
df['3m'] = pd.to_numeric(df['3m'])  
df['3a'] = pd.to_numeric(df['3a'])
df['Fgm'] = pd.to_numeric(df['Fgm'])
df['Fga'] = pd.to_numeric(df['Fga'])
df['Ftm'] = pd.to_numeric(df['Ftm'])
df['Fta'] = pd.to_numeric(df['Fta'])

# Set data types in columns
num_cols = [ 'Minutes', '2%', '3%', 'Fg%', 'Ft%',
        'Off reb', 'Def reb', 'Tot reb', 'Assists', 'Fouls comm',
        'Fouls against', 'Turnovers', 'Steals', 'Blocked shots',
        'Blocked shot attempt', 'Efficiency', '+/-', 'Pts'
        ]

for col in num_cols:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# Delete unnecessary columns
df = df.drop(['2m/2a', '2%', '3m/3a', '3%', 'Fgm/Fga', 'Fg%', 'Fta/Ftm', 'Ft%', 'Unnamed: 24'], axis=1)

# Export to csv file
df.to_csv('clean_stat_data.csv', index = False, encoding = 'utf-8')
