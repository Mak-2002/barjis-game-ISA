from Board import Board
from Player import Player
from ShellThrow import ShellThrow
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
        expected_value = 0
        children = state.children
        for i in range(7):
            evaluation_value = 0
            if state.player_id == 1:  # maximizing player
                evaluation_value = float('-inf')
                for child in children[i]:
                    evaluation_value = max(BarjisGame.expectiminimax_from_current_state(child, depth - 1),
                                           evaluation_value)
                expected_value += evaluation_value * ShellThrow.probability[i]
            else:  # minimizing player
                evaluation_value = float('inf')
                for child in children[i]:
                    evaluation_value = min(BarjisGame.expectiminimax_from_current_state(child, depth - 1),
                                           evaluation_value)
                expected_value += evaluation_value * ShellThrow.probability[i]
            state.cost = expected_value
            for child in children[i]:
                if child.cost == evaluation_value:
                    state.best_child[i] = child
                    break

    def has_ended(self):
        return self.current_state.is_terminal()
