import pygame
from game import constants, utils
class Slider:
    def __init__(self, x, y, width, min_val, max_val, current_val, label):
        self.x = x
        self.y = y
        self.width = width
        self.height = utils.scale_y(10)

        self.min_val = min_val
        self.max_val = max_val
        self.value = current_val

        self.label = label
        self.font = utils.get_font(utils.scale_y(constants.SIZE_TINY))

        self.dragging = False

    def get_percentage(self):
        return (self.value - self.min_val) / (self.max_val - self.min_val)

    def update_from_mouse(self, mouse_x):
        mouse_x = max(self.x, min(mouse_x, self.x + self.width))
        percentage = (mouse_x - self.x) / self.width
        self.value = self.min_val + percentage * (self.max_val - self.min_val)

    def check_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.x <= event.pos[0] <= self.x + self.width and \
               self.y <= event.pos[1] <= self.y + self.height:
                self.dragging = True

        if event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False

        if event.type == pygame.MOUSEMOTION and self.dragging:
            self.update_from_mouse(event.pos[0])

    def draw(self, screen):
        # Background
        pygame.draw.rect(screen, (180, 180, 180), (self.x, self.y, self.width, self.height))

        # Fill
        fill_width = self.get_percentage() * self.width
        pygame.draw.rect(screen, (60, 60, 60), (self.x, self.y, fill_width, self.height))

        # Label text
        if self.max_val <= 1:  # volume
            display_val = f"{int(self.value * 100)}%"
        else:  # delay
            display_val = f"{int(self.value)} ms"

        text = self.font.render(f"{self.label}: {display_val}", True, (255,255,255))
        screen.blit(text, (self.x, self.y - utils.scale_y(40)))
