import pygame
import random

# Pygame
pygame.init()

# экран
WIDTH, HEIGHT = 600, 400
CELL_SIZE = 20
GRID_WIDTH = WIDTH // CELL_SIZE
GRID_HEIGHT = HEIGHT // CELL_SIZE

# Цвета
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

# Инициализация экрана
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# Шрифты
font = pygame.font.SysFont("Arial", 20)

# Класс змеи
class Snake:
    def __init__(self):
        self.body = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = (1, 0)  # Двигается вправо
        self.grow = False

    def move(self):
        """Двигает змею в текущем направлении"""
        head_x, head_y = self.body[0]
        dx, dy = self.direction
        new_head = (head_x + dx, head_y + dy)

        if self.grow:
            self.body.insert(0, new_head)
            self.grow = False
        else:
            self.body.insert(0, new_head)
            self.body.pop()

    def check_collision(self):
        """Проверяет столкновение со стенами или с собой"""
        head = self.body[0]
        if head[0] < 0 or head[0] >= GRID_WIDTH or head[1] < 0 or head[1] >= GRID_HEIGHT:
            return True
        if head in self.body[1:]:
            return True
        return False

    def grow_snake(self):
        """Увеличивает размер змеи"""
        self.grow = True

    def draw(self, surface):
        """Рисует змею на экране"""
        for segment in self.body:
            pygame.draw.rect(surface, GREEN, (segment[0] * CELL_SIZE, segment[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

# Класс еды
class Food:
    def __init__(self, snake_body):
        self.position = self.generate_position(snake_body)
        self.value = random.choice([1, 2, 3])  # Вес еды
        self.timer = 5000  # Время жизни еды (в миллисекундах)
        self.spawn_time = pygame.time.get_ticks()

    def generate_position(self, snake_body):
        """Генерирует случайную позицию для еды, избегая тела змеи"""
        while True:
            pos = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
            if pos not in snake_body:
                return pos

    def draw(self, surface):
        """Рисует еду на экране"""
        pygame.draw.rect(surface, RED, (self.position[0] * CELL_SIZE, self.position[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    def is_expired(self):
        """Проверяет, истекло ли время жизни еды"""
        return pygame.time.get_ticks() - self.spawn_time > self.timer

# Основной игровой цикл
snake = Snake()
food = Food(snake.body)
clock = pygame.time.Clock()
speed = 10
score = 0
level = 1

running = True
while running:
    screen.fill(BLACK)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake.direction != (0, 1):
                snake.direction = (0, -1)
            elif event.key == pygame.K_DOWN and snake.direction != (0, -1):
                snake.direction = (0, 1)
            elif event.key == pygame.K_LEFT and snake.direction != (1, 0):
                snake.direction = (-1, 0)
            elif event.key == pygame.K_RIGHT and snake.direction != (-1, 0):
                snake.direction = (1, 0)
    
    snake.move()
    
    # Проверка столкновений
    if snake.check_collision():
        running = False
    
    # Проверка съедания еды
    if snake.body[0] == food.position:
        snake.grow_snake()
        score += food.value  # Добавляем очки в зависимости от веса еды
        food = Food(snake.body)  # Генерируем новую еду
        
        # Увеличение уровня каждые 5 очков
        if score % 5 == 0:
            level += 1
            speed += 2

    # Проверка исчезновения еды
    if food.is_expired():
        food = Food(snake.body)
    
    # Отображение змеи, еды и счёта
    snake.draw(screen)
    food.draw(screen)
    
    score_text = font.render(f"Score: {score}  Level: {level}", True, WHITE)
    screen.blit(score_text, (10, 10))
    
    pygame.display.flip()
    clock.tick(speed)

pygame.quit()
