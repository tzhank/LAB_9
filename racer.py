# Импорт библиотек
import pygame, sys
from pygame.locals import *
import random, time

# Инициализация pygame
pygame.init()

# FPS (кадры в секунду)
FPS = 60
FramePerSec = pygame.time.Clock()

# Цвета
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Размер экрана и игровые переменные
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SPEED = 5  # Скорость врага
SCORE = 0  # Счёт
COINS_COLLECTED = 0  # Количество собранных монет
COIN_SPEED_INCREASE = 5  # Увеличение скорости после сбора N монет

# Шрифты и текст
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, BLACK)

# Загрузка фонового изображения
background = pygame.image.load("AnimatedStreet.png")

# Создание окна игры
DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Racer Game")

# Класс врага (машины)
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Enemy.png")
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

    def move(self):
        """Перемещение врага вниз. Если он выходит за экран, перезапуск позиции."""
        global SCORE
        self.rect.move_ip(0, SPEED)
        if self.rect.top > SCREEN_HEIGHT:
            SCORE += 1
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

# Класс игрока (машины)
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Player.png")
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)

    def move(self):
        """Перемещение игрока влево и вправо в пределах экрана."""
        pressed_keys = pygame.key.get_pressed()
        if self.rect.left > 0 and pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if self.rect.right < SCREEN_WIDTH and pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)

# Класс монет с разными значениями
class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Coin.png")
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), random.randint(40, SCREEN_HEIGHT - 200))
        self.value = random.choice([1, 2, 5])  # Случайное значение монеты

    def move(self):
        """Перемещение монеты вниз. Если выходит за экран - сброс позиции."""
        self.rect.move_ip(0, SPEED // 2)
        if self.rect.top > SCREEN_HEIGHT:
            self.reset()

    def reset(self):
        """Сброс позиции монеты и случайное назначение нового значения."""
        self.rect.top = 0
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), random.randint(40, SCREEN_HEIGHT - 200))
        self.value = random.choice([1, 2, 5])

# Создание спрайтов
P1 = Player()
E1 = Enemy()
C1 = Coin()

# Группы спрайтов
enemies = pygame.sprite.Group()
enemies.add(E1)
coins = pygame.sprite.Group()
coins.add(C1)
all_sprites = pygame.sprite.Group()
all_sprites.add(P1, E1, C1)

# Событие увеличения скорости
INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)

# Игровой цикл
while True:
    # Обработка событий
    for event in pygame.event.get():
        if event.type == INC_SPEED:
            SPEED += 0.5
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # Отрисовка фона и счёта
    DISPLAYSURF.blit(background, (0, 0))
    scores = font_small.render(str(SCORE), True, BLACK)
    DISPLAYSURF.blit(scores, (10, 10))
    coins_text = font_small.render(f"Coins: {COINS_COLLECTED}", True, BLACK)
    DISPLAYSURF.blit(coins_text, (SCREEN_WIDTH - 100, 10))

    # Движение и отрисовка всех спрайтов
    for entity in all_sprites:
        DISPLAYSURF.blit(entity.image, entity.rect)
        entity.move()

    # Проверка столкновения с врагом
    if pygame.sprite.spritecollideany(P1, enemies):
        pygame.mixer.Sound('crash.wav').play()
        time.sleep(0.5)
        DISPLAYSURF.fill(RED)
        DISPLAYSURF.blit(game_over, (30, 250))
        pygame.display.update()
        time.sleep(2)
        pygame.quit()
        sys.exit()

    # Проверка столкновения с монетой
    collided_coin = pygame.sprite.spritecollideany(P1, coins)
    if collided_coin:
        COINS_COLLECTED += collided_coin.value  # Увеличиваем количество монет на значение монеты
        collided_coin.reset()  # Сбрасываем позицию монеты

        # Увеличение скорости врага после сбора определенного количества монет
        if COINS_COLLECTED % COIN_SPEED_INCREASE == 0:
            SPEED += 1

    # Обновление экрана
    pygame.display.update()
    FramePerSec.tick(FPS)
