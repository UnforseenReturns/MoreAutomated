import tkinter as tk
from tkinter import ttk
import json
import os

# Load team data from a JSON file
def load_team_data(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    print("Team data loaded successfully.")
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
        standings[x['name']]['ties'],
        standings[x['name']]['division_wins'],
        standings[x['name']]['conference_wins'],
        standings[x['name']]['points_scored'] - standings[x['name']]['points_allowed'],
        standings[x['name']]['points_scored']
    ), reverse=True)
    return sorted_teams

# Function to display standings
def display_standings(tab, standings, teams):
    for widget in tab.winfo_children():
        widget.destroy()
    sorted_teams = calculate_standings(teams, standings)
    for idx, team in enumerate(sorted_teams, start=1):
        tk.Label(tab, text=f"{idx}. {team['name']} (Wins: {standings[team['name']]['wins']}, Losses: {standings[team['name']]['losses']}, Ties: {standings[team['name']]['ties']})").pack()

# Function to update the GUI with playoff picture
def update_playoff_picture(tab, standings, teams):
    for widget in tab.winfo_children():
        widget.destroy()
    display_playoff_picture(tab, standings, teams)

# Function to display playoff picture
def display_playoff_picture(tab, standings, teams):
    conferences = {'NFC': [], 'AFC': []}
    for team in teams:
        conferences[team['conference']].append(team)

    playoff_teams = {'NFC': [], 'AFC': []}
    for conference, conference_teams in conferences.items():
        divisions = {team['division'] for team in conference_teams}
        division_leaders = []
        for division in divisions:
            division_teams = [team for team in conference_teams if team['division'] == division]
            sorted_division_teams = sorted(division_teams, key=lambda x: (
                standings[x['name']]['wins'],
                -standings[x['name']]['losses'],
                standings[x['name']]['ties'],
                standings[x['name']]['division_wins'],
                standings[x['name']]['conference_wins'],
                standings[x['name']]['points_scored'] - standings[x['name']]['points_allowed'],
                standings[x['name']]['points_scored']
            ), reverse=True)
            division_leaders.append(sorted_division_teams[0])

        remaining_teams = [team for team in conference_teams if team not in division_leaders]
        sorted_remaining_teams = sorted(remaining_teams, key=lambda x: (
            standings[x['name']]['wins'],
            -standings[x['name']]['losses'],
            standings[x['name']]['ties'],
            standings[x['name']]['division_wins'],
            standings[x['name']]['conference_wins'],
            standings[x['name']]['points_scored'] - standings[x['name']]['points_allowed'],
            standings[x['name']]['points_scored']
        ), reverse=True)
        playoff_teams[conference] = division_leaders + sorted_remaining_teams[:3]

    nfc_frame = ttk.Frame(tab)
    afc_frame = ttk.Frame(tab)
    nfc_frame.pack(side='left', fill='both', expand=True)
    afc_frame.pack(side='right', fill='both', expand=True)

    tk.Label(nfc_frame, text="NFC Playoff Picture").pack()
    for idx, team in enumerate(playoff_teams['NFC'], start=1):
        tk.Label(nfc_frame, text=f"{idx}. {team['name']} (Wins: {standings[team['name']]['wins']}, Losses: {standings[team['name']]['losses']}, Ties: {standings[team['name']]['ties']})").pack()

    tk.Label(afc_frame, text="AFC Playoff Picture").pack()
    for idx, team in enumerate(playoff_teams['AFC'], start=1):
        tk.Label(afc_frame, text=f"{idx}. {team['name']} (Wins: {standings[team['name']]['wins']}, Losses: {standings[team['name']]['losses']}, Ties: {standings[team['name']]['ties']})").pack()

# Function to save game session data to a file
def save_game_data(file_path, standings):
    with open(file_path, 'w') as file:
        json.dump(standings, file)
    print("Game data saved successfully.")

# Function to load game session data from a file
def load_game_data(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)
        print("Game data loaded successfully.")
        return data
    else:
        print("No saved game data found.")
    return None

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

            # Update standings when result is selected
            result_menu.bind('<<ComboboxSelected>>', lambda e, h=home_team_var, a=away_team_var, r=result_var: record_game_result(h, a, r))

    # Add Standings and Playoff Picture tabs
    standings_tab = ttk.Frame(tab_control)
    playoff_picture_tab = ttk.Frame(tab_control)
    tab_control.add(standings_tab, text="Standings")
    tab_control.add(playoff_picture_tab, text="Playoff Picture")

    # Add "Show Standings" button
    show_standings_button = ttk.Button(tab_frame, text="Show Standings", command=lambda: display_standings(standings_tab, standings, teams))
    show_standings_button.grid(row=5, columnspan=4, padx=5, pady=5)

    # Add "Show Playoff Picture" button
    show_playoff_picture_button = ttk.Button(tab_frame, text="Show Playoff Picture", command=lambda: update_playoff_picture(playoff_picture_tab, standings, teams))
    show_playoff_picture_button.grid(row=6, columnspan=4, padx=5, pady=5)

    # Add "Update Standings and Playoff Picture" button
    update_button = ttk.Button(tab_frame, text="Update Standings and Playoff Picture", command=lambda: update_all(standings_tab, playoff_picture_tab, standings, teams))
    update_button.grid(row=7, columnspan=4, padx=5, pady=5)

    # Add "Save Game Data" button
    save_button = ttk.Button(tab_frame, text="Save Game Data", command=lambda: save_game_data('game_data.json', standings))
    save_button.grid(row=8, columnspan=4, padx=5, pady=5)

    # Add "Load Game Data" button
    load_button = ttk.Button(tab_frame, text="Load Game Data", command=lambda: load_game_data('game_data.json'))
    load_button.grid(row=9, columnspan=4, padx=5, pady=5)

    # Add "Clear Data" button
    clear_button = ttk.Button(tab_frame, text="Clear Data", command=lambda: clear_data(teams))
    clear_button.grid(row=10, columnspan=4, padx=5, pady=5)

    tab_control.pack(expand=1, fill='both')
    root.mainloop()

# Function to record game results and update standings
def record_game_result(home_team_var, away_team_var, result_var):
    home_team = home_team_var.get()
    away_team = away_team_var.get()
    result = result_var.get()
    if home_team and away_team and result:
        if result == "Home Win":
            game_result = {'home_team': home_team, 'away_team': away_team, 'home_score': 1, 'away_score': 0}
        elif result == "Away Win":
            game_result = {'home_team': home_team, 'away_team': away_team, 'home_score': 0, 'away_score': 1}
        else:  # Tie
            game_result = {'home_team': home_team, 'away_team': away_team, 'home_score': 0, 'away_score': 0}
        update_standings(standings, game_result)

# Function to update both standings and playoff picture
def update_all(standings_tab, playoff_picture_tab, standings, teams):
    display_standings(standings_tab, standings, teams)
    update_playoff_picture(playoff_picture_tab, standings, teams)

# Function to clear all data
def clear_data(teams):
    global standings
    standings = initialize_standings(teams)
    print("All data cleared.")

# Main function
def main():
    team_data_file = 'team_data.json'  # Ensure this path is correct
    global standings
    teams = load_team_data(team_data_file)

    # Load existing game data if available
    game_data_file = 'game_data.json'
    loaded_standings = load_game_data(game_data_file)
    if loaded_standings:
        standings = loaded_standings
    else:
        standings = initialize_standings(teams)

    create_gui(teams)

if __name__ == "__main__":
    main()
