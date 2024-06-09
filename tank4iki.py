import pygame
import sys

# Инициализация Pygame
pygame.init()

# Определение размера экрана
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Танки")

# Определение цветов
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Определение класса для танка
class Tank(pygame.sprite.Sprite):
    def __init__(self, x, y, color):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(color)
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 2  # Скорость передвижения танка
        self.speed_x = 0  # Скорость по горизонтали
        self.speed_y = 0  # Скорость по вертикали
        self.score = 0  # Счетчик убийств танков

    def move(self, dx, dy):
        self.rect.x += dx * self.speed
        self.rect.y += dy * self.speed
        self.rect.clamp_ip(screen.get_rect())  # Ограничение движения танка в пределах экрана

    def draw(self, surface):
        surface.blit(self.image, self.rect)

# Определение класса для пули
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, color):
        super().__init__()
        self.image = pygame.Surface((10, 10))
        self.image.fill(color)
        self.rect = self.image.get_rect(center=(x, y))
        self.direction = direction
        self.speed = 5  # Скорость полета снаряда

    def update(self):
        if self.direction == "up":
            self.rect.y -= self.speed
        elif self.direction == "down":
            self.rect.y += self.speed
        elif self.direction == "left":
            self.rect.x -= self.speed
        elif self.direction == "right":
            self.rect.x += self.speed

# Создание объектов для танков
tank1 = Tank(100, SCREEN_HEIGHT // 2, BLACK)
tank2 = Tank(SCREEN_WIDTH - 100, SCREEN_HEIGHT // 2, RED)

# Группа спрайтов для танков
all_sprites = pygame.sprite.Group()
all_sprites.add(tank1)
all_sprites.add(tank2)

# Группа спрайтов для пуль
bullets = pygame.sprite.Group()

# Основной цикл игры
running = True
while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:  # Стрельба при нажатии на пробел
                if tank1.speed_x != 0:
                    bullet = Bullet(tank1.rect.centerx, tank1.rect.centery, "right", BLACK)
                elif tank1.speed_y != 0:
                    bullet = Bullet(tank1.rect.centerx, tank1.rect.centery, "down", BLACK)
                bullets.add(bullet)
            elif event.key == pygame.K_RETURN:  # Стрельба при нажатии на Enter
                if tank2.speed_x != 0:
                    bullet = Bullet(tank2.rect.centerx, tank2.rect.centery, "right", RED)
                elif tank2.speed_y != 0:
                    bullet = Bullet(tank2.rect.centerx, tank2.rect.centery, "down", RED)
                bullets.add(bullet)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        tank1.move(0, -1)
        tank1.speed_x, tank1.speed_y = 0, -1
    elif keys[pygame.K_s]:
        tank1.move(0, 1)
        tank1.speed_x, tank1.speed_y = 0, 1
    elif keys[pygame.K_a]:
        tank1.move(-1, 0)
        tank1.speed_x, tank1.speed_y = -1, 0
    elif keys[pygame.K_d]:
        tank1.move(1, 0)
        tank1.speed_x, tank1.speed_y = 1, 0

    if keys[pygame.K_UP]:
        tank2.move(0, -1)
        tank2.speed_x, tank2.speed_y = 0, -1
    elif keys[pygame.K_DOWN]:
        tank2.move(0, 1)
        tank2.speed_x, tank2.speed_y = 0, 1
    elif keys[pygame.K_LEFT]:
        tank2.move(-1, 0)
        tank2.speed_x, tank2.speed_y = -1, 0
    elif keys[pygame.K_RIGHT]:
        tank2.move(1, 0)
        tank2.speed_x, tank2.speed_y = 1, 0

    all_sprites.draw(screen)
    bullets.update()
    bullets.draw(screen)

    pygame.display.flip()

# Завершение игры
pygame.quit()
sys.exit()