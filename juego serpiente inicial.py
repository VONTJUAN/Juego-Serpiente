import pygame
import time
import random

# Inicializar Pygame
pygame.init()

# Colores
blanco = (255, 255, 255)
negro = (0, 0, 0)
rojo = (213, 50, 80)
verde = (0, 255, 0)
azul = (50, 153, 213)

# Dimensiones de la pantalla
ancho = 600
alto = 400

pantalla = pygame.display.set_mode((ancho, alto))
pygame.display.set_caption('Snake - Juego en Python')

# Reloj del juego
reloj = pygame.time.Clock()
velocidad_snake = 15

# Tamaño del bloque de la serpiente
tam_bloque = 10

# Fuente
fuente = pygame.font.SysFont("bahnschrift", 25)


def mensaje(msg, color):
    texto = fuente.render(msg, True, color)
    pantalla.blit(texto, [ancho / 6, alto / 3])


def puntuacion(puntos):
    valor = fuente.render("Puntuación: " + str(puntos), True, blanco)
    pantalla.blit(valor, [0, 0])


def nuestro_snake(tam_bloque, lista_snake):
    for x in lista_snake:
        pygame.draw.rect(pantalla, verde, [x[0], x[1], tam_bloque, tam_bloque])


def juego():
    game_over = False
    game_cerrar = False

    x = ancho / 2
    y = alto / 2

    x_cambio = 0
    y_cambio = 0

    lista_snake = []
    largo_snake = 1

    comida_x = round(random.randrange(0, ancho - tam_bloque) / 10.0) * 10.0
    comida_y = round(random.randrange(0, alto - tam_bloque) / 10.0) * 10.0

    while not game_over:

        while game_cerrar:
            pantalla.fill(azul)
            mensaje("Has perdido. C - Continuar / S - Salir", rojo)
            puntuacion(largo_snake - 1)
            pygame.display.update()

            for evento in pygame.event.get():
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_s:
                        game_over = True
                        game_cerrar = False
                    if evento.key == pygame.K_c:
                        juego()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                game_over = True
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_LEFT:
                    x_cambio = -tam_bloque
                    y_cambio = 0
                elif evento.key == pygame.K_RIGHT:
                    x_cambio = tam_bloque
                    y_cambio = 0
                elif evento.key == pygame.K_UP:
                    y_cambio = -tam_bloque
                    x_cambio = 0
                elif evento.key == pygame.K_DOWN:
                    y_cambio = tam_bloque
                    x_cambio = 0

        if x >= ancho or x < 0 or y >= alto or y < 0:
            game_cerrar = True

        x += x_cambio
        y += y_cambio
        pantalla.fill(negro)
        pygame.draw.rect(pantalla, rojo, [comida_x, comida_y, tam_bloque, tam_bloque])

        cabeza = []
        cabeza.append(x)
        cabeza.append(y)
        lista_snake.append(cabeza)

        if len(lista_snake) > largo_snake:
            del lista_snake[0]

        for segmento in lista_snake[:-1]:
            if segmento == cabeza:
                game_cerrar = True

        nuestro_snake(tam_bloque, lista_snake)
        puntuacion(largo_snake - 1)

        pygame.display.update()

        if x == comida_x and y == comida_y:
            comida_x = round(random.randrange(0, ancho - tam_bloque) / 10.0) * 10.0
            comida_y = round(random.randrange(0, alto - tam_bloque) / 10.0) * 10.0
            largo_snake += 1

        reloj.tick(velocidad_snake)

    pygame.quit()
    quit()


juego()