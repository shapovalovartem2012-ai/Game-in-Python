import json

import pygame

pygame.init()

width = 1920
height = 1040


game_over = 0
score = 0

tile_size = 40

clock = pygame.time.Clock()
fps = 60
with open("levels/level1.json","r") as file:
    world_data = json.load(file)

level = 1
max_level = 7

sound_jump = pygame.mixer.Sound("Music/jump.wav")
sound_coin = pygame.mixer.Sound("Music/coin.wav")
sound_game_over = pygame.mixer.Sound("Music/game_over.wav")
sound_door_opening = pygame.mixer.Sound("Music/31769__slanesh__porte-pierre-2.wav")

def draw_text(text, color, size, x, y):
    font = pygame.font.SysFont("Arial", size)
    img = font.render(text, True, color)
    display.blit(img, (x, y))

class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        img = pygame.image.load("images/key1.png")
        self.image = pygame.transform.scale(img, (tile_size * 1, tile_size * 1))
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)

coin_group = pygame.sprite.Group()

class ExitDoor(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        img = pygame.image.load("images/main_game_door.png")
        self.image = pygame.transform.scale(img, (tile_size, int(tile_size * 1.5)))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

exit_group = pygame.sprite.Group()

class Button:
    def __init__(self,x,y,image):
        self.image = image
        self.rect = self.image.get_rect(center=(x, y))

    def draw(self):
        action = False
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            if pygame.mouse.get_pressed()[0] == 1:
                action = True
        display.blit(self.image,self.rect)
        return action

class Lava(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        img = pygame.image.load("images/Water.png")
        self.image = pygame.transform.scale(img,
                                            (tile_size, tile_size // 2))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

lava_group = pygame.sprite.Group()

class World:
    def __init__(self,data):
        dirt_img = pygame.image.load("images/block_dirt.png")
        grass_img = pygame.image.load("images/block_snowy_grass.png")
        self.tile_list = []
        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == 1 or tile == 2:
                    images = {1:dirt_img,2:grass_img}
                    img = pygame.transform.scale(images[tile],
                                                 (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img,img_rect)
                    self.tile_list.append(tile)
                elif tile == 3:
                    lava = Lava(col_count * tile_size,
                                row_count * tile_size + (tile_size // 2))
                    lava_group.add(lava)
                elif tile == 5:
                    exit_door = ExitDoor(col_count * tile_size,
                                row_count * tile_size - (tile_size // 2))
                    exit_group.add(exit_door)
                elif tile == 6:
                    coin = Coin (col_count * tile_size + (tile_size // 2),
                                 row_count * tile_size + (tile_size // 2))
                    coin_group.add(coin)


                col_count += 1
            row_count += 1

    def draw(self):
        for i in self.tile_list:
            display.blit(i[0],i[1])

world = World(world_data)

def reset_level():
    global world
    Player1.rect.x = 100
    Player1.rect.y = height - 130
    lava_group.empty()
    exit_group.empty()
    with open(f"levels/level{level}.json", "r") as file:
        world_data = json.load(file)
    world = World(world_data)
    return world

class Player:
    def __init__(self):
        self.image_left = []
        self.image_right = []
        self.index = 0
        self.counter = 0
        self.direction = 0
        for num in range(1,5):
            img_right = pygame.image.load(f"images/way{num}.png")
            img_right = pygame.transform.scale(img_right, (60,75))
            img_left = pygame.transform.flip(img_right, True,False)
            self.image_left.append(img_left)
            self.image_right.append(img_right)
        self.image = self.image_right[self.index]

        self.rect = self.image.get_rect()
        self.gravity = 0
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.jumped = False
        self.rect.x = 100
        self.rect.y = height - 480



    def update(self):
        global game_over
        x = 0
        y = 0
        walk_speed = 10
        if game_over == 0:
            key = pygame.key.get_pressed()
            if key[pygame.K_a]:
                x -= 7
                self.direction = -1
                self.counter += 1
            if key[pygame.K_d]:
                x += 7
                self.direction = 1
                self.counter += 1
            if self.counter > walk_speed:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.image_right):
                    self.index = 0
                if self.direction == 1:
                    self.image = self.image_right[self.index]
                else:
                    self.image = self.image_left[self.index]
            if key[pygame.K_SPACE] and self.jumped == False:
                self.gravity = -10
                self.jumped = True
                sound_jump.play()
            self.gravity += 1
            if self.gravity > 10:
               self.gravity = 10
            y += self.gravity
            for tile in world.tile_list:
                if tile[1].colliderect(self.rect.x + x, self.rect.y,
                                       self.width, self.height):
                    x = 0
                if tile[1].colliderect(self.rect.x, self.rect.y + y,
                                       self.width, self.height):
                    if self.gravity < 0:
                        y = tile[1].bottom - self.rect.top
                        self.gravity = 0
                    elif self.gravity >= 0:
                        y = tile[1].top - self.rect.bottom
                        self.gravity = 0
                        self.jumped = False
            if self.rect.bottom > height:
                self.rect.bottom = height
            self.rect.x += x
            self.rect.y += y

            if pygame.sprite.spritecollide(self, lava_group, False):
                game_over = -1

            if pygame.sprite.spritecollide(self, exit_group, False):
                game_over = 1

        elif game_over == -1:
            img_ghost = pygame.image.load("images/Ghost123.png")
            img_ghost = pygame.transform.scale(img_ghost, (225, 183))
            self.image = img_ghost
            self.rect.y -= 10

        display.blit(self.image,self.rect)
img_exit = pygame.image.load("images/exit_btn.png")
img_start = pygame.image.load("images/start_btn 2.png")
img_restart = pygame.image.load("images/buton_restart.png")
Player1 = Player()
Restart = Button(960,620,img_restart)
Start = Button(960,320,img_start)
ExitBtn = Button(960,520,img_exit)

display = pygame.display.set_mode((width,height))
pygame.display.set_caption("...")
fon = pygame.image.load("images/main_background.png")
fon_rect = fon.get_rect()

tilemap = pygame.image.load("images/main tile map5-export.png")

run = True
main_menu = True
life = 3
while run:
    clock.tick(fps)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    display.blit(fon,fon_rect)
    if main_menu:
        if Start.draw():
            main_menu = False
            score = 0
            level = 1
            world = reset_level()
        elif ExitBtn.draw():
            run = False
    else:
        world.draw()
        lava_group.draw(display)
        exit_group.draw(display)
        coin_group.draw(display)
        draw_text(str(score), (225, 255, 255), 30, 10, 10)
        Player1.update()

        if pygame.sprite.spritecollide(Player1, coin_group, True):
            score += 1
            sound_coin.play()
            print(score)
        if game_over == -1:
            if Restart.draw():
                sound_game_over.play()
                life -= 1
                Player1 = Player()
                world = reset_level()
                game_over = 0
                if life == 0:
                    main_menu = True


        if game_over == 1:
            game_over = 0
            if level < max_level:
                sound_door_opening.play()
                level += 1
                world = reset_level()
            else:
                print("win")
                main_menu = True

        lava_group.update()
    pygame.display.update()