from Piece import Piece
from ShellThrow import ShellThrow


class Player:
    current_player_number = 1
    HUMAN = 1
    COMPUTER = 2

    def __init__(self, mode):
        if Player.current_player_number == 3:
            raise Exception('This is a 2-player game')

        self.number = Player.current_player_number
        self.mode = mode

        self.pieces = [Piece(player=Player.current_player_number) for _ in range(4)]
        self.pieces_out_of_game = set()
        for piece in self.pieces:
            self.pieces_out_of_game.add(piece)

        self.pieces_in_game = set()
        self.pieces_in_kitchen = set()
        Player.current_player_number += 1

    def make_move(self, can_insert: bool = True):
        possible_moves = set()
        throw = ShellThrow()
        for piece in self.pieces:
            if piece.study_move(throw) is not None:
                possible_moves.add(piece)

        self.human_move(possible_moves) if self.mode == self.HUMAN else self.computer_move(possible_moves)
        if throw.reserves_turn():
            self.make_move(can_insert=False)

    def computer_move(self, possible_moves):
        pass

    def human_move(self, possible_moves):
        pass
