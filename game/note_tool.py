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
        self.laser_start = None
        self.laser_end = None
        self.laser_temp_position = None
        self.initial_editor_time_ms = 0

        self.object_place_type = None
        self.active = True


    def draw_background(self, screen):
        screen.blit(self.image, self.rect)

    def draw_notes(self, screen, editor_time_ms):
        for note in self.notes:
            note.draw(screen, editor_time_ms)
    
    def draw_note_hover(self, screen, position, editor_time_ms, bpm, beat_divisor_value, audio_length_ms):
        mouse_x, mouse_y = position
        distance_px = utils.scale_y(constants.HIT_LINE_Y) - mouse_y
        note_time_ms = editor_time_ms + (distance_px / constants.SCROLL_SPEED)
        if (self.object_place_type == "note") and self.in_bounds(position) and note_time_ms >= 0 and note_time_ms <= audio_length_ms:

            start_x = utils.scale_x(490)
            lane_width = utils.scale_x(100)
            lane_index = int((mouse_x - start_x) / lane_width)
            lane_x = start_x + lane_index * lane_width

            note_time = game_objects.HitObject.click_y_to_time(
            mouse_y, editor_time_ms, bpm, beat_divisor_value, self.get_closest_breakpoint)
            time_until_note = note_time - editor_time_ms
            note_y = utils.scale_y(constants.HIT_LINE_Y) - time_until_note * constants.SCROLL_SPEED

            screen.blit(self.note_hover_image, (lane_x, note_y))


    def check_for_input(self, position, editor_time_ms, bpm, beat_divisor_value, audio_length_ms, screen):
        if not self.in_bounds(position):
            return None
        
        clicked_note = self.get_note_at_click(position, editor_time_ms)
        if clicked_note[0]:
            return clicked_note[0]

        clicked_laser = self.get_laser_at_click(position, editor_time_ms)
        if clicked_laser:
            return clicked_laser

        if self.object_place_type == "laser":
            if self.laser_start is None:
                # First click
                self.laser_start = position
                self.laser_temp_position = position
                self.initial_editor_time_ms = editor_time_ms
                return None
            else:
                # Second click
                self.laser_end = position
                hit_object = self.place_laser(
                    self.laser_start, self.laser_end,
                    self.initial_editor_time_ms, editor_time_ms,
                    bpm, beat_divisor_value, audio_length_ms)
                self.laser_start = None
                self.laser_end = None
                return hit_object

        if self.object_place_type == "note":
            hit_object = self.place_note(position, editor_time_ms, bpm, beat_divisor_value, audio_length_ms)
            return hit_object

        return None

    def place_note(self, position, editor_time_ms, bpm, beat_divisor_value, audio_length_ms):
        mouse_x, mouse_y = position
        lane_width = utils.scale_x(100)
        grid_start_x = utils.scale_x(490)
        distance_px = utils.scale_y(constants.HIT_LINE_Y) - mouse_y
        note_time_ms = editor_time_ms + (distance_px / constants.SCROLL_SPEED)

        if note_time_ms < 0 or note_time_ms > audio_length_ms:
            return
        
        key = int((mouse_x - grid_start_x) / lane_width) + 1
        note_time = game_objects.HitObject.click_y_to_time(
            mouse_y, editor_time_ms, bpm, beat_divisor_value, self.get_closest_breakpoint)
        
        for note in self.notes:
            if note.key == key and note.time == note_time:
                return
            
        new_note = HitObject(key, duration=0, time=note_time)

        self.notes.append(new_note)
        return new_note

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



    def place_laser(self, position_1, position_2, initial_editor_time_ms, editor_time_ms, bpm, beat_divisor_value, audio_length_ms):
        laser_width = utils.scale_x(50)
        start_pos = int((position_1[0] - self.pos_x) / laser_width) + 1
        end_pos = int((position_2[0] - self.pos_x) / laser_width) + 1       
        start_time = game_objects.HitObject.click_y_to_time(
            position_1[1], initial_editor_time_ms, bpm, beat_divisor_value, self.get_closest_breakpoint)
        end_time = game_objects.HitObject.click_y_to_time(
            position_2[1], editor_time_ms, bpm, beat_divisor_value, self.get_closest_breakpoint)
        if start_time > end_time:
            start_time, end_time = end_time, start_time
            start_pos, end_pos = end_pos, start_pos 
        new_laser = LaserObject(start_time, end_time, start_pos, end_pos, True)
        self.lasers.append(new_laser)
        return new_laser

    def draw_laser_hover(self, screen, position, editor_time_ms, bpm, beat_divisor_value, audio_length_ms):
        if self.object_place_type == "laser" and self.in_bounds(position):
            mouse_x, mouse_y = position
            laser_width = utils.scale_x(50)
            grid_start_x = utils.scale_x(440)
            distance_px = utils.scale_y(constants.HIT_LINE_Y) - mouse_y
            laser_time_ms = editor_time_ms + (distance_px / constants.SCROLL_SPEED)

            if laser_time_ms < 0 or laser_time_ms > audio_length_ms:
                return
            
            start_pos = int((self.laser_temp_position[0] - self.pos_x) / laser_width) + 1
            end_pos = int((position[0] - self.pos_x) / laser_width) + 1       
            start_time = game_objects.HitObject.click_y_to_time(
                self.laser_temp_position[1], self.initial_editor_time_ms, bpm, beat_divisor_value, self.get_closest_breakpoint)
            end_time = game_objects.HitObject.click_y_to_time(
                position[1], editor_time_ms, bpm, beat_divisor_value, self.get_closest_breakpoint)
            if start_time > end_time:
                start_time, end_time = end_time, start_time
                start_pos, end_pos = end_pos, start_pos 
            temp_laser = LaserObject(start_time, end_time, start_pos, end_pos, True)
            temp_laser.update_points(editor_time_ms)
            temp_laser.draw(screen)

    def draw_lasers(self, screen, editor_time_ms):
        for laser in self.lasers:
            laser.update_points(editor_time_ms)
            laser.draw(screen)

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
    
    def get_laser_at_click(self, position, editor_time_ms):
        mouse_x, mouse_y = position

        for laser in self.lasers:
            left_x, right_x = laser.get_x_at_y_for_click(editor_time_ms, mouse_y)

            if left_x is None:
                continue

            if left_x <= mouse_x <= right_x:
                return laser

        return None

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



    def save_map(self, file_path, metadata, audio_length_ms):
        with open(file_path, "w", encoding="utf-8") as f:

            f.write("[Metadata]\n")
            f.write(f"Title: {metadata['Title']}\n")
            f.write(f"Artist: {metadata['Artist']}\n")
            f.write(f"Creator: {metadata['Creator']}\n")
            f.write(f"Version: {metadata['Version']}\n")
            length = audio_length_ms // 1000
            f.write(f"Length: {length}\n")
            scroll_speed = float(metadata["Scroll Speed"])
            f.write(f"Scroll Speed: {scroll_speed:.2f}\n")            
            f.write(f"Audio Lead In: {metadata['Audio Lead In']}\n")
            f.write(f"Image Path: {metadata['Image Path']}\n")
            f.write(f"Audio Path: {metadata['Audio Path']}\n")

            f.write("\n")

            f.write("// Hit Object Ordering\n")
            f.write("// 3-key configuration (1-3), hold duration, time position,\n")
            f.write("[HitObjects]\n")

            for note in self.notes:
                key = note.key
                duration = note.duration
                time = note.time

                f.write(f"{key}, {duration}, {time}\n")

            f.write("\n")

            f.write("// Laser Object Ordering\n")
            f.write("// start time, end time, start position, end position\n")
            f.write("[LaserObjects]\n")

            for laser in self.lasers:
                start = laser.start_time
                end = laser.end_time
                start_pos = game_objects.LaserObject.denormalize_position(laser.start_pos)
                end_pos = game_objects.LaserObject.denormalize_position(laser.end_pos)
                f.write(f"{start}, {end}, {start_pos}, {end_pos}\n")


    


