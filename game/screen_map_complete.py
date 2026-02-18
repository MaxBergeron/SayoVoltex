from game import constants, utils, button, states
import pygame, sys

def map_complete_menu(screen, counters):

    clock = pygame.time.Clock()

    # Extract counters
    point_counter = counters["point_counter"]
    percentage_counter = counters["percentage_counter"]
    combo_counter = counters["combo_counter"]

    # Fonts
    title_font = utils.get_font(utils.scale_y(70))
    stat_font = utils.get_font(utils.scale_y(40))
    small_font = utils.get_font(utils.scale_y(30))

    # Buttons
    continue_button = button.Button(
        image=None,
        pos=(utils.scale_x(640), utils.scale_y(700)),
        text_input="Continue",
        font=stat_font,
        base_color="#d7fcd4",
        hovering_color="White"
    )

    retry_button = button.Button(
        image=None,
        pos=(utils.scale_x(640), utils.scale_y(800)),
        text_input="Retry",
        font=stat_font,
        base_color="#d7fcd4",
        hovering_color="White"
    )

    exit_button = button.Button(
        image=None,
        pos=(utils.scale_x(640), utils.scale_y(900)),
        text_input="Exit",
        font=stat_font,
        base_color="#d7fcd4",
        hovering_color="White"
    )

    while True:
        clock.tick(60)
        mouse_pos = pygame.mouse.get_pos()

        # Background
        screen.fill((20, 20, 20))

        # Title
        title_text = title_font.render("MAP COMPLETE!", True, (255, 255, 255))
        screen.blit(title_text, title_text.get_rect(center=(utils.scale_x(640), utils.scale_y(120))))

        # Score
        score_text = stat_font.render(
            f"Score: {point_counter.value}",
            True,
            (255, 255, 255)
        )
        screen.blit(score_text, (utils.scale_x(200), utils.scale_y(250)))

        # Accuracy
        acc_text = stat_font.render(
            f"Accuracy: {percentage_counter.value:.1f}%",
            True,
            (255, 255, 255)
        )
        screen.blit(acc_text, (utils.scale_x(200), utils.scale_y(320)))

        # Max Combo
        combo_text = stat_font.render(
            f"Max Combo: {combo_counter.value}",
            True,
            (255, 255, 255)
        )
        screen.blit(combo_text, (utils.scale_x(200), utils.scale_y(390)))

        # Breakdown
        breakdown_title = small_font.render("Hit Breakdown:", True, (200, 200, 200))
        screen.blit(breakdown_title, (utils.scale_x(200), utils.scale_y(470)))

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

        screen.blit(perfect_text, (utils.scale_x(220), utils.scale_y(520)))
        screen.blit(good_text, (utils.scale_x(220), utils.scale_y(570)))
        screen.blit(ok_text, (utils.scale_x(220), utils.scale_y(620)))
        screen.blit(miss_text, (utils.scale_x(220), utils.scale_y(670)))

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

        pygame.display.flip()