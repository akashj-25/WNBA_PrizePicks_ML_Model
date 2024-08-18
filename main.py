from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd

wnba_teams = {
    "ATL": "Atlanta Dream",
    "CHI": "Chicago Sky",
    "CON": "Connecticut Sun",
    "DAL": "Dallas Wings",
    "IND": "Indiana Fever",
    "LAS": "Las Vegas Aces",
    "LVA": "Las Vegas Aces",
    "LAL": "Los Angeles Sparks",
    "MIN": "Minnesota Lynx",
    "NYL": "New York Liberty",
    "PHO": "Phoenix Mercury",
    "SEA": "Seattle Storm",
    "WAS": "Washington Mystics"
}
wnba_players = [
    "A'ja Wilson", "Aaliyah Edwards", "Abby Meyers", "Abby Williams", "Abigail Marotte",
    "Aerial Powers", "Aisha Sheppard", "Alanna Smith", "Alyssa Thomas", "Amanda Zahui",
    "Amy Atwell", "Anneli Maley", "Arike Ogunbowale", "Ashley Owusu", "Azura Stevens",
    "Brianna Turner", "Brittney Griner", "Brooklyn Bay", "Caitlin Clark", "Candace Parker",
    "Chelsea Gray", "Courtney Vandersloot", "Crystal Dangerfield", "Dana Evans",
    "Diamond DeShields", "Diana Taurasi", "DiJonai Carrington", "Elena Delle Donne",
    "Elizabeth Williams", "Emma Meesseman", "Erica Wheeler", "Gabby Williams", "Haley Jones",
    "Isabelle Harrison", "Jackie Young", "Jewell Loyd", "Jonquel Jones", "Jordan Canada",
    "Joyner Holmes", "Jordin Canada", "Jordin Son", "Joyce Billings", "Juhyun Park",
    "Kahleah Copper", "Kelsey Mitchell", "Kelsey Plum", "Kiah Stokes", "Kia Nurse",
    "Kristine Anigwe", "Kylee Shook", "Laeticia Amihere", "Lauren Cox", "Lauren Manis",
    "Lexie Brown", "Lindsay Allen", "Louise Brown", "Megan Gustafson", "Michaela Onyenwere",
    "Myisha Hines-Allen", "Napheesa Collier", "Natasha Cloud", "Natasha Howard",
    "Nneka Ogwumike", "Olivia Nelson-Ododa", "Parker Davis", "Rhyne Howard", "Ruthy Hebard",
    "Satou Sabally", "Sophie Cunningham", "Stephanie Mavunga", "Sydney Wiese", "Teaira McCowan",
    "Tiffany Mitchell", "Victoria Vivians", "Yueru Li", "Allisha Gray", "Alysha Clark",
    "Betnijah Laney", "Brionna Jones", "Cheyenne Parker", "Courtney Williams", "Dearica Hamby",
    "Ezi Magbegor", "Jasmine Thomas", "Kelsey Plum", "Lexie Brown", "Marina Mabrey",
    "Riquna Williams", "Skylar Diggins-Smith"
    # Add more players here
]

# Create a dictionary mapping player names to integers
player_dict = {player: index for index, player in enumerate(wnba_players, start=1)}

# Print the dictionary
print(player_dict)




# Adjust the display settings to show all columns and rows
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_colwidth', None)

# Set up the Chrome WebDriver
driver = webdriver.Chrome()
driver.get("https://stats.wnba.com/lineups/advanced/")
# Wait for the table to load (adjust the wait time and condition as needed)
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, '//table'))
)

# Locate the table
table = driver.find_element(By.XPATH, '//table')

# Extract the table headers
headers = [header.text for header in table.find_elements(By.XPATH, './/th')]

# Extract the table rows
rows = table.find_elements(By.XPATH, './/tr')[1:]  # Skip the header row

# Extract the data
data = []
for row in rows:
    cells = row.find_elements(By.XPATH, './/td')
    # Convert names in the first column (LINEUPS) to uppercase
    cells = ([cell.text for cell in cells])
    cells[0] = cells[0].upper()
    data.append(cells)

# Create a DataFrame
lineup_rating_data = pd.DataFrame(data, columns=headers)


print(lineup_rating_data.head())


# Open the first webpage
driver.get('https://stats.wnba.com/players/list/')

# Locate the player link by its visible text and click on it
player_name = "Wilson, A'ja"
list_element = driver.find_element(By.LINK_TEXT, player_name)
list_element.click()

# Wait for and click on the Profile tab
profile_tab = WebDriverWait(driver, 20).until(
    EC.element_to_be_clickable((By.LINK_TEXT, "Profile"))
)
profile_tab.click()

# Wait for and click on the Advanced Box Scores option
advanced_box_scores = WebDriverWait(driver, 20).until(
    EC.element_to_be_clickable((By.LINK_TEXT, "Advanced Box Scores"))
)
advanced_box_scores.click()

# Introduce a delay to ensure the table loads
time.sleep(5)

# Locate the table element and extract data
player_table = driver.find_element(By.CSS_SELECTOR, 'table')
headers = [header.text for header in player_table.find_elements(By.CSS_SELECTOR, 'th')]
rows = []
for row in player_table.find_elements(By.CSS_SELECTOR, 'tr')[1:]:  # Skip the header row
    cells = row.find_elements(By.CSS_SELECTOR, 'td')
    rows.append([cell.text for cell in cells])
player_df = pd.DataFrame(rows, columns=headers)

