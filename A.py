import json

# Load team data from a JSON file
def load_team_data(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data['teams']

# Initialize team standings
def initialize_standings(teams):
    standings = {team['name']: {
        'wins': 0,
        'losses': 0,
        'ties': 0,
        'division_wins': 0,
        'conference_wins': 0,
        'points_scored': 0,
        'points_allowed': 0
    } for team in teams}
    return standings

# Update standings based on game results
def update_standings(standings, game_result):
    home_team = game_result['home_team']
    away_team = game_result['away_team']
    home_score = game_result['home_score']
    away_score = game_result['away_score']
    
    if home_score > away_score:
        standings[home_team]['wins'] += 1
        standings[away_team]['losses'] += 1
    elif away_score > home_score:
        standings[away_team]['wins'] += 1
        standings[home_team]['losses'] += 1
    else:
        standings[home_team]['ties'] += 1
        standings[away_team]['ties'] += 1
    
    standings[home_team]['points_scored'] += home_score
    standings[home_team]['points_allowed'] += away_score
    standings[away_team]['points_scored'] += away_score
    standings[away_team]['points_allowed'] += home_score

# Main function to simulate and update standings
def main():
    team_data_file = 'team_data.json'  # Ensure this path is correct
    teams = load_team_data(team_data_file)
    standings = initialize_standings(teams)
    
    # Example game result
    game_result = {
        'home_team': 'Baltimore Ravens',
        'away_team': 'Pittsburgh Steelers',
        'home_score': 24,
        'away_score': 17
    }
    
    update_standings(standings, game_result)
    print(standings)

if __name__ == "__main__":
    main()
