import pygame
import random as rn 
import os
pygame.init()
pygame.font.init()

WIN_WIDTH = 1000
WIN_HEIGHT = 600
STAT_FONT = pygame.font.SysFont("comicsans", 50)


win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption('SAVE FRECCIA')

FRECCIA_IMG = pygame.image.load(os.path.join("imgs","arr.png"))
BOMB_IMAGE = pygame.image.load(os.path.join("imgs","bomb.png"))
CLOUD_IMAGES = [pygame.image.load(os.path.join("imgs","cloud1.png")),
                pygame.image.load(os.path.join("imgs","cloud2.png")),
                pygame.image.load(os.path.join("imgs","cloud3.png")),
                pygame.image.load(os.path.join("imgs","cloud4.png")),
                pygame.image.load(os.path.join("imgs","cloud5.png")),
                pygame.image.load(os.path.join("imgs","cloud6.png")),
                pygame.image.load(os.path.join("imgs","cloud7.png")),
                ]

for CLOUD in CLOUD_IMAGES:
    pygame.transform.smoothscale(CLOUD, (100,100))

class Freccia:
    def __init__(self):
        self.x = 50
        self.y = 50
        self.width = 90
        self.height = 70
        self.vel = 5
        self.img = pygame.transform.smoothscale(FRECCIA_IMG, (self.width, self.height))

    def move_left(self):
        if self.x <= 0:
            self.x = self.x
        else:
            self.x -= self.vel

    def move_right(self):
        if self.x >= WIN_WIDTH-self.width:
            self.x = self.x
        else:
            self.x += self.vel

    def draw(self, win):
        win.blit(self.img, (self.x, self.y),)

    def get_mask(self):
        return pygame.mask.from_surface(self.img)



class Bomb:

    def __init__(self):
        self.y = WIN_HEIGHT
        self.x = rn.randint(0,WIN_WIDTH)
        self.vel = 2
        self.height = 60
        self.width = 60
        self.img = pygame.transform.smoothscale(BOMB_IMAGE, (self.width, self.height))

    def move(self):
        self.y -= self.vel

    def draw(self, win):
        win.blit(self.img, (self.x, self.y))

    def collide(self, freccia):
        freccia_mask = freccia.get_mask()
        bomb_mask = pygame.mask.from_surface(self.img)

        offset = (self.x - freccia.x, self.y - round(freccia.y))

        overlap = freccia_mask.overlap(bomb_mask, offset)

        if overlap:
            return True
        
        return False


class Cloud:
    def __init__(self):
        self.x = rn.randint(0,WIN_WIDTH)
        self.y = WIN_HEIGHT
        self.vel = 1
        self.k = rn.randint(0,6)
        self.imgs = CLOUD_IMAGES
        self.img = pygame.transform.smoothscale(self.imgs[self.k], (120,100))

    def move(self):
        self.y -= self.vel

    def draw(self, win):
        win.blit(self.img, (self.x, self.y))





def draw_all(win, freccia, bombs, score):
    win.fill((134,197,218))
    freccia.draw(win)

    for cloud in clouds:
        cloud.draw(win)

    for bomb in bombs:
        bomb.draw(win)
    
    text = STAT_FONT.render("Score: " + str(score), 1, (255,255,255))
    win.blit(text, (WIN_WIDTH - 10 - text.get_width(), 10))







freccia = Freccia()
bombs = [Bomb()]
clouds = [Cloud()]
score = 0
dif = 150
run = True
while run:
    pygame.time.delay(10)

    #quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
    
    #movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        freccia.move_left()

    if keys[pygame.K_RIGHT]:
        freccia.move_right()

    #move all bombs
    for bomb in bombs:
        if bomb.collide(freccia):
            run = False
            pygame.quit()
        if bomb.y <= 0:
            score += 10
            flag = False
            bombs.remove(bomb)
        bomb.move()

    for cloud in clouds:
        cloud.move()
    if score%50 == 0 and score != 0 and not flag and dif >= 10:
        if dif == 10:
            dif -= 5
        else:
            dif -= 20
        flag = True
    
    #spawns clouds
    if rn.randint(0,75) == 1:
        clouds.append(Cloud())

    #spawns bombs
    if rn.randint(0,dif) == 1:
        bombs.append(Bomb())


    draw_all(win, freccia, bombs, score)
    pygame.display.update()