# Initialize lists to store starting lineups and opposing lineups for each game
starting_lineups = []
opposing_lineups = []
print(player_df)
# Iterate over each link in the "MATCH UP" column
matchup_links = player_table.find_elements(By.XPATH, "//td[1]/a")
num_links = len(matchup_links)
num_links = num_links // 2  # Adjust to avoid processing both home and away links
for i in range(num_links):
    # Re-fetch the links to ensure they are up-to-date after navigation
    matchup_links = driver.find_elements(By.XPATH, "//td[1]/a")
    if i >= len(matchup_links):
        break
    link = matchup_links[i]
    link_text = link.text
    if link_text[-5] != '@':
        team1 = wnba_teams[link_text[-3:]]
        team2 = wnba_teams[link_text[-11:-8]]
    else:
        team1 = wnba_teams[link_text[-3:]]
        team2 = wnba_teams[link_text[-9:-6]]

    print(f"Clicking on matchup: {link_text}")
    # Use JavaScript to click the link as a fallback
    driver.execute_script("arguments[0].click();", link)

    # Wait for the new page to load
    time.sleep(5)  # Adjust sleep time as necessary

    try:
        # Locate the "Las Vegas Aces" section using XPath
        element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, f"//div[@class='nba-stat-table__caption' and contains(text(), '{team1}')]"))
        )
        print(element.text)

        # Locate the table containing player data
        player_data_tables = WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.nba-stat-table'))
        )

        # Extract the names of all players for the first team, excluding "DNP - Coach's Decision"
        first_team_table = player_data_tables[0].find_element(By.TAG_NAME, 'table')
        players_team_1 = [row for row in first_team_table.find_elements(By.CSS_SELECTOR, 'tr')[1:]  # Skip the header row
                          if "DNP - Coach's Decision" not in row.text]

        # Find the index of the "Player" and "MIN" columns
        header_row = first_team_table.find_element(By.CSS_SELECTOR, 'thead tr')
        header_columns = header_row.find_elements(By.CSS_SELECTOR, 'th')
        player_column_index = None
        minutes_column_index = None


        for index, column in enumerate(header_columns):
            if column.text.strip() == 'PLAYER':
                player_column_index = index
            if column.text.strip() == 'MIN':
                minutes_column_index = index

        if player_column_index is None or minutes_column_index is None:
            raise Exception("Player or MIN column not found in first table")

        starting_lineup = []
        for player_row in players_team_1:
            player_name = player_row.find_elements(By.CSS_SELECTOR, 'td')[player_column_index].text
            player_minutes = player_row.find_elements(By.CSS_SELECTOR, 'td')[minutes_column_index].text
            name_parts = player_name.split(' ')
            if player_minutes == '' or player_name[0] == 'TOTALS:':
                break
            first_initial = name_parts[0][0]
            last_name = name_parts[1]
            result_name = f"{first_initial}. {last_name}"

            if (player_minutes[0] == "2" or player_minutes[0] == "3") and player_minutes[1] != ".":
                starting_lineup.append(f"{result_name}")


        print(starting_lineup)
        # Locate the "Washington Mystics" section using XPath
        element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, f"//div[@class='nba-stat-table__caption' and contains(text(), '{team2}')]"))
        )
        print(element.text)
        # Locate the table containing player data
        second_team_table = player_data_tables[1].find_element(By.TAG_NAME, 'table')
        players_team_2 = [row for row in second_team_table.find_elements(By.CSS_SELECTOR, 'tr')[1:]  # Skip the header row
                          if "DNP - Coach's Decision" not in row.text]

        # Find the index of the "Player" column for the second table
        header_row = second_team_table.find_element(By.CSS_SELECTOR, 'thead tr')
        header_columns = header_row.find_elements(By.CSS_SELECTOR, 'th')
        player_column_index = None
        minutes_column_index = None


        for index, column in enumerate(header_columns):
            if column.text.strip() == 'PLAYER':
                player_column_index = index
            if column.text.strip() == 'MIN':
                minutes_column_index = index

        if player_column_index is None or minutes_column_index is None:
            raise Exception("Player or MIN column not found in second table")

        opposing_lineup = []
        for player_row in players_team_2:
            player_name = player_row.find_elements(By.CSS_SELECTOR, 'td')[player_column_index].text
            player_minutes = player_row.find_elements(By.CSS_SELECTOR, 'td')[minutes_column_index].text
            name_parts = player_name.split(' ')
            if player_minutes == '' or player_name[0] == 'TOTALS:':
                break
            first_initial = name_parts[0][0]
            last_name = name_parts[1]
            result_name = f"{first_initial}. {last_name}"

            if (player_minutes[0] == "2" or player_minutes[0] == "3") and player_minutes[1] != ".":
                opposing_lineup.append(f"{result_name}")

        print(opposing_lineup)

    except TimeoutException as e:
        print(f"Timeout occurred: {str(e)}")
        continue

    # Navigate back to the previous page
    driver.back()
    time.sleep(5)  # Adjust sleep time as necessary
    starting_lineups.append(starting_lineup)
    opposing_lineups.append(opposing_lineup)




home_away = []
match_up = []

for matchup in player_df['MATCH UP']:
    if '@' in matchup:
        home_away.append(0)
        match_up.append(matchup[-9:])
    else:
        home_away.append(1)
        match_up.append(matchup[-11:])

player_df['home_away'] = home_away
player_df['match_up'] = match_up

# Adding starting_lineups and opposing_lineups
player_df['starting_lineup'] = starting_lineups
player_df['opposing_lineup'] = opposing_lineups

# Save to CSV
player_df.to_csv('player_stats.csv', index=False)
print(player_df['starting_lineup'])

# Select specific columns from the player DataFrame
# (Continue with your further processing as needed)
