import pygame
import random
import time

pygame.init()

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
ROJO = (220, 20, 60)
VERDE = (34, 139, 34)
VERDE_CLARO = (144, 238, 144)
AZUL = (50, 153, 213)
GRIS = (100, 100, 100)
AMARILLO = (255, 255, 0)
# Tamaño de la ventana
ANCHO = 600
ALTO = 400

# Bloques
TAM_BLOQUE = 20
FPS = 15

pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("🐍 Snake por niveles")

fuente = pygame.font.SysFont("consolas", 24, bold=True)
reloj = pygame.time.Clock()


def dibujar_puntuacion(puntos, nivel):
    texto = fuente.render(f"Puntos: {puntos}  Nivel: {nivel}", True, BLANCO)
    pantalla.blit(texto, [10, 10])


def dibujar_manzana(pos):
    pygame.draw.circle(pantalla, ROJO, pos, TAM_BLOQUE // 2)
    pygame.draw.circle(pantalla, NEGRO, pos, TAM_BLOQUE // 2, 2)
    pygame.draw.circle(pantalla, VERDE, (pos[0], pos[1] - 10), 4)


def dibujar_serpiente(lista):
    for i, segmento in enumerate(lista):
        if i == len(lista) - 1:
            pygame.draw.rect(pantalla, VERDE, [
                             segmento[0], segmento[1], TAM_BLOQUE, TAM_BLOQUE], border_radius=4)
            ojo_r = 3
            offset = 4
            pygame.draw.circle(
                pantalla, NEGRO, (segmento[0] + offset, segmento[1] + offset), ojo_r)
            pygame.draw.circle(
                pantalla, NEGRO, (segmento[0] + TAM_BLOQUE - offset, segmento[1] + offset), ojo_r)
        else:
            pygame.draw.rect(pantalla, VERDE_CLARO, [
                             segmento[0], segmento[1], TAM_BLOQUE, TAM_BLOQUE], border_radius=2)


def dibujar_obstaculos(lista):
    for ox, oy in lista:
        pygame.draw.rect(pantalla, GRIS, [ox, oy, TAM_BLOQUE, TAM_BLOQUE])
        pygame.draw.rect(pantalla, NEGRO, [ox, oy, TAM_BLOQUE, TAM_BLOQUE], 2)


def mostrar_mensaje(texto, color, pausa=0):
    mensaje = fuente.render(texto, True, color)
    pantalla.blit(mensaje, [ANCHO // 3.5, ALTO // 2])
    pygame.display.update()
    if pausa > 0:
        time.sleep(pausa)


def generar_obstaculos(cantidad, serpiente, comida):
    obstaculos = []
    while len(obstaculos) < cantidad:
        ox = random.randrange(0, ANCHO - TAM_BLOQUE, TAM_BLOQUE)
        oy = random.randrange(0, ALTO - TAM_BLOQUE, TAM_BLOQUE)
        if [ox, oy] not in serpiente and (ox, oy) != comida:
            obstaculos.append((ox, oy))
    return obstaculos


def juego():
    x = ANCHO // 2
    y = ALTO // 2
    x_cambio = 0
    y_cambio = 0

    serpiente = []
    longitud = 3

    comida_x = random.randrange(0, ANCHO - TAM_BLOQUE, TAM_BLOQUE)
    comida_y = random.randrange(0, ALTO - TAM_BLOQUE, TAM_BLOQUE)

    direccion = ''
    corriendo = True
    muerto = False
    nivel = 1
    puntos = 0
    obstaculos = generar_obstaculos(nivel + 2, serpiente, (comida_x, comida_y))

    mostrar_mensaje(f"Nivel {nivel}", AMARILLO, pausa=2)

    while corriendo:
        while muerto:
            pantalla.fill(NEGRO)
            mostrar_mensaje("¡Has perdido! C - continuar / S - salir", ROJO)
            pygame.display.update()

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    corriendo = False
                    muerto = False
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_c:
                        muerto = False
                        x = ANCHO // 2
                        y = ALTO // 2
                        x_cambio = 0
                        y_cambio = 0
                        serpiente = []
                        longitud = 3
                        direccion = ''
                        puntos = 0
                        nivel = 1
                        comida_x = random.randrange(
                            0, ANCHO - TAM_BLOQUE, TAM_BLOQUE)
                        comida_y = random.randrange(
                            0, ALTO - TAM_BLOQUE, TAM_BLOQUE)
                        obstaculos = generar_obstaculos(
                            nivel + 2, serpiente, (comida_x, comida_y))
                        mostrar_mensaje(f"Nivel {nivel}", AMARILLO, pausa=2)

                    elif evento.key == pygame.K_s:
                        corriendo = False
                        muerto = False

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriendo = False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_LEFT and direccion != 'DERECHA':
                    x_cambio = -TAM_BLOQUE
                    y_cambio = 0
                    direccion = 'IZQUIERDA'
                elif evento.key == pygame.K_RIGHT and direccion != 'IZQUIERDA':
                    x_cambio = TAM_BLOQUE
                    y_cambio = 0
                    direccion = 'DERECHA'
                elif evento.key == pygame.K_UP and direccion != 'ABAJO':
                    y_cambio = -TAM_BLOQUE
                    x_cambio = 0
                    direccion = 'ARRIBA'
                elif evento.key == pygame.K_DOWN and direccion != 'ARRIBA':
                    y_cambio = TAM_BLOQUE
                    x_cambio = 0
                    direccion = 'ABAJO'

        x += x_cambio
        y += y_cambio

        if x < 0 or x >= ANCHO or y < 0 or y >= ALTO:
            muerto = True

        pantalla.fill(AZUL)
        pygame.draw.rect(pantalla, BLANCO, (0, 0, ANCHO, ALTO), 4)

        dibujar_obstaculos(obstaculos)
        dibujar_manzana((comida_x + TAM_BLOQUE // 2,
                        comida_y + TAM_BLOQUE // 2))

        cabeza = [x, y]
        serpiente.append(cabeza)
        if len(serpiente) > longitud:
            del serpiente[0]

        if len(serpiente) > 1 and direccion != '':
            for bloque in serpiente[:-1]:
                if bloque == cabeza:
                    muerto = True

        for ox, oy in obstaculos:
            if x == ox and y == oy:
                muerto = True

        dibujar_serpiente(serpiente)
        dibujar_puntuacion(puntos, nivel)

        pygame.display.update()

        if x == comida_x and y == comida_y:
            comida_x = random.randrange(0, ANCHO - TAM_BLOQUE, TAM_BLOQUE)
            comida_y = random.randrange(0, ALTO - TAM_BLOQUE, TAM_BLOQUE)
            longitud += 1
            puntos += 1

            if puntos % 5 == 0:
                nivel += 1
                mostrar_mensaje(f"Nivel {nivel}", AMARILLO, pausa=2)
                nuevos_obs = generar_obstaculos(
                    nivel + 2, serpiente, (comida_x, comida_y))
                obstaculos.extend(nuevos_obs)

        reloj.tick(FPS)

    pygame.quit()


juego()
