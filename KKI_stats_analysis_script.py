"""
A script analyzing basketball stats in csv file
into dataframe and cleaning data
"""

import pandas as pd
import KKI_stats_module as ksm

# Dataframe settings
pd.set_option('display.max_rows', 200)
pd.options.display.float_format = '{:,.1f}'.format

# Put excel sheet into dataframe
df = pd.read_csv('clean_stat_data.csv')

top = 50

''' Category leaders '''

# Points per minute leader
df_pts = ksm.top_per_40_min(df, 'Player', 'Pts', 40).head(top)
# print(df_pts.to_string(index=True))

# Rebounds per minute leader
df_reb = ksm.top_per_40_min(df, 'Player', 'Tot reb', 40).head(top)
# print(df_reb.to_string(index=True))

# Assists per minute leader
df_assists = ksm.top_per_40_min(df, 'Player', 'Assists', 40).head(top)
# print(df_assists.to_string(index=True))

''' Shooting percentage leader '''
pd.options.display.float_format = '{:,.2f}'.format

df_shooters = df.fillna(0).groupby('Player', as_index = False).sum()
df_shooters['Shots attempted'] = df_shooters['2a'] + df_shooters['3a'] + df_shooters['Fta']
df_shooters['Shots made - weighted'] = df_shooters['2m'] + df_shooters['3m']*1.5 + df_shooters['Ftm']*0.5
df_shooters['Effective shooting %'] = df_shooters['Shots made - weighted'] / df_shooters['Shots attempted']
# print(df_shooters)

# Sort
df_shooters = df_shooters.sort_values(by=['Effective shooting %'], ascending = False)[['Player', 'Effective shooting %', 'Shots attempted']]

# Filter shooters that shot less than 40 shots total during season
df_shooters = df_shooters[df_shooters['Shots attempted'] >= 40]
df_shooters.index = range(1,len(df_shooters)+1)
df_shooters = df_shooters.head(top)
# print(df_shooters)

''' Merged lists '''

# Merged list of pts and rebounds
df_pts_reb = pd.merge(df_pts, df_reb, on=['Player', 'Minutes'], how='inner')
# print(df_pts_reb)

# Merged list of pts, rebounds and assists
df_pts_reb_assists = pd.merge(df_pts_reb, df_assists, on=['Player', 'Minutes'], how='inner')
# print(df_pts_reb_assists)

# Merged list of pts, rebounds, assists and eff shooting %
df_pts_reb_assists_shooting = pd.merge(df_pts_reb_assists, df_shooters, on=['Player'], how='inner')
df_pts_reb_assists_shooting.index = range(1,len(df_pts_reb_assists_shooting)+1)
print(df_pts_reb_assists_shooting[['Pts per 40 min', 'Tot reb per 40 min', 'Assists per 40 min', 'Effective shooting %']])




