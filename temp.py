self.pieces = []
        self.pieces_out_of_board = set()
        self.pieces_in_board = set()
        self.pieces_in_kitchen = set()
        if pieces:
            for piece in pieces:
                self.pieces.append(piece)
                if piece.stage == Piece.OUT_OF_BOARD:
                    self.pieces_out_of_board.add(piece)
                elif piece.stage == Piece.KITCHEN:
                    self.pieces_in_kitchen.add(piece)
                else:
                    self.pieces_in_board.add(piece)
        else:
            for number in range(4):
                self.pieces.append(
                    Piece(player=self, number=number))
            for piece in self.pieces:
                self.pieces_out_of_board.add(piece)