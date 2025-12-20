import pygame, sys
from game import button, states, constants, utils

def map_loader(screen):
    pygame.display.set_caption(constants.SELECTED_TILE.title)

    map_background = pygame.image.load(constants.SELECTED_TILE.image_path)
    map_background = pygame.transform.scale(map_background, screen.get_size()).convert()

    dark_factor = constants.DARK_PERCENTAGE
    dark_map_background = map_background.copy()
    dark_map_background.fill((dark_factor * 255, dark_factor * 255, dark_factor * 255), special_flags=pygame.BLEND_MULT)

    hit_line_y = 640
    audio_lead_in = constants.SELECTED_TILE.audio_lead_in
    scroll_speed = constants.SELECTED_TILE.scroll_speed

    while True:
        screen.blit(dark_map_background, (0, 0))
        draw_lanes(screen, hit_line_y)
       
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.flip()








def draw_lanes(screen, hit_line_y):
    x_center = constants.BASE_W // 2
    lane_offsets = [-150, -50, 50, 150]
    lane_positions = [x_center + offset for offset in lane_offsets]

    # Vertical lanes
    for x in lane_positions:
        pygame.draw.line(
            screen,
            (255, 255, 255),
            (utils.scale_x(x), 0),
            (utils.scale_x(x), utils.scale_y(1080)),
            max(1, utils.scale_x(3)),
        )

    # Side boundaries
    pygame.draw.line(
        screen, (255, 255, 255),
        (utils.scale_x(x_center + 200), 0),
        (utils.scale_x(x_center + 200), utils.scale_y(1080)),
        max(1, utils.scale_x(3)),
    )
    pygame.draw.line(
        screen, (255, 255, 255),
        (utils.scale_x(x_center - 200), 0),
        (utils.scale_x(x_center - 200), utils.scale_y(1080)),
        max(1, utils.scale_x(3)),
    ) 
    # Horizontal hit line
    pygame.draw.line(
        screen, (255, 0, 0),
        (utils.scale_x(x_center - 202), utils.scale_y(hit_line_y)),
        (utils.scale_x(x_center + 202), utils.scale_y(hit_line_y)),
        max(1, utils.scale_y(3)),
    )