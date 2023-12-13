#@author: Kate Little
#@version: 2023
# NOTE : All code in this file was created with the assistance of chatGPT 
# For the whole project, I used AI to help generate a 1st draft of the code and debug 

import pygame
import random
import math

from fsm import FSM 

WIDTH, HEIGHT = 800, 600
filepath = "images/"
            
# Class defining Obstacles in the game
class Obstacle(pygame.sprite.Sprite):
    def __init__(self, map_width, map_height, player):
        super().__init__()
        self.x = int(random.randint(-map_width // 2, map_width // 2))
        self.y = int(random.randint(-map_height // 2, map_height // 2))
        # make it so that it moves at player's speed
        self.speed = 1 
        self.images = [pygame.image.load(filepath+"suitcase.png"), pygame.image.load(filepath+"tsa_officer.png")]
        self.image = random.choice(self.images) 
        # Set dimensions 
        self.width, self.height = 25, 40
        self.close_to_player = False
        self.player = player

        # Create FSM 
        self.fsm = FSM("chasing")
        self.init_fsm()

    # Draw obstacle 
    def draw(self, screen, player_x, player_y):
        screen.blit(self.image, (self.x + WIDTH // 2 - player_x - self.width // 2, self.y + HEIGHT // 2 - player_y - self.height // 2))

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
        #Otherwise, if they have eaten, return "meal" as input
        # Otherwise, return "nothing" to signify how the player has not done anything important that will change the obstacle's state
        if self.player.has_reached_plane(): 
            return "plane"
        elif self.player.has_eaten_recently(): 
            return "meal"
        else: 
            return "nothing"
