import initial_data
from Game import Game

game = Game(initial_data.board, computer=False)
game.start()
