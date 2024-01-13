import copy

from Board import Board
from Piece import Piece
from Player import Player
from ShellThrow import ShellThrow


class State:
    def __init__(self, board: Board, player: Player, parent_state=None):
        self.parent = parent_state
        self.board = board
        self.player = player

    def ludo_heuristic(self, player_id):  # TODO
        """
        An enhanced heuristic for Ludo.

        :param player_id: The ID of the player for whom the heuristic is calculated.
        :return: A heuristic value for the current game state.
        """
        player_positions = game_state['player_positions'][player_id]
        opponents_positions = [game_state['player_positions'][opponent] for opponent in game_state['opponents']]

        score = 0

        # Enhanced scoring for progress and safety
        for position in player_positions:
            if position == 0:  # In yard
                score -= 10
            elif position > 50:  # In home stretch
                score += 20
            else:
                score += position  # Linear progress

        # Scoring for risk and aggression
        for position in player_positions:
            if position in opponents_positions:
                score -= 15  # Risk of being captured
            for opponent_positions in opponents_positions:
                if position + 6 >= min(opponent_positions) and position < min(opponent_positions):
                    score += 10  # Potential to capture an opponent

        # Scoring for diversification
        unique_positions = len(set(player_positions))
        score += unique_positions * 5  # Encourage spreading out

        # Adjust weights here based on playtesting and preference
        return score

    def get_children(self):
        board = self.board
        for i in range(7):
            throw = ShellThrow(i)


    def get_state_after_move(self, piece: Piece, throw: ShellThrow):
        new_piece = piece.get_new_piece_after_applying_move(throw)
        if new_piece is None:
            return None
        return State(self.board, self.player, piece, new_piece, bool(throw.khal), self)
