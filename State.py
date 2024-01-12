import copy

from Board import Board
from Piece import Piece
from Player import Player


class State:
    def __init__(self, board: Board, player: Player, old_piece: Piece, new_piece: Piece,
                 a_piece_inserted: bool = False):
        self.board = copy.deepcopy(board)
        self.player = player
        self.old_piece = old_piece
        self.new_piece = new_piece
        self.a_piece_inserted = a_piece_inserted
