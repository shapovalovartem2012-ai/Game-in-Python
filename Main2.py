import json
import pygame

pygame.init()

# Размеры окна игры
width = 1920
height = 1040

# Переменные состояния игры
game_over = 0
tile_size = 40  # Размер тайла

# Настройка FPS
clock = pygame.time.Clock()
fps = 60

# Загрузка данных первого уровня
with open("levels/level1.json", "r") as file:
    world_data = json.load(file)

# Информация об уровнях
level = 1  # Текущий уровень
max_level = 7  # Максимальное количество уровней


# Класс для выхода (двери)
class ExitDoor(pygame.sprite.Sprite):  # Переименовано с Exit на ExitDoor
    def __init__(self, x, y):
        super().__init__()
        img = pygame.image.load("images/main_game_door.png")
        self.image = pygame.transform.scale(img, (tile_size, int(tile_size * 1.5)))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


# Группа спрайтов для выходов
exit_group = pygame.sprite.Group()


# Класс для кнопок в меню
class Button:
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect(center=(x, y))

    def draw(self):
        action = False
        # Проверка нажатия на кнопку
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            if pygame.mouse.get_pressed()[0] == 1:
                action = True
        display.blit(self.image, self.rect)
        return action


# Класс для лавы/воды (опасности)
class Lava(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        img = pygame.image.load("images/Water.png")
        self.image = pygame.transform.scale(img,
                                            (tile_size, tile_size // 2))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


# Группа спрайтов для лавы
lava_group = pygame.sprite.Group()


# Класс для создания игрового мира
class World:
    def __init__(self, data):
        dirt_img = pygame.image.load("images/block_dirt.png")
        grass_img = pygame.image.load("images/block_snowy_grass.png")
        self.tile_list = []
        row_count = 0
        # Создание тайлов на основе данных уровня
        for row in data:
            col_count = 0
            for tile in row:
                if tile == 1 or tile == 2:
                    images = {1: dirt_img, 2: grass_img}
                    img = pygame.transform.scale(images[tile],
                                                 (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                elif tile == 3:
                    # Создание лавы
                    lava = Lava(col_count * tile_size,
                                row_count * tile_size + (tile_size // 2))
                    lava_group.add(lava)
                elif tile == 5:
                    # Создание выхода
                    exit_door = ExitDoor(col_count * tile_size,  # Используем переименованный класс
                                         row_count * tile_size - (tile_size // 2))
                    exit_group.add(exit_door)
                col_count += 1
            row_count += 1

    def draw(self):
        # Отрисовка всех тайлов мира
        for i in self.tile_list:
            display.blit(i[0], i[1])


# Создание начального мира
world = World(world_data)


# Функция сброса уровня
def reset_level():
    global world
    # Сброс позиции игрока
    Player1.rect.x = 100
    Player1.rect.y = height - 130
    # Очистка групп спрайтов
    lava_group.empty()
    exit_group.empty()
    # Загрузка данных текущего уровня
    with open(f"levels/level{level}.json", "r") as file:
        world_data = json.load(file)
    # Создание нового мира
    world = World(world_data)
    return world


# Класс игрока
class Player:
    def __init__(self):
        # Загрузка и настройка анимаций
        self.image_left = []
        self.image_right = []
        self.index = 0
        self.counter = 0
        self.direction = 0
        for num in range(1, 5):
            img_right = pygame.image.load(f"images/way{num}.png")
            img_right = pygame.transform.scale(img_right, (81, 109))
            img_left = pygame.transform.flip(img_right, True, False)
            self.image_left.append(img_left)
            self.image_right.append(img_right)
        self.image = self.image_right[self.index]

        # Настройка физики и позиции
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
            # Обработка нажатий клавиш
            key = pygame.key.get_pressed()
            # Движение влево
            if key[pygame.K_a]:
                x -= 7
                self.direction = -1
                self.counter += 1
            # Движение вправо
            if key[pygame.K_d]:
                x += 7
                self.direction = 1
                self.counter += 1

            # Обновление анимации ходьбы
            if self.counter > walk_speed:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.image_right):
                    self.index = 0
                if self.direction == 1:
                    self.image = self.image_right[self.index]
                else:
                    self.image = self.image_left[self.index]

            # Прыжок
            if key[pygame.K_SPACE] and self.jumped == False:
                self.gravity = -10
                self.jumped = True

            # Гравитация
            self.gravity += 1
            if self.gravity > 10:
                self.gravity = 10
            y += self.gravity

            # Проверка коллизий с тайлами
            for tile in world.tile_list:
                # Коллизия по горизонтали
                if tile[1].colliderect(self.rect.x + x, self.rect.y,
                                       self.width, self.height):
                    x = 0
                # Коллизия по вертикали
                if tile[1].colliderect(self.rect.x, self.rect.y + y,
                                       self.width, self.height):
                    if self.gravity < 0:
                        y = tile[1].bottom - self.rect.top
                        self.gravity = 0
                    elif self.gravity >= 0:
                        y = tile[1].top - self.rect.bottom
                        self.gravity = 0
                        self.jumped = False

            # Ограничение на выход за границы экрана снизу
            if self.rect.bottom > height:
                self.rect.bottom = height

            # Обновление позиции
            self.rect.x += x
            self.rect.y += y

            # Проверка столкновения с лавой (проигрыш)
            if pygame.sprite.spritecollide(self, lava_group, False):
                game_over = -1

            # Проверка столкновения с выходом (победа на уровне)
            if pygame.sprite.spritecollide(self, exit_group, False):
                game_over = 1

        # Анимация смерти
        elif game_over == -1:
            img_ghost = pygame.image.load("images/Ghost123.png")
            img_ghost = pygame.transform.scale(img_ghost, (225, 183))
            self.image = img_ghost
            self.rect.y -= 10

        # Отрисовка игрока
        display.blit(self.image, self.rect)


# Загрузка изображений для кнопок
img_exit = pygame.image.load("images/exit_btn.png")
img_start = pygame.image.load("images/start_btn 2.png")
img_restart = pygame.image.load("images/buton_restart.png")

# Создание игрока и кнопок
Player1 = Player()
Restart = Button(960, 620, img_restart)
Start = Button(960, 320, img_start)
ExitBtn = Button(960, 520, img_exit)  # Переименовано с Exit на ExitBtn

# Создание окна игры
display = pygame.display.set_mode((width, height))
pygame.display.set_caption("...")

# Загрузка фона
fon = pygame.image.load("images/main_background.png")
fon_rect = fon.get_rect()

# Загрузка тайлмапы
tilemap = pygame.image.load("images/main tile map5-export.png")

# Основные флаги игры
run = True
main_menu = True

# Главный игровой цикл
while run:
    # Ограничение FPS
    clock.tick(fps)

    # Обработка событий в начале цикла
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # Отрисовка фона
    display.blit(fon, fon_rect)

    if main_menu:
        # Обработка главного меню
        if Start.draw():
            main_menu = False
            level = 1
            world = reset_level()
        elif ExitBtn.draw():  # Используем переименованную кнопку
            run = False
    else:
        # Отрисовка игрового мира
        world.draw()  # Используем глобальный объект мира
        lava_group.draw(display)
        exit_group.draw(display)
        Player1.update()

        # Обработка проигрыша
        if game_over == -1:
            if Restart.draw():
                Player1 = Player()
                world = reset_level()
                game_over = 0

        # Обработка перехода на следующий уровень
        if game_over == 1:
            game_over = 0
            if level < max_level:
                level += 1
                world = reset_level()
            else:
                print("win")
                main_menu = True

    # Обновление экрана
    pygame.display.update()

# Завершение работы Pygame
pygame.quit()