import pygame, sys
from game import button, settings, states, utils, constants





def main_menu(screen):
    pygame.display.set_caption("Menu")  
    main_menu_background = pygame.image.load("assets/backgrounds/start_screen_background.png")
    main_menu_background = pygame.transform.scale(main_menu_background, screen.get_size()).convert()

    sayovoltex_logo = pygame.image.load("assets/images/sayovoltex_logo.png").convert_alpha()
    sayovoltex_logo = pygame.transform.scale(sayovoltex_logo, (utils.scale_x(500), utils.scale_y(500)))

    play_button = button.Button(image=sayovoltex_logo, pos=(utils.scale_x(640), utils.scale_y(300)), 
                             text_input="", font=utils.get_font(utils.scale_y(constants.SIZE_MEDIUM_SMALL)), 
                             base_color="#d7fcd4", hovering_color="White")
    options_button = button.Button(image=None, pos=(utils.scale_x(640), utils.scale_y(650)), 
                                text_input="OPTIONS", font=utils.get_font(utils.scale_y(constants.SIZE_MEDIUM_SMALL)), 
                                base_color="#d7fcd4", hovering_color="White")
    quit_button = button.Button(image=None, pos=(utils.scale_x(1130), utils.scale_y(650)), 
                             text_input="QUIT", font=utils.get_font(utils.scale_y(constants.SIZE_MEDIUM_SMALL)),
                             base_color="#d7fcd4", hovering_color="White")
    editor_button = button.Button(image=None, pos=(utils.scale_x(150), utils.scale_y(650)), 
                             text_input="EDITOR", font=utils.get_font(utils.scale_y(constants.SIZE_MEDIUM_SMALL)),
                             base_color="#d7fcd4", hovering_color="White")
    information_button = button.Button(image=None, pos=(utils.scale_x(1250), utils.scale_y(30)), 
                             text_input="?", font=utils.get_font(utils.scale_y(constants.SIZE_MEDIUM_SMALL)),
                             base_color="#d7fcd4", hovering_color="White")
    

    # Load image assets for later
    utils.load_assets()
    game_settings = settings.load_settings()
    showed_intructions_on_launch = False
   
    
    while True:
        screen.blit(main_menu_background, (0, 0))

        menu_mouse_pos = pygame.mouse.get_pos()

        
        for b in [play_button, options_button, quit_button, editor_button, information_button]:
            b.change_color(menu_mouse_pos)
            b.update(screen)

        if game_settings["show_instructions_on_launch"] and not showed_intructions_on_launch:
            showed_intructions_on_launch = True
            background_copy = screen.copy()
            setup_instructions(screen, menu_mouse_pos, background_copy, game_settings)

        # Handle Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if play_button.check_for_input(menu_mouse_pos):
                    return states.PLAY
                elif options_button.check_for_input(menu_mouse_pos):
                    return states.OPTIONS
                elif quit_button.check_for_input(menu_mouse_pos):
                    return states.QUIT
                elif editor_button.check_for_input(menu_mouse_pos):
                    return states.EDITOR_INITIALIZE
                elif information_button.check_for_input(menu_mouse_pos):
                    background_copy = screen.copy()
                    setup_instructions(screen, menu_mouse_pos, background_copy, game_settings)
                    game_settings = settings.load_settings()
        pygame.display.flip()

