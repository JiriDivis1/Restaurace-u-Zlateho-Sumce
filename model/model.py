import pygame
import math
import json
import os

"""
Tato metoda vrátí velikost (width, height), aby zůstal zachovaný poměr stran, width je požadovaná šířka
"""
def get_new_size_by_height(picture, height):
    new_size = (picture.get_width() / picture.get_height(), 1)
    return (math.floor(new_size[0] * height), math.floor(new_size[1] * height))

def get_new_size_by_width(picture, width):
    new_size = (1, picture.get_height() / picture.get_width())
    return (math.floor(new_size[0] * width), math.floor(new_size[1] * width))

settings_file = open(os.path.join('model', 'Data', 'Settings', 'settings.json'))
settings_data = json.load(settings_file)

actual_event = "start_menu"  # Proměnná ve které je uložená aktuální událost ve hře (startMenu, settings, selectPlayer, ...)
running = True  # False = konec hry
clock = pygame.time.Clock()  # FPS

"""
KONSTANTY
"""
FPS = 60
WIDTH = settings_data['width']
HEIGHT = settings_data['height']
IS_SCREEN_RESIZABLE = settings_data['is_resizable']
IS_FULLSCREEN = settings_data['is_fullscreen']

BUTTON_WIDTH = WIDTH // 4
BUTTON_HEIGHT = BUTTON_WIDTH // 3.5

CHANGE_PEOPLE = 10  # konstanta určující jak moc se má měnit velikost lidí při pohybu po ose y
SPEED_OF_PEOPLES = 7  # rychlost pohybu lidí

"""
BARVY
"""
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
LIGHT_GRAY = (190, 190, 190)
GRAY = (42, 42, 42)
BLACK = (0, 0, 0)
TRANSPARENT = (255, 255, 255, 128)

"""
OBRÁZKY
"""
# ICON = pygame.image.load('model\Data\Pictures\icon.png')

# MENU
WOODEN_TEXTURE = pygame.image.load(
    os.path.join('model', 'Data', 'Pictures', 'Menu', 'Start_menu', 'wooden_texture.jpg'))
