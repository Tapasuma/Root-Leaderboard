import json
import os
from rich.console import Console
from rich.table import Table
from rich.columns import Columns
import pyfiglet
from colorama import Fore, Style, init

console = Console()

# Accsesses the .json file
base_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(base_dir, "data.json")
with open(file_path, "r") as f:
    data = json.load(f)

players = data["players"]
factions = data["factions"]


# See https://www.omnicalculator.com/sports/elo

def elo_calc(score: str, rating_1: int, rating_2: int) -> float:

    A = rating_1
    B = rating_2
    
    k_factor = 20 # Standard but can be changed depending on the skill level

    if score == "win":
        score = 1
    elif score == "draw":
        score = 0.5
    elif score == "loss":
        score = 0

    expected = 1 / (10 ** ((B - A) / 400) + 1)
    elo_change = k_factor * (score - expected)

    return elo_change


# Makes sure the script will find the json file as long as it is in the same folder, avoids problem with PATH
base_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(base_dir, "data.json")

def update_elo(file:str, category:str, name:str, elo_change:int) -> dict:

    with open(file, "r") as f: # Opens json in read mode and defines it as data
        data = json.load(f)

    if name in data[category]: 
        data[category][name] += elo_change # Adds the change in elo to the player/faction
        with open(file_path, "w") as f: # Opens the json in write mode
            json.dump(data, f, indent=4) # Updates the json by overwriting
    return data[category]


def create_leaderboard(category_dict: dict, category_str: str) -> Table:

    table = Table(row_styles=["none", "dim"], style="red")

    table.add_column(category_str, header_style="bold red") # ex "players"
    table.add_column("ELO", header_style="bold red")

    sorted_list = sorted(category_dict.items(), key=lambda x: x[1], reverse=True) # key=lambda works as a function with input x and output x[1] (elo)
    for name, elo in sorted_list:
        table.add_row(name, str(elo), style="red")

    return table


def add_player(file:str, new_player:str, starting_elo:int) -> dict:

    with open(file, "r") as f: # Opens json in read mode and defines it as data
        data = json.load(f)

    if new_player not in data["players"]:

        data["players"][new_player] = starting_elo
        with open(file_path, "w") as f: # Opens the json in write mode
            json.dump(data, f, indent=4) # Updates the json by overwriting

    return data["players"]

def remove_player(file:str, player:str) -> str:

    with open(file, "r") as f: # Opens json in read mode and defines it as data
        data = json.load(f)

    if player not in data["players"]:
        return f"{player} does not exist"
    del data["players"][player]
    with open(file_path, "w") as f: # Opens the json in write mode
        json.dump(data, f, indent=4) # Updates the json by overwriting

    return f"{player} was removed"


def load_data(file:str) -> json: # Funciton to use whenever data needs to be called so that it always is up to date
    with open(file, "r") as f:
        data = json.load(f)
    return data


def print_logo():
    # The Omarchy font
    title = pyfiglet.figlet_format("ROOT LEADERBOARD", font="delta_corps_priest_1")

    width = 80
    divider = "─" * width

    print()
    print(Fore.RED + title + Style.RESET_ALL)
    print(Fore.RED + divider + Style.RESET_ALL)
    print(Fore.RED + '"There is no escape; we pay for the violence of our ancestors"  F. Herbert' + Style.RESET_ALL)
    print(Fore.RED + divider + Style.RESET_ALL)
    print()

def draw(raw:str) -> list:

    if raw == "N":
        return []

    draw_players = input("Which players drawed? ")
    draw_list = draw_players.split(", ")
    return draw_list


if __name__ == "__main__":
    
    #print(update_elo(file_path, "players", "Billy", 12))
    #print(update_elo(file_path, "players", "Bella", 12))
    #table_players = create_leaderboard(players, "PLAYERS")
    #table_factions= create_leaderboard(factions, "FACTIONS")
    #leaderboard = Columns([table_players, table_factions])
    #console.print(leaderboard)
    #print(add_player(file_path, "Hugo", 1212))
    print(elo_calc("draw",2405, 2467))