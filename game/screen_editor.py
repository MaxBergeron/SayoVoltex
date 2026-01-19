import pygame, sys
from game import button, states, utils, constants
from game.textfield import TextInputBox
from pathlib import Path
import tkinter as tk
from tkinter import filedialog




def editor_menu(screen):
    pygame.display.set_caption("Editor")

    main_menu_background = pygame.image.load("assets/backgrounds/editor_background.jpg").convert()
    main_menu_background = pygame.transform.scale(main_menu_background, screen.get_size()).convert()

    menu_text = utils.get_font(utils.scale_y(constants.SIZE_LARGE)).render("EDITOR MENU", True, "#b68f40")
    menu_text_rect = menu_text.get_rect(center=(utils.scale_x(640), utils.scale_y(100)))

    user_audio_file_path = "test"
    text_user_audio_file_rect = None
    user_image_file_path = "test"

    audio_file_uploaded = False
    image_file_uploaded = False
    song_parameters_set = False
    editor_method_chosen = False

    font_small = utils.get_font(utils.scale_y(constants.SIZE_SMALL))
    font_tiny = utils.get_font(utils.scale_y(constants.SIZE_TINY))
    font_xtiny = utils.get_font(utils.scale_y(constants.SIZE_XTINY))
    font_xxtiny = utils.get_font(utils.scale_y(constants.SIZE_XXTINY))
    
    x = utils.scale_x(250)
    padding = utils.scale_x(12)
    center_x = utils.scale_x(constants.BASE_W // 2)

    text_or = font_small.render("OR", True, "#b68f40")
    text_or_rect = text_or.get_rect(center=(utils.scale_x(640), utils.scale_y(340)))


    # Labels
    title_label = font_tiny.render("Title:", True, "#b68f40")
    title_label_rect = title_label.get_rect(midleft=(x, utils.scale_y(160)))
    artist_label = font_tiny.render("Artist:", True, "#b68f40")
    artist_label_rect = artist_label.get_rect(midleft=(x, utils.scale_y(200)))
    creator_label = font_tiny.render("Creator:", True, "#b68f40")
    creator_label_rect = creator_label.get_rect(midleft=(x, utils.scale_y(240)))
    version_label = font_tiny.render("Version:", True, "#b68f40")
    version_label_rect = version_label.get_rect(midleft=(x, utils.scale_y(280)))
    scroll_speed_label = font_tiny.render("Scroll Speed:", True, "#b68f40")
    scroll_speed_label_rect = scroll_speed_label.get_rect(midleft=(x, utils.scale_y(320)))
    bpm_label = font_tiny.render("BPM:", True, "#b68f40")
    bpm_label_rect = bpm_label.get_rect(midleft=(x, utils.scale_y(360)))
    audio_lead_in_label = font_tiny.render("Audio Lead In:", True, "#b68f40")
    audio_lead_in_label_rect = audio_lead_in_label.get_rect(midleft=(x, utils.scale_y(400)))


    # Text input boxes
    title_input = TextInputBox(title_label_rect.right + padding, title_label_rect.centery, utils.scale_x(180), font_xtiny)
    artist_input = TextInputBox(artist_label_rect.right + padding, artist_label_rect.centery, utils.scale_x(180), font_xtiny)
    version_input = TextInputBox(version_label_rect.right + padding, version_label_rect.centery, utils.scale_x(180), font_xtiny)
    scroll_speed_input = TextInputBox(scroll_speed_label_rect.right + padding, scroll_speed_label_rect.centery, utils.scale_x(180), font_xtiny)
    bpm_input = TextInputBox(bpm_label_rect.right + padding, bpm_label_rect.centery, utils.scale_x(180), font_xtiny)
    audio_lead_in_input = TextInputBox(audio_lead_in_label_rect.right + padding, audio_lead_in_label_rect.centery, utils.scale_x(180), font_xtiny)
    creator_input = TextInputBox(creator_label_rect.right + padding, creator_label_rect.centery, utils.scale_x(180), font_xtiny)

    # Group all input boxes for convenience
    popup_group = pygame.sprite.Group(title_input, artist_input, version_input, scroll_speed_input, bpm_input, audio_lead_in_input, creator_input)

    choose_existing_song_button = button.Button(image=None, pos=(utils.scale_x(center_x), utils.scale_y(240)), text_input="Choose Existing Song",
                                  font=utils.get_font(utils.scale_y(constants.SIZE_SMALL)),
                                  base_color="#d7fcd4", hovering_color="White")
    new_song_button = button.Button(image=None, pos=(utils.scale_x(center_x), utils.scale_y(440)), text_input="New Song",
                                  font=utils.get_font(utils.scale_y(constants.SIZE_SMALL)),
                                  base_color="#d7fcd4", hovering_color="White")
    submit_button = button.Button(image=None, pos=(utils.scale_x(925), utils.scale_y(540)), text_input="Submit",
                                  font=utils.get_font(utils.scale_y(constants.SIZE_SMALL)),
                                  base_color="#d7fcd4", hovering_color="White")
    upload_audio_file_button = button.Button(image=None, pos=(utils.scale_x(900), utils.scale_y(160)), text_input="Upload Audio File",
                                  font=utils.get_font(utils.scale_y(constants.SIZE_TINY)),
                                  base_color="#d7fcd4", hovering_color="White")
    upload_image_file_button = button.Button(image=None, pos=(utils.scale_x(900), utils.scale_y(240)), text_input="Upload Image File",
                                  font=utils.get_font(utils.scale_y(constants.SIZE_TINY)),
                                  base_color="#d7fcd4", hovering_color="White")

    clock = pygame.time.Clock()

    while True:
        clock.tick(60)
        menu_mouse_pos = pygame.mouse.get_pos()

        event_list = pygame.event.get()
        for event in event_list:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.blit(main_menu_background, (0, 0))

        if not editor_method_chosen:
            choose_load_popup(screen, menu_mouse_pos, choose_existing_song_button, new_song_button)
            screen.blit(text_or, text_or_rect)
            for event in event_list:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if choose_existing_song_button.check_for_input(menu_mouse_pos):
                        editor_method_chosen = True
                        # Here you would typically load a file dialog to choose a song file
                    if new_song_button.check_for_input(menu_mouse_pos):
                        editor_method_chosen = True

        # New song 
        if not song_parameters_set and editor_method_chosen:
            initial_settings_popup(screen, menu_mouse_pos, event_list, popup_group, submit_button, upload_audio_file_button, upload_image_file_button)
            for event in event_list:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if upload_audio_file_button.check_for_input(menu_mouse_pos):
                        user_audio_file_path, audio_file_uploaded = upload_audio_file()
                        user_audio_file_path = utils.after_second_to_last_slash(user_audio_file_path)
                        user_audio_file_path = utils.shorten_text(user_audio_file_path, max_length=25)
                        text_user_audio_file_path = font_xtiny.render(user_audio_file_path, True, "#b68f40")
                        text_user_audio_file_rect = text_user_audio_file_path.get_rect(center=(utils.scale_x(900), utils.scale_y(200)))
                    elif upload_image_file_button.check_for_input(menu_mouse_pos):
                        user_image_file_path, image_file_uploaded = upload_image_file()
                        user_image_file_path = utils.after_second_to_last_slash(user_image_file_path)
                        user_image_file_path = utils.shorten_text(user_image_file_path, max_length=25)
                        text_user_image_file_path = font_xtiny.render(user_image_file_path, True, "#b68f40")
                        text_user_image_file_rect = text_user_image_file_path.get_rect(center=(utils.scale_x(900), utils.scale_y(280)))
                    elif submit_button.check_for_input(menu_mouse_pos):
                        print("Submit button clicked")
                        if any(box.text == "" for box in popup_group):
                            pass
                        else:
                            song_parameters_set = True
                            folder_path = f"song_folder/{title_input.text}-{version_input.text}-{creator_input.text}"
                            Path(folder_path).mkdir(exist_ok=True)
                            song_path = Path(folder_path) / f"{title_input.text}-{version_input.text}-{creator_input.text}.txt"
                            if not song_path.exists():
                                create_song_file(song_path, title_input.text, artist_input.text, version_input.text, scroll_speed_input.text, bpm_input.text, audio_lead_in_input.text, creator_input.text)
    


            if audio_file_uploaded:
                screen.blit(text_user_audio_file_path, text_user_audio_file_rect)
            if image_file_uploaded:
                screen.blit(text_user_image_file_path, text_user_image_file_rect)

            screen.blit(title_label, title_label_rect)
            screen.blit(artist_label, artist_label_rect)
            screen.blit(version_label, version_label_rect)
            screen.blit(scroll_speed_label, scroll_speed_label_rect)
            screen.blit(bpm_label, bpm_label_rect)
            screen.blit(audio_lead_in_label, audio_lead_in_label_rect)
            screen.blit(creator_label, creator_label_rect)

        pygame.display.flip()

def initial_settings_popup(screen, menu_mouse_pos, event_list, popup_group, submit_button, upload_audio_file_button, upload_image_file_button):
    popup_width, popup_height = utils.scale_x(800), utils.scale_y(450)
    popup_x = (screen.get_width() - popup_width) // 2
    popup_y = (screen.get_height() - popup_height) // 2
    popup_rect = pygame.Rect(popup_x, popup_y, popup_width, popup_height)

    pygame.draw.rect(screen, (50, 50, 50), popup_rect)
    pygame.draw.rect(screen, (255, 255, 255), popup_rect, 2)

    popup_group.update(event_list)
    popup_group.draw(screen)

    upload_audio_file_button.change_color(menu_mouse_pos)
    upload_audio_file_button.update(screen)

    upload_image_file_button.change_color(menu_mouse_pos)
    upload_image_file_button.update(screen)

    submit_button.change_color(menu_mouse_pos)
    submit_button.update(screen)

def choose_load_popup(screen, menu_mouse_pos, choose_existing_song_button, new_song_button):
    popup_width, popup_height = utils.scale_x(800), utils.scale_y(450)
    popup_x = (screen.get_width() - popup_width) // 2
    popup_y = (screen.get_height() - popup_height) // 2
    popup_rect = pygame.Rect(popup_x, popup_y, popup_width, popup_height)

    pygame.draw.rect(screen, (50, 50, 50), popup_rect)
    pygame.draw.rect(screen, (255, 255, 255), popup_rect, 2)

    choose_existing_song_button.change_color(menu_mouse_pos)
    choose_existing_song_button.update(screen)
    new_song_button.change_color(menu_mouse_pos)
    new_song_button.update(screen)

def create_song_file(song_path, title, artist, version, scroll_speed, bpm, audio_lead_in, creator):
    with open(song_path, "w") as f:
        f.write("[Metadata]\n")

        f.write(f"Title: {title}\n")
        f.write(f"Artist: {artist}\n")
        f.write(f"Creator: {creator}\n")
        f.write(f"Version: {version}\n")
        f.write("Length: \n")
        f.write(f"Scroll Speed: {scroll_speed}\n")
        f.write(f"BPM: {bpm}\n")
        f.write(f"Audio Lead In: {audio_lead_in}\n")
        f.write(f"Image Path: \n")
        f.write(f"Audio Path: \n")

        f.write("\n// Hit Object Ordering\n")
        f.write("// 3-key configuration (1-3), hold duration, time position, \n")
        f.write("[HitObjects]\n")

        f.write("\n// Laser Object Ordering\n")
        f.write("// start time, end time, start position, end position\n")
        f.write("[LaserObjects]\n")

def upload_audio_file():
    root = tk.Tk()
    root.withdraw()

    # Open file dialog and get path
    file_path = filedialog.askopenfilename(
        title="Select a song file",
        filetypes=(("audio files", "*.mp3 *.wav *.ogg"), ("All files", "*.*"))
    )

    if file_path:
        print("User selected:", file_path)
        return file_path, True
    else:
        return file_path, False


def upload_image_file():
    root = tk.Tk()
    root.withdraw()

    # Open file dialog and get path
    file_path = filedialog.askopenfilename(        title="Select an image file",
        filetypes=(("image files", "*.png *.jpg *.jpeg"), ("All files", "*.*"))
    )

    if file_path:
        return file_path, True
    else:
        return file_path, False
