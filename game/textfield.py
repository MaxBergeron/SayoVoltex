import pygame

class TextInputBox(pygame.sprite.Sprite):
    def __init__(self, x, y, w, font):
        super().__init__()
        self.color = (255, 255, 255)
        self.backcolor = None
        self.pos = (x, y) 
        self.width = w
        self.font = font
        self.active = False
        self.text = ""
        self.render_text()

    def render_text(self):
        t_surf = self.font.render(self.text, True, self.color, self.backcolor)
        self.image = pygame.Surface((max(self.width, t_surf.get_width()+10), t_surf.get_height()+10), pygame.SRCALPHA)
        if self.backcolor:
            self.image.fill(self.backcolor)
        self.image.blit(t_surf, (5, 5))
        pygame.draw.rect(self.image, self.color, self.image.get_rect().inflate(-2, -2), 2)
        self.rect = self.image.get_rect(midleft=self.pos)

    def update(self, event_list):

        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(event.pos):
                    self.active = True
                else:
                    self.active = False

            if event.type == pygame.KEYDOWN and self.active:
                if event.key == pygame.K_RETURN:
                    self.active = False
                elif event.key == pygame.K_BACKSPACE:
                    self.backspace_held = True
                    self.backspace_timer = 0  # reset timer
                elif event.key == pygame.K_v and (event.mod & pygame.KMOD_CTRL):
                    pasted = pygame.scrap.get(pygame.SCRAP_TEXT)
                    if pasted:
                        text = pasted.decode("utf-8", errors="ignore")
                        text = text.replace("\x00", "").strip()

                        self.text += text
                        self.render_text()
                else:
                    self.text += event.unicode
                    self.render_text()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_BACKSPACE:
                    self.backspace_held = False

        # Handle hold-backspace
        if getattr(self, "backspace_held", False):
            if not hasattr(self, "last_backspace_time"):
                self.last_backspace_time = pygame.time.get_ticks()
            current_time = pygame.time.get_ticks()
            if current_time - self.last_backspace_time >= 50:  # repeat every 100ms
                self.text = self.text[:-1]
                self.render_text()
                self.last_backspace_time = current_time