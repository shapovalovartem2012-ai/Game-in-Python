import pygame
from pygame.examples.cursors import image

pygame.init()

width = 1920
height = 1020

clock = pygame.time.Clock()
fps = 60
class Hero:


    def __init__(self):
        self.image = pygame.image.load("images/way1.png")
        self.rect = self.image.get_rect()
        self.direction = 0


    def update(self):
        if self.rect.x == 1820:
            self.direction = 1
        if self.rect.x == 0:
            self.direction = 0
        if self.direction == 0:
            self.rect.x += 10
        else:
                self.rect.x -= 10

        display.blit(self.image, self.rect)



Player1 = Hero()

display = pygame.display.set_mode((width,height))
pygame.display.set_caption("...")
fon1 = pygame.image.load("images/1.gif")
fon2 = pygame.image.load("images/2.gif")
fon3 = pygame.image.load("images/3.gif")
fon4 = pygame.image.load("images/4.gif")
tilemap = pygame.image.load("images/main tile map5-export.png")



run = True
while run:
    clock.tick(fps)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    display.blit(fon4, (0, 0))
    display.blit(fon3, (0, 0))
    display.blit(fon2, (0, 0))
    display.blit(fon1, (0, 0))
    display.blit(tilemap, (0, 0))
    Player1.update()
    pygame.display.update()
pygame.quit()



