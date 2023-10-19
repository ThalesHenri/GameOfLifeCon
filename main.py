import pygame
import random

#CONSTANTES
GREY = (99, 98, 99)
PURPLE = (255, 25, 232)
BLACK = (0,0,0)


#vars
width = 800
height = 800
tile_size = 20
tabuleiro_width = width // tile_size
tabuleiro_height = height // tile_size
fps = 60

SCREEN = pygame.display.set_mode((width,height))
pygame.display.set_caption("Conway's Game of Life")
clock = pygame.time.Clock()

def desenhando_tabuleiro(posicoes):
    for posicao in posicoes: #desenhando os objetos na tela.
        col, linha = posicao
        top_left = (col*tile_size,linha*tile_size)
        pygame.draw.rect(SCREEN,PURPLE,(*top_left,tile_size,tile_size))
    for linha in range(tabuleiro_height): #desenhando o tabuleiro
        pygame.draw.line(SCREEN,BLACK,(0,linha*tile_size),(width,linha*tile_size))
    for col in range(tabuleiro_height):
        pygame.draw.line(SCREEN,BLACK,(col*tile_size,0),(col*tile_size,height))
    
def ajustar_tabuleiro(posicoes):
    todos_vizinhos = set()
    novas_posicoes = set()
    for posicao in posicoes:
        vizinhos = achar_visinhos(posicao)
        todos_vizinhos.update(vizinhos)

        vizinhos = list(filter(lambda x: x in posicoes, vizinhos))

        if len(vizinhos) in [2,3]:
            novas_posicoes.add(posicao)

    for posicao in todos_vizinhos:
        vizinhos = achar_visinhos(posicao)
        vizinhos = list(filter(lambda x: x in posicoes, vizinhos))

        if len(vizinhos) == 3:
            novas_posicoes.add(posicao)

    return novas_posicoes

def achar_visinhos(pos):
    x,y = pos
    vizinhos = []
    for dx in [-1,0,1]:
        if x + dx < 0 or x + dx > tabuleiro_width:
            continue
        for dy in [-1,0,1]:
            if y + dy < 0 or y + dy > tabuleiro_height:
                continue
            if dx == 0 and dy == 0:
                continue

            vizinhos.append((x + dx, y + dy))
    
    return vizinhos


def gen(num):
    return set([(random.randrange(0,tabuleiro_height),random.randrange(0,tabuleiro_width)) for _ in range(num)])

def main_loop():
    run = True 
    playing = False
    posicoes = set()
    count = 0
    update_freq = 120

    while run:
        clock.tick(fps)
        
        if playing:
            count += 1
        
        if count >= update_freq:
            count = 0
            posicoes = ajustar_tabuleiro(posicoes)

        pygame.display.set_caption("Playing" if playing else "Paused")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                x,y = pygame.mouse.get_pos()
                col = x//tile_size
                linha = y//tile_size
                pos = (col,linha)

                if pos in posicoes:
                    posicoes.remove(pos)
                else:
                    posicoes.add(pos)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    playing = not playing
                elif event.key == pygame.K_c: #limpar a tela 
                    posicoes = set()
                    playing = False
                elif event.key == pygame.K_g: #gerar posições aleatórias no tabuleiro
                    posicoes = gen(random.randrange(2,5) * tabuleiro_width)
        SCREEN.fill(GREY)
        desenhando_tabuleiro(posicoes)
        pygame.display.update()
    
    pygame.quit()            


if __name__ == "__main__":
    main_loop()