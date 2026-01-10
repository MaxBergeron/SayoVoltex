import pygame, sys
from game import button, states, constants, utils, music_player, get_game_objects, map_counters, game_objects, laser_cursor

active_popup = None

def map_loader(screen):
    pygame.display.set_caption(constants.SELECTED_TILE.title)

    map_background = pygame.image.load(constants.SELECTED_TILE.image_path)
    map_background = pygame.transform.scale(map_background, screen.get_size()).convert()

    dark_factor = constants.DARK_PERCENTAGE
    dark_map_background = map_background.copy()
    dark_map_background.fill((dark_factor * 255, dark_factor * 255, dark_factor * 255), special_flags=pygame.BLEND_MULT)

    continue_button = button.Button(image=None, pos=(utils.scale_x(640), utils.scale_y(240)), 
                             text_input="Continue", font=utils.get_font(utils.scale_y(constants.SIZE_MEDIUM_SMALL)), 
                             base_color="#d7fcd4", hovering_color="White")
    retry_button = button.Button(image=None, pos=(utils.scale_x(640), utils.scale_y(360)), 
                             text_input="Retry", font=utils.get_font(utils.scale_y(constants.SIZE_MEDIUM_SMALL)), 
                             base_color="#d7fcd4", hovering_color="White")
    exit_button = button.Button(image=None, pos=(utils.scale_x(640), utils.scale_y(480)), 
                             text_input="Exit", font=utils.get_font(utils.scale_y(constants.SIZE_MEDIUM_SMALL)), 
                             base_color="#d7fcd4", hovering_color="White")
    
    counters = {
        "point_counter": map_counters.PointCounter(),
        "percentage_counter": map_counters.PercentageCounter(),
        "combo_counter": map_counters.ComboCounter()
        }
    
    cursor = laser_cursor.LaserCursor()

    scroll_speed = constants.SELECTED_TILE.scroll_speed

    paused = False
    global active_popup


    x_center = constants.BASE_W // 2
    y_center = constants.BASE_H // 2


    clock = pygame.time.Clock()

    hit_sound = pygame.mixer.Sound(constants.HIT_SOUND_PATH)
    hit_sound.set_volume(constants.HIT_SOUND_VOLUME)
    tick_sound = pygame.mixer.Sound(constants.TICK_SOUND_PATH)
    tick_sound.set_volume(constants.TICK_SOUND_VOLUME)
    hit_object_data = get_game_objects.parse_file(constants.SELECTED_TILE.song_data_path)

    laser_objects = hit_object_data["LaserObjects"]
    chain_lasers(laser_objects)

    for note in hit_object_data["HitObjects"]:
        note.position_x = utils.scale_x(x_center - 150) + (note.key - 1) * utils.scale_x(100)

    player = music_player.MusicPlayer(constants.SELECTED_TILE.audio_path)
    player.play()
    pygame.time.wait(constants.SELECTED_TILE.audio_lead_in)

    while True:
        dt = clock.tick(120)
        knob_input = 0

        # Pause handling
        if paused:
            map_mouse_pos = pygame.mouse.get_pos()

            screen.blit(dark_map_background, (0, 0))
            draw_lanes(screen, x_center)

            for note in hit_object_data["HitObjects"]:
                if note.hit or note.hold_complete or note.miss:
                    continue
                note.draw(screen, current_time_ms)

            for laser in hit_object_data["LaserObjects"]:
                laser.draw(screen)


            for counter in counters.values():
                counter.update(screen)

            cursor.draw(screen)

            if active_popup:
                screen.blit(active_popup["image"], active_popup["rect"])

            pause_menu(screen, player)
            for b in [continue_button, retry_button, exit_button]:
                b.change_color(map_mouse_pos)
                b.update(screen)
            pygame.display.flip()

            # Pause events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        player.unpause()
                        paused = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if continue_button.check_for_input(map_mouse_pos):
                        player.unpause()
                        paused = False
                    elif retry_button.check_for_input(map_mouse_pos):
                        return states.MAP
                    elif exit_button.check_for_input(map_mouse_pos):
                        return states.PLAY
            continue  # skip the rest of the loop while paused

        # Update time
        current_time_ms = player.get_position() * 1000

        # Draw background,lanes, and counwers
        screen.blit(dark_map_background, (0, 0))
        draw_lanes(screen, x_center)
        for counter in counters.values():
            counter.update(screen)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused = True
                    continue

                key_str = utils.get_action_from_key(event.key)
                for note in hit_object_data["HitObjects"]:
                    if note.hit or note.miss or note.hold_complete:
                        continue

                    # TAP note
                    if note.duration == 0 and utils.convert_int_to_key(note.key) == key_str:
                        # Hit within window
                        if abs(current_time_ms - note.time) <= constants.HIT_WINDOW * constants.MISS_WINDOW_RATIO:
                            if abs(current_time_ms - note.time) <= constants.HIT_WINDOW:
                                note.hit = True
                                hit_sound.play()
                                evaluate_note(screen, note, current_time_ms, counters["point_counter"], counters["percentage_counter"], counters["combo_counter"])
                            else:
                                note.miss = True
                                hit_sound.play()
                                evaluate_note(screen, note, current_time_ms, counters["point_counter"], counters["percentage_counter"], counters["combo_counter"])

                    # HOLD note
                    elif utils.convert_int_to_key(note.key) == key_str:
                        if abs(current_time_ms - note.time) <= constants.HIT_WINDOW and not note.hold_started:
                            note.hold_started = True
                            note.holding = True
                            hit_sound.play()

                        elif note.time < current_time_ms < note.time + note.duration and not note.hold_started:
                            note.holding = True
                            hit_sound.play()
                
                # Handle cursor movement
                knob_input = 0
                keys = pygame.key.get_pressed()
                if event.key == utils.key_bindings["key_CW"]:
                    knob_input += 1
                elif event.key == utils.key_bindings["key_CCW"]:
                    knob_input -= 1

            elif event.type == pygame.KEYUP:
                key_str = utils.get_action_from_key(event.key)
                for note in hit_object_data["HitObjects"]:
                    if note.hit or note.miss or note.hold_complete:
                        continue

                    # HOLD release
                    if note.duration > 0 and (note.hold_started or note.holding) and utils.convert_int_to_key(note.key) == key_str:
                        if abs(current_time_ms - (note.time + note.duration)) <= constants.HIT_WINDOW:
                            note.hold_complete = True
                            hit_sound.play()
                            evaluate_note(screen, note, current_time_ms, counters["point_counter"], counters["percentage_counter"], counters["combo_counter"])
                        note.holding = False

        

        # Update cursor position
        cursor.update_movement(knob_input, dt / 1000)

        for note in hit_object_data["HitObjects"]:
            if note.hit or note.miss:
                continue
            # TAP note auto-miss
            if note.duration == 0 and current_time_ms - note.time > constants.HIT_WINDOW:
                note.miss = True
                evaluate_note(screen, note, current_time_ms, counters["point_counter"], counters["percentage_counter"], counters["combo_counter"])


            # HOLD note auto-miss if never started
            elif note.duration > 0 and not note.hold_started and current_time_ms > note.time + note.duration + constants.HIT_WINDOW:
                note.miss = True
                evaluate_note(screen, note, current_time_ms, counters["point_counter"], counters["percentage_counter"], counters["combo_counter"])

        # Draw notes
        for note in hit_object_data["HitObjects"]:
            if note.hit or note.hold_complete or note.miss:
                continue
            note.draw(screen, current_time_ms)
        
        for laser in hit_object_data["LaserObjects"]:
            laser.update_points(current_time_ms)
            laser.draw(screen)
            evaluate_laser(screen, laser, cursor, current_time_ms, tick_sound, counters["point_counter"], counters["percentage_counter"], counters["combo_counter"])
            # Set position of cursor 
            prev = laser.prev_laser
            wait_time = laser.half_width // constants.SCROLL_SPEED
            if not laser.is_chained_from_prev and prev and prev.end_time + wait_time < current_time_ms and not laser.cursor_positioned:
                laser.cursor_positioned = True
                cursor.set_position(laser.start_pos)
            
        cursor.draw(screen)



        # Draw accuracy popups
        if active_popup:
            screen.blit(active_popup["image"], active_popup["rect"])
            active_popup["timer"] -= dt
            if active_popup["timer"] <= 0:
                active_popup = None




        pygame.display.flip()



