import pygame
import sys

pygame.init()

clock = pygame.time.Clock()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Перестрелка")

WHITE = (255, 255, 255)
BLACK = (255, 0, 0)  # Изменен цвет первого танка на красный
RED = (0, 0, 0)      # Изменен цвет второго танка на черный
GRAY = (169, 169, 169)

font = pygame.font.Font(None, 36)

class Tank(pygame.sprite.Sprite):
    def __init__(self, x, y, color, initial_direction, name):
        super().__init__()
        self.color = color
        self.name = name
        self.image = pygame.Surface((50, 50), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=(x, y))
        self.start_position = (x, y)
        self.speed = 1
        self.score = 0
        self.direction = initial_direction
        self.last_shot_time = 0
        self.shoot_delay = 1000
        self.is_respawning = False
        self.invulnerable_time = 3000
        self.invulnerable_end_time = 0
        self.draw_tank()

    def draw_tank(self):
        self.image.fill((0, 0, 0, 0))
        points = {
            'right': [(0, 0), (50, 25), (0, 50)],
            'left': [(50, 0), (0, 25), (50, 50)],
            'up': [(0, 50), (25, 0), (50, 50)],
            'down': [(0, 0), (25, 50), (50, 0)]
        }
        pygame.draw.polygon(self.image, self.color, points[self.direction])

    def move(self, dx, dy):
        if self.is_respawning:
            return

        old_rect = self.rect.copy()
        self.rect.x += dx * self.speed
        self.rect.y += dy * self.speed

        if any(pygame.sprite.collide_rect(self, wall) for wall in walls) or \
           any(tank != self and pygame.sprite.collide_rect(self, tank) for tank in tanks):
            self.rect = old_rect
        else:
            self.update_direction(dx, dy)

        self.rect.clamp_ip(screen.get_rect())

    def update_direction(self, dx, dy):
        if dx > 0:
            self.direction = 'right'
        elif dx < 0:
            self.direction = 'left'
        elif dy > 0:
            self.direction = 'down'
        elif dy < 0:
            self.direction = 'up'

        self.draw_tank()

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
        self.invulnerable_end_time = pygame.time.get_ticks() + self.invulnerable_time

    def update(self):
        if self.is_respawning and pygame.time.get_ticks() >= self.invulnerable_end_time:
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
        if not self.target_tank.is_respawning:
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
                self.kill()

                if self.target_tank.score >= 5:
                    print(f"Выиграл танк {self.target_tank.name}")

                    if tank1.score >= 5:
                        tank1.color, tank2.color = tank2.color, tank1.color  
                    elif tank2.score >= 5:
                        tank1.color, tank2.color = tank2.color, tank1.color  

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
walls.add(Wall(200, 150, 20, 100, GRAY), Wall(400, 300, 20, 200, GRAY),
          Wall(600, 100, 20, 150, GRAY), Wall(100, 400, 20, 100, GRAY))

tank1 = Tank(100, SCREEN_HEIGHT // 2, BLACK, 'right', 'Чёрный - 1')
tank2 = Tank(SCREEN_WIDTH - 100, SCREEN_HEIGHT // 2, RED, 'left', 'Красный - 2')

all_sprites = pygame.sprite.Group(tank1, tank2, *walls)
tanks = pygame.sprite.Group(tank1, tank2)

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
    clock.tick(400)

    if tank1.score >= 5 or tank2.score >= 5:
        running = False

pygame.quit()
sys.exit()
