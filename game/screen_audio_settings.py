import pygame, sys
from game import button, constants, states, utils, settings, slider

def audio_settings_menu(screen):
    pygame.display.set_caption("Audio Settings")

    background = pygame.image.load("assets/backgrounds/set_resolution_background.png")
    background = pygame.transform.scale(background, screen.get_size()).convert()

    game_settings = settings.load_settings()

    # Load saved values or defaults
    music_vol = game_settings.get("music_volume", 1.0)
    hit_vol = game_settings.get("hit_volume", 0.8)
    audio_delay = game_settings.get("audio_delay", 0)

    # Create sliders
    music_slider = slider.Slider(
        utils.scale_x(300),
        utils.scale_y(200),
        utils.scale_x(600),
        0.0, 1.0,
        music_vol,
        "Music Volume"
    )

    hit_slider = slider.Slider(
        utils.scale_x(300),
        utils.scale_y(350),
        utils.scale_x(600),
        0.0, 1.0,
        hit_vol,
        "Hit Sound Volume"
    )

    delay_slider = slider.Slider(
        utils.scale_x(300),
        utils.scale_y(500),
        utils.scale_x(600),
        -200, 200,
        audio_delay,
        "Audio Delay"
    )

    back_button = button.Button(
        image=None,
        pos=(utils.scale_x(150), utils.scale_y(650)),
        text_input="Back",
        font=utils.get_font(utils.scale_y(constants.SIZE_MEDIUM_SMALL)),
        base_color="#d7fcd4",
        hovering_color="White"
    )

    while True:
        screen.blit(background, (0,0))
        mouse_pos = pygame.mouse.get_pos()

        music_slider.draw(screen)
        hit_slider.draw(screen)
        delay_slider.draw(screen)

        back_button.change_color(mouse_pos)
        back_button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            music_slider.check_event(event)
            hit_slider.check_event(event)
            delay_slider.check_event(event)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return states.OPTIONS
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if back_button.check_for_input(mouse_pos):

                    # Save settings
                    game_settings["music_volume"] = music_slider.value
                    game_settings["hit_volume"] = hit_slider.value
                    game_settings["audio_delay"] = int(delay_slider.value)

                    settings.save_settings(game_settings)

                    return states.OPTIONS

        pygame.display.flip()
