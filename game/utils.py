import pygame
from game import constants
from pathlib import Path
import os

from game.game_objects import HitObject, LaserObject



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
    
    constants.ACCURACY_POPUPS = {
        "perfect": pygame.transform.scale(
            pygame.image.load("assets/images/perfect_popup.png").convert_alpha(),
            (int(constants.SCALE_X * 200), int(constants.SCALE_Y * 100))
        ),
        "good": pygame.transform.scale(
            pygame.image.load("assets/images/good_popup.png").convert_alpha(),
            (int(constants.SCALE_X * 200), int(constants.SCALE_Y * 100))
        ),
        "ok": pygame.transform.scale(
            pygame.image.load("assets/images/ok_popup.png").convert_alpha(),
            (int(constants.SCALE_X * 200), int(constants.SCALE_Y * 100))
        ),
        "miss": pygame.transform.scale(
            pygame.image.load("assets/images/miss_popup.png").convert_alpha(),
            (int(constants.SCALE_X * 200), int(constants.SCALE_Y * 100))
        ),
    }
    

def tint(surface, color):
    s = surface.copy()
    s.fill(color, special_flags=pygame.BLEND_RGBA_MULT)
    return s


def convert_int_to_key(key_int):
    key_map = {
        1: "key_1",
        2: "key_2",
        3: "key_3"
    }
    return key_map.get(key_int, None)

def get_action_from_key(key):
    for action, mapped_key in key_bindings.items():
        if key == mapped_key:
            return action
    return None

def after_second_to_last_slash(path: str) -> str:
    parts = Path(path).as_posix().split("/")
    return "/".join(parts[-2:])

def shorten_text(text: str, max_length: int = 40) -> str:
    if len(text) <= max_length:
        return text
    return text[:max_length - 3] + "..."


def parse_song_file(path):
    metadata = {}
    data = {
        "HitObjects": [],
        "LaserObjects": []
    }

    current_section = None

    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()

            # Skip empty lines or comments
            if not line or line.startswith("//"):
                continue

            # Section headers
            if line.startswith("[") and line.endswith("]"):
                section = line[1:-1]

                if section == "Metadata":
                    current_section = "Metadata"
                elif section == "HitObjects":
                    current_section = "HitObjects"
                elif section == "LaserObjects":
                    current_section = "LaserObjects"
                else:
                    current_section = None

                continue

            # METADATA 
            if current_section == "Metadata" and ":" in line:
                key, value = map(str.strip, line.split(":", 1))
                metadata[key] = value
                if key == "Scroll Speed":
                    constants.SCROLL_SPEED = float(value)
                continue

            # OBJECT DATA
            if current_section in ("HitObjects", "LaserObjects") and "," in line:
                parts = [p.strip() for p in line.split(",")]

                if current_section == "HitObjects":
                    data["HitObjects"].append(HitObject(*parts))

                elif current_section == "LaserObjects":
                    data["LaserObjects"].append(LaserObject(*parts))

    return metadata, data

def find_map_file(song_folder):
    if not song_folder == "":
        for file in os.listdir(song_folder):
            if file.endswith(".txt"):
                return os.path.join(song_folder, file)
    else:
        return None 
    
def wrap_text(text, font, max_width):
    words = text.split(" ")
    lines = []
    current_line = ""

    for word in words:
        test_line = current_line + (" " if current_line else "") + word
        if font.size(test_line)[0] <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word

    if current_line:
        lines.append(current_line)

    return lines

def seconds_to_minutes_seconds(total_seconds):
    minutes = int(total_seconds) // 60
    seconds = int(total_seconds) % 60
    return f"{minutes}:{seconds:02}"

def ms_to_min_sec_ms(total_ms):
    minutes = int(total_ms) // 60000
    seconds = (int(total_ms) % 60000) // 1000
    ms = int(total_ms) % 1000
    return f"{minutes}:{seconds:02}:{ms:02}"