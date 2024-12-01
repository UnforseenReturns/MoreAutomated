# Function to save game session data to a file
def save_game_data(file_path, standings, week_data):
    data_to_save = {
        'standings': standings,
        'week_data': week_data
    }
    with open(file_path, 'w') as file:
        json.dump(data_to_save, file)
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
    week_data = {week: [] for week in range(1, 18)}

    def autocomplete(event, combobox, team_names):
        entry = combobox.get().upper()
        if entry in team_names:
            combobox.set(team_names[entry])

    def record_game_result(home_team_var, away_team_var, result_var, week, game):
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
            week_data[week][game] = game_result

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

        week_data[week] = [{} for _ in range(16)]  # Initialize week data

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

            # Load saved data into dropdowns
            if 'home_team' in week_data[week][game]:
                home_team_var.set(week_data[week][game]['home_team'])
            if 'away_team' in week_data[week][game]:
                away_team_var.set(week_data[week][game]['away_team'])
            if 'result' in week_data[week][game]:
                result_var.set(week_data[week][game]['result'])

            # Update standings when result is selected
            result_menu.bind('<<ComboboxSelected>>', lambda e, h=home_team_var, a=away_team_var, r=result_var, w=week, g=game: record_game_result(h, a, r, w, g))

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
    save_button = ttk.Button(tab_frame, text="Save Game Data", command=lambda: save_game_data('game_data.json', standings, week_data))
    save_button.grid(row=8, columnspan=4, padx=5, pady=5)

    # Add "Load Game Data" button
    load_button = ttk.Button(tab_frame, text="Load Game Data", command=lambda: load_game_data_with_gui('game_data.json', standings_tab, playoff_picture_tab, teams))
    load_button.grid(row=9, columnspan=4, padx=5, pady=5)

    # Add "Clear Data" button
    clear_button = ttk.Button(tab_frame, text="Clear Data", command=lambda: clear_data(teams))
    clear_button.grid(row=10, columnspan=4, padx=5, pady=5)

    tab_control.pack(expand=1, fill='both')
    root.mainloop()

# Function to load game data and update the GUI
def load_game_data_with_gui(file_path, standings_tab, playoff_picture_tab, teams):
    loaded_data = load_game_data(file_path)
    if loaded_data and 'standings' in loaded_data:
        global standings
        standings = loaded_data['standings']
        week_data = loaded_data['week_data']
        display_standings(standings_tab, standings, teams)
        update_playoff_picture(playoff_picture_tab, standings, teams)
        create_gui(teams)  # Recreate GUI with loaded data
    else:
        print("No 'standings' data found in loaded data.")

# Main function
def main():
    team_data_file = 'team_data.json'  # Ensure this path is correct
    global standings
    teams = load_team_data(team_data_file)

    # Load existing game data if available
    game_data_file = 'game_data.json'
    loaded_data = load_game_data(game_data_file)
    if loaded_data and 'standings' in loaded_data:
        standings = loaded_data['standings']
        week_data = loaded_data['week_data']
    else:
        standings = initialize_standings(teams)
        week_data = {week: [{} for _ in range(16)] for week in range(1, 18)}

    create_gui(teams)

if __name__ == "__main__":
    main()
