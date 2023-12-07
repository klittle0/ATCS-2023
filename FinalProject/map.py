import pygame
import random
import math

WIDTH, HEIGHT = 800, 600
MAP_WIDTH, MAP_HEIGHT = 8000, 6000
PERSON_SIZE = 30
FOOD_SIZE = 10
WHITE = (255, 255, 255)
RED = (255, 0, 0)
FPS = 60

class Obstacle:
    def __init__(self, map_width, map_height):
        self.x = random.randint(-map_width // 2, map_width // 2)
        self.y = random.randint(-map_height // 2, map_height // 2)
        self.speed = 0.8 + 0.1  # Initial speed

    def draw(self, screen):
        pygame.draw.circle(screen, RED, (self.x + WIDTH // 2, self.y + HEIGHT // 2), PERSON_SIZE // 2)

    def chase_player(self, player):
        dx = player.x - self.x
        dy = player.y - self.y

        self.speed = 0.8 + 0.1
        if dx != 0:
            if dx < 0:
                self.x -= self.speed  # Decrease x distance
            else:
                self.x += self.speed  # Decrease x distance

        if dy != 0:
            if dy < 0:
                self.y -= self.speed  # Decrease y distance
            else:
                self.y += self.speed  # Decrease y distance

        print("OBSTACLE: ", self.x, self.y)
        print(player.x, player.y)

class Player:
    def __init__(self, width, height):
        self.x = width // 2
        self.y = height // 2
        self.radius = PERSON_SIZE // 2
        self.speed = 0.8

    def move(self, keys, map_width, map_height):
        if keys[pygame.K_LEFT] and self.x - self.speed > -map_width // 2:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] and self.x + self.speed < map_width // 2:
            self.x += self.speed
        if keys[pygame.K_UP] and self.y - self.speed > -map_height // 2:
            self.y -= self.speed
        if keys[pygame.K_DOWN] and self.y + self.speed < map_height // 2:
            self.y += self.speed

class Game:
    def __init__(self):
        pygame.init()


        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Airport Adventure')

        self.clock = pygame.time.Clock()

        self.foods = []
        self.obstacles = []

        self.player = Player(WIDTH, HEIGHT)
        self.generate_food()
        self.generate_obstacles()

    def generate_food(self):
        for _ in range(1000):
            x = random.randint(-MAP_WIDTH // 2, MAP_WIDTH // 2)
            y = random.randint(-MAP_HEIGHT // 2, MAP_HEIGHT // 2)
            self.foods.append((x, y))

    def generate_obstacles(self):
        for _ in range(20):
            obstacle = Obstacle(MAP_WIDTH, MAP_HEIGHT)
            self.obstacles.append(obstacle)

    def run(self):
        running = True

        while running:
            self.screen.fill(WHITE)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            keys = pygame.key.get_pressed()
            self.player.move(keys, MAP_WIDTH, MAP_HEIGHT)

            for obstacle in self.obstacles:
                obstacle.chase_player(self.player)
                obstacle.draw(self.screen)

            for food in self.foods:
                pygame.draw.circle(self.screen, RED,
                                   (food[0] + self.player.x + WIDTH // 2,
                                    food[1] + self.player.y + HEIGHT // 2),
                                   FOOD_SIZE // 2)

            pygame.draw.circle(self.screen, RED, (WIDTH // 2, HEIGHT // 2), self.player.radius)

            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()

game = Game()
game.run()
