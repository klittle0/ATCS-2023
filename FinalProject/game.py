#@author: Kate Little
#@version: 2023
# NOTE : All code in this file was created with the assistance of chatGPT 
# For the whole project, I used AI to help generate a 1st draft of the code and debug 

import pygame
import random
import math
import time

from obstacle import Obstacle
from player import Player 

WIDTH, HEIGHT = 800, 600
MAP_WIDTH, MAP_HEIGHT = 8000, 6000
FOOD_SIZE = 10
WHITE = (255, 255, 255)
BLUE = (177, 212, 229)
DARK_BLUE = (0, 173, 219)
FPS = 60
filepath = "images/"

# Represents the main game logic and functionality 
class Game:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Airport Adventure')

        self.clock = pygame.time.Clock()

        self.foods = []
        self.obstacles = pygame.sprite.Group()
        # Generate random colors that correspond with each food 
        self.food_colors = [(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)) for _ in range(700)]

        self.player = Player(WIDTH, HEIGHT)
        self.generate_food()
        self.generate_obstacles()
    
    def print_message(self, message): 
            font = pygame.font.Font(None, 80)
            text_surface = font.render(message, True, DARK_BLUE)
            text_rect = text_surface.get_rect()
            # Position the text in the center of the screen
            text_rect.center = (WIDTH // 2, HEIGHT // 2)
            self.screen.blit(text_surface, text_rect)
            pygame.display.flip()

    def generate_food(self):
        for _ in range(700):
            x = random.randint(-MAP_WIDTH // 2, MAP_WIDTH // 2)
            y = random.randint(-MAP_HEIGHT // 2, MAP_HEIGHT // 2)
            self.foods.append((x, y))

    def generate_obstacles(self):
        for _ in range(50):
            obstacle = Obstacle(MAP_WIDTH, MAP_HEIGHT, self.player)
            obstacle.x = random.randint(-MAP_WIDTH // 2 + self.player.width, MAP_WIDTH // 2 - self.player.width)
            obstacle.y = random.randint(-MAP_HEIGHT // 2 + self.player.height, MAP_HEIGHT // 2 - self.player.height)
            # Initialize's the obstacle's FSM 
            obstacle.init_fsm()
            self.obstacles.add(obstacle)


    def run(self):
        
        running = True  
        print("Welcome to Airplane Adventure! Avoid obstacles so you can find your plane before it takes off!")

        
        while running:
            self.screen.fill(BLUE)

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
            for obstacle in self.obstacles:
                # process the obstacle's FSM 
                obstacle.fsm.process(obstacle.get_input_symbol())

                # Update obstacle's position based on FSM state
                if obstacle.get_state() == "chasing":
                    obstacle.chase_player()
                elif obstacle.get_state() == "scattering":
                    obstacle.scatter_from_player()
                
                #obstacle.chase_player(self.player)
                obstacle.draw(self.screen, self.player.x, self.player.y)

                # Check collision between player and obstacle
                obstacle_x, obstacle_y = obstacle.x, obstacle.y
                delta_x = obstacle_x - self.player.x
                delta_y = obstacle_y - self.player.y
                distance = math.sqrt(delta_x ** 2 + delta_y ** 2)

                # Obstacle disappears and player speed decreases when collision detected
                if distance <= (self.player.width + obstacle.width // 2):
                    self.obstacles.remove(obstacle)
                    self.player.speed -= 0.35  

            # Iterate over food items with index for accurate removal
            index = 0
            while index < len(self.foods):
                
                food = self.foods[index]
                food_x, food_y = food[0], food[1]

                # Calculate distance between player and food item
                distance = math.sqrt((food_x - self.player.x) ** 2 + (food_y - self.player.y) ** 2)

                # Check collision between player and food
                if distance <= (self.player.width + FOOD_SIZE // 2):
                    self.foods.pop(index)
                    self.player.speed += 0.1  # Increase player speed slightly when eating food
                    self.player.last_meal_time = time.time()
                else:
                    # Draw food item
                    food_color = self.food_colors[index]
                    pygame.draw.circle(self.screen, food_color, (food_x + WIDTH // 2 - self.player.x, 
                                                                 food_y + HEIGHT // 2 - self.player.y), FOOD_SIZE // 2)
                    index += 1  # Move to the next food item if no collision

            # Draw player 
            self.screen.blit(self.player.image, self.player.rect)

            # Preps to draw airplane in upper right corner of map 
            airplane_image = pygame.image.load(filepath+"airplane.png")
            airplane_rect = airplane_image.get_rect()

            # Calculate airplane position relative to player and map
            airplane_offset_x = MAP_WIDTH // 2 - self.player.x + WIDTH // 2 - airplane_rect.width + 200
            airplane_offset_y = -MAP_HEIGHT // 2 - self.player.y + HEIGHT // 2 - 200
            # Draw airplane 
            self.screen.blit(airplane_image, (airplane_offset_x, airplane_offset_y))

            if self.player.is_dead():
                self.print_message("You Lose")
                running = False

            if self.player.has_won: 
                self.print_message("You Win!")
                running = False
        
            pygame.display.flip()
            self.clock.tick(FPS)
            
        pygame.time.wait(2000)
        pygame.quit()

game = Game()
game.run()
