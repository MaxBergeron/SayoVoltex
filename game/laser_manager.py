import pygame
from game.game_objects import LaserObject
from game import constants, utils

def draw_laser(screen, laser_object, current_time):
    start_x = laser_x_from_norm(laser_object.start_pos)
    end_x   = laser_x_from_norm(laser_object.end_pos)

    start_y = y_from_time(laser_object.start_time, current_time)
    end_y   = y_from_time(laser_object.end_time, current_time)

    w1 = utils.scale_x(50)
    w2 = utils.scale_y(50)

    points = [
        (start_x, start_y),
        (start_x + w1, start_y),
        (end_x, end_y),
        (end_x - w2, end_y),
    ]

    pygame.draw.polygon(screen, constants.LASER_COLOR, points)











def perspective(y):
    # Assume the screen’s bottom (HIT_LINE_Y) is “near” and top (0) is “far”
    return max(0.2, 1 - y / constants.BASE_H)

def y_from_time(note_time, current_time):
    return constants.HIT_LINE_Y - (note_time - current_time) * constants.SCROLL_SPEED

def laser_x_from_norm(norm):
    return constants.LEFT_LANE + norm * (constants.RIGHT_LANE - constants.LEFT_LANE)

