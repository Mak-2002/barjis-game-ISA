import random

from Piece import Piece


class Player:
    current_player_number = 1
    HUMAN = 1
    COMPUTER = 2

    throw_result_moves = {
        0: 6,
        1: 10,  # khal
        2: 2,
        3: 3,
        4: 4,
        5: 24,  # khal
        6: 12,
    }

    def __init__(self, mode):
        if Player.current_player_number == 3:
            raise Exception('This is a 2-player game')

        self.number = Player.current_player_number
        self.mode = mode
        self.pieces = [Piece(player=Player.current_player_number) for _ in range(4)]
        Player.current_player_number += 1

    def make_move(self):
        self.human_move() if self.mode == self.HUMAN else self.computer_move()

    def computer_move(self):
        throw_result = self.throw_shells()

    def human_move(self):
        throw_result = self.throw_shells()

    @staticmethod
    def throw_result_has_khal(throw_result):
        return throw_result in [1, 5]

    @staticmethod
    def throw_shells():
        mouths_down = 0
        for _ in range(6):
            mouths_down += random.choice([0, 1])
        return mouths_down
