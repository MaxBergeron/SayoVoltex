import pygame
from game import constants


key_bindings = {
    "key_1": pygame.K_z,
    "key_2": pygame.K_x,
    "key_3": pygame.K_c,
    "key_CCW": pygame.K_q,    
    "key_CW": pygame.K_w,
}

def set_keybinding(action, key):
    key_bindings[action] = key

def get_font(size): 
    return pygame.font.Font("assets/font/font.ttf", int(size))

def scale_x(num):
    return int(num * constants.SCALE_X)
def scale_y(num):
    return int(num * constants.SCALE_Y)
def scale_pos(x, y):
    return int(x * constants.SCALE_X), int(y * constants.SCALE_Y)
def scale_size(width, height):
    return int(width * constants.SCALE_X), int(height * constants.SCALE_Y)

def load_assets():
    NOTE_W = scale_x(100)
    NOTE_H = scale_y(10)

    constants.TAP_NOTE_IMAGE = pygame.transform.scale(
        pygame.image.load("assets/skin/hit_note.png").convert_alpha(),
        (NOTE_W, NOTE_H)
    )

    constants.HOLD_NOTE_HEAD_IMAGE = pygame.transform.scale(
        pygame.image.load("assets/skin/hold_note_head.png").convert_alpha(),
        (NOTE_W, NOTE_H)
    )

    constants.HOLD_NOTE_BODY_IMAGE = pygame.transform.scale(
        pygame.image.load("assets/skin/hold_note_body.png").convert_alpha(),
        (NOTE_W, NOTE_H)
    )

    constants.HOLD_NOTE_TAIL_IMAGE = pygame.transform.scale(
        pygame.image.load("assets/skin/hold_note_tail.png").convert_alpha(),
        (NOTE_W, NOTE_H)
    )
    constants.HOLD_NOTE_HEAD_IMAGE_TINTED = tint(constants.HOLD_NOTE_HEAD_IMAGE, (0, 200, 255))
    constants.HOLD_NOTE_BODY_IMAGE_TINTED = tint(constants.HOLD_NOTE_BODY_IMAGE, (0, 200, 255))
    constants.HOLD_NOTE_TAIL_IMAGE_TINTED = tint(constants.HOLD_NOTE_TAIL_IMAGE, (0, 200, 255))

def tint(surface, color):
    s = surface.copy()
    s.fill(color, special_flags=pygame.BLEND_RGBA_MULT)
    return s


def convert_int_to_key(key_int):
    key_map = {
        1: "key_1",
        2: "key_2",
        3: "key_3",
        4: "key_CCW",
        5: "key_CW"
    }
    return key_map.get(key_int, None)

def get_action_from_key(key):
    for action, mapped_key in key_bindings.items():
        if key == mapped_key:
            return action
    return None