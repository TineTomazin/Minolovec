import pygame
from random import randrange
pygame.init()
clock = pygame.time.Clock()
WIDTH, HEIGHT = 900, 900
screen = pygame.display.set_mode((WIDTH+2, HEIGHT+2))
pygame.display.set_caption('Minesweeper')

VRSTIC, STOLPCEV = 30, 30
STBOMB = (VRSTIC * STOLPCEV) // 10
VELIKOST_MREZE = WIDTH // STOLPCEV

slika_bombe = pygame.image.load("bomba.png").convert_alpha()
slika_bombe = pygame.transform.scale(slika_bombe, (VELIKOST_MREZE, VELIKOST_MREZE))

slika_zastave = pygame.image.load("bomb_flag.png").convert_alpha()
slika_zastave = pygame.transform.scale(slika_zastave, (VELIKOST_MREZE, VELIKOST_MREZE))

font = pygame.font.SysFont('Arial', 20)
font_GO = pygame.font.SysFont('Arial', 70)

mines = [[0 for _ in range(STOLPCEV)] for _ in range(VRSTIC)]
odkritost = [[0 for _ in range(STOLPCEV)] for _ in range(VRSTIC)]

game_on = True

while STBOMB > 0:
    v = randrange(0, VRSTIC)
    s = randrange(0, STOLPCEV)

    if mines[v][s] != 9:
        mines[v][s] = 9
        STBOMB -= 1

for i in range(VRSTIC):
    for j in range(STOLPCEV):
        if mines[i][j] != 9:
            bomb_okrog = 0
            for ii in range(i-1, i+2):
                for jj in range(j-1, j+2):
                    if ii >= 0 and jj >= 0 and ii < VRSTIC and jj < STOLPCEV and mines[ii][jj] == 9:
                        bomb_okrog += 1
            
            mines[i][j] = bomb_okrog

def odkrijVsaPolja():
    for i in range(VRSTIC):
        for j in range(STOLPCEV):
            odkritost[i][j] = 1

def narisiMrezo():
    # narisi horizonalne crte
    for i in range(HEIGHT//VRSTIC+1):
        pygame.draw.line(screen, "black", (0,i*VELIKOST_MREZE), (900, i*VELIKOST_MREZE), 2)

    # narisi vertikalne crte
    for i in range(WIDTH//STOLPCEV+1):
        pygame.draw.line(screen, "black", (i*VELIKOST_MREZE, 0), (i*VELIKOST_MREZE,900), 2)

def narisiCelice():
    for i in range(len(mines)):
        for j in range(len(mines[i])):
            if odkritost[i][j] == 1:
                if mines[i][j] >= 0 and mines[i][j] < 9:
                    text = font.render(str(mines[i][j]), True, 'red')
                    screen.blit(text, (i*VELIKOST_MREZE+10, j*VELIKOST_MREZE+4))
                elif mines[i][j] == 9:
                    screen.blit(slika_bombe, (i*VELIKOST_MREZE+2, j*VELIKOST_MREZE+2))
            elif odkritost[i][j] == 2:
                screen.blit(slika_zastave, (i*VELIKOST_MREZE+2, j*VELIKOST_MREZE+2))

def narisiIgro():
    narisiMrezo()
    narisiCelice()
    if not game_on:
        text = font_GO.render("GAME OVER", True, 'red')
        screen.blit(text, (300, 400))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        
        if event.type == pygame.MOUSEBUTTONUP:
            if game_on:
                x, y = event.pos
                x, y = x//VELIKOST_MREZE, y//VELIKOST_MREZE
                if event.button == 1:
                    odkritost[x][y] = 1
                    if mines[x][y] == 9:
                        game_on = False
                        odkrijVsaPolja()
                elif event.button == 3:
                    if odkritost[x][y] == 2:
                        odkritost[x][y] = 0
                    else:
                        odkritost[x][y] = 2

    screen.fill('silver')

    narisiIgro()

    pygame.display.update()
    clock.tick(60)