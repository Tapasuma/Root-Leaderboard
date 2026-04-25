import os
from rich.console import Console
from rich.table import Table
from rich.columns import Columns
from functions import elo_calc, update_elo, create_leaderboard, add_player, load_data, remove_player, print_logo, draw
from colorama import Fore, Style, init

init()
print_logo()

base_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(base_dir, "data.json")
console = Console()

while True:

    table = Table(style="red")

    table.add_column("Welcome to Root Leaderboard!", style="red", header_style="red")
    table.add_row("1. View leaderboard")
    table.add_row("2. Change elo")
    table.add_row("3. Add new player")
    table.add_row("4. Remove player")
    table.add_row("5. Exit")

    console.print(table)
    choice = int(input())

    ############################# VIEW LEADERBOARD 
    if choice == 1: 

        data = load_data(file_path)

        table_players = create_leaderboard(data["players"], "PLAYERS")
        table_factions= create_leaderboard(data["factions"], "FACTIONS")
        leaderboard = Columns([table_players, table_factions])

        print()
        console.print(leaderboard)
        print()


    ############################# CHANGE ELO
    elif choice == 2: 

        standing_players = input("Please enter the names of the players, starting with first place, e.g. Bella, Billy, Bailey, Bob: ")
        standing_factions = input("Please enter the factions in short-form (V for Vagabond, WA for Woodland Alliance, ED for Eyrie Dynasty, MC for Marquise de Cat) starting with first place, e.g. V, WA, ED, MC: ")
        raw = input("Did anyone draw? y/n: ")

        draw_list = draw(raw)

        list_players = standing_players.split(", ") # Now the winner has index 0, second place index 1 and so on...
        list_factions = standing_factions.split(", ")

        nbr_players = len(list_players)
        print("Number of players :",nbr_players)

        ###### Checks if any names or factions are missing from dicitionaries ######

        data = load_data(file_path)
        players = data["players"]
        factions = data["factions"]

        missing_p = [p for p in list_players or draw_list if p not in players] # Appends p if true, iterates over list_players, if statement
        if missing_p:
            print(f"Missing players: {', '.join(missing_p)}. Please add them first.")
            continue

        missing_f = [f for f in list_factions if f not in factions] # Appends f if true, iterates over list_factions, if statement
        if missing_f:
            print(f"Missing factions: {', '.join(missing_f)}. Please use V for Vagabond, WA for Woodland Alliance, ED for Eyrie Dynasty, and MC for Marquise de Cat")
            continue

        ###### Walks through all the duels and calculated the elo for each and summarises it in a list, one for players and one for factions ######

        elo_change = [0] * nbr_players

        for n in range(nbr_players-1): 
            for x in range(n + 1, nbr_players):

                # Summarizes the elo for the player and the corresponding character
                score_1 = players[list_players[n]] + factions[list_factions[n]] 
                score_2 = players[list_players[x]] + factions[list_factions[x]]

                if list_players[n] and list_players[x] in draw_list:
                    elo_diff = elo_calc("draw", score_1, score_2)
                    #print(f"draw {elo_diff}")
                else:
                    elo_diff = elo_calc("win", score_1, score_2)
                    #print("win")

                # Saves the elo change
                elo_change[n] += elo_diff
                elo_change[x] -= elo_diff

        #### Adds the total change in elo to the dictionaries ######

        for k in range(nbr_players):
            print(list_players[k],":", round(elo_change[k]))
            updated_players = update_elo(file_path, "players", list_players[k], round(elo_change[k]))

            print(list_factions[k],":", round(elo_change[k]))
            updated_factions = update_elo(file_path, "factions", list_factions[k], round(elo_change[k]))
        
        print("Updated elo")

    ########################### ADD NEW PLAYER
    elif choice == 3:

        new_player = input("What is the name of the new player?\n")
        starting_elo = int(input("What is their staring elo?\n"))

        #players[new_player] = new_rating
        #print(players)

        add_player(file_path, new_player, starting_elo)
        print(f"Added player {new_player}")

    ########################### REMOVE PLAYER
    elif choice == 4:

        data = load_data(file_path)

        player_to_remove = input("What is the name of the player you want to remove?\n")
        sure = input("Are you sure you want to remove them? y/n\n")
        if sure == "y":
            print(remove_player(file_path, player_to_remove))

    ########################### EXIT
    elif choice == 5:
        break