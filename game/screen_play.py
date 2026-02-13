import pygame, sys, os
from game import button, states, utils, constants, song_tile, map_details



def play_menu(screen):
    pygame.display.set_caption("Play")
    play_background = pygame.image.load("assets/backgrounds/play_background.jpg")
    play_background = pygame.transform.scale(play_background, screen.get_size()).convert()

    play_text = utils.get_font(utils.scale_y(constants.SIZE_LARGE)).render("Play", True, "#b68f40")
    play_text_rect = play_text.get_rect(center=(utils.scale_x(640), utils.scale_y(100)))

    song_tile_cover = pygame.image.load("assets/images/song_tile_cover.png").convert_alpha()
    song_tile_cover = pygame.transform.scale(song_tile_cover, (utils.scale_x(225), utils.scale_y(75)))

    back_button = button.Button(image=None, pos=(utils.scale_x(150), utils.scale_y(650)), 
                             text_input="Back", font=utils.get_font(utils.scale_y(constants.SIZE_MEDIUM_SMALL)), 
                             base_color="#d7fcd4", hovering_color="White")

    song_tiles = []

    selected_tile = None

    song_folder = "song_folder"
    for entry in os.listdir(song_folder):
        full_path = os.path.join(song_folder, entry)
        if os.path.isdir(full_path):
            tile = song_tile.SongTile(
                song_folder_path = full_path,
                cover = song_tile_cover,
            )
            song_tiles.append(tile)

    for i, tile in enumerate(song_tiles):
        tile.position = (
            utils.scale_x(1080),
            utils.scale_y(20) + i * utils.scale_y(100)
        )

    map_info = map_details.MapDetails()

    while True:
        screen.blit(play_background, (0, 0))
        play_mouse_pos = pygame.mouse.get_pos()

        screen.blit(play_text, play_text_rect)
        for tile in song_tiles:
            tile.update(screen)

        for b in [back_button]:
            b.change_color(play_mouse_pos)
            b.update(screen)

        map_info.update(screen)

        # Handle Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if back_button.check_for_input(play_mouse_pos):
                    return states.MENU
                for tile in song_tiles:
                    if tile.check_for_input(play_mouse_pos):
                        if selected_tile != tile:
                            selected_tile = tile

                            map_info.title = tile.title
                            map_info.artist = tile.artist
                            map_info.creator = tile.creator
                            map_info.version = tile.version
                            map_info.length = tile.length
                            map_info.scroll_speed = tile.scroll_speed
                            map_info.BPM = tile.BPM
                        else:
                            constants.SELECTED_TILE = tile
                            constants.SCROLL_SPEED = tile.scroll_speed
                            return states.MAP
            elif event.type == pygame.MOUSEWHEEL:
                if not song_tiles:
                    return
                
                scroll_amount = -event.y * utils.scale_y(25)

                if song_tiles[0].position[1] + scroll_amount < utils.scale_y(20):
                    break
                if song_tiles[-1].position[1] + scroll_amount > utils.scale_y(630):
                    break

                for tile in song_tiles:
                    tile.position = (tile.position[0],tile.position[1] + scroll_amount)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return states.MENU
                


        pygame.display.flip()