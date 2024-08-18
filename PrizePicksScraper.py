import requests
import pandas as pd

pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth', None)


headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.79 Safari/537.36'
}

url = 'https://api.prizepicks.com/projections'

response = requests.get(url, headers=headers)

# Check the status code of the response
print(f"Status Code: {response.status_code}")

# Try to parse the JSON only if the status code indicates success
if response.status_code == 200:
    try:
        responseData = response.json()
        # Flatten the JSON data and create a dataframe
        df = pd.json_normalize(responseData, 'data')
        df2 = pd.json_normalize(responseData, 'included')
        print(df['attributes.game_id'].value_counts())

        # Remove the 'relationships.new_player.data.id' column
        df = df.drop(columns=['type', 'attributes.board_time', 'attributes.custom_image', 'attributes.rank',
                              'attributes.refundable', 'attributes.start_time', 'attributes.adjusted_odds',
                              'attributes.end_time', 'attributes.status', 'attributes.tv_channel',
                              'attributes.updated_at', 'relationships.duration.data', 'relationships.league.data.type',
                              'relationships.new_player.data.type', 'relationships.projection_type.data.type',
                              'relationships.stat_type.data.type', 'attributes.hr_20', 'attributes.today',
                              'relationships.duration.data.type', 'attributes.game_id'])
        df2 = df2.drop(
            columns=['type', 'attributes.display_name', 'attributes.image_url', 'relationships.league.data.type',
                     'attributes.lfg_ignored_leagues', 'attributes.rank', 'attributes.active', 'attributes.f2p_enabled',
                     'attributes.last_five_games_enabled', 'attributes.league_icon_id', 'attributes.projections_count',
                     'attributes.show_trending', 'relationships.projection_filters.data'])
        # Print the column names to understand the structure
        print("Column names:", df.columns)
        print("Column names:", df2.columns)
        df.rename(columns={'attributes.description': 'team', 'attributes.line_score': 'line', 'relationships.new_player.data.id': 'player_ID', 'attributes.league' : 'sport'}, inplace = True)

        # Add a new column 'player_ID' and populate it with data from the nested structure

        df_merged = pd.merge(df, df2, left_on='player_ID', right_on='id', how='inner')
        print(df_merged)

    except requests.exceptions.JSONDecodeError as e:
        print(f"JSONDecodeError: {e}")
else:
    print("Failed to retrieve data from the API")






















