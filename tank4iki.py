import pygame
import sys
import random

pygame.init()

clock = pygame.time.Clock()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Перестрелка")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GRAY = (169, 169, 169)

font = pygame.font.Font(None, 36)

class Tank(pygame.sprite.Sprite):
    def __init__(self, x, y, color):
        super().__init__()
        self.original_image = pygame.Surface((50, 30))  # Оригинальная поверхность танка
        self.original_image.fill(color)  # Заполнение цветом
        self.image = self.original_image  # Текущее изображение танка
        self.rect = self.image.get_rect(center=(x, y))
        self.start_position = (x, y)
        self.speed = 1
        self.speed_x = 0
        self.speed_y = 0
        self.score = 0
        self.direction = 'right'
        self.last_shot_time = 0
        self.shoot_delay = 1000
        self.is_respawning = False
        self.respawn_timer = 0
        self.invulnerable_time = 3000  # Время неуязвимости при респауне (в миллисекундах)
        self.invulnerable_end_time = 0

    def move(self, dx, dy):
        if self.is_respawning:
            return

        old_rect = self.rect.copy()
        self.rect.x += dx * self.speed
        self.rect.y += dy * self.speed

        for wall in walls:
            if pygame.sprite.collide_rect(self, wall):
                self.rect = old_rect
                return

        for tank in tanks:
            if tank != self and pygame.sprite.collide_rect(self, tank):
                self.rect = old_rect
                return

        self.rect.clamp_ip(screen.get_rect())
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

        self.rotate()

    def rotate(self):
        if self.direction == 'right':
            angle = 0
        elif self.direction == 'left':
            angle = 180
        elif self.direction == 'down':
            angle = 90
        elif self.direction == 'up':
            angle = 270

        old_center = self.rect.center
        self.image = pygame.transform.rotate(self.original_image, angle)
        self.rect = self.image.get_rect()
        self.rect.center = old_center

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
        self.respawn_timer = pygame.time.get_ticks()
        self.invulnerable_end_time = pygame.time.get_ticks() + self.invulnerable_time  # Установка времени окончания неуязвимости

    def update(self):
        if self.is_respawning:
            current_time = pygame.time.get_ticks()
            if current_time >= self.invulnerable_end_time:
                self.is_respawning = False

    def draw(self, surface):
        surface.blit(self.image, self.rect)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, target_tank, color):
        super().__init__()
        self.image = pygame.Surface((10, 10))
        self.image.fill(color)
        self.rect = self.image.get_rect(center=(x, y))
        self.direction = direction
        self.speed = 5
        self.target_tank = target_tank

    def update(self):
        if not self.target_tank.is_respawning:  # Проверка, что танк не в режиме неуязвимости
            if self.direction == "up":
                self.rect.y -= self.speed
            elif self.direction == "down":
                self.rect.y += self.speed
            elif self.direction == "left":
                self.rect.x -= self.speed
            elif self.direction == "right":
                self.rect.x += self.speed

            if pygame.sprite.collide_rect(self, self.target_tank):
                self.target_tank.score += 1
                print(f"Score for {self.target_tank}: {self.target_tank.score}")
                self.kill()

                if self.target_tank.score > 0:
                    self.target_tank.respawn()

            for wall in walls:
                if pygame.sprite.collide_rect(self, wall):
                    self.kill()

class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft=(x, y))

walls = pygame.sprite.Group()
wall1 = Wall(200, 150, 20, 100, GRAY)
wall2 = Wall(400, 300, 20, 200, GRAY)
wall3 = Wall(600, 100, 20, 150, GRAY)
wall4 = Wall(100, 400, 20, 100, GRAY)
walls.add(wall1, wall2, wall3, wall4)

tank1 = Tank(100, SCREEN_HEIGHT // 2, BLACK)
tank2 = Tank(SCREEN_WIDTH - 100, SCREEN_HEIGHT // 2, RED)

all_sprites = pygame.sprite.Group()
all_sprites.add(tank1, tank2)
all_sprites.add(walls)

tanks = pygame.sprite.Group()
tanks.add(tank1, tank2)

running = True
while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                tank1.shoot(tank2, BLACK)
            elif event.key == pygame.K_RETURN:
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

    all_sprites.update()
    all_sprites.draw(screen)

    text = font.render(f"Score: {tank2.score} - {tank1.score}", True, BLACK)
    screen.blit(text, (10, 10))

    pygame.display.flip()
    clock.tick(500)

pygame.quit()
sys.exit()
