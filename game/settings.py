import json, os, pygame

SETTINGS_FILE = "game/settings.json"

# Default settings (used if file doesn't exist)
DEFAULT_SETTINGS = {
    "music_volume": 1.0,
    "sfx_volume": 0.8,
    "audio_delay": 0,
    "scroll_speed": 1.0,
    "resolution": [1280, 720],
    "fullscreen": False,
    "key_1": pygame.K_z,
    "key_2": pygame.K_x,
    "key_3": pygame.K_c,
    "key_CCW": pygame.K_q,    
    "key_CW": pygame.K_w,
    "show_instructions_on_launch": True,
}


def load_settings():
    """Load settings from file or return defaults."""
    if not os.path.exists(SETTINGS_FILE):
        return DEFAULT_SETTINGS.copy()

    with open(SETTINGS_FILE, "r") as f:
        return json.load(f)


def save_settings(settings):
    """Save settings dictionary to file."""
    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f, indent=4)