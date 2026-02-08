import pygame, sys
from game import utils, constants

class Dropdown:
    def __init__(self, x, y, w, h, title, options, font_dropdown, font_popup, editable):
        self.rect = pygame.Rect(utils.scale_x(x), utils.scale_y(y), utils.scale_x(w), utils.scale_y(h))
        self.title = title
        self.options = options
        self.font_dropdown = font_dropdown
        self.font_popup = font_popup 
        self.open = False
        self.selected = None
        self.input_active = False
        self.user_input = ""
        self.key_being_edited = None
        self.old_value = ""
        self.editable = editable
        self.popup_mode = None

        # Colors
        self.base_color = (50, 50, 50)
        self.hover_color = (80, 80, 80)
        self.option_color = (60, 60, 60)
        self.option_hover_color = (100, 100, 100)
        self.text_color = (255, 255, 255)

    def handle_event(self, event, data, editor_grid=None):
        if self.input_active and event.type == pygame.KEYDOWN:
            if self.title == "Breakpoints" and not self.popup_mode == "add_breakpoint":
                if event.key == pygame.K_y:
                    data["value"].remove(self.key_being_edited)
                    self.input_active = False
                elif event.key == pygame.K_n or event.key == pygame.K_ESCAPE:
                    self.input_active = False
                elif event.key == pygame.K_RETURN:
                    if self.user_input.strip() != "":
                        data[self.key_being_edited] = self.user_input.strip()
                    self.input_active = False
                elif event.key == pygame.K_ESCAPE:
                    self.input_active = False
                elif event.key == pygame.K_BACKSPACE:
                    self.user_input = self.user_input[:-1]
                else:
                    self.user_input += event.unicode

            if self.popup_mode == "add_breakpoint":
                if event.key == pygame.K_RETURN:
                    if self.user_input.strip().isdigit():
                        new_bp = int(self.user_input.strip())
                        editor_grid.add_breakpoint(new_bp)
                    self.user_input = ""
                    self.input_active = False
                    self.popup_mode = None
                elif event.key == pygame.K_ESCAPE:
                    self.user_input = ""
                    self.input_active = False
                    self.popup_mode = None
                elif event.key == pygame.K_BACKSPACE:
                    self.user_input = self.user_input[:-1]
                else:
                    if event.unicode.isdigit():
                        self.user_input += event.unicode

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.open = not self.open
            elif self.open:
                for i, option in enumerate(self.options):
                    option_rect = pygame.Rect(
                        self.rect.x,
                        self.rect.y + (i + 1) * self.rect.height,
                        self.rect.width,
                        self.rect.height
                    )
                    if option_rect.collidepoint(event.pos):
                        self.selected = option
                        # Dont allow breakpoint 0 to be deleted
                        if self.title == "Breakpoints" and self.selected == self.options[0]:
                            return
                        self.open = False
                        if self.editable:
                            # Change song setup settings
                            if self.title == "Change Song Setup Settings":
                                self.key_being_edited = option
                                self.old_value = data.get(option, "")
                                self.user_input = self.old_value
                                self.input_active = True
                            # Breakpoints
                            else:
                                self.key_being_edited = option
                                self.input_active = True
                        # Note subdivision
                        else:
                             data["value"] = option
                             self.title = option

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()

        # Draw main dropdown box
        color = self.hover_color if self.rect.collidepoint(mouse_pos) else self.base_color
        pygame.draw.rect(screen, color, self.rect)
        text_surf = self.font_dropdown.render(str(self.title), True, self.text_color)
        screen.blit(text_surf, text_surf.get_rect(center=self.rect.center))

        # Draw dropdown options
        if self.open:
            for i, option in enumerate(self.options):
                option_rect = pygame.Rect(
                    self.rect.x,
                    self.rect.y + (i + 1) * self.rect.height,
                    self.rect.width,
                    self.rect.height
                )
                opt_color = self.option_hover_color if option_rect.collidepoint(mouse_pos) else self.option_color
                pygame.draw.rect(screen, opt_color, option_rect)
                opt_text = self.font_dropdown.render(str(option), True, self.text_color)
                screen.blit(opt_text, opt_text.get_rect(center=option_rect.center))
        if self.popup_mode == "add_breakpoint":
            screen_w, screen_h = screen.get_size()
            popup_w, popup_h = utils.scale_x(screen_w // 2), utils.scale_y(screen_h // 3)
            popup_x, popup_y = utils.scale_x((screen_w - screen_w // 2) // 2), utils.scale_y((screen_h - screen_h // 3) // 2)
            popup_rect = pygame.Rect(popup_x, popup_y, popup_w, popup_h)

            pygame.draw.rect(screen, (50, 50, 50), popup_rect)
            pygame.draw.rect(screen, (255, 255, 255), popup_rect, utils.scale_x(3))            
            prompt_text = self.font_popup.render(
                "Enter new breakpoint time (ms):",
                True, (255, 255, 255))
            input_text = self.font_popup.render(
                f"{self.user_input}",
                True, (200, 200, 0))
            confirm_text = self.font_popup.render(
                "Press ENTER to add, ESC to cancel",
                True, (180, 180, 180))
            screen.blit(prompt_text, (popup_x + utils.scale_x(20), popup_y + utils.scale_y(20)))
            screen.blit(input_text, (popup_x + utils.scale_x(20), popup_y + utils.scale_y(60)))
            screen.blit(confirm_text, (popup_x + utils.scale_x(20), popup_y + utils.scale_y(110)))

        # Draw popup if active
        if self.input_active and not self.popup_mode == "add_breakpoint":
            screen_w, screen_h = screen.get_size()
            popup_w, popup_h = utils.scale_x(screen_w // 2), utils.scale_y(screen_h // 3)
            popup_x, popup_y = utils.scale_x((screen_w - screen_w // 2) // 2), utils.scale_y((screen_h - screen_h // 3) // 2)
            popup_rect = pygame.Rect(popup_x, popup_y, popup_w, popup_h)

            # Draw popup background
            pygame.draw.rect(screen, (50, 50, 50), popup_rect)
            pygame.draw.rect(screen, (255, 255, 255), popup_rect, utils.scale_x(3))

            # Render popup text
            padding_x, padding_y = utils.scale_x(20), utils.scale_y(20)
            if self.title == "Change Song Setup Settings":
                prompt_text = self.font_popup.render(f"Enter new value for {self.key_being_edited}:", True, (255, 255, 255))
                old_text = self.font_popup.render(f"Old value: {self.old_value}", True, (180, 180, 180))
                input_text = self.font_popup.render(self.user_input, True, (200, 200, 0))

                screen.blit(prompt_text, (popup_x + padding_x, popup_y + padding_y))
                screen.blit(old_text, (popup_x + padding_x, popup_y + utils.scale_y(60)))
                screen.blit(input_text, (popup_x + padding_x, popup_y + utils.scale_y(100)))
            elif self.title == "Breakpoints":
                prompt_text = self.font_popup.render(
                    "Delete this breakpoint?", True, (255, 255, 255))
                old_text = self.font_popup.render(
                    f"Breakpoint time: {self.key_being_edited} ms",
                    True, (180, 180, 180))
                confirm_text = self.font_popup.render(
                    "Press Y to confirm, N to cancel",
                    True, (200, 200, 0))
                screen.blit(prompt_text, (popup_x + padding_x, popup_y + padding_y))
                screen.blit(old_text, (popup_x + padding_x, popup_y + utils.scale_y(60)))
                screen.blit(confirm_text, (popup_x + padding_x, popup_y + utils.scale_y(100)))


    def start_add_breakpoint_prompt(self):
        self.popup_mode = "add_breakpoint"
        self.input_active = True
        self.user_input = ""