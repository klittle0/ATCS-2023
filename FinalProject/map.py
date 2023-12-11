import pygame
import random
import math

WIDTH, HEIGHT = 800, 600
MAP_WIDTH, MAP_HEIGHT = 8000, 6000
PERSON_SIZE = 30
FOOD_SIZE = 10
WHITE = (255, 255, 255)
GRAY = (211, 211, 211)
RED = (255, 0, 0)
FPS = 60

class Player(pygame.sprite.Sprite):
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

            
class Obstacle(pygame.sprite.Sprite):
    def __init__(self, map_width, map_height):
        self.x = random.randint(-map_width // 2, map_width // 2)
        self.y = random.randint(-map_height // 2, map_height // 2)
        # make it so that it moves at player's speed
        self.speed = 0.7  # Initial speed

    def draw(self, screen, player_x, player_y):
        pygame.draw.circle(screen, RED, (self.x + WIDTH // 2 - player_x, self.y + HEIGHT // 2 - player_y), PERSON_SIZE // 2)

    def chase_player(self, player):
        dx = player.x - self.x
        dy = player.y - self.y

        distance = math.sqrt(dx ** 2 + dy ** 2)
        if distance > 5:
            if abs(dx) > 5:
                dx /= distance
            if abs(dy) > 5:
                dy /= distance

        self.x += dx * self.speed
        self.y += dy * self.speed

    

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
            self.screen.fill(GRAY)
        
            # Draw grid lines
            for x in range(-MAP_WIDTH // 2, MAP_WIDTH // 2, 50):
                pygame.draw.line(self.screen, WHITE, (x + WIDTH // 2 - self.player.x % 50, -MAP_HEIGHT // 2 + HEIGHT // 2 - self.player.y % 50), 
                                 (x + WIDTH // 2 - self.player.x % 50, MAP_HEIGHT // 2 + HEIGHT // 2 - self.player.y % 50), 1)
            for y in range(-MAP_HEIGHT // 2, MAP_HEIGHT // 2, 50):
                pygame.draw.line(self.screen, WHITE, (-MAP_WIDTH // 2 + WIDTH // 2 - self.player.x % 50, y + HEIGHT // 2 - self.player.y % 50), 
                                 (MAP_WIDTH // 2 + WIDTH // 2 - self.player.x % 50, y + HEIGHT // 2 - self.player.y % 50), 1)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            keys = pygame.key.get_pressed()
            self.player.move(keys, MAP_WIDTH, MAP_HEIGHT)

            # Move and draw obstacles
            print(self.player.speed)
            for obstacle in self.obstacles:
                obstacle.chase_player(self.player)
                obstacle.draw(self.screen, self.player.x, self.player.y)

                # Check collision between player and obstacle
                obstacle_x, obstacle_y = obstacle.x, obstacle.y
                distance = math.sqrt((obstacle_x - self.player.x) ** 2 + (obstacle_y - self.player.y) ** 2)

                if distance <= (self.player.radius + PERSON_SIZE // 2):
                    self.obstacles.remove(obstacle)
                    self.player.speed -= 0.2  # Decrease player speed when hitting an obstacle

             # Iterate over food items with index for accurate removal
            index = 0
            while index < len(self.foods):
                food = self.foods[index]
                food_x, food_y = food[0], food[1]

                # Calculate distance between player and food item
                distance = math.sqrt((food_x - self.player.x) ** 2 + (food_y - self.player.y) ** 2)

                # Check collision between player and food
                if distance <= (self.player.radius + FOOD_SIZE // 2):
                    self.foods.pop(index)
                    self.player.speed += 0.1  # Increase player speed slightly when eating food
                else:
                    # Draw food item
                    pygame.draw.circle(self.screen, RED, (food_x + WIDTH // 2 - self.player.x, food_y + HEIGHT // 2 - self.player.y), FOOD_SIZE // 2)
                    index += 1  # Move to the next food item if no collision

            pygame.draw.circle(self.screen, RED, (WIDTH // 2, HEIGHT // 2), self.player.radius)


            pygame.draw.circle(self.screen, RED, (WIDTH // 2, HEIGHT // 2), self.player.radius)

            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()

game = Game()
game.run()
