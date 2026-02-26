import os
import shutil
import pygame, sys, ctypes, subprocess
from game import button, states, utils, constants
from game.textfield import TextInputBox
from pathlib import Path
import tkinter as tk
from tkinter import filedialog
from mutagen import File


def editor_initialize_menu(screen):
    pygame.display.set_caption("Editor_Choice")

    main_menu_background = pygame.image.load("assets/backgrounds/editor_initialize_background.jpg").convert()
    main_menu_background = pygame.transform.scale(main_menu_background, screen.get_size()).convert()

    menu_text = utils.get_font(utils.scale_y(constants.SIZE_LARGE)).render("EDITOR INITIALIZE MENU", True, "#b68f40")
    menu_text_rect = menu_text.get_rect(center=(utils.scale_x(640), utils.scale_y(100)))

    user_audio_file_path = "test"
    text_user_audio_file_rect = None
    user_image_file_path = "test"
    metadata, objectdata = None, None

    audio_file_path_got = False
    image_file_path_got = False
    song_parameters_set = False
    editor_method_chosen = None


    font_small = utils.get_font(utils.scale_y(constants.SIZE_SMALL))
    font_tiny = utils.get_font(utils.scale_y(constants.SIZE_TINY))
    font_xtiny = utils.get_font(utils.scale_y(constants.SIZE_XTINY))
    font_xxtiny = utils.get_font(utils.scale_y(constants.SIZE_XXTINY))
    
    x = utils.scale_x(250)
    padding = utils.scale_x(12)
    center_x = constants.BASE_W // 2

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
    get_audio_file_path_button = button.Button(image=None, pos=(utils.scale_x(900), utils.scale_y(160)), text_input="Upload Audio File",
                                  font=utils.get_font(utils.scale_y(constants.SIZE_TINY)),
                                  base_color="#d7fcd4", hovering_color="White")
    get_image_file_path_button = button.Button(image=None, pos=(utils.scale_x(900), utils.scale_y(240)), text_input="Upload Image File",
                                  font=utils.get_font(utils.scale_y(constants.SIZE_TINY)),
                                  base_color="#d7fcd4", hovering_color="White")
    upload_song_folder_button = button.Button(image=None, pos=(utils.scale_x(center_x), utils.scale_y(300)), text_input="Upload Song Folder",
                                  font=utils.get_font(utils.scale_y(constants.SIZE_SMALL)),
                                  base_color="#d7fcd4", hovering_color="White")
    back_button = button.Button(image=None, pos=(utils.scale_x(325), utils.scale_y(540)), 
                             text_input="Back", font=utils.get_font(utils.scale_y(constants.SIZE_SMALL)), 
                             base_color="#d7fcd4", hovering_color="White")
    
    test_button = button.Button(image=None, pos=(utils.scale_x(center_x), utils.scale_y(540)), text_input="TEST",
                                  font=utils.get_font(utils.scale_y(constants.SIZE_SMALL)),
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

        # Choose load method
        if editor_method_chosen is None:
            choose_load_popup(screen, menu_mouse_pos, choose_existing_song_button, new_song_button, back_button, test_button)
            screen.blit(text_or, text_or_rect)
            for event in event_list:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if choose_existing_song_button.check_for_input(menu_mouse_pos):
                        editor_method_chosen = "existing"
                        # Here you would typically load a file dialog to choose a song file
                    elif new_song_button.check_for_input(menu_mouse_pos):
                        editor_method_chosen = "new"
                    elif back_button.check_for_input(menu_mouse_pos):
                        return states.MENU
                    elif test_button.check_for_input(menu_mouse_pos):
                        metadata = assign_metadata("Title", "artist", "version", "0.35", "182", "0", "creator", "song_folder\Susume-Easy-Corgo\Gary Come Home Punk Cover.wav", "image_file_path")
                        return states.EDITOR, metadata, objectdata, None
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return states.MENU

        # New song 
        if not song_parameters_set and editor_method_chosen == "new":
            initial_settings_popup(screen, menu_mouse_pos, event_list, popup_group, submit_button, get_audio_file_path_button, get_image_file_path_button, back_button)
            for event in event_list:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if get_audio_file_path_button.check_for_input(menu_mouse_pos):
                        user_audio_file_path, audio_file_path_got = get_audio_file_path()
                        display_audio_file_path = utils.after_second_to_last_slash(user_audio_file_path)
                        display_audio_file_path = utils.shorten_text(display_audio_file_path, max_length=25)
                        text_user_audio_file_path = font_xtiny.render(display_audio_file_path, True, "#b68f40")
                        text_user_audio_file_rect = text_user_audio_file_path.get_rect(center=(utils.scale_x(900), utils.scale_y(200)))
                    elif get_image_file_path_button.check_for_input(menu_mouse_pos):
                        user_image_file_path, image_file_path_got = get_image_file_path()
                        display_image_file_path = utils.after_second_to_last_slash(user_image_file_path)
                        display_image_file_path = utils.shorten_text(display_image_file_path, max_length=25)
                        text_user_image_file_path = font_xtiny.render(display_image_file_path, True, "#b68f40")
                        text_user_image_file_rect = text_user_image_file_path.get_rect(center=(utils.scale_x(900), utils.scale_y(280)))
                    elif back_button.check_for_input(menu_mouse_pos):
                        for input_box in popup_group:
                            input_box.text = ""
                            input_box.render_text()
                        editor_method_chosen = None
                    elif submit_button.check_for_input(menu_mouse_pos):
                        if any(box.text == "" for box in popup_group) or not audio_file_path_got or not image_file_path_got:
                            error_message = "Please fill in all fields and upload files."
                            utils.show_error_modal(screen, error_message)
                        elif not user_audio_file_path.lower().endswith(('.mp3', '.ogg', '.wav')):
                            error_message = "Invalid audio file type. Please upload an mp3, ogg, or wav file."
                            utils.show_error_modal(screen, error_message)
                        elif not user_image_file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
                            error_message = "Invalid image file type. Please upload a png, jpg, jpeg, or webp file."
                            utils.show_error_modal(screen, error_message)
                        elif get_audio_length(user_audio_file_path) == 0:
                            error_message = "Audio file length is 0. Please upload a valid audio file."
                            utils.show_error_modal(screen, error_message)
                        elif not scroll_speed_input.text[0].isdigit() or not bpm_input.text.isdigit() or not audio_lead_in_input.text.isdigit():
                            error_message = "Scroll Speed, BPM, and Audio Lead In must be a number."
                            utils.show_error_modal(screen, error_message)
                        else:
                            folder_path = f"song_folder/{title_input.text}-{version_input.text}-{creator_input.text}"
                            Path(folder_path).mkdir(exist_ok=True)
                            map_path = Path(folder_path) / f"{title_input.text}-{version_input.text}-{creator_input.text}.txt"
                            if not map_path.exists():
                                song_parameters_set = True
                                audio_file_path = normalize_path(copy_file_to_folder(user_audio_file_path, folder_path))
                                wav_path, ogg_path = ensure_audio_pair(audio_file_path, folder_path)
                                image_file_path = normalize_path(copy_file_to_folder(user_image_file_path, folder_path))
                                create_song_file(map_path, title_input.text, artist_input.text, version_input.text, 
                                                 scroll_speed_input.text, bpm_input.text, audio_lead_in_input.text, 
                                                 creator_input.text, audio_file_path, image_file_path)
                                metadata = assign_metadata(title_input.text, artist_input.text, version_input.text, 
                                                 scroll_speed_input.text, bpm_input.text, audio_lead_in_input.text, 
                                                 creator_input.text, audio_file_path, image_file_path)
                                return states.EDITOR, metadata, objectdata, map_path
                            else:
                                error_message = "Song folder already exists."
                                utils.show_error_modal(screen, error_message)

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        editor_method_chosen = None
                        for input_box in popup_group:
                            input_box.text = ""
                            input_box.render_text()
            if audio_file_path_got:
                screen.blit(text_user_audio_file_path, text_user_audio_file_rect)
            if image_file_path_got:
                screen.blit(text_user_image_file_path, text_user_image_file_rect)

            screen.blit(title_label, title_label_rect)
            screen.blit(artist_label, artist_label_rect)
            screen.blit(version_label, version_label_rect)
            screen.blit(scroll_speed_label, scroll_speed_label_rect)
            screen.blit(bpm_label, bpm_label_rect)
            screen.blit(audio_lead_in_label, audio_lead_in_label_rect)
            screen.blit(creator_label, creator_label_rect)

        # Choose existing song
        if not song_parameters_set and editor_method_chosen == "existing":
            choose_existing_song_popup(screen, menu_mouse_pos, upload_song_folder_button, back_button)
            for event in event_list:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if upload_song_folder_button.check_for_input(menu_mouse_pos):
                        folder_path, success = upload_song_folder()
                        map_path = utils.find_map_file(folder_path)
                        # Go to editor
                        if success:
                            song_parameters_set = True 
                            metadata, objectdata = utils.parse_song_file(map_path)
                            return states.EDITOR, metadata, objectdata, map_path
                    elif back_button.check_for_input(menu_mouse_pos):
                        editor_method_chosen = None
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        editor_method_chosen = None 

        pygame.display.flip()

def initial_settings_popup(screen, menu_mouse_pos, event_list, popup_group, submit_button, get_audio_file_path_button, get_image_file_path_button, back_button):
    popup_width, popup_height = utils.scale_x(800), utils.scale_y(450)
    popup_x = (screen.get_width() - popup_width) // 2
    popup_y = (screen.get_height() - popup_height) // 2
    popup_rect = pygame.Rect(popup_x, popup_y, popup_width, popup_height)

    pygame.draw.rect(screen, (50, 50, 50), popup_rect)
    pygame.draw.rect(screen, (255, 255, 255), popup_rect, 2)

    popup_group.update(event_list)
    popup_group.draw(screen)

    get_audio_file_path_button.change_color(menu_mouse_pos)
    get_audio_file_path_button.update(screen)

    get_image_file_path_button.change_color(menu_mouse_pos)
    get_image_file_path_button.update(screen)
    submit_button.change_color(menu_mouse_pos)
    submit_button.update(screen)
    back_button.change_color(menu_mouse_pos)
    back_button.update(screen)


def choose_existing_song_popup(screen, menu_mouse_pos, upload_song_folder_button, back_button):
    popup_width, popup_height = utils.scale_x(800), utils.scale_y(450)
    popup_x = (screen.get_width() - popup_width) // 2
    popup_y = (screen.get_height() - popup_height) // 2
    popup_rect = pygame.Rect(popup_x, popup_y, popup_width, popup_height)

    pygame.draw.rect(screen, (50, 50, 50), popup_rect)
    pygame.draw.rect(screen, (255, 255, 255), popup_rect, 2)

    upload_song_folder_button.change_color(menu_mouse_pos)
    upload_song_folder_button.update(screen)
    back_button.change_color(menu_mouse_pos)
    back_button.update(screen)

def choose_load_popup(screen, menu_mouse_pos, choose_existing_song_button, new_song_button, back_button, test_button):
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
    back_button.change_color(menu_mouse_pos)
    back_button.update(screen)
    test_button.change_color(menu_mouse_pos)
    test_button.update(screen)

def create_song_file(map_path, title, artist, version, scroll_speed, BPM, audio_lead_in, creator, audio_file_path, image_file_path):
    with open(map_path, "w", encoding="utf-8") as f:
        f.write("[Metadata]\n")

        f.write(f"Title: {title}\n")
        f.write(f"Artist: {artist}\n")
        f.write(f"Creator: {creator}\n")
        f.write(f"Version: {version}\n")
        f.write(f"Length: {get_audio_length(audio_file_path)}\n")
        f.write(f"Scroll Speed: {scroll_speed}\n")
        f.write(f"BPM: {BPM}\n")
        f.write(f"Audio Lead In: {audio_lead_in}\n")
        f.write(f"Image Path: {image_file_path}\n")
        f.write(f"Audio Path: {audio_file_path}\n")

        f.write("\n// Hit Object Ordering\n")
        f.write("// 3-key configuration (1-3), hold duration, time position, \n")
        f.write("[HitObjects]\n")

        f.write("\n// Laser Object Ordering\n")
        f.write("// start time, end time, start position, end position\n")
        f.write("[LaserObjects]\n")

def get_audio_file_path():
    root = tk.Tk()
    root.withdraw()

    downloads_folder = os.path.join(os.path.expanduser("~"), "Downloads")
    if not os.path.exists(downloads_folder):
        downloads_folder = os.path.expanduser("~")

    # Open file dialog and get path
    file_path = filedialog.askopenfilename(
        title="Select a song file",
        initialdir=downloads_folder,
        filetypes=(("audio files", "*.mp3 *.ogg *.wav"), ("All files", "*.*"))
    )

    if not file_path:
        return None, False

    root.destroy()

    return file_path, True
    
def ensure_audio_pair(file_path, folder_path):
    base_name = os.path.splitext(os.path.basename(file_path))[0]

    wav_path = os.path.join(folder_path, base_name + ".wav")
    ogg_path = os.path.join(folder_path, base_name + ".ogg")

    ext = os.path.splitext(file_path)[1].lower()
    ext = ext.lower()

    if ext == ".wav":
        if not os.path.exists(ogg_path):
            subprocess.run([
                "ffmpeg", "-y",
                "-i", wav_path,
                "-c:a", "libvorbis",
                "-qscale:a", "5",
                ogg_path
            ], check=True)
        return wav_path, ogg_path

    elif ext == ".ogg":
        if not os.path.exists(wav_path):
            subprocess.run([
                "ffmpeg", "-y",
                "-i", ogg_path,
                wav_path
            ], check=True)
        return wav_path, ogg_path

    else:
        # mp3 or something else
        # convert to both
        if not os.path.exists(wav_path):
            subprocess.run(["ffmpeg", "-y", "-i", file_path, wav_path], check=True)

        if not os.path.exists(ogg_path):
            subprocess.run([
                "ffmpeg", "-y",
                "-i", file_path,
                "-c:a", "libvorbis",
                "-qscale:a", "5",
                ogg_path
            ], check=True)

        return wav_path, ogg_path


def get_image_file_path():
    root = tk.Tk()
    root.withdraw()

    downloads_folder = os.path.join(os.path.expanduser("~"), "Downloads")
    if not os.path.exists(downloads_folder):
        downloads_folder = os.path.expanduser("~")

    # Open file dialog and get path
    file_path = filedialog.askopenfilename(        
        title="Select an image file",
        initialdir=downloads_folder,
        filetypes=(("image files", "*.png *.jpg *.jpeg *.webp"), ("All files", "*.*"))
    )

    if file_path:
        return file_path, True
    else:
        return file_path, False
    
def copy_file_to_folder(source_path, dest_folder):
    # Check source exists
    if not source_path or not os.path.exists(source_path):
        raise FileNotFoundError(f"Source file does not exist: {source_path}")

    # Make destination folder if it doesn't exist
    os.makedirs(dest_folder, exist_ok=True)

    # Build destination path
    filename = os.path.basename(source_path)
    dest_path = os.path.join(dest_folder, filename)

    # Avoid overwriting existing files
    if os.path.exists(dest_path):
        base, ext = os.path.splitext(filename)
        counter = 1
        while os.path.exists(dest_path):
            dest_path = os.path.join(dest_folder, f"{base}_{counter}{ext}")
            counter += 1

    shutil.copy2(source_path, dest_path)

    return dest_path
    
def upload_song_folder():
    root = tk.Tk()
    root.withdraw()

    # Path to this script's directory
    base_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.abspath(os.path.join(base_dir, os.pardir))


    # Path to song_folder inside it
    song_folder_path = os.path.join(project_dir, "song_folder")

    # Open folder dialog and get path
    folder_path = filedialog.askdirectory(
        title="Select a song folder",
        initialdir=song_folder_path
    )

    root.destroy()

    hwnd = pygame.display.get_wm_info()['window']
    ctypes.windll.user32.ShowWindow(hwnd, 9)  # SW_RESTORE
    ctypes.windll.user32.SetForegroundWindow(hwnd)

    if folder_path:
        return folder_path, True
    else:
        return folder_path, False
    
def normalize_path(path):
    path = os.path.normpath(path)
    return path.replace("\\", "/")
    
@staticmethod
def get_audio_length(file_path):
    audio = File(file_path)
    if audio is None:
        raise ValueError("Unsupported audio format")
    return int(audio.info.length)

def assign_metadata(title, artist, version, scroll_speed, BPM, audio_lead_in, creator, audio_file_path, image_file_path):
    metadata = {
        "Title": title, "Artist": artist, "Version": version,
        "Scroll Speed": scroll_speed, "BPM": BPM, "Audio Lead In": audio_lead_in,
        "Creator": creator, "Audio Path": audio_file_path, "Image Path": image_file_path
    }
    return metadata