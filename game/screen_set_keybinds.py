import pygame, sys
from game import button, constants, states, utils, settings



def set_keybinds_menu(screen):
    pygame.display.set_caption("Set Keybinds")
    set_keybinds_background = pygame.image.load("assets/backgrounds/options_background.png")
    set_keybinds_background = pygame.transform.scale(set_keybinds_background, screen.get_size()).convert()
    sayodevice_template_image = pygame.image.load("assets/images/template_sayodevice.png").convert_alpha()
    sayodevice_template_image = pygame.transform.scale(sayodevice_template_image, (utils.scale_x(500), utils.scale_y(500)))

    set_key_button_image = pygame.image.load("assets/images/clear_box.png").convert_alpha()
    set_key_button_image = pygame.transform.scale(set_key_button_image, (utils.scale_x(138), utils.scale_y(113)))
    #set_key_button_image.set_alpha(200)

    set_wheel_button_image = pygame.image.load("assets/images/clear_box.png").convert_alpha()
    set_wheel_button_image = pygame.transform.scale(set_wheel_button_image, (utils.scale_x(80), utils.scale_y(126)))
    #set_wheel_button_image.set_alpha(200)

    set_keybinds_text = utils.get_font(utils.scale_y(constants.SIZE_LARGE)).render("SET KEYBINDS", True, "#b68f40")
    set_keybinds_text_rect = set_keybinds_text.get_rect(center=(utils.scale_x(640), utils.scale_y(100)))

    back_button = button.Button(image=None, pos=(utils.scale_x(150), utils.scale_y(650)), 
                             text_input="Back", font=utils.get_font(utils.scale_y(constants.SIZE_MEDIUM_SMALL)), 
                             base_color="#d7fcd4", hovering_color="White")
    set_key1_button = button.Button(image=set_key_button_image, pos=(utils.scale_x(495), utils.scale_y(572)), 
                             text_input="", font=utils.get_font(utils.scale_y(constants.SIZE_MEDIUM_SMALL)), 
                             base_color="#d7fcd4", hovering_color="White")
    set_key2_button = button.Button(image=set_key_button_image, pos=(utils.scale_x(654), utils.scale_y(571)), 
                             text_input="", font=utils.get_font(utils.scale_y(constants.SIZE_MEDIUM_SMALL)), 
                             base_color="#d7fcd4", hovering_color="White")
    set_key3_button = button.Button(image=set_key_button_image, pos=(utils.scale_x(809), utils.scale_y(570)), 
                             text_input="", font=utils.get_font(utils.scale_y(constants.SIZE_MEDIUM_SMALL)), 
                             base_color="#d7fcd4", hovering_color="White")
    set_keyCCW_button = button.Button(image=set_wheel_button_image, pos=(utils.scale_x(441), utils.scale_y(420)),
                                text_input="", font=utils.get_font(utils.scale_y(constants.SIZE_MEDIUM_SMALL)), 
                                base_color="#d7fcd4", hovering_color="White")
    set_keyCW_button = button.Button(image=set_wheel_button_image, pos=(utils.scale_x(525), utils.scale_y(420)),
                                text_input="", font=utils.get_font(utils.scale_y(constants.SIZE_MEDIUM_SMALL)), 
                                base_color="#d7fcd4", hovering_color="White")
    
    apply_button = button.Button(image=None, pos=(utils.scale_x(1130), utils.scale_y(650)),
                                text_input="Apply", font=utils.get_font(utils.scale_y(constants.SIZE_MEDIUM_SMALL)),
                                base_color="#d7fcd4", hovering_color="White")

    waiting_for_key = False
    key_to_bind = None
    game_settings = settings.load_settings()

                                                     
    while True:
        
        screen.blit(set_keybinds_background, (0, 0))
        screen.blit(sayodevice_template_image, (utils.scale_x(400), utils.scale_y(200)))

        set_keybinds_mouse_pos = pygame.mouse.get_pos()

        screen.blit(set_keybinds_text, set_keybinds_text_rect)

        for b in [set_key1_button, set_key2_button, set_key3_button, set_keyCCW_button, set_keyCW_button, back_button, apply_button]:
            b.change_color(set_keybinds_mouse_pos)
            b.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if not waiting_for_key:
                    if back_button.check_for_input(set_keybinds_mouse_pos):
                        return states.MENU
                    if apply_button.check_for_input(set_keybinds_mouse_pos):
                        settings.save_settings(game_settings)
                    if set_key1_button.check_for_input(set_keybinds_mouse_pos):
                        waiting_for_key = True
                        key_to_bind = "key_1"
                    if set_key2_button.check_for_input(set_keybinds_mouse_pos):
                        waiting_for_key = True
                        key_to_bind = "key_2"
                    if set_key3_button.check_for_input(set_keybinds_mouse_pos):
                        waiting_for_key = True
                        key_to_bind = "key_3"
                    if set_keyCCW_button.check_for_input(set_keybinds_mouse_pos):
                        waiting_for_key = True
                        key_to_bind = "key_CCW"
                    if set_keyCW_button.check_for_input(set_keybinds_mouse_pos):
                        waiting_for_key = True
                        key_to_bind = "key_CW"

            if event.type == pygame.KEYDOWN:
                if waiting_for_key:
                    if event.key == pygame.K_ESCAPE:
                        waiting_for_key = False  
                    else:
                        game_settings[key_to_bind] = event.key
                        waiting_for_key = False
                else:
                    if event.key == pygame.K_ESCAPE:
                        return states.OPTIONS
        if waiting_for_key:
            draw_bind_key_popup(screen)
        pygame.display.flip()

def draw_bind_key_popup(screen):
    popup_width, popup_height = utils.scale_x(600), utils.scale_y(250)
    popup_x = (screen.get_width() - popup_width) // 2
    popup_y = (screen.get_height() - popup_height) // 2
    popup_rect = pygame.Rect(popup_x, popup_y, popup_width, popup_height)
    pygame.draw.rect(screen, (50, 50, 50), popup_rect)
    pygame.draw.rect(screen, (255, 255, 255), popup_rect, 2)

    prompt_text = utils.get_font(constants.SIZE_TINY).render("Press a key to bind, or ESC to cancel", True, (255, 255, 255))
    prompt_rect = prompt_text.get_rect(center=popup_rect.center)
    screen.blit(prompt_text, prompt_rect)