import pygame
from game import constants, utils

class LaserCursor:
    def __init__(self):
        self.image = pygame.image.load("assets/skin/temp_cursor.png").convert_alpha()
        self.length = utils.scale_x(100)

        self.velocity = 0.0
        self.acceleration = 6.7  # how fast it reacts to input
        self.friction = 0.85     # how fast it slows down per frame

        self.left_boundary = utils.scale_x(constants.BASE_W) // 2 - utils.scale_x(200)
        self.right_boundary = utils.scale_x(constants.BASE_W) // 2 + utils.scale_x(200)

        self.value = 0.0
        self.position_y = utils.scale_y(constants.HIT_LINE_Y)
        self.position_x = self.left_boundary

    def update_movement(self, knob_input, delta_time):

        # --- Instant direction change ---
        if (self.velocity > 0 and knob_input < 0) or (self.velocity < 0 and knob_input > 0):
            self.velocity = 0

        # --- Apply acceleration (impulse per input) ---
        self.velocity += knob_input * self.acceleration  # delta_time removed here

        # --- Apply friction ---
        self.velocity *= self.friction

        # --- Update normalized position (0 to 1) ---
        self.value += self.velocity * delta_time

        # --- Clamp within normalized boundaries ---
        self.value = max(0.0, min(1.0, self.value))

        # --- Convert normalized value to screen X ---
        self.position_x = self.left_boundary + self.value * (self.right_boundary - self.left_boundary)




    def set_position(self, value):
        self.value = max(0.0, min(1.0, value))

        width = self.right_boundary - self.left_boundary
        self.position_x = self.left_boundary + width * self.value
    
    def get_position(self):
        return self.position_x
    
    def move_right(self):
        pass

    def move_left(self):
        pass

    def draw(self, screen):
        screen.blit(self.image, (self.position_x, self.position_y))
