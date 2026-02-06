import pygame, bisect
from fractions import Fraction
from game import constants, utils, game_objects
from game.game_objects import HitObject, LaserObject



class NoteTool:
    def __init__(self):
        self.lane_count = 3
        self.pos_x = utils.scale_x(440)
        self.pos_y = utils.scale_y(0)
        self.length = utils.scale_x(400)
        self.width = utils.scale_y(720)

        self.image = pygame.image.load("assets/images/editor_grid.png")
        self.image = pygame.transform.scale(self.image, (self.length, self.width))
        self.rect = self.image.get_rect(topleft=(self.pos_x, self.pos_y))
        self.note_hover_image = pygame.image.load("assets/skin/hit_note.png").convert_alpha()
        self.note_hover_image.set_alpha(128)

        self.notes = []
        self.lasers = []
        self.breakpoints= []
        self.add_breakpoint(0)

        self.object_place_type = None
        self.active = True
        self.preview_time_ms = 0


    def draw_background(self, screen):
        screen.blit(self.image, self.rect)

    def draw_notes(self, screen, editor_time_ms):
        for note in self.notes:
            note.draw(screen, editor_time_ms)
    
    def draw_note_hover(self, screen, position, editor_time_ms, bpm, beat_divisor_value):
        mouse_x, mouse_y = position
        if (self.object_place_type == "note") and (utils.scale_x(490) < mouse_x < utils.scale_x(790)) and (mouse_y < utils.scale_y(670)):

            start_x = utils.scale_x(490)
            lane_width = utils.scale_x(100)
            lane_index = int((mouse_x - start_x) / lane_width)
            lane_x = utils.scale_x(490 + lane_index * 100)

            bpm = int(bpm)
            beat_divisor_value = float(Fraction(beat_divisor_value))

            ms_per_beat = 60000 / bpm # 1/4
            ms_per_subdivision = (ms_per_beat / 0.25) * beat_divisor_value 
            breakpoint_time = self.get_closest_breakpoint(editor_time_ms)
            note_time = HitObject.click_y_to_time(mouse_y, editor_time_ms, ms_per_subdivision, breakpoint_time)
            time_until_note = note_time - editor_time_ms
            note_y = constants.HIT_LINE_Y - time_until_note * constants.SCROLL_SPEED

            screen.blit(self.note_hover_image, (lane_x, note_y))


    def check_for_input(self, position, editor_time_ms, bpm, beat_divisor_value):
        if self.in_bounds(position):
            if self.object_place_type == "note":
                self.place_note(position, editor_time_ms, bpm, beat_divisor_value)
            elif self.object_place_type == "laser":
                self.place_laser(position, editor_time_ms)
        return self.rect.collidepoint(position)
    
    def place_note(self, position, editor_time_ms, bpm, beat_divisor_value):
        mouse_x, mouse_y = position
        key = int((mouse_x - utils.scale_x(490)) / 100) + 1
        bpm = int(bpm)
        beat_divisor_value = float(Fraction(beat_divisor_value))

        ms_per_beat = 60000 / bpm # 1/4
        ms_per_subdivision = (ms_per_beat / 0.25) * beat_divisor_value 
        breakpoint_time = self.get_closest_breakpoint(editor_time_ms)
        note_time = HitObject.click_y_to_time(mouse_y, editor_time_ms, ms_per_subdivision, breakpoint_time)

        # No identical notes
        for note in self.notes:
            if note.key == key and note.time == note_time:
                return

        new_note = HitObject(key, duration=0, time=note_time)

        self.notes.append(new_note)

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
            if (position[0] > utils.scale_x(490) and position[0] < utils.scale_x(790) and position[1] < utils.scale_y(670)): 
                return True 
        elif (self.object_place_type == "laser"): 
            if (position[0] > utils.scale_x(440) and position[0] < utils.scale_x(840) and position[1] < utils.scale_y(670)): 
                return True 
        return False
    

    
    def add_breakpoint(self, num):
        if num not in self.breakpoints:
            bisect.insort(self.breakpoints, num)

    def get_closest_breakpoint(self, t):
        index = bisect.bisect_right(self.breakpoints, t) - 1

        if index >= 0:
            return self.breakpoints[index]
        return None
    

    


