import copy
from collections import defaultdict

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

    def __init__(self, game: Game):
        self.x_blocks = set()
        self.game = game
        # data should be a 3d array
        # the 1st index represents arm number, the 2nd and 3rd represent the arm

        # We designed the board to be split into three lanes
        # the zeros is the mutual lane that goes around the circumference of board, and has the length of 68
        # the first is a 7-blocks lane that only the first player will cross
        # the second is the second player's one

        self.piece_count = [defaultdict(int) for _ in range(3)]
        self.piece_ownership_in_main_lane_block = {}

    def fill_board(self, data):
        self.locate_x_blocks(data)

    def __deepcopy__(self, memo):
        # Create a shallow copy of the object
        new_board = Board(self.game)

        new_board.x_blocks = copy.deepcopy(self.x_blocks, memo)
        new_board.game = self.game  # game doesn't need deep copying

        new_board.piece_count = copy.deepcopy(self.piece_count, memo)

        new_board.piece_ownership_in_main_lane_block = copy.deepcopy(self.piece_ownership_in_main_lane_block, memo)

        return new_board

    def locate_x_blocks(self, data):
        arm = 0
        index = 61
        # let's clarify why we chose 61 as the starting index: we assumed that index 0 is the index the first player
        # lands on when he enters the main lane, so, we shifted back 8 positions before index 0 to reach the start of
        # the arm, and because the main lane is a cyclic lane of 68 blocks, we land on 61
        j, i = 0, 0

        def add_to_x_blocks():
            if data[arm][i][j] == 'X':
                self.x_blocks.add(index)

        while arm < 4:
            j, i = 0, 0

            # checking through blocks 0,0 to 0,7
            while j < 8:
                add_to_x_blocks()
                index = self.update_index(index, 1)
                j += 1

            # checking block 1,7
            j -= 1
            i += 1
            add_to_x_blocks()
            index = self.update_index(index, 1)

            # checking through 2,7 to 2,0
            i += 1
            while j >= 0:
                add_to_x_blocks()
                index = self.update_index(index, 1)
                j -= 1

            # moving to the next arm
            arm += 1

    def update_index(self, index, move):
        return (index + move) % self.MAIN_LANE_LENGTH

    def check_if_x_block(self, index):
        return index in self.x_blocks

    def get_main_lane_block_ownership(self, index):
        if index not in self.piece_ownership_in_main_lane_block:
            return None
        return self.piece_ownership_in_main_lane_block[index]

    def main_lane_block_belongs_to_player(self, index, player: Player):
        return self.get_main_lane_block_ownership(index) in [0, player.number]

    def remove_pieces_from_main_lane_block(self, index):
        player_number = self.get_main_lane_block_ownership(index)
        if player_number == 0:
            return
        player = self.game.players[player_number]
        pieces_in_block = [piece for piece in player.pieces_in_game if piece.position == index]
        for piece in pieces_in_block:
            piece.knock_out_of_board()
        self.piece_count[0][index] = 0

    def replace_piece(self, old_piece: Piece, new_piece: Piece):
        # todo: store state
        old_lane = old_piece.get_lane()
        self.piece_count[old_lane][old_piece.position] -= 1
        if self.piece_count[old_lane][old_piece.position] == 0 and old_lane == self.MAIN_LANE:
            self.piece_ownership_in_main_lane_block -= {old_piece.position}

        new_lane = new_piece.get_lane()
        other_player = self.game.players[3 - new_piece.player.number]
        if new_lane == self.MAIN_LANE:
            index = new_piece.position
            if self.get_main_lane_block_ownership(index) == other_player:
                self.remove_pieces_from_main_lane_block(index)
            self.piece_ownership_in_main_lane_block[index] = new_piece.player

        self.piece_count[new_lane][new_piece.position] += 1

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
                index = self.update_index(index, 1)
                j += 1

            # checking block 1,7
            j -= 1
            i += 1
            data[arm][i][j] = self.get_print_str(index, self.MAIN_LANE)
            index = self.update_index(index, 1)

            # checking through 2,7 to 2,0
            i += 1
            while j >= 0:
                data[arm][i][j] = self.get_print_str(index, self.MAIN_LANE)
                index = self.update_index(index, 1)
                j -= 1

        j = 0
        while j < 7:
            data[0][1][j] = self.get_print_str(j, self.PLAYER1_LANE)
            data[2][1][j] = self.get_print_str(j, self.PLAYER2_LANE)

        return output_manip.get_board_str(data[0], data[1], data[2], data[3])
