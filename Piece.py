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
    SHORT_LANE_FIRST_TIME = 1
    MAIN_LANE = 2
    SHORT_LANE_LAST_TIME = 3
    KITCHEN = 4

    def __init__(self, player, board: Board):
        self.board = board
        self.position = 0
        self.stage = 0
        # stage:
        #   0: out of board
        #   1: in it's 7-block lane for the first time
        #   2: in main lane
        #   3: in it's 7-block for the last time
        #   4: in kitchen
        self.steps_taken = 0
        self.player = player

        self.enter_board()

    def __copy__(self):
        new_piece = Piece(self.player, self.board)
        new_piece.position = self.position
        new_piece.stage = self.stage
        new_piece.steps_taken = self.steps_taken

    def knock_out_of_board(self):
        self.position = -1
        self.stage = self.OUT_OF_BOARD
        self.player.pieces_in_game.discard(self)
        self.player.pieces_out_of_game.add(self)

    def enter_board(self):
        self.position = 0
        self.steps_taken = 0
        self.stage = self.SHORT_LANE_FIRST_TIME
        self.player.pieces_in_game.add(self)
        self.player.pieces_out_of_game.discard(self)

    def enter_kitchen(self):
        self.position = -1
        self.stage = self.KITCHEN
        self.player.pieces_in_kitchen.add(self)
        self.player.pieces_in_game.discard(self)

    def assign_lane(self):
        steps_taken = self.steps_taken
        if steps_taken > 83:
            return None

        if steps_taken <= 6:
            self.stage = self.SHORT_LANE_FIRST_TIME
            self.position = steps_taken
        elif steps_taken <= 75:
            self.stage = self.MAIN_LANE
            self.position = self.board.update_index(0, steps_taken - 7 + (self.player.number - 1) * 36)
        elif steps_taken < 83:
            self.stage = self.SHORT_LANE_LAST_TIME
            self.position = 6 - (steps_taken - 76)
        elif steps_taken == 83:
            self.stage = self.KITCHEN
            self.position = -1
        return self

    def study_move(self, throw: ShellThrow):
        new_piece = copy.copy(self)
        new_piece.steps_taken += throw.moves
        return new_piece.assign_lane()

    def move(self, move):
