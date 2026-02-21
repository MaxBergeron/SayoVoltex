import pygame, os
from game import utils, constants

class SongTile:
    def __init__(self, song_folder_path, cover):

        self.cover = cover

        self.song_data_path = self.find_song_metadata(song_folder_path)

        parsed_metadata = self.parse_song_metadata(self.song_data_path)
        self.title = parsed_metadata.get("Title", "NULL")
        self.artist = parsed_metadata.get("Artist", "NULL")
        self.creator = parsed_metadata.get("Creator", "NULL")
        self.version = parsed_metadata.get("Version", "NULL") 
        self.length = int(parsed_metadata.get("Length") or 0)
        self.scroll_speed = float(parsed_metadata.get("Scroll Speed") or 0)
        self.BPM = int(parsed_metadata.get("BPM") or 0)
        self.audio_lead_in = int(parsed_metadata.get("Audio Lead In") or 0)
        default_image_path = "assets/images/default_texture.jpg"
        self.image_path = parsed_metadata.get("Image Path", default_image_path)
        self.audio_path = parsed_metadata.get("Audio Path", "NULL")

        self.image = pygame.image.load(self.image_path).convert_alpha()
        width, height = self.image.get_size()
        crop_rect = pygame.Rect(width//6, height//6, 2*width//3, 2*height//3)
        self.image = self.image.subsurface(crop_rect).copy()
        self.image = pygame.transform.scale(self.image, (utils.scale_x(150), utils.scale_y(75)))

        # Position and rect
        self.pos_x = 0
        self.pos_y = 0
        self.rect = pygame.Rect(self.pos_x, self.pos_y, utils.scale_x(300), utils.scale_y(75))



    def update(self, screen):
        screen.blit(self.image, (self.pos_x, self.pos_y))
        screen.blit(self.cover, (self.pos_x, self.pos_y))

    def check_for_input(self, position):
        return self.rect.collidepoint(position)
    
    @property
    def position(self):
        return self.pos_x, self.pos_y

    @position.setter
    def position(self, value):
        self.pos_x, self.pos_y = value
        self.rect.topleft = (self.pos_x, self.pos_y)
    
    def find_song_metadata(self, folder_path):
        for f in os.listdir(folder_path):
            full_path = os.path.join(folder_path, f)
            if os.path.isfile(full_path) and f.lower().endswith('.txt'):
                return full_path
        return None

    @staticmethod
    def parse_song_metadata(song_data_path):
        metadata = {}
        reading_metadata = False

        with open(song_data_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()

                # Skip empty lines or comments
                if not line or line.startswith("//"):
                    continue

                # Start reading after [Metadata] section
                if line == "[Metadata]":
                    reading_metadata = True
                    continue

                # Stop reading if another section starts
                if reading_metadata and line.startswith("[") and line.endswith("]"):
                    break

                # Only process key:value pairs while in [Metadata]
                if reading_metadata and ":" in line:
                    key, value = map(str.strip, line.split(":", 1))
                    metadata[key] = value

        return metadata