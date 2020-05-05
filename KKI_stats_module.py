"""
This module contains functions
for cleaning and manipulating data in
dataframe in order to make the data ready
for analysis.
"""

import pandas as pd

def search_for_substring(df, column_name, substr):
    """
    Searches for a specific substring in 
    each row of a column in a dataframe which contains the
    team names in each game. It inserts these team names into
    seperate columns.

    Parameters
    ----------
    df : dataframe
        pandas dataframe with data
    column_name : string
        name of the column we're iterating through
    substr : string
        string we're searching for in each row of column
    """

    # row_number variable used to keep track of which row
    # code is on. 
    row_number = 0
    home_team = ""
    away_team = ""

    for row in df[column_name]:
        # Blank row items are of datatype 'float' and 
        # all other row items are of datatype 'str'. 
        # Therefore we need to change each row item
        # to str in order to use find function below.
        str_row = str(row)
        # Check if str substr is in row item - find function
        # returns index of first char in substring if it 
        # exists in string, else -1. 
        if (str_row.find(substr) >-1 ):
            text_found = df.iloc[row_number,0]
            # Call function to determine which team is home/away.
            home_team, away_team = search_home_away_team(text_found)
            # Put home/away team name into same row
            # of 'Home team'/'Guest team' columns.
            df.loc[row_number, 'Home team'] = home_team      
            df.loc[row_number, 'Guest team'] = away_team
        
        # If substring not found then insert empty strings 
        # into columns.
        else:
            df.loc[row_number, 'Home team'] = home_team
            df.loc[row_number, 'Guest team'] = away_team

        row_number += 1

def search_home_away_team (game_text):
    """
    This function searches in string and returns
    the names of home team an away team.

    Parameters
    ----------
    game_text : string
        string containing name of home and away teams
    """

    # Teams in league
    teams = ['Valur', 'Haukar', 'KR', 'Fjölnir', 'ÍR', 'Tindastóll', 'Keflavík', 'Njarðvík', 'Þór Þorlákshöfn', 'Þór Akureyri', 'Stjarnan', 'Grindavík']
    for team in teams:
        # Home team name always starts at char[8].
        if (game_text.find(team) == 8):
            home_team = team
        # Team name after char[8] must therefore be away team.
        if (game_text.find(team) > 8):
            away_team = team
    return home_team, away_team

def search_for_beginning_of_teams (df, column_name, substr1, substr2):
    """
    This function puts information about whether
    player is on home or away team in appropriate
    columns.

    Parameters
    ----------
    df : dataframe
        dataframe with stats
    
    column_name : string
        name of dataframe column to search

    substr1 : string
        string to search row that proceeds
        player data for home team

    substr2 : string
        string to search row that proceeds
        player data for away team
    """

    row_number = 0
    # Switch to keep track of whether the player rows are 
    # for home or away teams. home_away_switch % 2 = 0 indicates
    # home team. home_away_switch % 2 = 1 indicates away team.
    home_away_switch = 0
    # Switch to keep track of where player rows begin and end.
    # 1 equals 'not player row', 0 equals 'player row'.
    on_off_switch = 1
    for row in df[column_name]:
        str_row = str(row)
        # If substring is in string then do
        if (str_row == substr1):
            home_away_switch += 1
            on_off_switch = 0
        if (str_row == substr2):
            on_off_switch = 1
        if (home_away_switch%2 == 1 and on_off_switch == 0 and str_row != substr1):
            df.loc[row_number,'Team'] = df.loc[row_number, 'Home team']
        elif(home_away_switch%2 == 0 and on_off_switch == 0 and str_row != substr1):
            df.loc[row_number,'Team'] = df.loc[row_number, 'Guest team']
        row_number += 1

def insert_game_id(df, column_name):
    """
    This function puts creates a counter and
    puts a running number for each game in 
    a seperate column so that each game has in
    id number.

    Parameters
    ----------
    df : dataframe
        dataframe with stats
    
    column_name : string
        name of dataframe column to search

    """
    row_number = 0
    game_counter = 0
    game_counter_switch = 0
    for row in df[column_name]:
        # When we encounter a row which is not empty
        # the counter and switch values change
        if (not pd.isnull(row)):
            if (game_counter_switch == 0):
                game_counter_switch = 1
                game_counter += 1
            # Call function to adjust game counter value since we
            # want same game number value despite game_counter 
            # increasing as we go from home to away team
            df.loc[row_number, 'Game number'] = game_counter_adjustm(game_counter)
        else:
            game_counter_switch = 0

        row_number += 1

def game_counter_adjustm(game_counter):
    """
    Returns a game_counter variable that
    is the same for home and away team

    Parameters
    ----------
    game_counter : int
        running count of number of times we switch between home
        and away teams in data
    """
    if (game_counter % 2 == 0):
        return game_counter / 2
    else:
        return game_counter // 2 + 1

def mark_remove_star(df):
    """
    Loop through 'Player' column and mark in a seperate
    column if name is "*" marked plus remove star which
    denotes a 'starter' in data.

    Parameters
    ----------
    df : dataframe
        dataframe with stats data
    """
    for row in range(len(df.index)):
        if (df.loc[row,'Player'][0] == '*'):
            df.loc[row, 'Starter'] = 1
            df.loc[row,'Player'] = df.loc[row,'Player'][1:]

def split_fraction(df, orig_col, col_a = None, col_b = None):
    """
    Iterates through column with combined 'attempt' and 'made'
    data and puts 'attempts' and 'made' shot into respective
    columns.

    Parameters
    ----------
    df : dataframe
        dataframe with stats data
    
    orig_col: string
        name of column with data to split
    
    col_a: string
        name of column to put made number of shots in

    col_b: string
        name of column to put attempted number of shots in
    """
    for row in range(len(df.index)):
        att_made_list = df.loc[row, orig_col].split('/')

        # Some rows are empty so they don't have two 
        # elements in list - that is why an if loop
        # must be implemented.
        if (len(att_made_list)==2):
            df.loc[row, col_a] = att_made_list[0]
            df.loc[row, col_b] = att_made_list[1]

def top_per_40_min(df, category, sortby, filter):
    """
    Returns dataframe with top players in category.

    Parameters
    ----------
    df : dataframe
        dataframe with stats data
    
    category: string
        name of column to use in ranking

    sortby: string
        name of column to sort by

    filter: int
        minimum number of minutes per game to be
        included in ranking
    """

    # Create dataframe grouped by players
    df_players = df.fillna(0).groupby(category, as_index = False).mean()
    df_players[sortby + ' per 40 min'] = df_players[sortby]/df_players['Minutes']*40

    # Filter players that played less than 40 min total during season
    df_players_sum = df.fillna(0).groupby(category, as_index = False).sum()
    df_players = df_players[df_players_sum['Minutes'] >= filter]

    # Sort by points per 40 min
    df_players = df_players.sort_values(by=[sortby + ' per 40 min'], ascending = False)[['Player', sortby + ' per 40 min','Minutes']]
    df_players.index = range(1,len(df_players)+1)

    return df_players