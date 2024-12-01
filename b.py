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

# Function to calculate standings
def calculate_standings(teams, standings):
    sorted_teams = sorted(teams, key=lambda x: (
        standings[x['name']]['wins'], 
        -standings[x['name']]['losses'], 
        standings[x['name']]['division_wins'], 
        standings[x['name']]['conference_wins'], 
        standings[x['name']]['points_scored'] - standings[x['name']]['points_allowed'],
        standings[x['name']]['points_scored']
    ), reverse=True)
    return sorted_teams

# Function to display standings
def display_standings(tab, standings, teams):
    sorted_teams = calculate_standings(teams, standings)
    for idx, team in enumerate(sorted_teams, start=1):
        tk.Label(tab, text=f"{idx}. {team['name']} (Wins: {standings[team['name']]['wins']}, Losses: {standings[team['name']]['losses']}, Ties: {standings[team['name']]['ties']})").pack()

# Function to update the GUI with playoff picture
def update_playoff_picture(tab_control, standings, teams):
    playoff_tab = ttk.Frame(tab_control)
    tab_control.add(playoff_tab, text="Playoff Picture")
    display_standings(playoff_tab, standings, teams)
    tab_control.select(playoff_tab)

# Function to create the GUI
def create_gui(teams):
    root = tk.Tk()
    root.title("NFL Playoff Machine")

    tab_control = ttk.Notebook(root)

    team_acronyms = [team['abbreviation'] for team in teams]
    team_names = {team['abbreviation']: team['name'] for team in teams}

    def autocomplete(event, combobox, team_names):
        entry = combobox.get().upper()
        if entry in team_names:
            combobox.set(team_names[entry])

    # Create a frame to hold the tabs
    tab_frame = tk.Frame(root)
    tab_frame.pack(side='top', fill='x')

    # Create a grid layout for the tabs
    for week in range(1, 18):
        tab = ttk.Frame(tab_control)
        row = (week - 1) // 4
        col = (week - 1) % 4
        tab_button = ttk.Button(tab_frame, text=f"Week {week}", command=lambda t=tab: tab_control.select(t))
        tab_button.grid(row=row, column=col, padx=5, pady=5)
        tab_control.add(tab, text=f"Week {week}")

        # Labels for columns
        tk.Label(tab, text="Home Team").grid(row=0, column=0, padx=5, pady=5)
        tk.Label(tab, text="Away Team").grid(row=0, column=1, padx=5, pady=5)
        tk.Label(tab, text="Result").grid(row=0, column=2, padx=5, pady=5)

        for game in range(16):
            home_team_var = tk.StringVar()
            away_team_var = tk.StringVar()
            result_var = tk.StringVar()

            # Create Combobox with team acronyms for autocomplete
            home_team_menu = ttk.Combobox(tab, textvariable=home_team_var, values=team_acronyms)
            home_team_menu.grid(row=game + 1, column=0, padx=5, pady=5)
            home_team_menu.bind('<FocusOut>', lambda e, c=home_team_menu: autocomplete(e, c, team_names))

            away_team_menu = ttk.Combobox(tab, textvariable=away_team_var, values=team_acronyms)
            away_team_menu.grid(row=game + 1, column=1, padx=5, pady=5)
            away_team_menu.bind('<FocusOut>', lambda e, c=away_team_menu: autocomplete(e, c, team_names))

            result_menu = ttk.Combobox(tab, textvariable=result_var)
            result_menu['values'] = ["Home Win", "Away Win", "Tie"]
            result_menu.grid(row=game + 1, column=2, padx=5, pady=5)

    # Add "Show Standings" button
    show_standings_button = ttk.Button(tab_frame, text="Show Standings", command=lambda: update_playoff_picture(tab_control, standings, teams))
    show_standings_button.grid(row=5, columnspan=4, padx=5, pady=5)

    tab_control.pack(expand=1, fill='both')
    root.mainloop()

# Main function
def main():
    team_data_file = 'team_data.json'  # Ensure this path is correct
    teams = load_team_data(team_data_file)
    global standings
    standings = initialize_standings(teams)

    create_gui(teams)

if __name__ == "__main__":
    main()