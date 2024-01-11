from Board import Board
from Piece import Piece
from ShellThrow import ShellThrow


class Player:
    current_player_number = 1
    HUMAN = 1
    COMPUTER = 2

    def __init__(self, mode, board: Board):
        if Player.current_player_number == 3:
            raise Exception('This is a 2-player game')

        self.number = Player.current_player_number
        self.mode = mode
        self.board = board
        self.pieces = [Piece(player=Player.current_player_number, board=self.board) for _ in range(4)]
        self.pieces_out_of_game = set()
        for piece in self.pieces:
            self.pieces_out_of_game.add(piece)

        self.pieces_in_game = set()
        self.pieces_in_kitchen = set()
        Player.current_player_number += 1

    def make_move(self, can_insert: bool = True):
        throw = ShellThrow()
        if self.mode == self.HUMAN:
            self.human_move(throw, can_insert)
        else:
            self.computer_move(throw, can_insert)

        if throw.reserves_turn():
            self.make_move(can_insert=False)

    def computer_move(self, throw: ShellThrow, can_insert):
        pass

    def human_move(self, throw: ShellThrow, can_insert):
        possible_moves = set()
        if can_insert and len(self.pieces_out_of_game) > 0 and throw.has_khal():
            choice = input('do you want to insert a piece? (y/n): ')
            if choice == 'y':
                self.insert_piece()
            else:
                throw.omit_khal()
        else:
            throw.omit_khal()

        for piece in self.pieces:
            if piece.study_move(throw) is not None:
                possible_moves.add(piece)
        if possible_moves:
            # TODO
            pass

    def insert_piece(self):
        piece = self.pieces_out_of_game.pop()
        piece.enter_board()
