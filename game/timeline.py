import pygame
from game import constants, utils

class Timeline:
    def __init__(self, ms):
        self.width = utils.scale_x(1280)  
        self.height = utils.scale_y(10)  
        self.x = 0
        self.y = utils.scale_y(690)

        self.font = pygame.font.SysFont("Arial", int(constants.SIZE_TINY))
        self.light_gray_color = (200, 200, 200) # light gray background
        self.dark_gray_color = (40, 40, 40)
        self.text_color = (255, 255, 255)  # white text

        self.timeline_cursor = pygame.image.load("assets/images/timeline_cursor.png").convert_alpha()
        self.timeline_cursor = pygame.transform.scale(self.timeline_cursor, (utils.scale_x(16), utils.scale_y(16)))
        self.tlc_x = self.x + 10
        self.tlc_y = self.y

        self.total_time = ms
        self.time = 0
        self.time_text = "Time: 0"

    def update(self, time_line_x_clicked):
        self.tlc_x = time_line_x_clicked
        print(self.total_time)
        self.time = self.total_time * (time_line_x_clicked / constants.BASE_W)
        self.time_text = f"{utils.ms_to_min_sec_ms(self.time)}"

    def check_for_input(self, mouse_pos):
        mouse_x, mouse_y = mouse_pos
        return ((self.x <= mouse_x <= self.x + self.width) and (self.y <= mouse_y <= self.y + self.height), mouse_x)
    
    def draw(self, screen):
        pygame.draw.rect(screen, self.light_gray_color, (self.x, self.y, self.width, self.height))
        if self.time != 0:
            pygame.draw.rect(screen, self.dark_gray_color, (self.x, self.y, self.get_progress_width(), self.height))


        text_surface = self.font.render(self.time_text, True, self.text_color)
        screen.blit(text_surface, (self.x + utils.scale_x(10), self.y - utils.scale_y(20) + (self.height - text_surface.get_height())))

        rect = self.timeline_cursor.get_rect(center=(self.tlc_x, self.tlc_y + utils.scale_y(5)))
        screen.blit(self.timeline_cursor, rect)

    def get_progress_width(self):
        percentage_time = self.time / self.total_time
        width = percentage_time * utils.scale_x(constants.BASE_W)
        return width