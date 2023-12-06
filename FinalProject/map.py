import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
MAP_WIDTH, MAP_HEIGHT = 8000, 6000
PERSON_SIZE = 30
FOOD_SIZE = 10
WHITE = (255, 255, 255)
RED = (255, 0, 0)
FPS = 60

# Create the window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Airport Adventure')

# Clock for controlling FPS
clock = pygame.time.Clock()

# Player attributes
player_x, player_y = WIDTH // 2, HEIGHT // 2
player_radius = PERSON_SIZE // 2
player_speed = 0.8  # Initial speed

# List to hold food items
foods = []

# Class for obstacles
class Obstacle:
    def __init__(self):
        self.x = random.randint(-MAP_WIDTH // 2, MAP_WIDTH // 2)
        self.y = random.randint(-MAP_HEIGHT // 2, MAP_HEIGHT // 2)
        self.speed = player_speed  # Same speed as player
    
    def draw(self, offset_x, offset_y):
        pygame.draw.circle(screen, RED, (self.x + offset_x + WIDTH // 2, self.y + offset_y + HEIGHT // 2), PERSON_SIZE // 2)

    def chase_player(self, player_x, player_y):
        dx = player_x - self.x
        dy = player_y - self.y
        distance = math.sqrt(dx ** 2 + dy ** 2)
        
        if distance != 0:
            # updates speed to match player
            self.speed = player_speed
            self.x += self.speed * dx / distance
            self.y += self.speed * dy / distance

# Function to generate food at random positions within visible area
def generate_food():
    for _ in range(1000):  # You can adjust the number of food items as needed
        x = random.randint(-MAP_WIDTH // 2, MAP_WIDTH // 2)
        y = random.randint(-MAP_HEIGHT // 2, MAP_HEIGHT // 2)
        foods.append((x, y))

generate_food()

# List to hold obstacles
obstacles = []

# Function to generate obstacles
def generate_obstacles():
    for _ in range(20):  # 20 obstacles
        obstacle = Obstacle()
        obstacles.append(obstacle)

generate_obstacles()

# Game loop
running = True
offset_x, offset_y = 0, 0

while running:
    screen.fill(WHITE)

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get the current position of the player
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and offset_x < MAP_WIDTH // 2:
        offset_x += player_speed
    if keys[pygame.K_RIGHT] and offset_x > -MAP_WIDTH // 2:
        offset_x -= player_speed
    if keys[pygame.K_UP] and offset_y < MAP_HEIGHT // 2:
        offset_y += player_speed
    if keys[pygame.K_DOWN] and offset_y > -MAP_HEIGHT // 2:
        offset_y -= player_speed

    # Update obstacles' positions and draw them
    for obstacle in obstacles:
        obstacle.chase_player(player_x, player_y)
        obstacle.draw(offset_x, offset_y)

    # Draw food items
    for food in foods:
        pygame.draw.circle(screen, RED, (food[0] + offset_x + WIDTH // 2, food[1] + offset_y + HEIGHT // 2), FOOD_SIZE // 2)

    # Draw player
    pygame.draw.circle(screen, RED, (WIDTH // 2, HEIGHT // 2), player_radius)

    # Check for collision with food
    for food in foods[:]:
        if math.dist((food[0] + offset_x + WIDTH // 2, food[1] + offset_y + HEIGHT // 2), (player_x, player_y)) <= (
                player_radius + FOOD_SIZE // 2):
            foods.remove(food)
            player_speed += 0.1  # Increase player speed slightly when eating food

    pygame.display.flip()
    clock.tick(FPS)

# Quit Pygame
pygame.quit()
