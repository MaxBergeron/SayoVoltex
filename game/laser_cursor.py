import pygame, math
from game import constants, utils

class LaserCursor:
    def __init__(self):
        self.length = utils.scale_x(100)
        self.height = utils.scale_y(20)

        self.image = pygame.image.load("assets/skin/cursor_blue.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.length, self.height))

        self.velocity = 0.0
        self.acceleration = 6    # per input impulse (KEY VALUE)
        self.damping = 100.0     # decay rate

        self.left_boundary = utils.scale_x(constants.BASE_W) // 2 - utils.scale_x(200)
        self.right_boundary = utils.scale_x(constants.BASE_W) // 2 + utils.scale_x(200) - self.length

        self.value = 0.0
        self.position_y = utils.scale_y(constants.HIT_LINE_Y)
        self.position_x = self.left_boundary

        self.left_edge = self.position_x
        self.right_edge = self.position_x + self.length

    def update_movement(self, knob_input, delta_time):
        """
        Smooth knob movement with immediate response to direction changes.
        knob_input: -1, 0, or +1
        delta_time: seconds elapsed
        """
        ACCEL = self.acceleration
        DAMPING = self.damping

        if knob_input != 0:
            # If changing direction, apply partial velocity reversal
            if self.velocity * knob_input < 0:
                # Reverse some of the velocity instead of ignoring input
                self.velocity *= 0.5  # reduce current velocity
            # Apply input impulse
            self.velocity += knob_input * ACCEL
        else:
            # Apply friction decay when idle
            self.velocity *= math.exp(-DAMPING * delta_time)

        # Integrate position
        self.value += self.velocity * delta_time

        # Clamp boundaries
        if self.value <= 0.0:
            self.value = 0.0
            if self.velocity < 0: self.velocity = 0
        elif self.value >= 1.0:
            self.value = 1.0
            if self.velocity > 0: self.velocity = 0

        # Convert normalized value to screen X
        self.position_x = self.left_boundary + self.value * (self.right_boundary - self.left_boundary)
        self.left_edge = self.position_x
        self.right_edge = self.position_x + self.length



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
