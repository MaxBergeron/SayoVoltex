import pygame, sys
from game import button, states, utils, constants
from game.textfield import TextInputBox


def editor_menu(screen):
    pygame.display.set_caption("Editor")

    clock = pygame.time.Clock()

    main_menu_background = pygame.image.load("assets/backgrounds/editor_background.jpg").convert()
    main_menu_background = pygame.transform.scale(main_menu_background, screen.get_size()).convert()

    menu_text = utils.get_font(utils.scale_y(constants.SIZE_LARGE)).render("EDITOR MENU", True, "#b68f40")
    menu_text_rect = menu_text.get_rect(center=(utils.scale_x(640), utils.scale_y(100)))

    song_parameters_set = False

    font_tiny = utils.get_font(utils.scale_y(constants.SIZE_TINY))
    font_xtiny = utils.get_font(utils.scale_y(constants.SIZE_XTINY))
    x = utils.scale_x(250)

    padding = utils.scale_x(12)

    text_box_1 = font_tiny.render("Title:", True, "#b68f40")
    text_box_rect_1 = text_box_1.get_rect(midleft=(x, utils.scale_y(160)))

    text_box_2 = font_tiny.render("Artist:", True, "#b68f40")
    text_box_rect_2 = text_box_2.get_rect(midleft=(x, utils.scale_y(200)))

    text_box_3 = font_tiny.render("Difficulty:", True, "#b68f40")
    text_box_rect_3 = text_box_3.get_rect(midleft=(x, utils.scale_y(240)))

    text_box_4 = font_tiny.render("Scroll Speed:", True, "#b68f40")
    text_box_rect_4 = text_box_4.get_rect(midleft=(x, utils.scale_y(280)))

    text_box_5 = font_tiny.render("BPM:", True, "#b68f40")
    text_box_rect_5 = text_box_5.get_rect(midleft=(x, utils.scale_y(320)))

    text_box_6 = font_tiny.render("Audio Lead In:", True, "#b68f40")
    text_box_rect_6 = text_box_6.get_rect(midleft=(x, utils.scale_y(360)))

    text_box_7 = font_tiny.render("Image File Path:", True, "#b68f40")
    text_box_rect_7 = text_box_7.get_rect(midleft=(x, utils.scale_y(400)))


    text_input_box_1 = TextInputBox(text_box_rect_1.right + padding, text_box_rect_1.centery, utils.scale_x(180), font_xtiny)
    text_input_box_2 = TextInputBox(text_box_rect_2.right + padding, text_box_rect_2.centery, utils.scale_x(180), font_xtiny)
    text_input_box_3 = TextInputBox(text_box_rect_3.right + padding, text_box_rect_3.centery, utils.scale_x(180), font_xtiny)
    text_input_box_4 = TextInputBox(text_box_rect_4.right + padding, text_box_rect_4.centery, utils.scale_x(180), font_xtiny)
    text_input_box_5 = TextInputBox(text_box_rect_5.right + padding, text_box_rect_5.centery, utils.scale_x(180), font_xtiny)
    text_input_box_6 = TextInputBox(text_box_rect_6.right + padding, text_box_rect_6.centery, utils.scale_x(180), font_xtiny)
    text_input_box_7 = TextInputBox(text_box_rect_7.right + padding, text_box_rect_7.centery, utils.scale_x(180), font_xtiny)

    popup_group = pygame.sprite.Group(text_input_box_1, text_input_box_2, text_input_box_3, text_input_box_4, text_input_box_5, text_input_box_6, text_input_box_7)


    submit_button = button.Button(image=None, pos=(utils.scale_x(925), utils.scale_y(540)), text_input="Submit",
                                  font=utils.get_font(utils.scale_y(constants.SIZE_SMALL)),
                                  base_color="#d7fcd4", hovering_color="White")

    while True:
        clock.tick(60)
        menu_mouse_pos = pygame.mouse.get_pos()

        event_list = pygame.event.get()
        for event in event_list:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.blit(main_menu_background, (0, 0))
 

        if not song_parameters_set:
            initial_settings_popup(screen, menu_mouse_pos, event_list, popup_group, submit_button)

        screen.blit(text_box_1, text_box_rect_1)
        screen.blit(text_box_2, text_box_rect_2)
        screen.blit(text_box_3, text_box_rect_3)
        screen.blit(text_box_4, text_box_rect_4)
        screen.blit(text_box_5, text_box_rect_5)
        screen.blit(text_box_6, text_box_rect_6)
        screen.blit(text_box_7, text_box_rect_7)

        pygame.display.flip()

def initial_settings_popup(screen, menu_mouse_pos, event_list, popup_group, submit_button):
    popup_width, popup_height = utils.scale_x(800), utils.scale_y(450)
    popup_x = (screen.get_width() - popup_width) // 2
    popup_y = (screen.get_height() - popup_height) // 2
    popup_rect = pygame.Rect(popup_x, popup_y, popup_width, popup_height)

    pygame.draw.rect(screen, (50, 50, 50), popup_rect)
    pygame.draw.rect(screen, (255, 255, 255), popup_rect, 2)

    popup_group.update(event_list)
    popup_group.draw(screen)

    submit_button.change_color(menu_mouse_pos)
    submit_button.update(screen)
