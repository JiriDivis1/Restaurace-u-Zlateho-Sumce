import pygame
import time

from model import *
from Profile import *
from Button import *

            
BUTTON_WIDTH = int(WIDTH // 2)

original_wooden_height = HEIGHT                         #pozice y wooden texture při spuštění
wooden_height = int(HEIGHT // 2 - HEIGHT * 0.1)         #pozice y wooden texture po přesunu

shift = original_wooden_height - wooden_height          #počet pixelů o kolik se menu posune

"""
TLAČÍTKA
"""
#start_menu
play_game_button = Button(YELLOW_BUTTON, BUTTON_WIDTH, int(HEIGHT * 0.55 + shift), "Hrát hru")
settings_button = Button(YELLOW_BUTTON, BUTTON_WIDTH, int(HEIGHT * 0.70 + shift), "Nastavení")
end_game = Button(YELLOW_BUTTON, BUTTON_WIDTH, int(HEIGHT * 0.85 + shift), "Ukončit hru")

#selectPlayer
alpha_version_button = Button(YELLOW_BUTTON, int(WIDTH * 0.75), int(HEIGHT * 0.85), "Alpha verze")

#selectCharacter
waiter_button = Button(YELLOW_BUTTON, int(WIDTH * 0.75), int(HEIGHT * 0.85), "Číšník")
waitress_button = Button(YELLOW_BUTTON, int(WIDTH * 0.25), int(HEIGHT * 0.85), "Číšnice")

waitress_image_button = Button(WAITRESS_BASIC_D, int(WIDTH * 0.25), HEIGHT // 2 - 30, None)
waiter_image_button = Button(WAITER_BASIC_D, int(WIDTH * 0.75), HEIGHT // 2 - 30, None )

def start_menu():
    global original_wooden_height
    actual_event = "start_menu"
    SCREEN.fill(WHITE)
    WOODEN_TEXTURE_RECT = WOODEN_TEXTURE.get_rect(topleft = (int(WIDTH // 2 - (WIDTH // 3) // 2), original_wooden_height))
    SCREEN.blit(WOODEN_TEXTURE, WOODEN_TEXTURE_RECT)
    play_game_button.draw_button()
    play_game_button.button_hover(pygame.mouse.get_pos(), GOLD_BUTTON)
    settings_button.draw_button()
    settings_button.button_hover(pygame.mouse.get_pos(), GOLD_BUTTON)
    end_game.draw_button()
    end_game.button_hover(pygame.mouse.get_pos(), GOLD_BUTTON)
    
#PŘÍCHOD MENU ZE SPODU NA HORU
    if original_wooden_height >= wooden_height:
        speed = 6
        original_wooden_height -= speed
        play_game_button.get_rect().y -= speed
        play_game_button.get_text_rect().y -= speed
        settings_button.get_rect().y -= speed
        settings_button.get_text_rect().y -= speed
        end_game.get_rect().y -= speed
        end_game.get_text_rect().y -= speed
        
def select_player():
    actual_event = "select_player"
    
    SCREEN.fill(WHITE)
    headline = header_font1.render("Výběr hráčů", True, GREEN)
    headline_rect = headline.get_rect(topleft = (0, 0))
    SCREEN.blit(headline, headline_rect)
    description = text_font.render("Zatím nelze vytvořit profil, hraješ na profilu Default", True, BLACK)
    description_rect = description.get_rect(topleft = (0, 70))
    SCREEN.blit(description, description_rect)
    
    alpha_version_button.draw_button()
    alpha_version_button.button_hover(pygame.mouse.get_pos(), GOLD_BUTTON)
    
def player_menu():
    actual_event = "player_menu"
    SCREEN.fill(WHITE)
    
def select_character():
    actual_event = "select_character"
    SCREEN.fill(WHITE)
    headline = header_font1.render("Vyber si postavu", True, GREEN)
    headline_rect = headline.get_rect(topleft = (0, 0))
    
    SCREEN.blit(headline, headline_rect)
    waiter_image_button.draw_button()
    waiter_button.draw_button()
    waiter_button.button_hover(pygame.mouse.get_pos(), GOLD_BUTTON)
    
    waitress_image_button.draw_button()
    waitress_button.draw_button()
    waitress_button.button_hover(pygame.mouse.get_pos(), GOLD_BUTTON)
    
    #SCREEN.blit(WAITRESS_PHOTO, (waitress_button.get_rect().left, 100))
    
    
    