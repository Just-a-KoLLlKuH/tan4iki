import pygame
import sys
import random

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
GRAY = (169, 169, 169)

# Шрифт для отображения текста
font = pygame.font.Font(None, 36)

# Определение класса для танка
class Tank(pygame.sprite.Sprite):
    def __init__(self, x, y, color):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(color)
        self.rect = self.image.get_rect(center=(x, y))
        self.start_position = (x, y)  # Стартовая позиция танка
        self.speed = 1  # Скорость передвижения танка
        self.speed_x = 0  # Скорость по горизонтали
        self.speed_y = 0  # Скорость по вертикали
        self.score = 0  # Счетчик убийств танков
        self.direction = 'right'  # Начальное направление танка
        self.last_shot_time = 0  # Время последнего выстрела
        self.shoot_delay = 1000  # Интервал между выстрелами в миллисекундах (1 секунда = 1000 мс)
        self.is_respawning = False  # Флаг респавна
        self.respawn_timer = 0  # Таймер для респавна

    def move(self, dx, dy):
        # Если танк в процессе респавна, не даем ему двигаться
        if self.is_respawning:
            return

        # Сохраняем текущие координаты перед перемещением
        old_rect = self.rect.copy()
        self.rect.x += dx * self.speed
        self.rect.y += dy * self.speed

        # Проверяем столкновения с каждой стеной
        for wall in walls:
            if pygame.sprite.collide_rect(self, wall):
                # Если произошло столкновение, возвращаем танк на предыдущее положение
                self.rect = old_rect
                return

        # Проверяем столкновения с другими танками
        for tank in tanks:
            if tank != self and pygame.sprite.collide_rect(self, tank):
                self.rect = old_rect
                return

        self.rect.clamp_ip(screen.get_rect())  # Ограничение движения танка в пределах экрана
        self.update_direction(dx, dy)

    def update_direction(self, dx, dy):
        if dx > 0:
            self.direction = 'right'
        elif dx < 0:
            self.direction = 'left'
        elif dy > 0:
            self.direction = 'down'
        elif dy < 0:
            self.direction = 'up'

    def can_shoot(self):
        current_time = pygame.time.get_ticks()
        return current_time - self.last_shot_time > self.shoot_delay

    def shoot(self, target_tank, bullet_color):
        if self.can_shoot():
            bullet = Bullet(self.rect.centerx, self.rect.centery, self.direction, target_tank, bullet_color)
            all_sprites.add(bullet)
            self.last_shot_time = pygame.time.get_ticks()

    def respawn(self):
        self.is_respawning = True
        self.rect.center = self.start_position
        self.respawn_timer = pygame.time.get_ticks()  # Запускаем таймер для респавна

    def update(self):
        # Проверяем, если танк в процессе респавна и прошло больше 2 секунд
        if self.is_respawning and pygame.time.get_ticks() - self.respawn_timer > 2000:
            self.is_respawning = False  # Останавливаем респавн

    def draw(self, surface):
        surface.blit(self.image, self.rect)

# Определение класса для пули
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, target_tank, color):
        super().__init__()
        self.image = pygame.Surface((10, 10))
        self.image.fill(color)
        self.rect = self.image.get_rect(center=(x, y))
        self.direction = direction
        self.speed = 5  # Скорость полета снаряда
        self.target_tank = target_tank  # Целевой танк, на который должна попасть пуля

    def update(self):
        if self.direction == "up":
            self.rect.y -= self.speed
        elif self.direction == "down":
            self.rect.y += self.speed
        elif self.direction == "left":
            self.rect.x -= self.speed
        elif self.direction == "right":
            self.rect.x += self.speed

        # Проверяем столкновение пули с целевым танком
        if self.rect.colliderect(self.target_tank.rect):
            self.target_tank.score += 1
            print(f"Score for {self.target_tank}: {self.target_tank.score}")
            self.kill()  # Удаляем пулю из группы после попадания

            # Если танк попал и его score больше 0, запускаем респавн
            if self.target_tank.score > 0:
                self.target_tank.respawn()

        # Проверяем столкновение пули со стенами
        for wall in walls:
            if pygame.sprite.collide_rect(self, wall):
                self.kill()

# Определение класса для стены
class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft=(x, y))

# Создание стен
walls = pygame.sprite.Group()
wall1 = Wall(200, 150, 20, 100, GRAY)
wall2 = Wall(400, 300, 20, 200, GRAY)
wall3 = Wall(600, 100, 20, 150, GRAY)
wall4 = Wall(100, 400, 20, 100, GRAY)
walls.add(wall1, wall2, wall3, wall4)

# Создание объектов для танков
tank1 = Tank(100, SCREEN_HEIGHT // 2, BLACK)
tank2 = Tank(SCREEN_WIDTH - 100, SCREEN_HEIGHT // 2, RED)

# Группа спрайтов для всех объектов (танки, стены)
all_sprites = pygame.sprite.Group()
all_sprites.add(tank1, tank2)
all_sprites.add(walls)

# Список танков для проверки столкновений между ними
tanks = pygame.sprite.Group()
tanks.add(tank1, tank2)

# Основной цикл игры
running = True
while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:  # Стрельба при нажатии на пробел
                tank1.shoot(tank2, BLACK)
            elif event.key == pygame.K_RETURN:  # Стрельба при нажатии на Enter
                tank2.shoot(tank1, RED)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        tank1.move(0, -1)
    elif keys[pygame.K_s]:
        tank1.move(0, 1)
    elif keys[pygame.K_a]:
        tank1.move(-1, 0)
    elif keys[pygame.K_d]:
        tank1.move(1, 0)

    if keys[pygame.K_UP]:
        tank2.move(0, -1)
    elif keys[pygame.K_DOWN]:
        tank2.move(0, 1)
    elif keys[pygame.K_LEFT]:
        tank2.move(-1, 0)
    elif keys[pygame.K_RIGHT]:
        tank2.move(1, 0)

    # Обновление и отрисовка спрайтов
    all_sprites.update()
    all_sprites.draw(screen)

    # Отображение счетчика убийств
    text = font.render(f"Score: {tank2.score} - {tank1.score}", True, BLACK)
    screen.blit(text, (10, 10))

    pygame.display.flip()

# Завершение игры
pygame.quit()
sys.exit()