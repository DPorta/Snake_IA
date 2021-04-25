import pygame
import math
import random
import sys
import time

windows_size=500

class Node():
    def __init__(self, pariente=None, posicion=None):
        self.parent = pariente
        self.position = posicion

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, otro):
        return self.position == otro.position

def A_Star(mapa, inicio, meta):
    Nodo_inicio = Node(None, inicio)
    Nodo_inicio.g = Nodo_inicio.h = Nodo_inicio.f = 0
    Nodo_fin = Node(None, meta)
    Nodo_fin.g = Nodo_fin.h = Nodo_fin.f = 0
    lista_abierta = []
    lista_cerrada = []
    lista_abierta.append(Nodo_inicio)
    while len(lista_abierta) > 0:
        Nodo_actual = lista_abierta[0]
        index_actual = 0
        for index, item in enumerate(lista_abierta):
            if item.f < Nodo_actual.f:
                Nodo_actual = item
                index_actual = index

        lista_abierta.pop(index_actual)
        lista_cerrada.append(Nodo_actual)

        if Nodo_actual == Nodo_fin:
            path = []
            current = Nodo_actual
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1]

        sucesores = []
        for pos in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]:

            Nodo_posicion = (Nodo_actual.position[0] + pos[0], Nodo_actual.position[1] + pos[1])
            if Nodo_posicion[0] > (len(mapa) - 1) or Nodo_posicion[0] < 0 or Nodo_posicion[1] > \
                    (len(mapa[len(mapa) - 1]) - 1) or Nodo_posicion[1] < 0:
                continue

            if mapa[Nodo_posicion[0]][Nodo_posicion[1]] != 0:
                continue

            nuevo = Node(Nodo_actual, Nodo_posicion)

            sucesores.append(nuevo)

        for sucesor in sucesores:
            for hijo in lista_cerrada:
                if sucesor == hijo:
                    continue

            # f() = g() + h()
            sucesor.g = Nodo_actual.g + 1
            sucesor.h = math.sqrt(((sucesor.position[0] - Nodo_fin.position[0]) ** 2) + (
                    (sucesor.position[1] - Nodo_fin.position[1]) ** 2))
            sucesor.f = sucesor.g + sucesor.h

            for nodo_abierto in lista_abierta:
                if sucesor == nodo_abierto and sucesor.g > nodo_abierto.g:
                    continue

            lista_abierta.append(sucesor)

class Snake():
    def __init__(self, x, y):
        self.position = [x, y]
        self.body = [[x, y], [x - 10, y], [x - 20, y]]
        self.direction = "Derecha"
        self.change_dir = self.direction

    def change_direction(self, direccion):
        if direccion == "Derecha" and not self.direction == "Izquierda":
            self.direction = "Derecha"
        if direccion == "Izquierda" and not self.direction == "Derecha":
            self.direction = "Izquierda"
        if direccion == "Arriba" and not self.direction == "Abajo":
            self.direction = "Arriba"
        if direccion == "Abajo" and not self.direction == "Arriba":
            self.direction = "Abajo"

    def move(self, comida_pos):
        if self.direction == "Derecha":
            self.position[0] += 10
        if self.direction == "Izquierda":
            self.position[0] -= 10
        if self.direction == "Arriba":
            self.position[1] -= 10
        if self.direction == "Abajo":
            self.position[1] += 10
        self.body.insert(0, list(self.position))
        if self.position == comida_pos:
            return 1  # True
        else:
            self.body.pop()
            return 0  # False

    def Colision(self):
        x = self.position[0]
        y = self.position[1]
        #limites del mapa -10 para prevenir colisiones
        if x > windows_size - 10 or x < 0:
            return 1
        elif y > windows_size - 10 or y < 0:
            return 1
        return 0

    def getHeadPos(self):
        return self.position

    def getBody(self):
        return self.body


