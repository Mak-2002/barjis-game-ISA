import copy
from typing import List

from BarjisGame import BarjisGame
from Board import Board
from Piece import Piece
from ShellThrow import ShellThrow


class State:
    def __init__(self, board: Board,
                 previous_player_id,
                 player_id,
                 player_consecutive_moves=1,
                 parent_state=None):
        self.board = board
        self.previous_player_id = previous_player_id
        self.player_id = player_id
        # self.throw = throw
        self.player_consecutive_moves = player_consecutive_moves
        self.parent = parent_state
        self.best_child = [None for _ in range(7)]
        self.cost = 0
        self.children: List[List[State]] = [[] for _ in range(7)]

    def __eq__(self, other):
        return self.player_id == other.player_id and self.board == other.board

    def winner(self):
        for i in range(1, 3):
            if len(self.board.get_player_pieces(i, Piece.IN_KITCHEN)) == 4:
                return i
        return 0

    @staticmethod
    def sign_due_to_player(player_id):
        if player_id == 1:
            return 1
        return -1

    def human_play(self):
        throw = ShellThrow()
        board = copy.deepcopy(self.board)
        print(board, end='\n\n')
        print_str = f"you have thrown the shells and you got {throw.name} with {throw.moves} moves"
        print_str += f" and an additional khal step" if throw.has_khal() else ""
        print(print_str)
        pieces_in_board = board.get_player_pieces(self.player_id, Piece.IN_BOARD)
        if throw.has_khal():
            if not pieces_in_board:
                board = board.insert_piece_and_copy(self.player_id)
                print('a new piece have been inserted...')
            else:
                choice = input('do you want to insert a piece? (y/n): ')
                if choice == 'y':
                    board = board.insert_piece_and_copy(self.player_id)
                    print('a new piece have been inserted...')
                else:
                    throw.omit_khal()
        movable_pieces = [piece for piece in pieces_in_board if piece.apply_move_and_copy(throw, board)]
        if movable_pieces:
            print('Pieces you can move:\n', ', '.join(str(piece.number) for piece in movable_pieces))
            choice = int(input('choose number to move: '))
            board.pieces[choice] = board.pieces[choice].apply_move_and_copy(throw, board)
        else:
            print('no pieces can be moved :(')
        if not self.children[throw.result]:
            BarjisGame.expectiminimax_from_state(self)
        for child in self.children[throw.result]:
            if child.board == board:
                return child
        return self.children[throw.result][0]

    def computer_play(self):
        throw = ShellThrow()
        if not self.best_child[throw.result]:
            BarjisGame.expectiminimax_from_state(self)

        if not self.best_child[throw.result]:
            return self.children[throw.result].pop()
        return self.best_child[throw.result]

    def get_children(self):
        player_id = self.player_id
        children: List[List[State]] = [[] for i in range(7)]
        for i in range(7):
            throw = ShellThrow(i)

            if throw.reserves_turn() and self.player_consecutive_moves < 10:
                next_player_id = player_id
                move_count = self.player_consecutive_moves + 1
            else:
                next_player_id = 3 - player_id
                move_count = 1

            if throw.has_khal():
                board_after_insertion = self.board.insert_piece_and_copy(player_id)
                if board_after_insertion is not None:
                    for piece in board_after_insertion.get_player_pieces(player_id, Piece.IN_BOARD):
                        new_board = board_after_insertion.move_piece_and_copy(piece, throw)
                        if new_board is not None:
                            children[i].append(State(new_board, player_id, next_player_id, move_count, self))

                throw = ShellThrow(i)
                throw.omit_khal()
            for piece in self.board.get_player_pieces(player_id, Piece.IN_BOARD):
                new_board = self.board.move_piece_and_copy(piece, throw)
                if new_board is not None:
                    children[i].append(State(new_board, player_id, next_player_id, move_count, self))

            if not children[i]:
                children[i].append(State(copy.deepcopy(self.board), player_id, next_player_id, move_count, self))
        return children

    def is_terminal(self):
        return max(len(self.board.get_player_pieces(1, Piece.IN_KITCHEN)),
                   len(self.board.get_player_pieces(2, Piece.IN_KITCHEN))) == 4

    def heuristic(self):
        score = 0
        for piece in self.board.pieces:
            sign = State.sign_due_to_player(piece.player_id)
            if piece.status == Piece.IN_KITCHEN:
                score += 100 * sign
            elif piece.status == Piece.IN_BOARD:
                if piece.lane == piece.player_id and piece.last_lane:
                    score += 15 * sign
                score += piece.steps_taken * sign
                if piece.lane == Board.MAIN_LANE and piece.position in self.board.x_blocks:
                    score += 10 * sign
        return score
