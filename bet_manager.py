import json

class Player:
    def __init__(self, name, number, money=0) -> None:
        self.name: str = name
        self.money: int = money
        self.number: int = number
        self.bets: list[int] = []
    
    def win(self):
        self.money += self.bet
        self.bets = []
    
    def lose(self):
        self.money -= self.bet
        self.bets = []
    
    def double(self, curr_bet: int):
        self.bets[curr_bet] *= 2
    
    def split(self):
        self.bets.append(self.bets[0])

def save_players(players: list[Player]):
    to_dump = []
    
    for player in players:
        to_dump.append(player.__dict__())
    
    with open("players.json", "w", encoding="utf-8") as f:
        f.write(json.dumps(to_dump))

def load_players() -> list[Player]:
    players = []
    
    with open("players.json", encoding="utf-8") as f:
        if f.read() == "":
            return players
        
        load: list[dict] = json.loads(f.read())
        for player in load:
            players.append(Player(player["name"], player["number"], player["money"]))

    return players
        
def main():
    players = load_players()
    while True:
        print("1. Start round")
        print("2. Add player")
        print("3. Remove player")
        print("4. Show Players")
        print("5. Exit and Save")
        choice = input(":")

if __name__ == "__main__":
    main()
        