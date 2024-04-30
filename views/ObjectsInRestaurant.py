import pygame
import sys

from model import *

sys.path.insert(1, 'model')

"""
Třída reprezentující všechny objekty, vyskytující se v levelu"""
class ObjectInRestaurant():
    def __init__(self, name, image, priority, x_pos, y_pos):
        self.name = name
        self.image = image
        self.priority = priority  # priority - kvůli překrývání, objekty před vykreslením vložím do pole, to setřídím podle priority a poté až vykreslím
        self.x_pos = x_pos
        self.y_pos = y_pos
        if x_pos == 0 and y_pos == 0 and type(self) is not Waiter:
            self.rect = self.image.get_rect(topleft=(self.x_pos, self.y_pos))
        elif type(self) is Waiter:
            self.rect = self.image.get_rect(topleft=(self.x_pos, self.y_pos))
            self.rect.centerx = self.x_pos
            self.rect.bottom = self.y_pos
        else:
            self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))

        self.mask = pygame.mask.from_surface(self.image)

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name
        return self

    def get_image(self):
        return self.image

    def set_image(self, image):
        self.image = image
        return self

    def get_priority(self):
        return self.priority

    def set_priority(self, priority):
        self.priority = priority
        return self

    def get_x_pos(self):
        return self.x_pos

    def set_x_pos(self, x_pos):
        self.x_pos = x_pos
        return self

    def get_y_pos(self):
        return self.y_pos

    def set_y_pos(self, y_pos):
        self.y_pos = y_pos
        return self

    def get_rect(self):
        return self.rect

    def set_rect(self, rect):
        self.rect = rect
        return self

    def get_mask(self):
        return self.mask

    def draw_object(self):
        if type(self) == Waiter:
            SCREEN.blit(self.get_image(), self.get_rect())
            pygame.draw.rect(SCREEN, RED, self.get_collision_rect())
        else:
            SCREEN.blit(self.get_image(), self.get_rect())

    def is_clicked(self, position):
        pos_in_mask = position[0] - self.get_rect().x, position[1] - self.get_rect().y
        touching = self.get_rect().collidepoint(*position) and self.get_mask().get_at(pos_in_mask)
        return touching


# Číšník a zákazníci
class People(ObjectInRestaurant):
    def __init__(self, name, image, priority, x_pos, y_pos):
        super().__init__(name, image, priority, x_pos, y_pos)
        self.change_size = 0  # pomocná proměnná pro změnu velikosti lidí

        # Proměnné pro pohyb osoby
        self.source_position = self.get_rect().centerx, self.get_rect().bottom  # Pozice osoby při kliknutí myši
        self.final_position = (0, 0)  # Pozice kam se má osoba přesunout
        self.direct_x = 1  # označuje směr(doleva, doprava) a rychlost
        self.direct_y = 1  # označuje směr(nahoru, dolů) a rychlost

        self.state = "basic"  # stav ve kterém je číšník nebo zákazník (základní, nosí jídelníček, nosí jídlo, ...)
        self.profile = "D"  # profil (D - Down, U - Up)

    def get_change_size(self):
        return self.change_size

    def set_change_size(self, change_size):
        self.change_size = change_size
        return self

    def get_source_position(self):
        return (self.get_rect().centerx, self.get_rect().bottom)

    def get_final_position(self):
        return self.final_position

    def set_final_position(self, final_position):
        self.final_position = final_position
        return self

    def get_direct_x(self):
        return self.direct_x

    def set_direct_x(self, direct_x):
        self.direct_x = direct_x
        return self

    def get_direct_y(self):
        return self.direct_y

    def set_direct_y(self, direct_y):
        self.direct_y = direct_y
        return self

    def get_state(self):
        return self.state

    def set_state(self, state):
        self.state = state
        return self

    def get_profile(self):
        return self.profile

    def set_profile(self, profile):
        self.profile = profile
        return self

        # Signalizuje, jestli se má změnit velikost 1 = zvětšit, 0 = neměnit, -1 = zmenšit

    def check_change_size(self, offset):
        self.set_change_size(self.get_change_size() + offset)
        if self.get_change_size() == CHANGE_PEOPLE:
            self.set_change_size(0)
            return 1
        elif self.get_change_size() == -1 * CHANGE_PEOPLE:
            self.set_change_size(0)
            return -1
        else:
            return 0

