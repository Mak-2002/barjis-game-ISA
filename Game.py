from Player import Player


class Game:

    def __init__(self):
        self.player = []
        self.player[1] = Player(mode=Player.HUMAN)
        self.player[2] = Player(mode=Player.COMPUTER)
        self.current_turn_user = 1
