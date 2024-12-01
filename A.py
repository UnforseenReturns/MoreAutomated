import tkinter as tk
from tkinter import ttk
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

# Function to create the GUI
def create_gui(teams):
    root = tk.Tk()
    root.title("NFL Playoff Machine")

    tab_control = ttk.Notebook(root)

    for week in range(1, 18):
        tab = ttk.Frame(tab_control)
        tab_control.add(tab, text=f"Week {week}")

        # Labels for columns
        tk.Label(tab, text="Home Team").grid(row=0, column=0, padx=5, pady=5)
        tk.Label(tab, text="Away Team").grid(row=0, column=1, padx=5, pady=5)
        tk.Label(tab, text="Result").grid(row=0, column=2, padx=5, pady=5)

        for game in range(16):
            home_team_var = tk.StringVar()
            away_team_var = tk.StringVar()
            result_var = tk.StringVar()

            home_team_menu = ttk.Combobox(tab, textvariable=home_team_var)
            home_team_menu['values'] = [team['name'] for team in teams]
            home_team_menu.grid(row=game + 1, column=0, padx=5, pady=5)

            away_team_menu = ttk.Combobox(tab, textvariable=away_team_var)
            away_team_menu['values'] = [team['name'] for team in teams]
            away_team_menu.grid(row=game + 1, column=1, padx=5, pady=5)

            result_menu = ttk.Combobox(tab, textvariable=result_var)
            result_menu['values'] = ["Home Win", "Away Win", "Tie"]
            result_menu.grid(row=game + 1, column=2, padx=5, pady=5)

    tab_control.pack(expand=1, fill='both')

    root.mainloop()

# Main function
def main():
    team_data_file = 'team_data.json'  # Ensure this path is correct
    teams = load_team_data(team_data_file)
    standings = initialize_standings(teams)
    
    create_gui(teams)

if __name__ == "__main__":
    main()
