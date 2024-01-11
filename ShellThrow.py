import random


class ShellThrow:
    moves_due_result = {
        0: 6,
        1: 10,
        2: 2,
        3: 3,
        4: 4,
        5: 24,
        6: 12,
    }

    move_name = {
        0: 'shakka',
        1: 'dast',
        2: 'dawaq',
        3: 'thalatha',
        4: 'arba3a',
        5: 'banj',
        6: 'bara'
    }

    def __init__(self):
        # simulate the throw of the six shells
        # we throw each one individually, then count the shells with their mouths down
        mouths_down = 0
        for _ in range(6):
            mouths_down += random.choice([0, 1])
        self.result = mouths_down
        self.moves = ShellThrow.moves_due_result[self.result]

    def has_khal(self):
        return self.result in [1, 5]

    def reserves_turn(self):
        return self.result in [0, 1, 5, 6]