class food_generator():
    def __init__(self):
        self.position = [random.randrange(1, windows_size // 10) * 10,
                         random.randrange(1, windows_size//10) * 10]
        self.isFoodOnScreen = True

    def comida_spawn(self):
        if self.isFoodOnScreen == False:
            self.position = [random.randrange(1, windows_size // 10) * 10,
                             random.randrange(1, windows_size//10) * 10]
            self.isFoodOnScreen = True
        return self.position

    def setFoodOnScreen(self, b):
        self.isFoodOnScreen = b


class Map:

    mapa = []
    def __init__(self):
        for i in range(windows_size//10):
            self.fil = []
            for j in range(windows_size//10):
                self.fil.append(0)
            self.mapa.append(self.fil)

    def getMap(self):
        return self.mapa

    '''
    score=a*
    score2=human
    '''
    def gameOver(self, score, score2):
        resultado = ""
        if (score == score2):
            resultado = "Empate!"
        if (score > score2):
            resultado = "A* wins"
        if (score < score2):
            resultado = "You win"

        pygame.display.set_caption(resultado)
        Fin = True
        while Fin:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    Fin = False
        pygame.quit()
        sys.exit()

def main():
    # Mapa (Matriz)
    MAPA = Map()
    mapa = MAPA.getMap()

    # Mapa (Pygame)
    window = pygame.display.set_mode((windows_size, windows_size))
    pygame.display.set_caption('A*')
    fps = pygame.time.Clock()

    # Comida
    foodSpawner = food_generator()

    # A*
    snake = Snake(0, 0)
    score = 0
    inicio = (int(snake.getHeadPos()[0] / 10), int(snake.getHeadPos()[1] / 10))
    objetivo = (int(foodSpawner.comida_spawn()[0] / 10), int(foodSpawner.comida_spawn()[1] / 10))

    # Humano
    snake2 = Snake(0, 20)
    score2 = 0

    window.fill(pygame.Color(0,0,0))

    while True:
        camino = A_Star(mapa, inicio, objetivo)
        snake_x = snake.getHeadPos()[0]
        snake_y = snake.getHeadPos()[1]
        # IA
        for (x, y) in camino:
            if x > snake_x:
                snake.change_direction('Derecha')
            if x < snake_x:
                snake.change_direction('Izquierda')
            if y > snake_y:
                snake.change_direction('Abajo')
            if y < snake_y:
                snake.change_direction('Arriba')
            snake_x = x
            snake_y = y
        # Humano
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                mapa.gameOver()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    snake2.change_direction('Derecha')
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    snake2.change_direction('Izquierda')
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    snake2.change_direction('Arriba')
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    snake2.change_direction('Abajo')
                if event.key == pygame.K_q: #opcional
                    score2 +=1

        comida_pos = foodSpawner.comida_spawn()  # Retorna posicion de la comida

        # IA
        if (snake.move(comida_pos) == 1):
            score += 1
            foodSpawner.setFoodOnScreen(False)
        # Humano
        if (snake2.move(comida_pos) == 1):
            score2 += 1
            foodSpawner.setFoodOnScreen(False)

        window.fill(pygame.Color(0, 0, 0))

        for x in range(windows_size//10):
            for y in range(windows_size//10):
                if (mapa[x][y] == 0):
                    pygame.draw.rect(window, pygame.Color(0, 40, 0),
                                     pygame.Rect(x * 10, y * 10, 10, 10), 1)  # x,y,ancho,alto
                if (mapa[x][y] == 1):
                    pygame.draw.rect(window, pygame.Color(0, 0, 0),
                                     pygame.Rect(x * 10, y * 10, 10, 10), 1)  # x,y,ancho,alto
        # IA
        for pos in snake.getBody():
            pygame.draw.rect(window, pygame.Color(0, 200, 100),
                             pygame.Rect(pos[0], pos[1], 10, 10))  # x,y,ancho,alto
        # Humano
        for pos in snake2.getBody():
            pygame.draw.rect(window, pygame.Color(255, 255, 255),
                             pygame.Rect(pos[0], pos[1], 10, 10))  # x,y,ancho,alto

        # Dibujar Comida
        pygame.draw.rect(window, pygame.Color(200, 0, 0),
                         pygame.Rect(comida_pos[0], comida_pos[1], 10, 10))
        # IA
        if (snake.Colision() == 1 ):#AGREGAR or score2==3 para poner fin al juego si el player llega a x puntos
            MAPA.gameOver(score, score2)
        # Humano
        if (snake2.Colision() == 1):
            MAPA.gameOver(score, score2)

        # Puntaje
        pygame.display.set_caption("A Star:" + str(score) + "  Player:" + str(score2))
        pygame.display.flip()
        fps.tick(24)

        # Nodo
        inicio = (int(snake.getHeadPos()[0] / 10), int(snake.getHeadPos()[1] / 10))
        objetivo = (int(comida_pos[0] / 10), int(comida_pos[1] / 10))


if __name__ == '__main__':
    main()

