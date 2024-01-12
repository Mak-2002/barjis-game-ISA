from Board import Board
from Player import Player


class Game:

    def __init__(self):
        self.board = Board([], self)  # TODO: fill data
        self.players = {
            1: Player(mode=Player.HUMAN, game=self),
            2: Player(mode=Player.COMPUTER, game=self)
        }
        self.current_player = self.players[1]

    def switch_turn(self):
        self.current_player = self.players[3 - self.current_player.number]

    def start(self):
        while not self.has_ended():
            self.current_player.make_move()

    def has_ended(self):
        return max(len(self.players[1].pieces_in_kitchen),
                   len(self.players[2].pieces_in_kitchen)) == 4

    def winner(self) -> Player:
        for player in self.players.values():
            if len(player.pieces_in_kitchen) == 4:
                return player