WOODEN_TEXTURE = pygame.transform.rotate(WOODEN_TEXTURE, 90)
WOODEN_TEXTURE = pygame.transform.scale(WOODEN_TEXTURE, (int(WIDTH // 3), int(HEIGHT)))
YELLOW_BUTTON = pygame.image.load(os.path.join('model', 'Data', 'Pictures', 'Menu', 'Start_menu', 'yellow_button.png'))
YELLOW_BUTTON = pygame.transform.scale(YELLOW_BUTTON, (int(BUTTON_WIDTH), int(BUTTON_HEIGHT)))
GOLD_BUTTON = pygame.image.load(os.path.join('model', 'Data', 'Pictures', 'Menu', 'Start_menu', 'gold_button.png'))
GOLD_BUTTON = pygame.transform.scale(GOLD_BUTTON, (int(BUTTON_WIDTH), int(BUTTON_HEIGHT)))
PRESS_BUTTON = pygame.image.load(os.path.join('model', 'Data', 'Pictures', 'Menu', 'Start_menu', 'press_button.png'))
PRESS_BUTTON = pygame.transform.scale(PRESS_BUTTON, (int(BUTTON_WIDTH), int(BUTTON_HEIGHT)))

"""
Restaurace
"""

# Písmena, která lze používat v identifikaci uzlu
letters = {
    'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6, 'g': 7, 'h': 8,
    'i': 9, 'j': 10, 'k': 11, 'l': 12, 'm': 13, 'n': 14, 'o': 15, 'p': 16,
    'q': 17, 'r': 18, 's': 19, 't': 20, 'u': 21, 'v': 22, 'w': 23, 'x': 24,
    'y': 25, 'z': 26, 'A': 27, 'B': 28, 'C': 29, 'D': 30, 'E': 31, 'F': 32

}

# Předchozí a následující písmeno jednotlivých písmen
prev_next_letter = {
    'a': [None, 'b'], 'b': ['a', 'c'], 'c': ['b', 'd'], 'd': ['c', 'e'], 'e': ['d', 'f'], 'f': ['e', 'g'],
    'g': ['f', 'h'], 'h': ['g', 'i'],
    'i': ['h', 'j'], 'j': ['i', 'k'], 'k': ['j', 'l'], 'l': ['k', 'm'], 'm': ['l', 'n'], 'n': ['m', 'o'],
    'o': ['n', 'p'], 'p': ['o', 'q'],
    'q': ['p', 'r'], 'r': ['q', 's'], 's': ['r', 't'], 't': ['s', 'u'], 'u': ['t', 'v'], 'v': ['u', 'w'],
    'w': ['v', 'x'], 'x': ['w', 'y'],
    'y': ['x', 'z'], 'z': ['y', 'A'], 'A': ['z', 'B'], 'B': ['A', 'C'], 'C': ['B', 'D'], 'D': ['C', 'E'],
    'E': ['D', 'F'], 'F': ['E', None]
}

COUNT_OF_ROWS, COUNT_OF_COLS = 9, 16

MAX_PEOPLE_START_HEIGHT = HEIGHT // 4
MAX_PEOPLE_START_WIDTH = MAX_PEOPLE_START_HEIGHT // 3
MIN_PEOPLE_START_HEIGHT = HEIGHT // 4
MIN_PEOPLE_START_WIDTH = MIN_PEOPLE_START_HEIGHT // 3
# COSTUMER1 = pygame.image.load(os.path.join('Data', 'Pictures', 'Peoples', 'Waiters', 'Waitress_basic_F.png'))

LEFT_CORNER = 248           #Levý roh místnosti (vzdálenost od SCREEN.left)
RIGHT_CORNER = 210          #Pravý roh (vzdálenost od SCREEN.right)

#Šířka obdélníku (uzlu)
FLOOR_NODES_WIDTH = WIDTH - LEFT_CORNER - RIGHT_CORNER
side_width = FLOOR_NODES_WIDTH // COUNT_OF_COLS

#Výška menu ve hře
MENU_HEIGHT = WIDTH // 6

"""
Objekty v restauraci
"""
FLOOR = pygame.image.load(os.path.join('model', 'Data', 'Pictures', 'Things', 'floor.png'))
#new_width, new_height = get_new_size_by_width(FLOOR, WIDTH)
FLOOR = pygame.transform.scale(FLOOR, (WIDTH, HEIGHT - MENU_HEIGHT))
WALLS = pygame.image.load(os.path.join('model', 'Data', 'Pictures', 'Things', 'walls.png'))
new_width, new_height = get_new_size_by_width(WALLS, WIDTH)
WALLS = pygame.transform.scale(WALLS, (new_width, new_height))
TABLE12 = pygame.image.load(os.path.join('model', 'Data', 'Pictures', 'Things', 'table12.png'))
new_width, new_height = get_new_size_by_width(TABLE12, WIDTH)
TABLE12 = pygame.transform.scale(TABLE12, (new_width, new_height))
CHAIR11 = pygame.image.load(os.path.join('model', 'Data', 'Pictures', 'Things', 'chair11.png'))
new_width, new_height = get_new_size_by_width(CHAIR11, WIDTH)
CHAIR11 = pygame.transform.scale(CHAIR11, (new_width, new_height))
CHAIR12 = pygame.image.load(os.path.join('model', 'Data', 'Pictures', 'Things', 'chair12.png'))
new_width, new_height = get_new_size_by_width(CHAIR12, WIDTH)
CHAIR12 = pygame.transform.scale(CHAIR12, (new_width, new_height))

TOP_FLOOR = pygame.mask.from_surface(FLOOR).get_bounding_rects()[0].top
FLOOR_MEDIAN = (WIDTH - LEFT_CORNER - RIGHT_CORNER) // 2

#Výška obdélníku/uzlu
FLOOR_NODES_HEIGHT = HEIGHT - TOP_FLOOR - MENU_HEIGHT
side_height = FLOOR_NODES_HEIGHT // COUNT_OF_ROWS

"""for image in imagesOfRestaurantObjects:
    new_size = get_new_size_by_width(image[1], WIDTH)
    image[1] = pygame.transform.scale(image[1], (new_size))"""

WAITER_BASIC_D = pygame.image.load(
    os.path.join('model', 'Data', 'Pictures', 'Peoples', 'Waiters', 'waiter_basic_D.png'))
new_size = get_new_size_by_height(WAITER_BASIC_D, HEIGHT // 2)
WAITER_BASIC_D = pygame.transform.scale(WAITER_BASIC_D, new_size)
WAITER_BASIC_DL = pygame.image.load(
    os.path.join('model', 'Data', 'Pictures', 'Peoples', 'Waiters', 'waiter_basic_DL.png'))
new_size = get_new_size_by_height(WAITER_BASIC_DL, HEIGHT // 2)
WAITER_BASIC_DL = pygame.transform.scale(WAITER_BASIC_DL, new_size)
WAITER_BASIC_L = pygame.image.load(
    os.path.join('model', 'Data', 'Pictures', 'Peoples', 'Waiters', 'waiter_basic_L.png'))
new_size = get_new_size_by_height(WAITER_BASIC_L, HEIGHT // 2)
WAITER_BASIC_L = pygame.transform.scale(WAITER_BASIC_L, new_size)
WAITER_BASIC_UL = pygame.image.load(
    os.path.join('model', 'Data', 'Pictures', 'Peoples', 'Waiters', 'waiter_basic_UL.png'))
new_size = get_new_size_by_height(WAITER_BASIC_UL, HEIGHT // 2)
WAITER_BASIC_UL = pygame.transform.scale(WAITER_BASIC_UL, new_size)
WAITER_BASIC_U = pygame.image.load(
    os.path.join('model', 'Data', 'Pictures', 'Peoples', 'Waiters', 'waiter_basic_U.png'))
new_size = get_new_size_by_height(WAITER_BASIC_U, HEIGHT // 2)
WAITER_BASIC_U = pygame.transform.scale(WAITER_BASIC_U, new_size)
WAITER_BASIC_UR = pygame.image.load(
    os.path.join('model', 'Data', 'Pictures', 'Peoples', 'Waiters', 'waiter_basic_UR.png'))
new_size = get_new_size_by_height(WAITER_BASIC_UR, HEIGHT // 2)
WAITER_BASIC_UR = pygame.transform.scale(WAITER_BASIC_UR, new_size)
WAITER_BASIC_R = pygame.image.load(
    os.path.join('model', 'Data', 'Pictures', 'Peoples', 'Waiters', 'waiter_basic_R.png'))
new_size = get_new_size_by_height(WAITER_BASIC_R, HEIGHT // 2)
WAITER_BASIC_R = pygame.transform.scale(WAITER_BASIC_R, new_size)
WAITER_BASIC_DR = pygame.image.load(
    os.path.join('model', 'Data', 'Pictures', 'Peoples', 'Waiters', 'waiter_basic_DR.png'))
new_size = get_new_size_by_height(WAITER_BASIC_DR, HEIGHT // 2)
WAITER_BASIC_DR = pygame.transform.scale(WAITER_BASIC_DR, new_size)

WAITRESS_BASIC_D = pygame.image.load(
    os.path.join('model', 'Data', 'Pictures', 'Peoples', 'Waiters', 'waitress_basic_D.png'))
new_size = get_new_size_by_height(WAITRESS_BASIC_D, HEIGHT // 2)
WAITRESS_BASIC_D = pygame.transform.scale(WAITRESS_BASIC_D, new_size)
WAITRESS_BASIC_DL = pygame.image.load(
    os.path.join('model', 'Data', 'Pictures', 'Peoples', 'Waiters', 'waitress_basic_DL.png'))
new_size = get_new_size_by_height(WAITRESS_BASIC_DL, HEIGHT // 2)
WAITRESS_BASIC_DL = pygame.transform.scale(WAITRESS_BASIC_DL, new_size)
WAITRESS_BASIC_L = pygame.image.load(
    os.path.join('model', 'Data', 'Pictures', 'Peoples', 'Waiters', 'waitress_basic_L.png'))
new_size = get_new_size_by_height(WAITRESS_BASIC_L, HEIGHT // 2)
WAITRESS_BASIC_L = pygame.transform.scale(WAITRESS_BASIC_L, new_size)
WAITRESS_BASIC_UL = pygame.image.load(
    os.path.join('model', 'Data', 'Pictures', 'Peoples', 'Waiters', 'waitress_basic_UL.png'))
new_size = get_new_size_by_height(WAITRESS_BASIC_UL, HEIGHT // 2)
WAITRESS_BASIC_UL = pygame.transform.scale(WAITRESS_BASIC_UL, new_size)
WAITRESS_BASIC_U = pygame.image.load(
    os.path.join('model', 'Data', 'Pictures', 'Peoples', 'Waiters', 'waitress_basic_U.png'))
new_size = get_new_size_by_height(WAITRESS_BASIC_U, HEIGHT // 2)
WAITRESS_BASIC_U = pygame.transform.scale(WAITRESS_BASIC_U, new_size)
WAITRESS_BASIC_UR = pygame.image.load(
    os.path.join('model', 'Data', 'Pictures', 'Peoples', 'Waiters', 'waitress_basic_UR.png'))
new_size = get_new_size_by_height(WAITRESS_BASIC_UR, HEIGHT // 2)
WAITRESS_BASIC_UR = pygame.transform.scale(WAITRESS_BASIC_UR, new_size)
WAITRESS_BASIC_R = pygame.image.load(
    os.path.join('model', 'Data', 'Pictures', 'Peoples', 'Waiters', 'waitress_basic_R.png'))
new_size = get_new_size_by_height(WAITRESS_BASIC_R, HEIGHT // 2)
WAITRESS_BASIC_R = pygame.transform.scale(WAITRESS_BASIC_R, new_size)
WAITRESS_BASIC_DR = pygame.image.load(
    os.path.join('model', 'Data', 'Pictures', 'Peoples', 'Waiters', 'waitress_basic_DR.png'))
new_size = get_new_size_by_height(WAITRESS_BASIC_DR, HEIGHT // 2)
WAITRESS_BASIC_DR = pygame.transform.scale(WAITRESS_BASIC_DR, new_size)

"""
Ostatní
"""

CHECK_MARK = pygame.image.load(os.path.join('model', 'Data', 'Pictures', 'Others', 'check_mark.png'))
CHECK_MARK = pygame.transform.scale(CHECK_MARK, (WIDTH // 20, WIDTH // 20))

"""
FONTY
"""
pygame.font.init()  # načtení fontu
header_font1 = pygame.font.SysFont("cambria", HEIGHT // 10)
header_font2 = pygame.font.SysFont("cambria", HEIGHT // 12)
text_font = pygame.font.SysFont("cambria", 40)
important_font = pygame.font.SysFont("cambria", 200)
node_font = pygame.font.SysFont("cambria", side_height // 2)

"""
OBRAZOVKA
"""
# os.environ['SDL_VIDEO_CENTERED'] = '1'
# info = pygame.display.Info()
# SCREEN_WIDTH, SCREEN_HEIGHT = info.current_w, info.current_h
# SCREEN = pygame.display.set_mode((SCREEN_WIDTH - 10, SCREEN_HEIGHT - 50))
if IS_FULLSCREEN:
    SCREEN = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
elif IS_SCREEN_RESIZABLE:
    SCREEN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
else:
    SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Restaurace u Zlatého Sumce")
# pygame.display.set_icon(icon)