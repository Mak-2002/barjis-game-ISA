from collections import defaultdict

from Piece import Piece
from Player import Player


class Board:
    PLAYER1_LANE = 1
    PLAYER2_LANE = 2
    MAIN_LANE = 3
    MAIN_LANE_LENGTH = 68
    lengths = [MAIN_LANE_LENGTH, 7, 7]

    def __init__(self, data, game):
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

        self.locate_x_blocks(data)

    def locate_x_blocks(self, data):
        arm = 0
        index = 61
        # let's clarify why we chose 61 as the starting index: we assumed that index 0 is the index the first player
        # lands on when he enters the main lane, so, we shifted back 8 positions before index 0 to reach the start of
        # the arm, and because the main lane is a cyclic lane of 68 blocks, we land on 61
        i, j = 0, 0

        def add_to_x_blocks():
            if data[arm][i][j] == 'X':
                self.x_blocks.add(index)

        while arm < 4:
            i, j = 0, 0

            # checking through blocks 0,0 to 0,7
            while i < 8:
                add_to_x_blocks()
                index = self.update_index(index, 1)
                i += 1

            # checking block 1,7
            i -= 1
            j += 1
            add_to_x_blocks()
            index = self.update_index(index, 1)

            # checking through 2,7 to 2,0
            j += 1
            while i >= 0:
                add_to_x_blocks()
                index = self.update_index(index, 1)
                i -= 1

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
        player = self.game.player[player_number]
        pieces_in_block = [piece for piece in player.pieces_in_game if piece.position == index]
        for piece in pieces_in_block:
            piece.knock_out_of_board()
        self.piece_count[0] -= {index}

    def replace_piece(self, old_piece: Piece, new_piece: Piece):
        old_lane = old_piece.get_lane()
        self.piece_count[old_lane][old_piece.position] -= 1
        if self.piece_count[old_lane][old_piece.position] == 0:
            self.piece_count[old_lane] -= {old_piece.position}
            if old_lane == self.MAIN_LANE:
                self.piece_ownership_in_main_lane_block[old_piece.position] = None

        new_lane = new_piece.get_lane()
        other_player = self.game.players[3 - new_piece.player.number]
        if new_lane == self.MAIN_LANE:
            index = new_piece.position
            if self.get_main_lane_block_ownership(index) == other_player:
                self.remove_pieces_from_main_lane_block(index)
            self.piece_ownership_in_main_lane_block[index] = new_piece.player

        self.piece_count[new_lane][new_piece.position] += 1
