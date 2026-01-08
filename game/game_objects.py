import pygame
from game import constants, utils

class HitObject:
    def __init__(self, key, duration, time):
        self.key = int(key)
        self.duration = int(duration)
        self.time = int(time)
        self.hit = False
        self.miss = False
        self.position_x = 0
        self.hold_started = False
        self.holding = False
        self.hold_complete = False

    def draw(self, screen, current_time_ms):
        scroll_speed = constants.SCROLL_SPEED
        top_y = utils.scale_x(constants.HIT_LINE_Y) - (self.time - current_time_ms) * scroll_speed

        # TAP note
        if self.duration <= 0:
            screen.blit(constants.TAP_NOTE_IMAGE, (self.position_x, top_y))
            return

        # HOLD note
        head_image, body_image, tail_image = self.assign_hold_note_images()

        note_length = self.duration * scroll_speed
        head_h = head_image.get_height()
        tail_h = tail_image.get_height()
        head_top = top_y
        tail_top = top_y - (note_length - head_h)
        body_top = tail_top + tail_h
        body_bottom = head_top

        # Draw head
        screen.blit(head_image, (self.position_x, top_y)) 

        y = body_bottom - body_image.get_height() 

        # Draw body
        while y >= body_top - tail_h - constants.HOLD_NOTE_BODY_IMAGE.get_height(): 
            screen.blit(body_image, (self.position_x, y)) 
            y -= body_image.get_height() 
        
        # Draw tail  
        screen.blit(tail_image, (self.position_x, top_y - note_length))

    def assign_hold_note_images(self):
        if self.hold_started or self.holding:
            return (
                constants.HOLD_NOTE_HEAD_IMAGE_TINTED,
                constants.HOLD_NOTE_BODY_IMAGE_TINTED,
                constants.HOLD_NOTE_TAIL_IMAGE_TINTED
            )
        else: 
            return (
                constants.HOLD_NOTE_HEAD_IMAGE,
                constants.HOLD_NOTE_BODY_IMAGE,
                constants.HOLD_NOTE_TAIL_IMAGE
            )



