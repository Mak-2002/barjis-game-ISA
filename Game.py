from Board import Board
from Player import Player


class Game:

    def __init__(self):
        self.board = Board([], self)  # TODO: fill data
        self.players = {
            1: Player(mode=Player.HUMAN, game=self),
            2: Player(mode=Player.COMPUTER, game=self)
        }
        self.current_turn_user = 1