def draw_lanes(screen, x_center):
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
        (utils.scale_x(x_center - 202), utils.scale_x(constants.HIT_LINE_Y)),
        (utils.scale_x(x_center + 202), utils.scale_x(constants.HIT_LINE_Y)),
        max(1, utils.scale_y(10)),
    )

def pause_menu(screen, player):
    player.pause()

    popup_width, popup_height = utils.scale_x(500), utils.scale_y(350)
    popup_x = (screen.get_width() - popup_width) // 2
    popup_y = (screen.get_height() - popup_height) // 2
    popup = pygame.Surface((popup_width, popup_height), pygame.SRCALPHA)
    popup.fill((50, 50, 50, 180))

    screen.blit(popup, (popup_x, popup_y))
    
def evaluate_note(screen, note, current_time_ms, point_counter, percentage_counter, combo_counter):
    hit_percent = 0

    if note.duration == 0 and note.hit:
        if abs(current_time_ms - note.time) <= (constants.HIT_WINDOW/2):
            hit_percent = 100
            combo_counter.value += 1
            point_counter.value += 300
            spawn_popup("perfect")

        elif abs(current_time_ms - note.time) <= (constants.HIT_WINDOW/1.5):
            hit_percent = 50
            combo_counter.value += 1
            point_counter.value += 150
            spawn_popup("good")

        elif abs(current_time_ms - note.time) <= (constants.HIT_WINDOW):
            hit_percent = 25
            combo_counter.value += 1
            point_counter.value += 50
            spawn_popup("ok")
    elif note.hold_started or note.hold_complete:
        if note.hold_started and note.holding and note.hold_complete:
            hit_percent = 100
            combo_counter.value += (2 + int(note.duration * 0.5 / 300))
            point_counter.value += 300 + note.duration * 0.5
            spawn_popup("perfect")
        else:
            hit_percent = 50
            combo_counter.value += 1
            point_counter.value +=150
            spawn_popup("good")
    else:
        hit_percent = 0
        combo_counter.value = 0
        spawn_popup("miss")


    point_counter.update_text_surface()
    combo_counter.update_text_surface()
    percentage_counter.add_hit(hit_percent)

