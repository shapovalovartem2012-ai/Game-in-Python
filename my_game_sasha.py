import pygame
import random

# Инициализация Pygame
pygame.init()

# Размеры окна
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Платформер")

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# Игровые объекты
player_width, player_height = 50, 50
player_x, player_y = WIDTH // 2, HEIGHT - player_height - 10
player_speed = 5

enemy_width, enemy_height = 50, 50
enemy_speed = 3

coin_width, coin_height = 30, 30

# Игровые переменные
score = 0
game_over = False
paused = False

# Шрифты
font = pygame.font.SysFont('Arial', 30)

# Игрок
player = pygame.Rect(WIDTH // 2, HEIGHT - player_height - 10, player_width, player_height)

# Враги и монеты
enemies = []
coins = []


# Основной цикл игры
def game_loop():
    global game_over, score, paused
    clock = pygame.time.Clock()

    # Основной игровой цикл
    while not game_over:
        screen.fill(WHITE)

        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True


            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused = not paused  # Переключение паузы

        # Пауза
        if paused:
            pause_text = font.render("Пауза (нажми ESC для продолжения)", True, BLACK)
            screen.blit(pause_text, (WIDTH // 2 - 220, HEIGHT // 2))
            pygame.display.flip()
            clock.tick(60)
            continue

        # Управление игроком
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x > 0:
            player.x -= player_speed
        if keys[pygame.K_RIGHT] and player.x < WIDTH - player.width:
            player.x += player_speed

        # Отображение игрока
        pygame.draw.rect(screen, BLACK, player)

        # Создание врагов
        if random.random() < 0.01:
            enemy_x = random.randint(0, WIDTH - enemy_width)
            enemy = pygame.Rect(enemy_x, -enemy_height, enemy_width, enemy_height)
            enemies.append(enemy)

        # Создание монет
        if random.random() < 0.02:
            coin_x = random.randint(0, WIDTH - coin_width)
            coin = pygame.Rect(coin_x, -coin_height, coin_width, coin_height)
            coins.append(coin)

        # Обновление врагов
        for enemy in enemies[:]:
            enemy.y += enemy_speed
            if enemy.y > HEIGHT:
                enemies.remove(enemy)
            if player.colliderect(enemy):
                game_over = True

        # Обновление монет
        for coin in coins[:]:
            coin.y += 4
            if coin.y > HEIGHT:
                coins.remove(coin)
            if player.colliderect(coin):
                coins.remove(coin)
                score += 10

        # Отображение врагов и монет
        for enemy in enemies:
            pygame.draw.rect(screen, RED, enemy)
        for coin in coins:
            pygame.draw.rect(screen, YELLOW, coin)

        # Отображение счёта
        score_text = font.render(f"Очки: {score}", True, BLACK)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(60)

    # Отображение конца игры
    game_over_text = font.render("Игра окончена!", True, RED)
    screen.blit(game_over_text, (WIDTH // 2 - 100, HEIGHT // 2))
    pygame.display.flip()
    pygame.time.wait(3000)


# Запуск игры
if __name__ == "__main__":
    game_loop()

pygame.quit()