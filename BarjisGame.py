from Board import Board
from Player import Player
from State import State


class BarjisGame:
    MAX_DEPTH = 50

    def __init__(self, initial_board_data):
        self.current_player_id = 1
        self.current_state: State = State(Board(initial_board_data), 1)
        self.players = {
            1: Player(1, Player.MODE_COMPUTER),
            2: Player(2, Player.MODE_COMPUTER)
        }

    def start(self):
        while not self.has_ended():
            self.current_state = self.current_state.make_move()

    @staticmethod
    def expectiminimax_from_current_state(state: State, depth=MAX_DEPTH):
        if state.is_terminal():
            state.cost = float('inf') if state.winner() == 1 else float('-inf')
            return state.cost
        if depth == 0:
            state.cost = state.heuristic()
        if state.player_id == 1:  # is maximizing player
            max_evaluation = float('-inf')
        for:
            pass

    def has_ended(self):
        return self.current_state.is_terminal()