def evaluate_laser(screen, laser, cursor, current_time_ms, tick_sound, point_counter, percentage_counter, combo_counter):
    if laser.miss or laser.completed or current_time_ms < laser.start_time:
        return
    
    percent = 0

    min_x, max_x = laser.get_x_at_y(current_time_ms, utils.scale_y(constants.HIT_LINE_Y))
    if min_x is None or max_x is None:
        return

    overlap = not (cursor.right_edge < min_x or cursor.left_edge > max_x)
    # Hold started
    if overlap and not laser.holding:
        print("Laser hold started")
        laser.holding = True
        laser.started = True
        laser.last_tick_time = current_time_ms
        tick_sound.play()
        combo_counter.value += 1

    # Hold continues
    elif overlap and laser.holding:
        if laser.last_tick_time is None:
            laser.last_tick_time = current_time_ms
        delta = current_time_ms - laser.last_tick_time

        if delta >= constants.LASER_TICK_MS:
            ticks = delta // constants.LASER_TICK_MS
            laser.last_tick_time += ticks * constants.LASER_TICK_MS
            laser.total_hold_time += ticks * constants.LASER_TICK_MS
            tick_sound.play()
            point_counter.value += 50 * ticks
            combo_counter.value += 1
            gave_percentage = False
            if not gave_percentage and laser.total_hold_time >= laser.end_time - laser.start_time:
                combo_counter.value += 1
                percent = 100
                percentage_counter.add_hit(percent)
                gave_percentage = True

    # Hold breaks
    elif laser.holding and not overlap:
        # Hold break after starting
        if not laser.miss and laser.started:
            combo_counter.value = 0
            spawn_popup("miss")
            percent = 25
            percentage_counter.add_hit(percent)
        elif not laser.miss and not laser.started:
            percent = 0
            percentage_counter.add_hit(percent)
        laser.miss = True
        laser.holding = False
        combo_counter.value = 0
        spawn_popup("miss")
    
    point_counter.update_text_surface()
    combo_counter.update_text_surface()
    
def spawn_popup(type):
    global active_popup
    popup_image = constants.ACCURACY_POPUPS[type]
    popup_rect = popup_image.get_rect(center=utils.scale_pos(constants.BASE_W // 2, constants.BASE_H // 2))
    active_popup = {
        "image": popup_image,
        "rect": popup_rect,
        "timer": 300  
    }

def chain_lasers(lasers):
    # Sort by time
    lasers.sort(key=lambda l: l.start_time)

    for i in range(1, len(lasers)):
        prev = lasers[i - 1]
        curr = lasers[i]
        curr.prev_laser = prev
        prev.next_laser = curr
        if prev.end_time == curr.start_time:
            curr.is_chained_from_prev = True