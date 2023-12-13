#@author: Kate Little
#@version: 2023
# NOTE : All code in this file was created with the assistance of chatGPT
# For the whole project, I used AI to help generate a 1st draft of the code and debug 

import pygame
import time

WIDTH, HEIGHT = 800, 600
MAP_WIDTH, MAP_HEIGHT = 8000, 6000
FPS = 60
filepath = "images/"

# Class defining Player behavior in the game 
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

            