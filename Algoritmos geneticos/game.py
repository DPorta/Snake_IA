import numpy as np
import tkinter as tk
import time as time
import random as rand

#Variables globales
UP=(-1,0)
DOWN=(1,0)
LEFT=(0,-1)
RIGHT=(0,1)

MOVES=[UP,DOWN,LEFT,RIGHT]

EMPTY = 0
FOOD = 99

class Game:
    def __init__(self, size, numSnakes, players, gui=None, display=False, maxTurns=100):
        self.size= size
        self.numSnakes = numSnakes
        self.players = players
        self.gui = gui
        self.display = display
        self.maxTurns = maxTurns

        self.numFood = 4
        self.turn = 0
        self.snakeSize = 3

        self.snakes = [[((j+1)*size//(2*self.numSnakes),self.size//2+i)for i in range (self.snakeSize)]
                     for j in range(self.numSnakes)]

        self.food = [(self.size//4, self.size//4),(3*self.size//4, self.size//4),
                     (self.size//4, 3*self.size//4),(3*self.size//4, 3*self.size//4)]

        self.playerIDs = [i for i in range (self.numSnakes)]

        self.board = np.zeros([self.size,self.size])
        for i in self.playerIDs:
            for tupla in self.snakes[i]:
                self.board[tupla[0]][tupla[1]] = i+1
        for tupla in self.food:
            self.board[tupla[0]][tupla[1]] = FOOD

        self.foodIndex = 0
        self.foodXY = [(rand.randint(0,9),rand.randint(0,9))for _ in range (200)]

    def move(self):
        moves = []
        #mover la cabeza del snake
        for i in self.playerIDs:
            snake_i = self.snakes[i]
            move_i = self.players[i].get_move(self.board, snake_i)
            moves.append(move_i)
            new_square = (snake_i[-1][0] + move_i[0], snake_i[-1][1] + move_i[1]) #a donde se mueve el snake
            snake_i.append(new_square)

        #acomodar su cola (si la cabeza no encuentra comida se actualiza la cola, sino se remueve la comida)
        for i in self.playerIDs:
            head_i=self.snakes[i][-1]
            if head_i not in self.food:
                self.board[self.snakes[i][0][0]][self.snakes[i][0][1]] = EMPTY
                self.snakes[i].pop(0)
            else:
                self.food.remove(head_i)

        #mirar que no salga de los limites
        for i in self.playerIDs:
            head_i=self.snakes[i][-1]
            if head_i[0] >= self.size or head_i[1] >=self.size or head_i[0] < 0 or head_i[1] < 0:
                self.playerIDs.remove(i)
            else:
                self.board[head_i[0]][head_i[1]] = i+1

        # mirar colisiones
        for i in self.playerIDs:
            head_i=self.snakes[i][-1]
            for j in range(self.numSnakes):
                if i==j:
                    if head_i in self.snakes[i][:-1]:
                        self.playerIDs.remove(i)
                else:
                    if head_i in self.snakes[j]:
                        self.playerIDs.remove(i)

        # aparecer comida
        while len(self.food)<self.numFood:
            x = self.foodXY[self.foodIndex][0]
            y = self.foodXY[self.foodIndex][1]
            while self.board[x][y] != EMPTY:
                self.foodIndex += 1
                x = self.foodXY[self.foodIndex][0]
                y = self.foodXY[self.foodIndex][1]

            self.food.append((x, y))
            self.board[x][y] = FOOD
            self.foodIndex += 1

        return moves

    def play(self, display, termination = False):
        #if display:
            #print("self.displayBoard()")
        while True:
            if termination:
                for i in self.playerIDs:
                    if len(self.snakes[0]) - self.turn/20 <= 0:
                        self.playerIDs.remove(i)
                        return -2
            if len(self.playerIDs) == 0:
                return -1
            if self.turn >= self.maxTurns:
                return 0
            moves = self.move()

            self.turn += 1
            if display:
                if self.gui is not None:
                    self.gui.update()
                time.sleep(1)

    def displayBoard(self):
        for i in range (self.size):
            for j in range (self.size):
                if self.board[i][j]==EMPTY:
                    print("|_",end="")
                elif self.board[i][j]==FOOD:
                    print("|#",end="")
                else:
                    print("|"+str(int(self.board[i][j])),end="")
            print("|")


class GUI:
    def __init__(self, game, size):
        self.game = game
        self.game.gui = self
        self.size = size

        self.ratio = self.size/self.game.size

        self.app= tk.Tk()
        self.app.title("Auto Snake")
        self.canvas=tk.Canvas(self.app, width=self.size,height=self.size,bg='#000000')
        self.canvas.pack()

        for i in range(len(self.game.snakes)):
            snake=self.game.snakes[i]
            self.canvas.create_rectangle(self.ratio*(snake[-1][1]), self.ratio*(snake[-1][0]),
                                         self.ratio*(snake[-1][1]+1), self.ratio*(snake[-1][0]+1),fill='white')
            for j in range(len(snake) - 1):
                self.canvas.create_rectangle(self.ratio * (snake[j][1]), self.ratio * (snake[j][0]),
                                             self.ratio * (snake[j][1] + 1), self.ratio * (snake[j][0] + 1), fill='white')
        for food in self.game.food:
            self.canvas.create_rectangle(self.ratio*(food[1]),self.ratio*(food[0]),
                                         self.ratio*(food[1]+1),self.ratio*(food[0]+1),fill='red')

    def update(self):
        self.canvas.delete("all")

        for i in range(len(self.game.snakes)):
            snake = self.game.snakes[i]
            self.canvas.create_rectangle(self.ratio * (snake[-1][1]), self.ratio * (snake[-1][0]),
                                         self.ratio * (snake[-1][1] + 1), self.ratio * (snake[-1][0] + 1), fill='white')
            for j in range(len(snake) - 1):
                self.canvas.create_rectangle(self.ratio * (snake[j][1]), self.ratio * (snake[j][0]),
                                             self.ratio * (snake[j][1] + 1), self.ratio * (snake[j][0] + 1),
                                             fill='white')
        for food in self.game.food:
            self.canvas.create_rectangle(self.ratio * (food[1]), self.ratio * (food[0]),
                                         self.ratio * (food[1] + 1), self.ratio * (food[0] + 1), fill='red')

        self.canvas.pack()
        self.app.update()


