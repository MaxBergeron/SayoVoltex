import pygame, sys
from game import button, states, utils



def set_keybinds_menu(screen):
    pygame.display.set_caption("Set Keybinds")
    set_keybinds_background = pygame.image.load("assets/set_keybinds_background.png")
    set_keybinds_background = pygame.transform.scale(set_keybinds_background, screen.get_size()).convert()
    sayodevice_template_image = pygame.image.load("assets/template_sayodevice.png").convert_alpha()
    sayodevice_template_image = pygame.transform.scale(sayodevice_template_image, (500, 400))

    button_image = pygame.image.load("assets/clear_box.png").convert_alpha()
    button_image = pygame.transform.scale(button_image, (250, 75))
                                                     
    while True:
        
        screen.blit(set_keybinds_background, (0, 0))
        screen.blit(sayodevice_template_image, (750, 150))

        options_mouse_pos = pygame.mouse.get_pos()

        options_text = utils.get_font(150).render("SET KEYBINDS", True, "#b68f40")
        options_text_rect = options_text.get_rect(center=(640, 100))
        
        back_button = button.Button(image=None, pos=(640, 400), 
                             text_input="Back", font=utils.get_font(75), 
                             base_color="#d7fcd4", hovering_color="White")
        set_key1_button = button.Button(image=button_image, pos=(400, 300), 
                             text_input="", font=utils.get_font(50), 
                             base_color="#d7fcd4", hovering_color="White")

        screen.blit(options_text, options_text_rect)

        for b in [set_key1_button, back_button]:
            b.change_color(options_mouse_pos)
            b.update(screen)



        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.check_for_input(options_mouse_pos):
                    return states.MENU
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return states.MENU

        pygame.display.flip()
