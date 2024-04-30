import pygame
import time
import os
import json

from model import *
from Profile import *
from ObjectsInRestaurant import *
from Graph import *

class Game():
    def __init__(self, profile_id, character_gender, level_id, money, buy_stuff):
        self.profile_id = profile_id                        # id profilu, pro který je hra sputěna
        self.character_gender = character_gender            # Pohlaví postavy v tomto levelu
        self.level_id = level_id                            # id levelu, který bude spuštěn
        self.money = money                                  # Částka, kolik máme aktuálně vyděláno (v tomto levelu)
        self.buy_stuff = buy_stuff                          # Věci které máme koupené
        self.objects_in_restaurant = []                     # objekty, které budeme ve hře zobrazovat. Koupené věci + minimální potřebné objekty z levelu
        self.waiter = None                                  # Postava, za kterou bude hráč hrát
        self.init_objects = False                           # Byla provedena inicializace objektů?
        self.graph = None

    def get_profile_id(self):
        return self.profile_id

    def get_character_gender(self):
        return self.character_gender

    def get_level_id(self):
        return self.level_id

    def get_money(self):
        return self.money

    def set_money(self, money):
        self.money = money
        return self

    def get_buy_stuff(self):
        return self.buy_stuff

    def get_objects_in_restaurant(self):
        return self.objects_in_restaurant

    def set_objects_in_restaurant(self, objects_in_restaurant):
        self.objects_in_restaurant = objects_in_restaurant
        return self

    """
    Vrátí objekt typu Waiter, který reprezentuje postavu"""
    def get_waiter(self):
        return self.waiter

    def get_init_objects(self):
        return self.init_objects

    def set_init_objects(self, init_objects):
        self.init_objects = init_objects
        return self

    def get_graph(self):
        return self.graph

    def set_graph(self, graph):
        self.graph = graph
        return self

    """
    Třídící algoritmus pro změnu pořadí vykreslení objektů (Kvůli jejich správnému překrytí)"""
    def insertion_sort(self):
        obj_in_restaurant = self.get_objects_in_restaurant()
        length = len(obj_in_restaurant)
        if length <= 1:
            return
        for i in range(1, length):
            key = obj_in_restaurant[i].get_priority()
            j = i - 1
            while j > key < obj_in_restaurant[j].get_priority():
                obj_in_restaurant[j + 1] = obj_in_restaurant[j]
                j -= 1
            obj_in_restaurant[j + 1] = obj_in_restaurant[i]

    """
    Vrátí index daného objektu, pokud index není, vrátí -1"""
    def get_index_of_game_objects(self, objName):
        game_objects = self.get_objects_in_restaurant()
        index = 0
        for obj in game_objects:
            if obj.get_name() == objName:
                return index
            index += 1
        return -1

    """
    Načte data z json souboru, obsahující data ohledně spuštěného levelu"""
    def load_data_from_level_file(self):
        pass

    """
    Vykonání všech úloh potřebných pro vykonání hry (Načtení dat z disku. Vytvoření pole objektů. Grafu, který 
    budeme procházet pomocí A* algoritmu)"""
    def init_objects_fun(self):
        disusable_nodes_file = open(os.path.join('model', 'Data', 'Levels', 'disusable_nodes.json'))
        disusable_nodes = json.load(disusable_nodes_file)

        graph = Graph(disusable_nodes)

        start_node_x, start_node_y = graph.get_node_indexes("ab")
        start_node_position = graph.get_nodes()[start_node_x][start_node_y].get_node_center_pos()
        start_node_x, start_node_y = graph.convert_node_point_to_area_point(start_node_position[0], start_node_position[1])

        objects_in_restaurant = []
        objects_in_restaurant.append(ObjectInRestaurant("FLOOR", FLOOR, 0, 0, 0))
        #objects_in_restaurant.append(ObjectInRestaurant("WALLS", WALLS, 0, 0, 0))
        #objects_in_restaurant.append(ObjectInRestaurant("CHAIR11", CHAIR11, 0, 0, 0))
        #objects_in_restaurant.append(ObjectInRestaurant("TABLE12", TABLE12, 0, 0, 0))
        #objects_in_restaurant.append(ObjectInRestaurant("CHAIR12", CHAIR12, 0, 0, 0))

        # bar = ObjectInRestaurant(BAR, 2, 0, 0)

        if self.get_character_gender() == "M":
            self.waiter = Waiter("WAITER", WAITER_BASIC_D, 0, start_node_x, start_node_y, "M")
            new_size = get_new_size_by_height(WAITER_BASIC_D, self.waiter.get_basic_height())
            self.waiter.set_image(pygame.transform.scale(WAITER_BASIC_D, new_size))
        else:
            self.waiter = Waiter("WAITER", WAITRESS_BASIC_D, 0, start_node_x, start_node_y, "F")
            new_size = get_new_size_by_height(WAITRESS_BASIC_D, self.waiter.get_basic_height())
            self.waiter.set_image(pygame.transform.scale(WAITRESS_BASIC_D, new_size))
        self.waiter.set_rect(self.waiter.get_image().get_rect(topleft=(self.waiter.get_x_pos(), self.waiter.get_y_pos())))
        self.waiter.get_rect().centerx = self.waiter.get_x_pos()
        self.waiter.get_rect().bottom = self.waiter.get_y_pos()

        #objects_in_restaurant.append(waiter)
        self.set_objects_in_restaurant(objects_in_restaurant)

        self.set_init_objects(True)
        self.set_graph(graph)
    """
    Spuštění samotné hry"""
    def start_game(self):
        if not self.get_init_objects():
            self.init_objects_fun()

        SCREEN.fill(WHITE)

        for obj in self.get_objects_in_restaurant():
            obj.draw_object()

        #Vykreslení uzlů v prostoru

        # Vykreslení uzlů v prostoru ...
        for i in range(COUNT_OF_ROWS):
            for j in range(COUNT_OF_COLS):
                act_node = self.get_graph().get_nodes()[i][j]

                if act_node.get_is_usable():
                    act_node.draw_area(TRANSPARENT)
                else:
                    act_node.draw_area(GRAY)

        waiter = self.get_waiter()
        waiter.draw_object()

        waiter.execute_movement()

    """
    Ukončení hry, uložení všech dat"""
    def end_game(self):
        pass

    """
    Pauznutí hry"""
    def start_pause(self):
        pass

    """
    Ukončení pauzy"""
    def end_pause(self):
        pass

"""
#Změní velikost obrázků všech objektů, používá se při změně velikosti obrazovky
def change_size_of_image():
    global game_objects
    for obj in game_objects:
        new_size = get_new_size_by_width(image[1], pygame.display.get_surface().get_width())
        obj.set_image(pygame.transform.scale(obj.get_image(), (new_size)))
"""