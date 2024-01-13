import copy

from Piece import Piece
from ShellThrow import ShellThrow


class Player:
    MODE_HUMAN = 1
    MODE_COMPUTER = 2

    def __init__(self, player_id, mode):
        self.id = player_id
        self.mode = mode

    def make_move(self, can_insert: bool = True):

        if self.mode == self.MODE_HUMAN:
            self.human_move(can_insert)
        else:
            self.computer_move()

    def computer_move(self, can_insert):

        pass

    def human_move(self, can_insert, subsequent_move_count: int = 1):
        if subsequent_move_count > 10:
            return
        print(self.board)
        throw = ShellThrow()
        insert_piece = False
        print(f"you have {throw.name()}")
        if can_insert and self.pieces_out_of_game and throw.has_khal():
            choice = input('do you want to insert a piece? (y/n): ')
            if choice == 'y':
                insert_piece = True
            else:
                throw.omit_khal()
        else:
            throw.omit_khal()

        movable_pieces = set()
        for piece in self.pieces_in_game:
            if piece.get_new_piece_after_applying_move(throw) is not None:
                movable_pieces.add(piece)
        if movable_pieces:
            print('pick one of the following pieces to move: ')
            for piece in movable_pieces:
                print(piece.number, end=' ')
            choice = input()
            self.move_piece_with_number(choice, throw, insert_piece)
        else:
            print('you cannot move any piece in the game')
        self.insert_piece() if insert_piece else None

    def insert_piece(self):
        P

    def move_piece_with_number(self, number, throw):
        new_board = copy.deepcopy(self.board)
        for piece in self.pieces_in_game:
            if isinstance(piece, Piece) and piece.number == number:
                new_piece = piece.get_new_piece_after_applying_move(throw)
                new_board.replace_piece(piece, new_piece)
                new_player = new_board.players[self.number]
                new_player.pieces_in_game.discard(piece)
                if new_piece.stage == Piece.KITCHEN:
                    new_piece.enter_kitchen()
                else:
                    new_player.pieces_in_game.add(new_piece)
                return new_board
        raise Exception(f"you have no pieces with the number {number} in the game")

    def __deepcopy__(self):
        new_pieces = [copy.copy(piece) for piece in self.pieces]
        new_player = Player(self.mode, self.board, new_pieces)
        new_player.number = self.number
        for piece in new_player.pieces:
            piece.player = new_player
        return new_player
