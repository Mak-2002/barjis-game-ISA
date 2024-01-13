import copy
from typing import List

import output_manip
from Piece import Piece
from Player import Player
from ShellThrow import ShellThrow


class Board:
    MAIN_LANE = 0
    PLAYER1_LANE = 1
    PLAYER2_LANE = 2
    MAIN_LANE_LENGTH = 68
    lengths = [MAIN_LANE_LENGTH, 7, 7]

    def __init__(self, initial_data=None):

        self.pieces: List[Piece] = []

        self.players = {
            1: Player(player_id=1, mode=Player.MODE_COMPUTER),
            2: Player(player_id=2, mode=Player.MODE_COMPUTER)
        }

        self.x_blocks = set()
        # data should be a 3d array
        # the 1st index represents arm number, the 2nd and 3rd represent the arm

        # We designed the board to be split into three lanes
        # the zeros is the mutual lane that goes around the circumference of board, and has the length of 68
        # the first is a 7-blocks lane that only the first player will cross
        # the second is the second player's one
        self.locate_x_blocks(initial_data)

        for i in range(1, 5):
            self.pieces.append(Piece(1, i))

        for i in range(5, 9):
            self.pieces.append(Piece(2, i))

    def __deepcopy__(self):
        new_board = Board()
        new_board.x_blocks = self.x_blocks.copy()
        new_board.pieces = [copy.copy(piece) for piece in self.pieces]
        return new_board

    def locate_x_blocks(self, data):
        index = 61
        # let's clarify why we chose 61 as the starting index: we assumed that index 0 is the index the first player
        # lands on when he enters the main lane, so, we shifted back 8 positions before index 0 to reach the start of
        # the arm, and because the main lane is a cyclic lane of 68 blocks, we land on 61
        j, i = 0, 0

        def add_to_x_blocks():
            if data[arm][i][j] == 'X':
                self.x_blocks.add(index)

        for arm in range(4):
            j, i = 0, 0

            # checking through blocks 0,0 to 0,7
            while j < 8:
                add_to_x_blocks()
                index = Board.update_index(index, 1)
                j += 1

            # checking block 1,7
            j -= 1
            i += 1
            add_to_x_blocks()
            index = Board.update_index(index, 1)

            # checking through 2,7 to 2,0
            i += 1
            while j >= 0:
                add_to_x_blocks()
                index = Board.update_index(index, 1)
                j -= 1

    @staticmethod
    def update_index(index, move):
        return (index + move) % Board.MAIN_LANE_LENGTH

    def check_if_x_block(self, index):
        return index in self.x_blocks

    def get_main_lane_block_ownership(self, index):
        for piece in self.pieces:
            if piece.lane == Board.MAIN_LANE and piece.position == index:
                return piece.player_id
        return 0

    def remove_pieces_from_main_lane_block(self, index):
        player_id = self.get_main_lane_block_ownership(index)
        if player_id == 0:
            return
        player = self.players[player_id]
        pieces_in_block = [piece for piece in self.pieces if piece.position == index and piece.lane == Board.MAIN_LANE]
        for piece in pieces_in_block:
            piece.knock_out_of_board()

    def get_pieces_in_position(self, lane, index):
        return [piece for piece in self.pieces if piece.position == index and piece.lane == lane]

    def get_player_pieces(self, player_id, status=-1):
        pieces = [piece for piece in self.pieces if piece.player_id == player_id]
        if status == -1:
            return pieces
        return [piece for piece in pieces if piece.status == status]

    def get_print_str_for_index(self, index, lane=MAIN_LANE):
        pieces_in_block = self.get_pieces_in_position(index, lane)
        if not pieces_in_block:
            if index in self.x_blocks and lane == Board.MAIN_LANE:
                return 'X'
            return ' '

        player_id = pieces_in_block[0].player_id
        return f"{player_id}:{','.join(map(str, pieces_in_block))}"

    def insert_piece_and_copy(self, player_id):
        new_board = copy.deepcopy(self)
        pieces_out_of_board = new_board.get_player_pieces(player_id, Piece.OUT_OF_BOARD)
        if not pieces_out_of_board:
            return None
        pieces_out_of_board[0].enter_board()
        # TODO: test
        return new_board

    def __str__(self):
        data = [[['' for _ in range(8)] for _ in range(3)] for _ in range(4)]

        index = 61
        # let's clarify why we chose 61 as the starting index: we assumed that index 0 is the index the first player
        # lands on when he enters the main lane, so, we shifted back 8 positions before index 0 to reach the start of
        # the arm, and because the main lane is a cyclic lane of 68 blocks, we land on 61

        for arm in range(4):
            j, i = 0, 0

            # checking through blocks 0,0 to 0,7
            while j < 8:
                data[arm][i][j] = self.get_print_str_for_index(index, self.MAIN_LANE)
                index = Board.update_index(index, 1)
                j += 1

            # checking block 1,7
            j -= 1
            i += 1
            data[arm][i][j] = self.get_print_str_for_index(index, self.MAIN_LANE)
            index = Board.update_index(index, 1)

            # checking through 2,7 to 2,0
            i += 1
            while j >= 0:
                data[arm][i][j] = self.get_print_str_for_index(index, self.MAIN_LANE)
                index = Board.update_index(index, 1)
                j -= 1

        j = 0
        while j < 7:
            data[0][1][j] = self.get_print_str_for_index(j, self.PLAYER1_LANE)
            data[2][1][j] = self.get_print_str_for_index(j, self.PLAYER2_LANE)
            j += 1

        return output_manip.get_board_str(data[0], data[1], data[2], data[3])

    def move_piece_and_copy(self, piece: Piece, throw: ShellThrow):
        new_board = copy.deepcopy(self)
        new_piece = new_board.pieces[piece.number].get_new_piece_after_applying_move(throw)
        if not new_piece:
            return None
        new_board.pieces[piece.number] = new_piece
        return new_board

    def get_piece_with_number(self, player_id, number):
        result = [piece for piece in self.pieces if piece.player_id == player_id and piece.number == number]
        if result:
            return result[0]
        return None
