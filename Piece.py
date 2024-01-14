import copy

from ShellThrow import ShellThrow


class Piece:
    OUT_OF_BOARD = 0
    IN_BOARD = 1
    IN_KITCHEN = 2

    def __init__(self, player_id: int, number: int):
        self.player_id = player_id
        self.number = number
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

    def __eq__(self, other):
        return (isinstance(other, Piece) and self.number == other.number and self.status == other.status and
                self.steps_taken == other.steps_taken)

    def knock_out_of_board(self):
        self.position = -1
        self.lane = -1
        self.status = Piece.OUT_OF_BOARD

    def enter_board(self):
        self.position = 0
        self.steps_taken = 0
        self.lane = self.player_id
        self.last_lane = False
        self.status = Piece.IN_BOARD

    def enter_kitchen(self):
        self.position = -1
        self.lane = -1
        self.last_lane = False
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
            self.last_lane = False
            self.position = (steps_taken - 7 + (self.player_id - 1) * 34) % 68
        elif steps_taken < 83:
            self.position = 6 - (steps_taken - 76)
            self.lane = self.player_id
            self.last_lane = True
        elif steps_taken == 83:
            self.enter_kitchen()
            return self
        self.status = Piece.IN_BOARD
        return self

    def apply_move_and_copy(self, throw: ShellThrow, board):
        new_piece = copy.copy(self)
        new_piece.steps_taken += throw.moves
        new_piece = new_piece.assign_lane()
        if not new_piece:
            return None
        pieces_in_block = board.get_pieces_in_position(new_piece.position, new_piece.lane)
        if pieces_in_block and pieces_in_block[0].player_id != new_piece.player_id:
            if new_piece.position in board.x_blocks:
                return None
            board.remove_pieces_from_main_lane_block(new_piece.position)
        return new_piece
