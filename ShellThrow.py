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

    move_names = {
        0: 'shakka',
        1: 'dast',
        2: 'dawaq',
        3: 'thalatha',
        4: 'arba3a',
        5: 'banj',
        6: 'bara'
    }

    probability = {
        0: 1 / 64,
        1: 6 / 64,
        2: 15 / 64,
        3: 20 / 64,
        4: 15 / 64,
        5: 6 / 64,
        6: 1 / 64
    }

    def __init__(self, number=-1):
        # simulate the throw of the six shells
        # we throw each one individually, then count the shells with their mouths down
        if number == -1:
            mouths_down = 0
            for _ in range(6):
                mouths_down += random.choice([0, 1])
            self.result = mouths_down
        else:
            self.result = number

        self.khal = int(self.has_khal())
        self.moves = ShellThrow.moves_due_result[self.result]
        self.probability = ShellThrow.probability[self.result]

    def has_khal(self):
        return self.result in [1, 5]

    def reserves_turn(self):
        return self.result in [0, 1, 5, 6]

    def omit_khal(self):
        self.moves += self.khal
        self.khal = 0

    def name(self):
        return self.move_names[self.result]