class LaserObject:
    def __init__(self, start_time, end_time, start_pos, end_pos, width=50):
        self.start_time = int(start_time)
        self.end_time = int(end_time)
        self.duration = self.end_time - self.start_time

        start_pos = int(start_pos)
        end_pos = int(end_pos)
        self.start_pos = self.normalize_position(start_pos)
        self.end_pos = self.normalize_position(end_pos)

        if (end_pos - start_pos) > 0:
            self.direction = "right"
        elif (end_pos - start_pos) < 0:
            self.direction = "left"
        else:
            self.direction = "none"

        self.prev_laser = None
        self.next_laser = None
        self.is_chained_from_prev = False

        self.started = False
        self.miss = False
        self.completed = False

        self.holding = False
        self.hold_completed = False
        self.total_hold_time = 0

        self.last_tick_time = None
        self.total_hold_time = 0

        self.width = utils.scale_x(width)
        self.half_width = utils.scale_x(width) / 2

        self.color = None

        self.points = []

    @staticmethod
    def normalize_position(pos):
        pos = int(pos)
        return (pos - 1) / 7

    # Computes the trapezoid points of the laser for the current frame.
    def update_points(self, current_time):
        start_x = self.laser_x_from_norm(self.start_pos)
        end_x = self.laser_x_from_norm(self.end_pos)
        start_y = self.y_from_time(self.start_time, current_time)
        end_y = self.y_from_time(self.end_time, current_time)

        if end_y > utils.scale_y(constants.HIT_LINE_Y):  # off the bottom of the screen
            self.completed = True

        dx = end_x - start_x
        dy = end_y - start_y
        going_right = end_x > start_x
        SLOPE_EPSILON = 1.0

        # Check if shallow slope
        if abs(dy) < abs(dx) + SLOPE_EPSILON:
            ratio = abs(dy / dx) if dx != 0 else 0
            ratio = min(ratio, 1.0)
            offset = (1.0 - ratio) * 50

            # If the pixels height difference is less than the offset (Very shallow or flat)
            if (self.end_time - self.start_time) * constants.SCROLL_SPEED < offset:
                extra_x = start_x - self.half_width
                # Very shallow slope right
                if going_right:
                    self.points = [
                        (start_x - self.half_width, start_y - offset), # Head offset
                        (start_x - self.half_width, start_y), # Head left
                        (start_x + self.half_width, start_y), # Head right
                        (end_x - self.half_width, end_y), # Tail left
                        (end_x + self.half_width, end_y), # Tail right
                        (end_x + self.half_width, end_y - offset) # Tail offset
                    ]
                # Very shallow slope left or flat
                else: 
                    self.points = [
                        (start_x + self.half_width, start_y - offset), # Head offset
                        (start_x + self.half_width, start_y), # Head right
                        (start_x - self.half_width, start_y), # Head left
                        (end_x + self.half_width, end_y), # Tail right
                        (end_x - self.half_width, end_y), # Tail left
                        (end_x - self.half_width, end_y - offset) # Tail offset
                    ]
            # Shallow slope Right
            elif going_right:
                extra_x = start_x - self.half_width
                self.points = [
                    (extra_x, start_y - offset), # Head offset
                    (start_x - self.half_width, start_y), # Head left
                    (start_x + self.half_width, start_y), # Head right
                    (end_x + self.half_width, end_y + offset), # Tail offset
                    (end_x + self.half_width, end_y), # Tail right
                    (end_x - self.half_width, end_y) # Tail left
                ]
            # Shallow slope left
            else:
                extra_x = start_x + self.half_width
                self.points = [
                    (start_x - self.half_width, start_y), # Head left
                    (start_x + self.half_width, start_y), # Head right
                    (extra_x, start_y - offset), # Head offset
                    (end_x + self.half_width, end_y), # Tail right
                    (end_x - self.half_width, end_y), # Tail left
                    (end_x - self.half_width, end_y + offset) # Tail offset
                ]
        # Non-shallow slope
        else:
            self.points = [
                (start_x - self.half_width, start_y), # Head left
                (start_x + self.half_width, start_y), # Head right
                (end_x + self.half_width, end_y), # Tail right
                (end_x - self.half_width, end_y) # Tail left
            ]

    def draw(self, screen):
        if not self.points or self.completed:
            return
        
        self.assign_laser_color()

        # Handle transparency 
        min_x = min(p[0] for p in self.points)
        min_y = min(p[1] for p in self.points)
        max_x = max(p[0] for p in self.points)
        max_y = max(p[1] for p in self.points)
        surf_width = max(1, max_x - min_x)
        surf_height = max(1, max_y - min_y)
        laser_surf = pygame.Surface((surf_width, surf_height), pygame.SRCALPHA)
        laser_points = [(x - min_x, y - min_y) for x, y in self.points]

        pygame.draw.polygon(laser_surf, self.color, laser_points)

        screen.blit(laser_surf, (min_x, min_y))

    def get_x_at_y(self, current_time, y):
        """
        Returns the left and right X positions of the laser at a specific Y (vertical line)
        based on the current trapezoid shape.
        """
        self.update_points(current_time)
    
        if not self.points or len(self.points) < 4:
            return (None, None)
        if current_time < self.start_time or current_time > self.end_time:
            return (None, None)

        # We'll check each edge of the polygon and see if it crosses Y
        left_x = None
        right_x = None

        for i in range(len(self.points)):
            p1 = self.points[i]
            p2 = self.points[(i + 1) % len(self.points)]

            y1, y2 = p1[1], p2[1]
            x1, x2 = p1[0], p2[0]

            # If the edge crosses the horizontal line y
            if (y1 <= y <= y2) or (y2 <= y <= y1):
                # Linear interpolation to find X at this Y
                if y2 - y1 != 0:
                    t = (y - y1) / (y2 - y1)
                    x_at_y = x1 + t * (x2 - x1)
                else:
                    x_at_y = x1

                if left_x is None or x_at_y < left_x:
                    left_x = x_at_y
                if right_x is None or x_at_y > right_x:
                    right_x = x_at_y

        return (left_x, right_x)

    @staticmethod
    def y_from_time(note_time, current_time):
        return constants.HIT_LINE_Y - (note_time - current_time) * constants.SCROLL_SPEED

    @staticmethod
    def laser_x_from_norm(norm):
        screen_center = utils.scale_x(constants.BASE_W) // 2
        left_lane = screen_center - utils.scale_x(200)
        right_lane = screen_center + utils.scale_x(200)
        laser_width = utils.scale_x(50)
        half_laser_width = laser_width // 2
        return (left_lane + half_laser_width) + norm * ((right_lane - half_laser_width) - (left_lane + half_laser_width))
    
    def assign_laser_color(self):
        if self.is_chained_from_prev and self.prev_laser:
            self.color = self.prev_laser.color
        else:
            if self.direction == "right":
                self.color = pygame.Color(constants.LASER_COLOR_GREEN)
            else:
                self.color = pygame.Color(constants.LASER_COLOR_RED)

        self.color.a = 180