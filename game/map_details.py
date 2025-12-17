import pygame
from game import utils, constants

class MapDetails:
    def __init__(self):
        self.title = ""
        self.artist = ""
        self.creator = ""
        self.version = ""
        self.length = 0
        self.scroll_speed = 0.00
        self.BPM = 0

        self.image = pygame.image.load("assets/map_details_image.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (utils.scale_x(400), utils.scale_y(250)))

    def update(self, screen):
        screen.blit(self.image, (utils.scale_x(0), utils.scale_y(0)))

        font_tiny = utils.get_font(utils.scale_y(constants.SIZE_TINY))
        font_xtiny = utils.get_font(utils.scale_y(constants.SIZE_XTINY))
        details = [
            f"Title: {self.title}",
            f"Artist: {self.artist}",
            f"Creator: {self.creator}",
            f"Version: {self.version}",
            f"Length: {self.seconds_to_minutes_seconds(self.length)}",
            f"Scroll Speed: {self.scroll_speed}",
            f"BPM: {self.BPM}",
        ]

        title_text = font_tiny.render(details[0], True, "White")
        screen.blit(title_text, (utils.scale_x(3), utils.scale_y(10)))
        artist_text = font_xtiny.render(details[1], True, "White")
        screen.blit(artist_text, (utils.scale_x(5), utils.scale_y(50)))
        creator_text = font_xtiny.render(details[2], True, "White")
        screen.blit(creator_text, (utils.scale_x(5), utils.scale_y(90)))
        version_text = font_xtiny.render(details[3], True, "White")
        screen.blit(version_text, (utils.scale_x(5), utils.scale_y(130)))
        length_text = font_xtiny.render(details[4], True, "White")
        screen.blit(length_text, (utils.scale_x(5), utils.scale_y(170)))
        scroll_speed_text = font_xtiny.render(details[5], True, "White")
        screen.blit(scroll_speed_text, (utils.scale_x(150), utils.scale_y(170)))
        bpm_text = font_xtiny.render(details[6], True, "White")
        screen.blit(bpm_text, (utils.scale_x(5), utils.scale_y(210)))

    def seconds_to_minutes_seconds(self, total_seconds):
        minutes = int(total_seconds) // 60
        seconds = int(total_seconds) % 60
        return f"{minutes}:{seconds:02}"
                 