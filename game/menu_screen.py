import pygame, sys
from game import button

pygame.init()

screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Menu")

main_menu_background = pygame.image.load("assets/main_menu_background.jpg")

def get_font(size): 
    return pygame.font.Font("assets/font/font.ttf", size)

def play_button_clicked():
    print("Play button clicked!")

def options_button_clicked():
    print("Options button clicked!")

def quit_button_clicked():
    pygame.quit()
    sys.exit()

def main_menu():
    while True:
        screen.blit(main_menu_background, (0, 0))

        menu_mouse_pos = pygame.mouse.get_pos()

        menu_text = get_font(150).render("MAIN MENU", True, "#b68f40")
        menu_text_rect = menu_text.get_rect(center=(640, 100))

        play_button = button.Button(image=None, pos=(640, 250), 
                             text_input="PLAY", font=get_font(75), 
                             base_color="#d7fcd4", hovering_color="White")
        options_button = button.Button(image=None, pos=(640, 400), 
                                text_input="OPTIONS", font=get_font(75), 
                                base_color="#d7fcd4", hovering_color="White")
        quit_button = button.Button(image=None, pos=(640, 550), 
                             text_input="QUIT", font=get_font(75),
                             base_color="#d7fcd4", hovering_color="White")
        
        screen.blit(menu_text, menu_text_rect)

        for b in [play_button, options_button, quit_button]:
            b.change_color(menu_mouse_pos)
            b.update(screen)

        # Handle Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.check_for_input(menu_mouse_pos):
                    play_button_clicked()
                elif options_button.check_for_input(menu_mouse_pos):
                    options_button_clicked()
                elif quit_button.check_for_input(menu_mouse_pos):
                    quit_button_clicked()
        pygame.display.flip()






