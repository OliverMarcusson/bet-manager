import json
from os import system
import keyboard

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
            print(f"Are you sure you want to delete {player.name}? (Money: {player.money})")
            choice = input("(Y/N):")
            
            if choice.upper() == "Y":
                del players[i]
            return
    print(f"Couldn't find a player with the name '{name}'.")        

def play_round(players):
    active_players: list[Player] = []
    for i, player in enumerate(players):
        print(f"{i+1}. {player.name}")
    
    ap_input = input("Active players, in order (nums):")
    for num in ap_input:
        active_players.append(players[int(num)-1])
    system("cls")
    
    print("Bets:")
    for player in active_players:
        bets = list(map(int, input(f"{player.name} ({player.money}):").split(",")))
        player.bets = bets
    system("cls")
    
    for player in active_players:
        for i, hand in enumerate(player.bets):
            while True:
                print(f"{player.name} Hand {i + 1} [of {len(player.bets)}] ({hand}):")
                print("D. Double")
                print("S. Split")
                print("N. Next")
                
                key = keyboard.read_key(True)
                match key:
                    case "d":
                        player.double(i)
                        break
                    
                    case "s":
                        player.split()
                        break
                    
                    case "n":
                        break
                    
                    case _:
                        system("cls")
            input("Press ENTER.")
    
    system("cls")
    input("Press ENTER when round is over.")
    system("cls")
    
    for player in active_players:
        for i, hand in enumerate(player.bets):
            while True:
                print(f"{player.name} Hand {i + 1} [of {len(player.bets)}] ({hand}):")
                print("B. Blackjack")
                print("W. Win")
                print("L. Loss")
                print("P. Push")
                
                key = keyboard.read_key(True)
                match key:
                    case "b":
                        player.blackjack(i)
                        break
                    
                    case "w":
                        player.win(i)
                        break
                    
                    case "l":
                        player.lose(i)
                        break
                    
                    case "p":
                        break
                    
                    case _:
                        system("cls")
            input("Press ENTER.")
            system("cls")
    
    system("cls")
    print("Results:")
    for player in active_players:
        print(f"{player.name} (Money: {player.money})")
    input()

def main():
    players = load_players()
    while True:
        print("1. Start round")
        print("2. Add player")
        print("3. Remove player")
        print("4. Show Players")
        print("5. Exit and Save")
        choice = input(":")
        
        match choice:
            case "1":
                system("cls")
                play_round(players)
                
            
            case "2":
                new_player(players)
                input()
                
            case "3":
                delete_player(players)
                input()
                    
            case "4":
                print("Current Players:")
                for player in players:
                    print(f"{player.name}, {player.number} (Money: {player.money})")
                input()
                    
            case "5":
                save_players(players)
                break
            
            case _:
                print("Invalid selection.")
                input()
        
        system("cls")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Exiting...")
        exit()
        