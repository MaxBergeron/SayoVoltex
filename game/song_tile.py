import pygame

class SongTile:
    def __init__(self, title, artist, creator, version, image_path, BPM, length_seconds, scroll_speed):
        self.title = title
        self.artist = artist
        self.creator = creator
        self.version = version
        self.image_path = image_path

        self.BPM = BPM
        self.length_seconds = length_seconds
        self.scroll_speed = scroll_speed

    def update(self, screen):
        if self.image_path is not None:
            image = pygame.image.load(self.image_path)
            screen.blit(image, (0, 0))
        # Add text rendering here if needed