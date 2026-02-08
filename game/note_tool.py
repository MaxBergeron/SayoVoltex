from turtle import position
import pygame, bisect, math
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


    def draw_background(self, screen):
        screen.blit(self.image, self.rect)

    def draw_notes(self, screen, editor_time_ms):
        for note in self.notes:
            note.draw(screen, editor_time_ms)
    
    def draw_note_hover(self, screen, position, editor_time_ms, bpm, beat_divisor_value):
        mouse_x, mouse_y = position
        if (self.object_place_type == "note") and self.in_bounds(position):

            start_x = utils.scale_x(490)
            lane_width = utils.scale_x(100)
            lane_index = int((mouse_x - start_x) / lane_width)
            lane_x = start_x + lane_index * lane_width

            note_time = game_objects.HitObject.click_y_to_time(
            mouse_y, editor_time_ms, bpm, beat_divisor_value, self.get_closest_breakpoint)
            time_until_note = note_time - editor_time_ms
            note_y = utils.scale_y(constants.HIT_LINE_Y) - time_until_note * constants.SCROLL_SPEED

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
        lane_width = utils.scale_x(100)
        grid_start_x = utils.scale_x(490)

        key = int((mouse_x - grid_start_x) / lane_width) + 1
        note_time = game_objects.HitObject.click_y_to_time(
            mouse_y, editor_time_ms, bpm, beat_divisor_value, self.get_closest_breakpoint)
        
        for note in self.notes:
            if note.key == key and note.time == note_time:
                return
            
        new_note = HitObject(key, duration=0, time=note_time)

        self.notes.append(new_note)

    def drag_note(self, note, new_position, editor_time_ms, bpm, beat_divisor_value, note_part_clicked):
        mouse_x, mouse_y = new_position
        bpm = int(bpm)
        beat_divisor_value = float(Fraction(beat_divisor_value))

        new_note_time = game_objects.HitObject.click_y_to_time(
            mouse_y, editor_time_ms, bpm, beat_divisor_value, self.get_closest_breakpoint)
        old_end_time = note.time + note.duration
        if note.duration == 0:
            note.duration = abs(new_note_time - note.time)
            if new_note_time < note.time:
                note.time = new_note_time
        elif note_part_clicked == "head":
            note.time = new_note_time
            note.duration = old_end_time - note.time
        elif note_part_clicked == "tail":
            note.duration = new_note_time - note.time



    def place_laser(self, position):
        laser_width = utils.scale_x(50)
        start_pos = int((position[0] - self.pos_x) / laser_width) + 1       
        self.lasers.append(LaserObject(0, 0, start_pos, 0))
        print (start_pos)


    def set_active(self, active):
        self.active = active
        if not active:
            self.current_lane = None

    def in_bounds(self, position): 
        half_width = utils.scale_x(constants.LANE_WIDTH / 2)
        if (self.object_place_type == "note"): 
            if self.rect.left + half_width < position[0] < self.rect.right - half_width and self.rect.top < position[1] < self.rect.bottom:
                return True 
        elif (self.object_place_type == "laser"): 
            if self.rect.left < position[0] < self.rect.right and self.rect.top < position[1] < self.rect.bottom: 
                return True
        elif (self.object_place_type == None):
                return True 
        return False
    
    def get_note_at_click(self, position, editor_time_ms):
        for note in self.notes:
            note_x = utils.scale_x(490 + (note.key - 1) * 100)
            note_width = utils.scale_x(100)

            head_y = utils.scale_y(constants.HIT_LINE_Y) - ((note.time - editor_time_ms) * constants.SCROLL_SPEED)
            head_height = utils.scale_y(20)
            
            if note.duration > 0:
                hold_height = note.duration * constants.SCROLL_SPEED
                tail_y = head_y - hold_height
                tail_rect = pygame.Rect(note_x, tail_y, note_width, head_height)
                
                if tail_rect.collidepoint(position):
                    return note, "tail"

            head_rect = pygame.Rect(note_x, head_y, note_width, head_height)
            if head_rect.collidepoint(position):
                return note, "head" 
            
            note_rect = pygame.Rect(note_x, tail_y if note.duration > 0 else head_y, note_width, head_height + (hold_height if note.duration > 0 else 0))
            if note_rect.collidepoint(position):
                return note, "body"


        return None, None
    
    def add_breakpoint(self, num):
        num = int(num)
        if num not in self.breakpoints:
            bisect.insort(self.breakpoints, num)

    def get_breakpoints(self):
        return self.breakpoints

    def get_closest_breakpoint(self, t):
        index = bisect.bisect_right(self.breakpoints, t) - 1
        if index >= 0:
            return self.breakpoints[index]
        return self.breakpoints[0]
    
    def change_cursor_on_hover(self, position, editor_time_ms):
        cursor_set = False  

        for note in self.notes:
            note_x = utils.scale_x(490 + (note.key - 1) * 100)
            note_width = utils.scale_x(100)
            head_y = utils.scale_y(constants.HIT_LINE_Y) - (
                (note.time - editor_time_ms) * constants.SCROLL_SPEED
            )
            head_height = utils.scale_y(20)

            if note.duration > 0:
                tail_y = head_y - note.duration * constants.SCROLL_SPEED
                tail_rect = pygame.Rect(note_x, tail_y, note_width, head_height)
                if tail_rect.collidepoint(position):
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                    cursor_set = True
                    break

            head_rect = pygame.Rect(note_x, head_y, note_width, head_height)
            if head_rect.collidepoint(position):
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                cursor_set = True
                break

        if not cursor_set:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)


    


