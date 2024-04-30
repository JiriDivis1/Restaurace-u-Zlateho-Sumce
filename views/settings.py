import pygame

from model import *
from Button import *

#promenné které obsahují hodnoty změněné, ale ještě neuložené, ty se uloží po stisknutí tlačítka
settings_width = WIDTH
settings_height = HEIGHT
settings_is_resizable = IS_SCREEN_RESIZABLE
settings_is_fullscreen = IS_FULLSCREEN

save_button = Button(YELLOW_BUTTON, int(WIDTH * 0.75), int(HEIGHT * 0.85), "Uložit změny")

def get_is_resizable():
    global settings_is_resizable
    return settings_is_resizable

def change_is_resizable():
    global settings_is_resizable
    if settings_is_resizable:
        settings_is_resizable = False
    else:
        settings_is_resizable = True

def get_is_fullscreen():
    global settings_is_fullscreen
    return settings_is_fullscreen

def change_is_fullscreen():
    global settings_is_fullscreen
    if settings_is_fullscreen:
        settings_is_fullscreen = False
    else:
        settings_is_fullscreen = True

def settings():
    global settings_is_resizable
    global settings_is_fullscreen
    actual_event = "settings"
    SCREEN.fill(WHITE)
    headerText = header_font1.render("Nastavení", True, BLACK)
    headerText_rect = headerText.get_rect(topleft = (0, 0))
    SCREEN.blit(headerText, headerText_rect)
    resizableText = text_font.render("Povolit manuální změnu velikosti obrazovky", True, BLACK)
    resizableText_rect = resizableText.get_rect(topleft = (60 + WIDTH // 20, WIDTH // 10))
    SCREEN.blit(resizableText, resizableText_rect)
    fullscreenText = text_Font.render("Celá obrazovka", True, BLACK)
    fullscreenText_rect = fullscreenText.get_rect(topleft = (60 + WIDTH // 20, WIDTH // 8 + WIDTH // 20))
    SCREEN.blit(fullscreenText, fullscreenText_rect)
    pygame.draw.rect(SCREEN, BLACK, pygame.Rect(30, WIDTH // 10, WIDTH // 20, WIDTH // 20), 10)
    pygame.draw.rect(SCREEN, BLACK, pygame.Rect(30, WIDTH // 8 + WIDTH // 20, WIDTH // 20, WIDTH // 20), 10)
    save_button.drawButton()
    save_button.button_hover(pygame.mouse.get_pos(), GOLD_BUTTON)
    if settings_is_resizable:
        SCREEN.blit(CHECK_MARK, (30, WIDTH // 10))
    if settings_is_fullscreen:
        SCREEN.blit(CHECK_MARK, (30, WIDTH // 8 + WIDTH // 20))