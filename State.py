from Board import Board
from Piece import Piece
from ShellThrow import ShellThrow


class State:
    def __init__(self, board: Board,
                 previous_player_id,
                 player_id,
                 throw: ShellThrow = None,
                 player_consecutive_moves=1,
                 parent_state=None):
        self.board = board
        self.previous_player_id = previous_player_id
        self.player_id = player_id
        self.throw = throw
        self.player_consecutive_moves = player_consecutive_moves
        self.parent = parent_state
        self.best_child = None
        self.cost = 0

    def __eq__(self, other):
        return self.player_id == other.player_id and self.board == other.board

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

    def winner(self):
        for i in range(1, 3):
            if len(self.board.get_player_pieces(i, Piece.IN_KITCHEN)) == 4:
                return i
        return 0

    def get_children(self):
        player_id = self.player_id
        children = []
        board = self.board
        for i in range(7):
            throw = ShellThrow(i)

            if throw.reserves_turn() and self.player_consecutive_moves < 10:
                next_player_id = player_id
                move_count = self.player_consecutive_moves + 1
            else:
                next_player_id = 3 - player_id
                move_count = 1

            if throw.has_khal():
                board_after_insertion = board.insert_piece_and_copy(player_id)
                if board_after_insertion is not None:
                    for piece in board_after_insertion.get_player_pieces(player_id, Piece.IN_BOARD):
                        new_board = board_after_insertion.move_piece_and_copy(piece, throw)
                        if new_board is not None:
                            children.append(State(new_board, player_id, next_player_id, throw, move_count, self))

                throw = ShellThrow(i).omit_khal()
                for piece in self.board.get_player_pieces(player_id, Piece.IN_BOARD):
                    new_board = self.board.move_piece_and_copy(piece, throw)
                    if new_board is not None:
                        children.append(State(new_board, player_id, next_player_id, throw, move_count, self))
        return children

    def is_terminal(self):
        return max(len(self.board.get_player_pieces(1, Piece.IN_KITCHEN)),
                   len(self.board.get_player_pieces(2, Piece.IN_KITCHEN))) == 4
