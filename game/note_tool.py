import pygame
from game import constants, utils, game_objects
from game.game_objects import HitObject, LaserObject



class NoteTool:
    """Basic editor tool for placing notes.

    This is intentionally minimal so it can be wired into the editor UI later.
    """

    def __init__(self):
        self.lane_count = 3
        self.pos_x = utils.scale_x(440)
        self.pos_y = utils.scale_y(0)
        self.length = utils.scale_x(400)
        self.width = utils.scale_y(720)

        self.image = pygame.image.load("assets/images/editor_grid.png")
        self.image = pygame.transform.scale(self.image, (self.length, self.width))
        self.rect = self.image.get_rect(topleft=(self.pos_x, self.pos_y))

        self.notes = []
        self.lasers = []

        self.object_place_type = None
        self.active = True
        self.preview_time_ms = 0




    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def check_for_input(self, position):
        if self.in_bounds(position):
            if self.object_place_type == "note":
                self.place_note(position)
            elif self.object_place_type == "laser":
                self.place_laser(position)
        return self.rect.collidepoint(position)
    
    def place_note(self, position):
        key = int((position[0] - utils.scale_x(490)) / 100) + 1
        self.notes.append(HitObject(key, 0, position[1]))
        print(key)

    def place_laser(self, position):
        start_pos = int((position[0] - utils.scale_x(440)) / 50) + 1
        self.lasers.append(LaserObject(0, 0, start_pos, 0))
        print (start_pos)



    def set_active(self, active):
        self.active = active
        if not active:
            self.current_lane = None
            self.preview_time_ms = None

    def in_bounds(self, position): 
        if (self.object_place_type == "note"): 
            if (position[0] > utils.scale_x(490) and position[0] < utils.scale_x(790)): 
                return True 
        elif (self.object_place_type == "laser"): 
            if (position[0] > utils.scale_x(440) and position[0] < utils.scale_x(840)): 
                return True 
        return False


