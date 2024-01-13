import copy
from typing import List

import output_manip
from Game import Game
from Piece import Piece
from Player import Player


class Board:
    MAIN_LANE = 0
    PLAYER1_LANE = 1
    PLAYER2_LANE = 2
    MAIN_LANE_LENGTH = 68
    lengths = [MAIN_LANE_LENGTH, 7, 7]

    def __init__(self, game: Game, initial_data=None):

        self.pieces: List[Piece] = []

        self.players = {
            1: Player(player_id=1, mode=Player.MODE_COMPUTER),
            2: Player(player_id=2, mode=Player.MODE_COMPUTER)
        }

        self.x_blocks = set()
        self.game = game
        # data should be a 3d array
        # the 1st index represents arm number, the 2nd and 3rd represent the arm

        # We designed the board to be split into three lanes
        # the zeros is the mutual lane that goes around the circumference of board, and has the length of 68
        # the first is a 7-blocks lane that only the first player will cross
        # the second is the second player's one
        self.locate_x_blocks(initial_data)

    def __deepcopy__(self):
        new_board = Board(self.game)
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

    def get_print_str(self, index, lane: int = 0):
        if lane == 0 and index in self.piece_ownership_in_main_lane_block:
            player = self.piece_ownership_in_main_lane_block[index]
            pieces = [piece.number for piece in player.pieces_in_game if
                      piece.position == index and piece.get_lane() == lane]
            return f"{player.number}:{','.join(map(str, pieces))}" if pieces else ''

        if lane != 0 and self.piece_count[lane][index] > 0:
            player = self.game.players[lane]
            pieces = [piece.number for piece in player.pieces_in_game if
                      piece.position == index and piece.get_lane() == lane]
            return f"{player.number}:{','.join(map(str, pieces))}" if pieces else ''

        if index in self.x_blocks and lane == self.MAIN_LANE:
            return 'X'

        return ' '

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
                    data[arm][i][j] = self.get_print_str(index, self.MAIN_LANE)
                    index = Board.update_index(index, 1)
                    j += 1

                # checking block 1,7
                j -= 1
                i += 1
                data[arm][i][j] = self.get_print_str(index, self.MAIN_LANE)
                index = Board.update_index(index, 1)

                # checking through 2,7 to 2,0
                i += 1
                while j >= 0:
                    data[arm][i][j] = self.get_print_str(index, self.MAIN_LANE)
                    index = Board.update_index(index, 1)
                    j -= 1

            j = 0
            while j < 7:
                data[0][1][j] = self.get_print_str(j, self.PLAYER1_LANE)
                data[2][1][j] = self.get_print_str(j, self.PLAYER2_LANE)

            return output_manip.get_board_str(data[0], data[1], data[2], data[3])
