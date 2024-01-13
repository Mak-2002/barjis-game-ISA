import copy


class Player:
    MODE_HUMAN = 1
    MODE_COMPUTER = 2

    def __init__(self, player_id, mode):
        self.id = player_id
        self.mode = mode

    def __deepcopy__(self):
        new_pieces = [copy.copy(piece) for piece in self.pieces]
        new_player = Player(self.mode, self.board, new_pieces)
        new_player.number = self.number
        for piece in new_player.pieces:
            piece.player = new_player
        return new_player
