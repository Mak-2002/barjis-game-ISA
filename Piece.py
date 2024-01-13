import copy

from Board import Board
from ShellThrow import ShellThrow


class Piece:
    """
     The class that represents a playing piece for one player
     it contains:
        position
        player
        lane
    """

    OUT_OF_BOARD = 0
    IN_BOARD = 1
    IN_KITCHEN = 2

    def __init__(self, player_id: int, number: int):
        self.number = number
        self.player_id = player_id
        self.position = -1
        self.lane = -1
        self.last_lane = False
        self.status = Piece.OUT_OF_BOARD
        self.steps_taken = 0

    def __copy__(self):
        new_piece = Piece(self.player_id, self.number)
        new_piece.position = self.position
        new_piece.lane = self.lane
        new_piece.last_lane = self.last_lane
        new_piece.status = self.status
        new_piece.steps_taken = self.steps_taken
        return new_piece

    def knock_out_of_board(self):
        self.position = -1
        self.lane = -1
        self.status = Piece.OUT_OF_BOARD

    def enter_board(self):
        self.position = 0
        self.steps_taken = 0
        self.lane = self.player_id
        self.status = Piece.IN_BOARD

    def enter_kitchen(self):
        self.position = -1
        self.lane = -1
        self.status = Piece.IN_KITCHEN

    def assign_lane(self):
        steps_taken = self.steps_taken
        if steps_taken > 83:
            return None

        if steps_taken <= 6:
            self.position = steps_taken
            self.lane = self.player_id
            self.last_lane = False
        elif steps_taken <= 75:
            self.lane = 0
            self.position = Board.update_index(0, steps_taken - 7 + (self.player_id - 1) * 36)
        elif steps_taken < 83:
            self.position = 6 - (steps_taken - 76)
            self.lane = self.player_id
            self.last_lane = True
        elif steps_taken == 83:
            self.enter_kitchen()
        return self

    def get_new_piece_after_applying_move(self, throw: ShellThrow):
        new_piece = copy.copy(self)
        new_piece.steps_taken += throw.moves
        return new_piece.assign_lane()
