from Board import Board
from Player import Player
from State import State


class BarjisGame:

    def __init__(self, initial_board_data):

        self.current_player_id = 1
        self.current_state: State = State(Board(initial_board_data))
        self.players = {
            1: Player(1, Player.MODE_COMPUTER),
            2: Player(2, Player.MODE_COMPUTER)
        }

    def start(self):
        while not self.has_ended():
            self.current_state = self.current_state.make_move()

    def has_ended(self):
        return max(

    def winner(self) -> Player:
        for player in self.players.values():
            if len(player.pieces_in_kitchen) == 4:
                return player
