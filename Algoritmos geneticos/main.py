from game import *
from player import *

size = 50
numSnakes = 1
players = [RandomPlayer(0)]
guiSize=800


#Tamaño de poblacion
pop_size=100
#Cantidad de generaciones
num_generations=100
num_trails=1
windows_size=7
hidden_size=15
#Tamaño del tablero
board_size=10
genPlayer=GeneticPlayer(pop_size, num_generations, num_trails, windows_size, hidden_size, board_size, mutation_chance=0.1, mutation_size=0.1)
genPlayer.evolve_pop()