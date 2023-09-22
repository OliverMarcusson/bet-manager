import json
from os import system
import keyboard
from colorama import just_fix_windows_console, Fore
from time import sleep

PLAYER_MONEY = lambda player: Fore.GREEN + str(player.money) + Fore.RESET if player.money > 0 else Fore.RED + str(player.money) + Fore.RESET

class Player:
    def __init__(self, name: str, number: str, money=0) -> None:
        self.name: str = name
        self.money: int = money
        
        if len(number) == 10:
            self.number = f"{number[:3]}-{number[3:6]} {number[6:8]} {number[8:10]}"
        else:
            self.number = number

        self.bets: list[int] = []
    
    def blackjack(self, curr_bet: int):
        self.money += self.bets[curr_bet] * 1.5
    
    def win(self, curr_bet):
        self.money += self.bets[curr_bet]
    
    def lose(self, curr_bet: int):
        self.money -= self.bets[curr_bet]
    
    def push(self):
        pass
    
    def double(self, curr_bet: int):
        self.bets[curr_bet] *= 2
    
    def split(self):
        self.bets.append(self.bets[0])

def save_players(players: list[Player]):
    to_dump = []
    
    for player in players:
        player.bets = []
        to_dump.append(player.__dict__)
    
    with open("players.json", "w", encoding="utf-8") as f:
        f.write(json.dumps(to_dump))

def load_players() -> list[Player]:
    players = []
    
    with open("players.json", encoding="utf-8") as f:
        json_string = f.read()
        
        if json_string == "":
            return players
        
        load: list[dict] = json.loads(json_string)
        
        for player in load:
            players.append(Player(player["name"], player["number"], player["money"]))

    return players

def new_player(players):
    name = input("Name:")
    number = input("Number:")
    money = input("Money:")
                
    if money == "":
        money = 0
    else:
        money = int(money)
                
    print(f"Player '{name}' added.")
    players.append(Player(name, number, money))
        
def delete_player(players):
    name = input("Name:")
    for i, player in enumerate(players):
        if player.name == name:
            print(f"Are you sure you want to delete {player.name}? (Money: {PLAYER_MONEY(player)})")
            choice = input("(Y/N):")
            
            if choice.upper() == "Y":
                del players[i]
            return
    print(f"Couldn't find a player with the name '{name}'.")        

def play_round(players):
    print(Fore.CYAN + "Select players:" + Fore.RESET)
    active_players: list[Player] = []
    for i, player in enumerate(players):
        print(f"{i+1}. {player.name}")
    
    ap_input = input("Active players, in order (nums):")
    for num in ap_input:
        active_players.append(players[int(num)-1])
    system("cls")
    
    print(Fore.CYAN + "Bets:" + Fore.RESET)
    for player in active_players:
        bets = list(map(int, input(f"{player.name} ({PLAYER_MONEY(player)}):").split(",")))
        player.bets = bets
    system("cls")
    sleep(0.5)
    
    for player in active_players:
        for i, hand in enumerate(player.bets):
            action = ""
            while True:
                print(f"{player.name} Hand {Fore.CYAN + str(i + 1) + Fore.RESET} [of {Fore.CYAN + str(len(player.bets)) + Fore.RESET}] ({Fore.CYAN + str(hand) + Fore.RESET}):")
                print("D. Double" if not action == "double" else Fore.CYAN + "D. Double" + Fore.RESET)
                print("S. Split" if not action == "split" else Fore.CYAN + "S. Split" + Fore.RESET)
                print("N. Next" if not action == "next" else Fore.CYAN + "N. Next" + Fore.RESET)
                
                key = keyboard.read_key(True)
                match key:
                    case "d":
                        action = "double"
                    case "s":
                        action = "split"
                    case "n":
                        action = "next"
                    case "enter":
                        break
                    case _:
                        system("cls")
                system("cls")
                
            match action:
                case "double":
                    player.double(i)
                case "split":
                    player.split()
                case _:
                    system("cls")
            sleep(0.5)
    
    system("cls")
    input("Press ENTER when round is over.")
    system("cls")
    sleep(0.5)
    
    for player in active_players:
        for i, hand in enumerate(player.bets):
            action = ""
            while True:
                print(f"{player.name} Hand {Fore.CYAN + str(i + 1) + Fore.RESET} [of {Fore.CYAN + str(len(player.bets)) + Fore.RESET}] ({Fore.CYAN + str(hand) + Fore.RESET}):")
                print("B. Blackjack" if not action == "blackjack" else Fore.CYAN + "B. Blackjack" + Fore.RESET)
                print("W. Win" if not action == "win" else Fore.GREEN + "W. Win" + Fore.RESET)
                print("L. Loss" if not action == "loss" else Fore.RED + "L. Loss" + Fore.RESET)
                print("P. Push" if not action == "push" else Fore.YELLOW + "P. Push" + Fore.RESET)
                
                key = keyboard.read_key(True)
                match key:
                    case "b":
                        action = "blackjack"
                    case "w":
                        action = "win"
                    case "l":
                        action = "loss"
                    case "p":
                        action = "push"
                    case "enter":
                        break
                    case _:
                        pass
                system("cls")
                
            match action:
                case "blackjack":
                    player.blackjack(i)
                case "win":
                    player.win(i)
                case "loss":
                    player.lose(i)
                case _:
                    system("cls")
            sleep(0.5)
            system("cls")
    
    system("cls")
    print(Fore.CYAN + "Results:" + Fore.RESET)
    for player in active_players:
        print(f"{player.name} (Money: {PLAYER_MONEY(player)})")
    input()

def main():
    system("cls")
    just_fix_windows_console()
    players = load_players()
    while True:
        print(Fore.CYAN + "Blackjack Bet Manager" + Fore.RESET)
        print("1. Start round")
        print("2. Add player")
        print("3. Remove player")
        print("4. Show Players")
        print(Fore.YELLOW + "5. Exit and Save" + Fore.RESET)
        choice = input(":")
        
        match choice:
            case "1":
                system("cls")
                play_round(players)
                
            
            case "2":
                system("cls")
                new_player(players)
                input()
                
            case "3":
                system("cls")
                delete_player(players)
                input()
                    
            case "4":
                system("cls")
                print(Fore.CYAN + "Current Players:" + Fore.RESET)
                for player in players:
                    print(f"{player.name}, {Fore.YELLOW + str(player.number) + Fore.RESET} (Money: {PLAYER_MONEY(player)})")
                input()
                    
            case "5":
                save_players(players)
                break
            
            case _:
                print("Invalid selection.")
                sleep(1)
        
        system("cls")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Exiting...")
        exit()
        