class Waiter(People):
    def __init__(self, name, image, priority, x_pos, y_pos, gender):
        super().__init__(name, image, priority, x_pos, y_pos)
        self.gender = gender
        self.collision_rect = pygame.Rect((self.get_rect().left, self.get_rect().bottom - 10),
                                          (self.get_rect().width, 10))
        self.basic_height = HEIGHT // 4
        self.dest_positions = []            # Pole pozicí (x, y), na které se bude postava přesouvat
        self.direct_x = 1
        self.direct_y = 1
        self.signal_movement_x = False      # Signalizuje, jestli se postava pohybuje po ose x
        self.signal_movement_y = False      # Signalizuje, jestli se postava pohybuje po ose y, kvůli změně profilu
        self.is_walking = False


    def get_gender(self):
        return self.gender

    def set_gender(self, gender):
        self.gender = gender
        return self

    def get_collision_rect(self):
        return self.collision_rect

    def set_collision_rect(self, collision_rect):
        self.collision_rect = collision_rect
        return self

    def create_new_collision_rect(self):
        return pygame.Rect((self.get_rect().left, self.get_rect().bottom - 10), (self.get_rect().width, 10))

    def get_basic_height(self):
        return self.basic_height

    def get_positions(self):
        return (self.get_rect().centerx, self.get_rect().bottom)

    def get_mask(self):
        return self.mask

    def get_dest_positions(self):
        return self.dest_positions

    def set_dest_positions(self, dest_positions):
        self.dest_positions = dest_positions
        return self

    def get_direct_x(self):
        return self.direct_x

    def set_direct_x(self, direct_x):
        self.direct_x = direct_x
        return self

    def get_direct_y(self):
        return self.direct_y

    def set_direct_y(self, direct_y):
        self.direct_y = direct_y
        return self

    def get_signal_movement_x(self):
        return self.signal_movement_x

    def set_signal_movement_x(self, signal_movement_x):
        self.signal_movement_x = signal_movement_x
        return self

    def get_signal_movement_y(self):
        return self.signal_movement_y

    def set_signal_movement_y(self, signal_movement_y):
        self.signal_movement_y = signal_movement_y
        return self

    def get_is_walking(self):
        return self.is_walking

    def set_is_walking(self, is_walking):
        self.is_walking = is_walking
        return self

    # Vrátí True, pokud kolize a objekt, se kterým je kolize
    # % - zkoušet kolizi se všemi objekty, ne jenom s table2
    def check_collision(self):
        if self.get_collision_rect().colliderect(table2.get_rect()):
            return (True, table2.get_rect())
        else:
            return (False, waiter.get_rect())

    def get_direction(self):
        if len(self.get_dest_positions()) > 1:
            act_node = self.get_dest_positions()[0]
            next_node = self.get_dest_positions()[1]
            # Půjdeme nahoru nebo dolů
            if act_node[0] != next_node[0] and act_node[1] == next_node[1]:
                # Půjdeme nahoru
                if act_node[0] > next_node[0]:
                    print("Půjdeme nahoru")
                # Půjdeme dolů
                else:
                    print("Půjdeme dolů")
            # Půjdeme doprava nebo doleva
            elif act_node[0] == next_node[0] and act_node[1] != next_node[1]:
                # Půjdeme doleva
                if act_node[1] < next_node[1]:
                    print("Půjdeme doleva")
                # Půjdeme doprava
                else:
                    print("Půjdeme doprava")
            # Půjdeme do šikma
            elif act_node[0] != next_node[0] and act_node[1] != next_node[1]:
                # Půjdeme nahoru ...
                if act_node[0] < next_node[0]:
                    # ... a doprava
                    if act_node[1] < next_node[1]:
                        print("Půjdeme nahoru doprava")
                    # ... a doleva
                    else:
                        print("Půjdeme nahoru doleva")
                # Půjdeme dolů ...
                else:
                    # ... a doprava
                    if act_node[1] < next_node[1]:
                        print("Půjdeme dolů doprava")
                    # ... a doleva
                    else:
                        print("Půjdeme dolů doleva")

    """
    Metoda, která vykoná pohyb"""
    def execute_movement(self):
        is_walking = self.get_is_walking()
        waiter_gender = self.get_gender()

        if is_walking:
            dest_positions = self.get_dest_positions()
            act_dest_position = dest_positions[0]
            # Funkce move_x a move_y vrátí True, jakmile je pohyb dokončen
            #movement_x = self.move_x(act_dest_position[0])
            #movement_y = self.move_y(act_dest_position[1])

            if self.get_signal_movement_x() and self.get_signal_movement_y():
                # NahoruDoleva
                if self.get_direct_x() < 0 and self.get_direct_y() < 0:
                    if self.get_profile() != "UL":
                        if waiter_gender == "M":
                            new_waiter_picture = WAITER_BASIC_UL
                        else:
                            new_waiter_picture = WAITRESS_BASIC_UL
                        new_size = get_new_size_by_height(new_waiter_picture, self.get_basic_height())
                        self.set_image(pygame.transform.scale(new_waiter_picture, new_size))
                        self.set_rect(self.get_image().get_rect(topleft=(self.get_rect().x, self.get_rect().y)))
                        self.set_profile("UL")
                # NahoruDoprava
                elif self.get_direct_x() > 0 and self.get_direct_y() < 0:
                    if self.get_profile() != "UR":
                        if waiter_gender == "M":
                            new_waiter_picture = WAITER_BASIC_UR
                        else:
                            new_waiter_picture = WAITRESS_BASIC_UR
                        new_size = get_new_size_by_height(new_waiter_picture, self.get_basic_height())
                        self.set_image(pygame.transform.scale(new_waiter_picture, new_size))
                        self.set_rect(self.get_image().get_rect(topleft=(self.get_rect().x, self.get_rect().y)))
                        self.set_profile("UR")
                # DolůDoleva
                elif self.get_direct_x() < 0 and self.get_direct_y() > 0:
                    if self.get_profile() != "DL":
                        if waiter_gender == "M":
                            new_waiter_picture = WAITER_BASIC_DL
                        else:
                            new_waiter_picture = WAITRESS_BASIC_DL
                        new_size = get_new_size_by_height(new_waiter_picture, self.get_basic_height())
                        self.set_image(pygame.transform.scale(new_waiter_picture, new_size))
                        self.set_rect(self.get_image().get_rect(topleft=(self.get_rect().x, self.get_rect().y)))
                        self.set_profile("DL")
                # DolůDoprava
                elif self.get_direct_x() > 0 and self.get_direct_y() > 0:
                    if self.get_profile() != "DR":
                        if waiter_gender == "M":
                            new_waiter_picture = WAITER_BASIC_DR
                        else:
                            new_waiter_picture = WAITRESS_BASIC_DR
                        new_size = get_new_size_by_height(new_waiter_picture, self.get_basic_height())
                        self.set_image(pygame.transform.scale(new_waiter_picture, new_size))
                        self.set_rect(self.get_image().get_rect(topleft=(self.get_rect().x, self.get_rect().y)))
                        self.set_profile("DR")

            elif self.get_signal_movement_x() and not self.get_signal_movement_y():
                # Doleva
                if self.get_direct_x() < 0:
                    if self.get_profile() != "L":
                        if waiter_gender == "M":
                            new_waiter_picture = WAITER_BASIC_L
                        else:
                            new_waiter_picture = WAITRESS_BASIC_L
                        new_size = get_new_size_by_height(new_waiter_picture, self.get_basic_height())
                        self.set_image(pygame.transform.scale(new_waiter_picture, new_size))
                        self.set_rect(self.get_image().get_rect(topleft=(self.get_rect().x, self.get_rect().y)))
                        self.set_profile("L")
                # Doprava
                else:
                    if self.get_profile() != "R":
                        if waiter_gender == "M":
                            new_waiter_picture = WAITER_BASIC_R
                        else:
                            new_waiter_picture = WAITRESS_BASIC_R
                        new_size = get_new_size_by_height(new_waiter_picture, self.get_basic_height())
                        self.set_image(pygame.transform.scale(new_waiter_picture, new_size))
                        self.set_rect(self.get_image().get_rect(topleft=(self.get_rect().x, self.get_rect().y)))
                        self.set_profile("R")
            elif not self.get_signal_movement_x() and self.get_signal_movement_y():
                # Nahoru
                if self.get_direct_y() < 0:
                    if self.get_profile() != "U":
                        if waiter_gender == "M":
                            new_waiter_picture = WAITER_BASIC_U
                        else:
                            new_waiter_picture = WAITRESS_BASIC_U
                        new_size = get_new_size_by_height(new_waiter_picture, self.get_basic_height())
                        self.set_image(pygame.transform.scale(new_waiter_picture, new_size))
                        self.set_rect(self.get_image().get_rect(topleft=(self.get_rect().x, self.get_rect().y)))
                        self.set_profile("U")
                # Doprava
                else:
                    if self.get_profile() != "D":
                        if waiter_gender == "M":
                            new_waiter_picture = WAITER_BASIC_D
                        else:
                            new_waiter_picture = WAITRESS_BASIC_D
                        new_size = get_new_size_by_height(new_waiter_picture, self.get_basic_height())
                        self.set_image(pygame.transform.scale(new_waiter_picture, new_size))
                        self.set_rect(self.get_image().get_rect(topleft=(self.get_rect().x, self.get_rect().y)))
                        self.set_profile("D")

            # Pohyb po ose x
            if self.get_signal_movement_x():
                movement_x = self.move_x(act_dest_position[0])
                if movement_x:
                    self.set_signal_movement_x(False)

            # Pohyb po ose y
            if self.get_signal_movement_y():
                movement_y = self.move_y(act_dest_position[1])
                if movement_y:
                    self.set_signal_movement_y(False)

            # Pohyb skončil
            if not self.get_signal_movement_x() and not self.get_signal_movement_y():
                dest_positions.pop(0)
                if dest_positions == []:
                    self.set_is_walking(False)
                else:
                    self.set_signal_movement_x(True)
                    self.set_signal_movement_y(True)

                if self.get_is_walking():
                    first_dest = dest_positions[0]
                    source_position = self.get_positions()

                    if source_position[0] <= first_dest[0]:
                        self.set_direct_x(SPEED_OF_PEOPLES)
                    else:
                        self.set_direct_x(-1 * SPEED_OF_PEOPLES)

                    if source_position[1] <= first_dest[1]:
                        self.set_direct_y(SPEED_OF_PEOPLES)
                    else:
                        self.set_direct_y(-1 * SPEED_OF_PEOPLES)

        # Postava se nepohybuje = nastavíme defaultní profil
        else:
         if self.get_profile != "D":
            if waiter_gender == "M":
                new_waiter_picture = WAITER_BASIC_D
            else:
                new_waiter_picture = WAITRESS_BASIC_D
            new_size = get_new_size_by_height(new_waiter_picture, self.get_basic_height())
            self.set_image(pygame.transform.scale(new_waiter_picture, new_size))
            self.set_rect(self.get_image().get_rect(topleft=(self.get_rect().x, self.get_rect().y)))
            self.set_collision_rect(self.create_new_collision_rect())
            self.set_profile("D")

    """
    Pohyb po ose x, vrací 1, pokud je číšník na pozici final_position, jinak 0"""
    def move_x(self, final_position):
        source_position = self.get_rect().centerx
        direct_x = self.get_direct_x()

        # Půjdeme doprava
        if direct_x > 0:
            if source_position < final_position:
                self.get_rect().centerx += direct_x
                self.get_collision_rect().centerx += direct_x
                return 0
            # Jsme v cíli
            else:
                self.get_rect().centerx = final_position
                self.get_collision_rect().centerx = final_position
                return 1
        # Půjdeme doleva
        else:
            if source_position > final_position:
                self.get_rect().centerx += direct_x
                self.get_collision_rect().centerx += direct_x
                return 0
            else:
                self.get_rect().centerx = final_position
                self.get_collision_rect().centerx = final_position
                return 1

    def move_y(self, final_position):
        source_position = self.get_rect().bottom
        direct_y = self.get_direct_y()

        # Půjdeme dolů
        if direct_y > 0:
            if source_position < final_position:
                self.get_rect().centery += direct_y
                self.get_collision_rect().centery += direct_y
                return 0
            # Jsme v cíli
            else:
                self.get_rect().bottom = final_position
                self.get_collision_rect().bottom = final_position
                return 1
        # Půjdeme nahoru
        else:
            if source_position > final_position:
                self.get_rect().centery += direct_y
                self.get_collision_rect().centery += direct_y
                return 0
            else:
                self.get_rect().bottom = final_position
                self.get_collision_rect().bottom = final_position
                return 1

class Costumer(People):
    def __init__(self, name, image, priority, x_pos, y_pos):
        super().__init__(image, priority, x_pos, y_pos)