from Game import Game
from Piece import Piece
from ShellThrow import ShellThrow
from State import State


class Player:
    current_player_number = 1
    HUMAN = 1
    COMPUTER = 2

    def __init__(self, mode, game: Game):
        if Player.current_player_number == 3:
            raise Exception('This is a 2-player game')

        self.number = Player.current_player_number
        self.mode = mode
        self.game = game
        self.pieces = []
        for number in range(4):
            self.pieces.append(
                Piece(player=self, board=self.game.board, number=number))
        self.pieces_out_of_game = set()
        for piece in self.pieces:
            self.pieces_out_of_game.add(piece)

        self.pieces_in_game = set()
        self.pieces_in_kitchen = set()
        Player.current_player_number += 1

    def make_move(self, can_insert: bool = True, subsequent_move_count: int = 1):
        if subsequent_move_count > 10:
            return

        throw = ShellThrow()
        if self.mode == self.HUMAN:
            self.human_move(throw, can_insert)
        else:
            self.computer_move(throw, can_insert)

        if throw.reserves_turn():
            self.make_move(can_insert=False, subsequent_move_count=subsequent_move_count + 1)
        else:
            self.game.switch_turn()

    def computer_move(self, throw: ShellThrow, can_insert):
        # TODO
        pass

    def human_move(self, throw: ShellThrow, can_insert):
        print(self.game.board)

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
            if piece.study_move(throw) is not None:
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
        piece = self.pieces_out_of_game.pop()
        piece.enter_board()

    def move_piece_with_number(self, number, throw, a_new_piece_inserted: bool = False):
        for piece in self.pieces_in_game:
            if isinstance(piece, Piece) and piece.number == number:
                new_piece = piece.study_move(throw)
                self.game.board.replace_piece(piece, new_piece)
                self.pieces_in_game.discard(piece)
                if new_piece.stage == Piece.KITCHEN:
                    self.pieces_in_kitchen.add(new_piece)
                else:
                    self.pieces_in_game.add(new_piece)
                state = State(self.game.board, self, piece, new_piece, a_new_piece_inserted)
                self.game.history.append(state)
                return
        raise Exception(f"you have no pieces with the number {number} in the game")
