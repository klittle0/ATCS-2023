import pygame
import random
import math
import time

from fsm import FSM 

WIDTH, HEIGHT = 800, 600
MAP_WIDTH, MAP_HEIGHT = 8000, 6000
FOOD_SIZE = 10
WHITE = (255, 255, 255)
BLUE = (177, 212, 229)
DARK_BLUE = (0, 173, 219)
RED = (255, 0, 0)
FPS = 60
filepath = "images/"

class Player(pygame.sprite.Sprite):
    def __init__(self, width, height):
        super().__init__()
        self.x = int(width // 2)
        self.y = int(height // 2)
        self.width = 48
        self.height = 52
        self.speed = 1
        self.image = pygame.image.load(filepath+"traveler.png")
        self.rect = self.image.get_rect()
        self.last_meal_time = 0
        self.has_won = False
        self.rect.center = (width // 2, height // 2)  # Set the center of the image

    # Sets key movements
    def move(self, keys, map_width, map_height):
        if keys[pygame.K_LEFT] and self.x - self.speed > -map_width // 2:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] and self.x + self.speed < map_width // 2:
            self.x += self.speed
        if keys[pygame.K_UP] and self.y - self.speed > -map_height // 2:
            self.y -= self.speed
        if keys[pygame.K_DOWN] and self.y + self.speed < map_height // 2:
            self.y += self.speed

    # Check if the player has eaten food in the last two seconds
    def has_eaten_recently(self):
        current_time = time.time()
        time_difference = current_time - self.last_meal_time
        # Return True if player has eaten within .8 seconds, otherwise return False
        return time_difference <= .8  
    
    # Checks to see if player is in top right corner of map, aka where the plane is 
    def has_reached_plane(self):
        # Define a margin for the corner
        margin = 10
        self.has_won = self.x >= MAP_WIDTH // 2 - margin and self.y <= -MAP_HEIGHT // 2 + margin
        # Check if the player's coordinates are within the upper right corner with a margin
        return self.has_won
    
    #If player has stopped moving, it's dead 
    def is_dead(self): 
        return self.speed <= 0

            
class Obstacle(pygame.sprite.Sprite):
    def __init__(self, map_width, map_height, player):
        super().__init__()
        self.x = int(random.randint(-map_width // 2, map_width // 2))
        self.y = int(random.randint(-map_height // 2, map_height // 2))
        # make it so that it moves at player's speed
        self.speed = 1 
        self.images = [pygame.image.load(filepath+"suitcase.png"), pygame.image.load(filepath+"tsa_officer.png")]
        self.image = random.choice(self.images)  # Randomly choose image
        # Set dimensions 
        self.width, self.height = 25, 40
        self.close_to_player = False
        self.player = player

        # Creates FSM 
        self.fsm = FSM("chasing")
        self.init_fsm()

    def draw(self, screen, player_x, player_y):
        screen.blit(self.image, (self.x + WIDTH // 2 - player_x - self.width // 2, self.y + HEIGHT // 2 - player_y - self.height // 2))

    # How can I get the variables from player??
    def init_fsm(self):
       # Potential states: chasing, scattering, still

       # If chasing the player, and it has recently eaten, then scatter
        self.fsm.add_transition("meal", "chasing", self.scatter_from_player, "scattering")
        
        # If chasing the player, and it has reached the plane, go still 
        self.fsm.add_transition("plane", "chasing", self.go_still, "still")

        # If chasing player, and it has done nothing important, keep chasing 
        self.fsm.add_transition("nothing", "chasing", None, "chasing")

        # If scattering, and the player has done nothing important, chase player 
        self.fsm.add_transition("nothing", "scattering", self.chase_player, "chasing")

        # If scattering, and the player has eaten recently, keep scattering 
        self.fsm.add_transition("meal", "scattering", self.scatter_from_player, "scattering")

        # If scattering, and the player has reached the plane, go still 
        self.fsm.add_transition("plane", "scattering", self.go_still, "still")


    # ACTION
    # Makes the obstacle stop moving 
    def go_still(self):
        self.speed = 0; 
    
    # ACTION
    # Makes the obstacle run away from the player 
    def scatter_from_player(self): 
        dx = -(self.player.x - self.x)
        dy = -(self.player.y - self.y)
        distance = math.sqrt(dx ** 2 + dy ** 2)

        if distance > 5:
            if abs(dx) > 5:
                dx /= distance
            if abs(dy) > 5:
                dy /= distance

        self.x += dx * self.speed
        self.y += dy * self.speed

    # ACTION 
    # Calculates Euclidean distance to player and chases it at current speed 
    def chase_player(self):
        dx = self.player.x - self.x
        dy = self.player.y - self.y
        distance = math.sqrt(dx ** 2 + dy ** 2)

        if distance > 5:
            if abs(dx) > 5:
                dx /= distance
            if abs(dy) > 5:
                dy /= distance

        self.x += dx * self.speed
        self.y += dy * self.speed

    def get_state(self):
        return self.fsm.current_state
    
    # Finds the player's most important condition and returns it as input for the fsm
    def get_input_symbol(self): 
        #If player has reached the plane, then return this as input symbol 
        #Otherwise, if they have eaten 
        # Otherwise, return "nothing" to signify how the player has not done anything important that will change the 
        # Obstacle's state 
        if self.player.has_reached_plane(): 
            return "plane"
        elif self.player.has_eaten_recently(): 
            return "meal"
        else: 
            return "nothing"



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
        for _ in range(35):
            obstacle = Obstacle(MAP_WIDTH, MAP_HEIGHT, self.player)
            obstacle.x = random.randint(-MAP_WIDTH // 2 + self.player.width, MAP_WIDTH // 2 - self.player.width)
            obstacle.y = random.randint(-MAP_HEIGHT // 2 + self.player.height, MAP_HEIGHT // 2 - self.player.height)
            # Initialize's the obstacle's FSM 
            obstacle.init_fsm()
            self.obstacles.add(obstacle)

    def run(self):
        running = True
        
        # Preps to draw airplane in upper right corner of map 
        airplane_image = pygame.image.load(filepath+"airplane.png")
        airplane_rect = airplane_image.get_rect()
        airplane_rect.top = -MAP_HEIGHT // 2 - 100  # Adjust the value as needed
        airplane_rect.right = MAP_WIDTH // 2 + 100  # Adjust the value as needed
        
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
                distance_squared = delta_x ** 2 + delta_y ** 2

                # Calculate maximum allowable distance
                max_distance = (self.player.width + obstacle.width // 2) ** 2

                # Check if the squared distance exceeds the maximum allowable distance
                if distance_squared <= max_distance:
                    distance = math.sqrt(distance_squared)
                else:
                    distance = float('inf')  # Assign a value to signify the distance is too large

                if distance <= (self.player.width + obstacle.width // 2):
                    self.obstacles.remove(obstacle)
                    self.player.speed -= 0.35  # Decrease player speed when hitting an obstacle

            # Iterate over food items with index for accurate removal
            index = 0
            while index < len(self.foods):
                # print(index)
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

            # Draw airplane 
            self.screen.blit(airplane_image, airplane_rect)

            # Draw a rectangle where the airplane should be positioned
            pygame.draw.rect(self.screen, (255, 0, 0), airplane_rect, 2)
    
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