def setup_instructions(screen, menu_mouse_pos, background_copy, game_settings):
    current_slide = 1

    go_left_button = button.Button(
        image=None,
        pos=(screen.get_width() // 2 - utils.scale_x(150), 
            screen.get_height() // 2 + utils.scale_y(200)),
        text_input="<",
        font=utils.get_font(utils.scale_y(constants.SIZE_MEDIUM_SMALL)),
        base_color="White",
        hovering_color="#b68f40"
    )
    go_right_button = button.Button(
        image=None,
        pos=(screen.get_width() // 2 + utils.scale_x(150), 
            screen.get_height() // 2 + utils.scale_y(200)),
        text_input=">",
        font=utils.get_font(utils.scale_y(constants.SIZE_MEDIUM_SMALL)),
        base_color="White",
        hovering_color="#b68f40"
    )

    exit_button = button.Button(
        image=None,
        pos=(screen.get_width() // 2, 
            screen.get_height() // 2 + utils.scale_y(200)),
        text_input="×",
        font=utils.get_font(utils.scale_y(constants.SIZE_SMALL)),
        base_color="White",
        hovering_color="#b68f40"
    )

    empty_checkbox_image = pygame.image.load("assets/images/empty_box.png").convert_alpha() 
    empty_checkbox_image = pygame.transform.scale(empty_checkbox_image, (utils.scale_x(25), utils.scale_y(25)))
    filled_checkbox_image = pygame.image.load("assets/images/checked_box.png").convert_alpha() 
    filled_checkbox_image = pygame.transform.scale(filled_checkbox_image, (utils.scale_x(25), utils.scale_y(25)))

    dont_show_on_launch_button = button.Button(
        image=empty_checkbox_image if game_settings["show_instructions_on_launch"] else filled_checkbox_image,
        pos=(screen.get_width() // 2 + utils.scale_x(400), 
            screen.get_height() // 2 + utils.scale_y(100)),
        text_input="",
        font=utils.get_font(utils.scale_y(constants.SIZE_SMALL)),
        base_color="White",
        hovering_color="#b68f40"
    )

    clock = pygame.time.Clock()
    waiting = True

    pygame.event.clear()

    while waiting:
        clock.tick(60)
        menu_mouse_pos = pygame.mouse.get_pos()

        screen.blit(background_copy, (0, 0))

        # Dark overlay (dim background)
        overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))

        # Draw error box
        box_rect = display_setup_instructions(screen, current_slide, go_left_button)

        button_y = box_rect.bottom - utils.scale_y(35)

        go_left_button.set_position((
            box_rect.centerx - utils.scale_x(120),
            button_y
        ))

        go_right_button.set_position((
            box_rect.centerx + utils.scale_x(120),
            button_y
        ))

        exit_button.set_position((
            box_rect.right - utils.scale_x(25),
            box_rect.top + utils.scale_y(25)
        ))

        for b in [go_left_button, go_right_button, exit_button]:
            b.change_color(menu_mouse_pos)
            b.update(screen)
        
        if current_slide == 1:
            checkbox_label_font = utils.get_font(utils.scale_y(constants.SIZE_XTINY))
            label_text = "Turn off open on launch"
            label_surface = checkbox_label_font.render(label_text, True, (255, 255, 255))
            label_rect = label_surface.get_rect(midright=(dont_show_on_launch_button.rect.left - utils.scale_x(10), dont_show_on_launch_button.rect.centery))
            screen.blit(label_surface, label_rect)
            dont_show_on_launch_button.change_color(menu_mouse_pos)
            dont_show_on_launch_button.update(screen)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if go_left_button.check_for_input(menu_mouse_pos):
                    current_slide = max(current_slide - 1, 1)                     
                if go_right_button.check_for_input(menu_mouse_pos):
                    current_slide = min(current_slide + 1, 4)
                if exit_button.check_for_input(menu_mouse_pos):
                    settings.save_settings(game_settings)
                    waiting = False
                if dont_show_on_launch_button.check_for_input(menu_mouse_pos):
                    if game_settings["show_instructions_on_launch"]:
                        dont_show_on_launch_button.change_image(filled_checkbox_image)
                        game_settings["show_instructions_on_launch"] = False
                    else:
                        dont_show_on_launch_button.change_image(empty_checkbox_image)
                        game_settings["show_instructions_on_launch"] = True
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_ESCAPE, pygame.K_RETURN):
                    settings.save_settings(game_settings)
                    waiting = False


def display_setup_instructions(screen, current_slide, go_left_button):
    title_font = utils.get_font(utils.scale_y(constants.SIZE_SMALL))
    body_font = utils.get_font(utils.scale_y(constants.SIZE_XTINY))

    button_height = go_left_button.rect.height
    padding = utils.scale_x(20)
    spacing = utils.scale_x(10)
    border_thickness = utils.scale_x(3)
    line_spacing = utils.scale_x(5)
    screen_w = screen.get_width()
    max_text_width = screen_w // 2
    title_surf = None

    if current_slide == 1:
        title_surf = title_font.render("How To Setup Your Sayodevice", True, (255, 255, 255))
        message = "Use the arrows to traverse through the 2 easy steps in order to set up your sayodevice in order to play SayoVoltex"
    elif current_slide == 2:
        title_surf = title_font.render("Step 1:", True, (255, 255, 255))
        message = "Visit sayodevice.com and if your device is not already added click “Add device” and select your sayodevice and then click on “Connect”. If you don’t want to lose your scroll button mapping select “Backup” under “Backup & Restore”."
    elif current_slide == 3:
        title_surf = title_font.render("Step 2:", True, (255, 255, 255))
        message = "Under Configuration -> Binding you will say a layout for your sayodevice, click on the large half circle on the left. Under “Key Mode” choose “Loop Key”, under “Key” choose any key not already set on your sayodevice (I would suggest w), and under “Input Interval” set it to “1”. Do the same thing for the half circle on the right but choose a different key (I would suggest q)."        
    else:
        title_surf = title_font.render("Thats It", True, (255, 255, 255))
        message = "Lastly go to options in SayoVoltex and configure your settings and you’ll be ready to play."
    center_x, center_y = utils.scale_pos(constants.BASE_W // 2, constants.BASE_H // 2)

    # Render title
    
    # Wrap message text
    lines = utils.wrap_text(message, body_font, max_text_width)
    text_surfs = [body_font.render(line, True, (255, 255, 255)) for line in lines]
    # Calculate box size
    text_width = max(surf.get_width() for surf in text_surfs)
    text_height = sum(surf.get_height() for surf in text_surfs) + line_spacing * (len(text_surfs) - 1)
    box_width = max(title_surf.get_width(), text_width) + padding * 2
    box_height = (title_surf.get_height() + spacing + text_height + button_height + padding * 2)
    box_rect = pygame.Rect(0, 0, box_width, box_height)
    box_rect.center = (center_x, center_y)
    # Draw box
    pygame.draw.rect(screen, (125, 150, 160), box_rect)
    pygame.draw.rect(screen, (255, 255, 255), box_rect, border_thickness)
    # Draw title
    title_rect = title_surf.get_rect(
        midtop=(box_rect.centerx, box_rect.top + padding)
    )
    screen.blit(title_surf, title_rect)
    # Draw wrapped text
    y = title_rect.bottom + spacing
    for surf in text_surfs:
        rect = surf.get_rect(midtop=(box_rect.centerx, y))
        screen.blit(surf, rect)
        y += surf.get_height() + line_spacing

    return box_rect