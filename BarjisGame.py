from Board import Board
from Player import Player
from ShellThrow import ShellThrow


class BarjisGame:
    MAX_DEPTH = 5

    def __init__(self, initial_board_data):
        from State import State
        self.current_state = State(Board(initial_board_data), 1, 1)
        self.players = {
            1: Player(1, Player.MODE_HUMAN),
            2: Player(2, Player.MODE_COMPUTER)
        }
        self.expectiminimax_from_state(self.current_state)

    def start(self):
        while not self.has_ended():
            current_player = self.players[self.current_state.player_id]
            if current_player.mode == Player.MODE_HUMAN:
                self.current_state = self.current_state.human_play()
            else:
                self.current_state = self.current_state.computer_play()
        if self.current_state.winner() == 1:
            print('congratulations! you have won the game against computer!')
        else:
            print('the computer has won the game against you!')
        print('statistics about the game:')
        # TODO

    @staticmethod
    def expectiminimax_from_state(state, depth=MAX_DEPTH):
        state.children = state.get_children()
        if state.is_terminal():
            state.cost = float('inf') if state.winner() == 1 else float('-inf')
            return state.cost
        if depth == 0:
            state.cost = state.heuristic()
            return state.cost
        expected_value = 0
        for throw_result in range(7):
            if state.player_id == 1:  # maximizing player
                evaluation_value = float('-inf')
                for child in state.children[throw_result]:
                    evaluation_value = max(BarjisGame.expectiminimax_from_state(child, depth - 1),
                                           evaluation_value)
                expected_value += evaluation_value * ShellThrow.probability[throw_result]

            else:  # minimizing player
                evaluation_value = float('inf')
                for child in state.children[throw_result]:
                    evaluation_value = min(BarjisGame.expectiminimax_from_state(child, depth - 1),
                                           evaluation_value)
                expected_value += evaluation_value * ShellThrow.probability[throw_result]
            state.cost = expected_value
            for child in state.children[throw_result]:
                if child.cost == evaluation_value:
                    state.best_child[throw_result] = child
                    break
            return state.cost

    def has_ended(self):
        print(type(self.current_state))
        return self.current_state.is_terminal()
