from typing import List, Optional

from Piece import Piece
from Player import Player


class Board:
    PLAYER1_LANE = 1
    PLAYER2_LANE = 2
    MAIN_LANE = 3
    MAIN_LANE_LENGTH = 68

    def __init__(self, data):
        self.x_blocks = set()

        # data should be a 3d array
        # the 1st index represents arm number, the 2nd and 3rd represent the arm

        # We designed the board to be split into three lanes
        # the first is a 7-blocks lane that only the first player will cross
        # the second is the second player's one
        # the third is the mutual lane that goes around the circumference of board, and has the length of 68

        lengths = [self.MAIN_LANE_LENGTH, 7, 7]

        self.lanes: List[List[Optional[Piece]]] = [[None] * length for length in lengths]
        # for each block of main lane, it's value will be:
        #   0: if it's empty
        #   1: occupied by first player
        #   2: occupied by second player

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

    def check_ownership(self, index):
        if not self.lanes[0][index]:
            return 0
        return self.lanes[0][index].player

    def belongs_to_this_player(self, player: Player, index):
        return self.check_ownership(index) in [0, player.number]
