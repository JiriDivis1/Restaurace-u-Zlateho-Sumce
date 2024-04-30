import pygame
import time
import sys
import math
import json
import os

sys.path.insert(1, 'views')
sys.path.insert(1, 'model')

from model import *
from menus import *
from settings import *
from Game import *
from Profiles import *



"""
Pomocné funkce
"""

"""
Zpracuje vstupy uživatelů"""
class Controller(object):
    def __init__(self):
        self.profiles = Profiles()
        self.set_usable_nodes = False

    def events(self, events):
        global SCREEN
        global WIDTH, HEIGHT
        global actual_event

        global settings_width
        global settings_height
        global settings_is_resizable
        global settings_is_fullscreen

        for event in events:

            if event.type == pygame.QUIT:
                return False
            # Změna velikosti obrazovky
            if event.type == pygame.VIDEORESIZE:
                new_width, new_height = pygame.display.get_surface().get_size()
                # výšku přizpůsobíme šířce
                if new_width != WIDTH:
                    WIDTH = new_width
                    HEIGHT = math.floor((9 / 16) * new_width)
                # šířku přizpůsobíme výšce
                elif new_height != HEIGHT:
                    HEIGHT = new_height
                    WIDTH = math.floor((16 / 9) * new_height)
                SCREEN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)

                changeSizeOfImages()

            # Hlavní menu
            if actual_event == "start_menu":
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # 1 = levé tlačítko na myši
                    if play_game_button.isButtonClicked(pygame.mouse.get_pos()):
                        actual_event = "select_player"
                        # loadPlayers()
                    elif settings_button.isButtonClicked(pygame.mouse.get_pos()):
                        actual_event = "settings"
                        continue
                    elif end_game.isButtonClicked(pygame.mouse.get_pos()):
                        SCREEN.fill(WHITE)
                        back_text = header1Font.render("Na shledanou, přijďte zas", True, RED)
                        back_text_rect = back_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
                        SCREEN.blit(back_text, back_text_rect)
                        pygame.display.update()
                        time.sleep(2)
                        return False
            # Nastavení
            if actual_event == "settings":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        actual_event = "start_menu"
                        continue
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    click_position = event.pos
                    # Nastavení obrazovky na resizable nebo naopak
                    if click_position[0] in range(30, 30 + WIDTH // 20) and click_position[1] in range(WIDTH // 10,
                                                                                                       WIDTH // 10 + WIDTH // 20):
                        change_is_resizable()
                    # Nastavení fullscreen obrazovky nebo naopak
                    if click_position[0] in range(30, 30 + WIDTH // 20) and click_position[1] in range(
                            WIDTH // 8 + WIDTH // 20, WIDTH // 8 + WIDTH // 20 + WIDTH // 20):
                        change_is_fullscreen()
                    # Uložit změny
                    elif save_button.isButtonClicked(pygame.mouse.get_pos()):
                        is_resizable = get_is_resizable()
                        is_fullscreen = get_is_fullscreen()
                        if is_resizable:
                            SCREEN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
                        else:
                            SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))

                        if is_fullscreen:
                            SCREEN = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                            WIDTH, HEIGHT = pygame.display.get_surface().get_size()
                            settings_width, settings_height = pygame.display.get_surface().get_size()
                        else:
                            WIDTH, HEIGHT = 1280, 720
                            settings_width, settings_height = 1280, 720
                            if is_resizable:
                                SCREEN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
                            else:
                                SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))

                        screen_settings = {
                            "width": settings_width,
                            "height": settings_height,
                            "is_resizable": is_resizable,
                            "is_fullscreen": is_fullscreen
                        }
                        json_object = json.dumps(screen_settings, indent=4)

                        with open(os.path.join('model', 'Data', 'Settings', 'settings.json'), "w") as outfile:
                            outfile.write(json_object)

            # Výběr hráčů
            if actual_event == "select_player":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_b:
                        actual_event = "start_menu"
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if alpha_version_button.isButtonClicked(pygame.mouse.get_pos()):
                        actual_event = "select_character"
                        continue
            # Výběr postavy
            if actual_event == "select_character":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_b:
                        actual_event = "start_menu"
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    # Zacatek hry + nastavení postavy
                    if waiter_button.isButtonClicked(pygame.mouse.get_pos()) or waiter_image_button.isButtonClicked(
                            pygame.mouse.get_pos()):
                        self.profiles.get_actual_profile().set_character_gender("M")
                        print("Hraješ za číšníka")
                        actual_event = "game"
                        continue
                    if waitress_button.isButtonClicked(pygame.mouse.get_pos()) or waitress_image_button.isButtonClicked(
                            pygame.mouse.get_pos()):
                        self.profiles.get_actual_profile().set_character_gender("F")
                        print("Hraješ za číšnici")
                        actual_event = "game"
                        continue

            """
            SAMOTNÁ HRA---------------------EVENTY-----------"""
            if actual_event == "game":
                game = self.profiles.get_actual_profile().get_game()
                if game:
                    graph = game.get_graph()
                    waiter = game.get_waiter()
                else:
                    waiter = None
                    graph = None
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        actual_event = "start_menu"
                        continue

                if event.type == pygame.KEYDOWN and event.key == pygame.K_n:
                    if self.set_usable_nodes:
                        self.set_usable_nodes = False
                        with open(os.path.join('model', 'Data', 'Levels', 'disusable_nodes.json'), "w") as json_file:
                            json.dump(graph.get_disusable_nodes(), json_file)
                    else:
                        self.set_usable_nodes = True
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    click_position = event.pos
                    for obj in game.get_objects_in_restaurant():
                        if obj.get_name() == "WALLS" and obj.is_clicked(click_position):
                            print("klikl jsi na stěnu")
                        elif obj.get_name() == "TABLE12" and obj.is_clicked(
                                click_position) or obj.get_name() == "CHAIR11" and obj.is_clicked(
                                click_position) or obj.get_name() == "CHAIR12" and obj.is_clicked(click_position):
                            print("klikl jsi na stůl")
                        elif obj.get_name() == "FLOOR" and obj.is_clicked(click_position) and not self.set_usable_nodes:
                            print("klikl jsi na podlahu")

                            # Zjistíme id uzlu, na který jsme klikli
                            dest_node = graph.get_node_on_position(click_position)
                            click_position = graph.convert_area_point_to_node_point(click_position[0],
                                                                                    click_position[1])

                            dest_node_id = dest_node.get_node_id()

                            # Klikli jsme na nepoužitelný uzel
                            if not dest_node.get_is_usable():
                                print("Sem nelze jít, jedná se o překážku")
                            else:
                                # Zjistíme na kterém uzlu se nacházíme
                                source_position = waiter.get_positions()
                                source_node = graph.get_node_on_position(source_position)
                                dest_positions = []

                                if source_node.is_clicked(
                                        graph.convert_area_point_to_node_point(source_position[0], source_position[1])):
                                    source_node_id = source_node.get_node_id()

                                    if source_node_id == dest_node_id:
                                        click_position = graph.convert_node_point_to_area_point(click_position[0],
                                                                                                click_position[1])
                                        if source_position[0] <= click_position[0]:
                                            waiter.set_direct_x(SPEED_OF_PEOPLES)
                                        else:
                                            waiter.set_direct_x(-1 * SPEED_OF_PEOPLES)

                                        if source_position[1] <= click_position[1]:
                                            waiter.set_direct_y(SPEED_OF_PEOPLES)
                                        else:
                                            waiter.set_direct_y(-1 * SPEED_OF_PEOPLES)

                                        dest_positions.append(click_position)
                                        waiter.set_dest_positions(dest_positions)
                                        waiter.set_is_walking(True)
                                        break

                                    dest_nodes = graph.a_star_algorithm(source_node_id, dest_node_id)

                                    # Odstranění chybných uzlů
                                    dest_nodes = graph.dest_nodes_filter(dest_nodes)

                                    for dest_node in dest_nodes:
                                        node_indexes = graph.get_node_indexes(dest_node)
                                        node = graph.get_nodes()[node_indexes[0]][node_indexes[1]]
                                        node_point = graph.convert_node_point_to_area_point(
                                            node.get_node_center_pos()[0], node.get_node_center_pos()[1])
                                        dest_positions.append(node_point)

                                    dest_positions.append(
                                        graph.convert_node_point_to_area_point(click_position[0], click_position[1]))

                                    waiter.set_dest_positions(dest_positions)
                                    waiter.set_is_walking(True)

                                    first_dest = dest_positions[0]

                                    # Určíme, zda se hráč má posouvat nahoru, ...
                                    if source_position[0] <= first_dest[0]:
                                        waiter.set_direct_x(SPEED_OF_PEOPLES)
                                    # ... nebo dolů
                                    else:
                                        waiter.set_direct_x(-1 * SPEED_OF_PEOPLES)

                                    # Určíme, zda se hráč má posouvat doprava, ...
                                    if source_position[1] <= first_dest[1]:
                                        waiter.set_direct_y(SPEED_OF_PEOPLES)
                                    # ... nebo doleva
                                    else:
                                        waiter.set_direct_y(-1 * SPEED_OF_PEOPLES)
                                    break
                            """
                            source_position = waiter.get_source_position()
                            subfinal_position = (None, None)
                            waiter.set_is_walking(True)

                            # Půjdeme doprava
                            if source_position[0] <= click_position[0]:
                                direct_x = SPEED_OF_PEOPLES
                            # Půjdeme doleva
                            else:
                                direct_x = -1 * SPEED_OF_PEOPLES

                            # Půjdeme dolů
                            if source_position[1] <= click_position[1]:
                                direct_y = SPEED_OF_PEOPLES
                            # Půjdeme nahoru
                            else:
                                direct_y = -1 * SPEED_OF_PEOPLES

                            waiter.set_movement(click_position, subfinal_position, direct_x, direct_y)
                            """
                        #Změna použitých uzlů na nepoužitelné a obráceně
                        elif obj.get_name() == "FLOOR" and obj.is_clicked(
                                click_position) and self.set_usable_nodes:
                            click_position = pygame.mouse.get_pos()
                            click_node = graph.get_node_on_position(click_position)

                            # Změna z použitelného na nepoužitelný
                            if click_node.get_is_usable():
                                click_node.set_is_usable(False)
                                graph.get_disusable_nodes().append(click_node.get_node_id())
                                # Nastavení sousedů click_node
                                graph.set_neighbours_of(click_node)
                            # Změna z nepoužitelného na použitelný
                            else:
                                click_node.set_is_usable(True)
                                graph.get_disusable_nodes().remove(click_node.get_node_id())
                                graph.set_neighbours_for(click_node)
                                # Nastavení sousedů click_node
                                graph.set_neighbours_of(click_node)

        if actual_event == "start_menu":
            start_menu()
        # alphaVerze tlačítko
        elif actual_event == "select_player":
            select_player()
        elif actual_event == "select_character":
            select_character()
        elif actual_event == "settings":
            settings()
        elif actual_event == "game":
            self.profiles.get_actual_profile().start_game()

        # pygame.display.update()
        return True