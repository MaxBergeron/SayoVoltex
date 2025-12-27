import pygame, sys
from game import button, states, constants, utils, music_player, get_game_objects

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

    x_center = constants.BASE_W // 2
    clock = pygame.time.Clock()

    hit_object_data = get_game_objects.parse_file(constants.SELECTED_TILE.song_data_path)

    for note in hit_object_data["HitObjects"]:
        note.position_x = utils.scale_x(x_center - 150) + (note.key - 1) * utils.scale_x(100)

    player = music_player.MusicPlayer(constants.SELECTED_TILE.audio_path)
    player.play()

    while True:
        clock.tick(120)
        current_time_ms = player.get_position() * 1000
    
        screen.blit(dark_map_background, (0, 0))
        draw_lanes(screen, hit_line_y, x_center)
       
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return states.MAP
                key_str = utils.get_action_from_key(event.key) 
                for note in hit_object_data["HitObjects"]:
                    # Dont reference if note is complete or off screen
                    if note.hit or note.hold_complete or current_time_ms - (note.time + note.duration) > utils.scale_y(300):
                        continue
                    # Tap note hit
                    if note.duration == 0 and utils.convert_int_to_key(note.key) == key_str:
                        # Hit out of window
                        if abs(current_time_ms - note.time) < constants.HIT_WINDOW * constants.MISS_WINDOW_RATIO:
                            note.hit = True
                            print(evaluate_hit(note, current_time_ms))

                    # Hold note Hit
                    elif utils.convert_int_to_key(note.key) == key_str:
                            if abs(current_time_ms - note.time) < constants.HIT_WINDOW and not note.hold_started:
                                note.hold_started = True
                                note.holding = True
                                print(evaluate_hit(note, current_time_ms))
                            # Hit Late
                            elif current_time_ms > note.time and current_time_ms < note.time + note.duration and not note.hold_started:
                                note.holding = True
                                print(evaluate_hit(note, current_time_ms))



                            
            elif event.type == pygame.KEYUP:
                key_str = utils.get_action_from_key(event.key)
                for note in hit_object_data["HitObjects"]:
                    # Dont reference if note is complete or off screen
                    if note.hit or note.hold_complete or current_time_ms - (note.time + note.duration) > utils.scale_y(300):
                        continue
                    # Hold note release
                    if note.duration > 0 and (note.hold_started or note.holding) and utils.convert_int_to_key(note.key) == key_str:
                        if abs(current_time_ms - (note.time + note.duration)) < constants.HIT_WINDOW:
                            note.hold_complete = True
                        print(evaluate_hit(note, current_time_ms))
                        note.holding = False

               


        for note in hit_object_data["HitObjects"]:
            if note.hit or note.hold_complete or current_time_ms - (note.time + note.duration) > utils.scale_y(300):
                continue
            draw_note(screen, note, hit_line_y, scroll_speed, current_time_ms)


        pygame.display.flip()





def draw_lanes(screen, hit_line_y, x_center):
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
        max(1, utils.scale_y(10)),
    )

def draw_note(screen, note, hit_line_y, scroll_speed, current_time_ms):
    top_y = hit_line_y - (note.time - current_time_ms) * scroll_speed

    # TAP note
    if note.duration <= 0:
        screen.blit(constants.TAP_NOTE_IMAGE, (note.position_x, top_y))
        return

    # HOLD note
    head_image, body_image, tail_image = assign_hold_note_images(note)

    note_length = note.duration * scroll_speed
    head_h = head_image.get_height()
    tail_h = tail_image.get_height()
    head_top = top_y
    tail_top = top_y - (note_length - head_h)
    body_top = tail_top + tail_h
    body_bottom = head_top

    # Draw head
    screen.blit(head_image, (note.position_x, top_y)) 

    y = body_bottom - body_image.get_height() 

    # Draw body
    while y >= body_top - tail_h - constants.HOLD_NOTE_BODY_IMAGE.get_height(): 
        screen.blit(body_image, (note.position_x, y)) 
        y -= body_image.get_height() 
    
    # Draw tail  
    screen.blit(tail_image, (note.position_x, top_y - note_length))



def assign_hold_note_images(note):
    if note.hold_started or note.holding:
        return (
            constants.HOLD_NOTE_HEAD_IMAGE_TINTED,
            constants.HOLD_NOTE_BODY_IMAGE_TINTED,
            constants.HOLD_NOTE_TAIL_IMAGE_TINTED
        )
    else: 
        return (
            constants.HOLD_NOTE_HEAD_IMAGE,
            constants.HOLD_NOTE_BODY_IMAGE,
            constants.HOLD_NOTE_TAIL_IMAGE
        )
    
def evaluate_hit(note, current_time_ms):
    if note.duration == 0 and note.hit:
        if abs(current_time_ms - note.time) < (constants.HIT_WINDOW/2):
            return 300
        elif abs(current_time_ms - note.time) < (constants.HIT_WINDOW/1.5):
            return 150
        elif abs(current_time_ms - note.time) < (constants.HIT_WINDOW):
            return 50
    elif note.hold_started or note.hold_complete:
        if note.hold_started and note.holding and note.hold_complete:
            return 300 + note.duration * .5
        return 150
    return 0
    
