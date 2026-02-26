from game import constants, utils, button, states
import pygame, sys

def map_complete_menu(screen, counters):

    clock = pygame.time.Clock()

    map_complete_background = pygame.image.load(constants.SELECTED_TILE.image_path)
    map_complete_background = pygame.transform.scale(map_complete_background, screen.get_size()).convert()

    dark_factor = constants.DARK_PERCENTAGE
    dark_map_complete_background = map_complete_background.copy()
    dark_map_complete_background.fill((dark_factor * 255, dark_factor * 255, dark_factor * 255), special_flags=pygame.BLEND_MULT)

    # Extract counters
    point_counter = counters["point_counter"]
    percentage_counter = counters["percentage_counter"]
    combo_counter = counters["combo_counter"]

    # Fonts
    title_font = utils.get_font(utils.scale_y(constants.SIZE_MEDIUM_SMALL))
    stat_font = utils.get_font(utils.scale_y(constants.SIZE_SMALL))
    small_font = utils.get_font(utils.scale_y(constants.SIZE_TINY))

    # Buttons
    continue_button = button.Button(
        image=None,
        pos=(utils.scale_x(1120), utils.scale_y(670)),
        text_input="Continue",
        font=stat_font,
        base_color="#d7fcd4",
        hovering_color="White"
    )

    retry_button = button.Button(
        image=None,
        pos=(utils.scale_x(640), utils.scale_y(670)),
        text_input="Retry",
        font=stat_font,
        base_color="#d7fcd4",
        hovering_color="White"
    )

    exit_button = button.Button(
        image=None,
        pos=(utils.scale_x(100), utils.scale_y(670)),
        text_input="Exit",
        font=stat_font,
        base_color="#d7fcd4",
        hovering_color="White"
    )

    while True:
        clock.tick(60)
        mouse_pos = pygame.mouse.get_pos()

        # Background
        screen.blit(dark_map_complete_background, (0,0))

        # Title
        title_text = title_font.render("MAP COMPLETE!", True, (255, 255, 255))
        screen.blit(title_text, title_text.get_rect(center=(utils.scale_x(640), utils.scale_y(50))))

        # Score
        score_text = stat_font.render(
            f"Score: {point_counter.value}",
            True,
            (255, 255, 255)
        )
        screen.blit(score_text, score_text.get_rect(center=(utils.scale_x(640), utils.scale_y(200))))

        # Accuracy
        acc_text = stat_font.render(
            f"Accuracy: {percentage_counter.value:.1f}%",
            True,
            (255, 255, 255)
        )
        screen.blit(acc_text, acc_text.get_rect(center=(utils.scale_x(640), utils.scale_y(260))))

        # Max Combo
        combo_text = stat_font.render(
            f"Max Combo: {combo_counter.highest_combo}",
            True,
            (255, 255, 255)
        )
        screen.blit(combo_text, combo_text.get_rect(center=(utils.scale_x(640), utils.scale_y(320))))

        # Breakdown
        breakdown_title = small_font.render("Hit Breakdown:", True, (200, 200, 200))
        screen.blit(breakdown_title, breakdown_title.get_rect(center=(utils.scale_x(640), utils.scale_y(400))))

        perfect_text = small_font.render(
            f"Perfect: {percentage_counter.perfect_hits}",
            True,
            (255, 255, 255)
        )
        good_text = small_font.render(
            f"Good: {percentage_counter.good_hits}",
            True,
            (255, 255, 255)
        )
        ok_text = small_font.render(
            f"Ok: {percentage_counter.ok_hits}",
            True,
            (255, 255, 255)
        )
        miss_text = small_font.render(
            f"Miss: {percentage_counter.miss_hits}",
            True,
            (255, 255, 255)
        )
        screen.blit(perfect_text, perfect_text.get_rect(center=(utils.scale_x(640), utils.scale_y(440))))
        screen.blit(good_text, good_text.get_rect(center=(utils.scale_x(640), utils.scale_y(480))))
        screen.blit(ok_text, ok_text.get_rect(center=(utils.scale_x(640), utils.scale_y(520))))
        screen.blit(miss_text, miss_text.get_rect(center=(utils.scale_x(640), utils.scale_y(560))))

        # Buttons
        for b in [continue_button, retry_button, exit_button]:
            b.change_color(mouse_pos)
            b.update(screen)

        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

                if continue_button.check_for_input(mouse_pos):
                    return states.PLAY   # go to song select or next screen

                if retry_button.check_for_input(mouse_pos):
                    return states.MAP    # restart map

                if exit_button.check_for_input(mouse_pos):
                    return states.PLAY   # back to menu
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return states.PLAY
                if event.key == pygame.K_RETURN:
                    return states.PLAY

        pygame.display.flip()