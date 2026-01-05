import pygame, math
from game.game_objects import LaserObject
from game import constants, utils



def draw_laser(screen, laser_object, current_time):
    """
    Draws a transparent trapezoid laser on the screen.
    Optimized for fullscreen and many lasers.
    """

    # --- Laser dimensions ---
    laser_width = utils.scale_x(50)  # width at the top
    half_width = laser_width // 2

    # --- Get laser positions in pixels ---
    start_x = laser_x_from_norm(laser_object.start_pos)
    end_x = laser_x_from_norm(laser_object.end_pos)
    start_y = y_from_time(laser_object.start_time, current_time)
    end_y = y_from_time(laser_object.end_time, current_time)

    # --- Define trapezoid points ---
    points = [
        (start_x - half_width, start_y),  # top-left
        (start_x + half_width, start_y),  # top-right
        (end_x + half_width, end_y),      # bottom-right
        (end_x - half_width, end_y),      # bottom-left
    ]

    # --- Compute bounding rect to minimize surface size ---
    min_x = min(p[0] for p in points)
    min_y = min(p[1] for p in points)
    max_x = max(p[0] for p in points)
    max_y = max(p[1] for p in points)
    surf_width = max(1, max_x - min_x)
    surf_height = max(1, max_y - min_y)

    laser_surf = pygame.Surface((surf_width, surf_height), pygame.SRCALPHA)
    laser_points = [(x - min_x, y - min_y) for x, y in points]

    # --- Draw transparent polygon ---
    color = pygame.Color(constants.LASER_COLOR)
    color.a = 180  # transparency
    pygame.draw.polygon(laser_surf, color, laser_points)

    # --- Blit laser surface to screen ---
    screen.blit(laser_surf, (min_x, min_y))









def y_from_time(note_time, current_time):
    return constants.HIT_LINE_Y - (note_time - current_time) * constants.SCROLL_SPEED

def laser_x_from_norm(norm):
    screen_center = utils.scale_x(constants.BASE_W) // 2
    left_lane = screen_center - utils.scale_x(200)
    right_lane = screen_center + utils.scale_x(200)
    laser_width = utils.scale_x(50)
    half_laser_width = laser_width // 2
    return (left_lane + half_laser_width) + norm * ((right_lane - half_laser_width) - (left_lane + half_laser_width))

