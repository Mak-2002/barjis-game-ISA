class Piece:
    """
     The class that represents a playing piece for one player
     it contains:
        position
        player
        lane
    """

    def __init__(self, player):
        self.position = -1
        # position:
        #   -1: out of board
        #   -2: in kitchen

        self.player = player
        self.lane = player
