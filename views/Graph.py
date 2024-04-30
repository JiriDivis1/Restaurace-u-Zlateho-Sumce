from model import *

class Node:
    def __init__(self, node_id, is_usable, x_pos, y_pos):
        if len(node_id) != 2:
            raise Exception("Node_id must have 2 chars")
        if not letters[node_id[0]] or letters[node_id[0]] > COUNT_OF_ROWS:
            raise Exception("Node_id for row cannot be used!")
        if not letters[node_id[1]] or letters[node_id[1]] > COUNT_OF_COLS:
            raise Exception("Node_id for column cannot be used!")

        self.node_id = node_id  # str - Identifikace uzlu (např. "ab")                                                                            #Pole sousedů daného uzlu
        self.is_usable = is_usable  # boolean - Lze použít, nebo se jedná o překážku
        self.neighbours = []  # pole sousedů uzlu

        self.node_x_pos = x_pos  # x-ová pozice čtverce
        self.node_y_pos = y_pos  # y-ová pozice čtverce
        self.node_rect = pygame.Rect(x_pos, y_pos, side_width, side_height)  # Čtverec, který reprezentuje uzel grafu
        self.node_center_pos = (self.node_rect.centerx, self.node_rect.centery)  # Střed čtverce
        self.text = node_font.render(self.node_id, True, BLACK)  # Text
        area_center_pos = Graph.convert_node_point_to_area_point(self.node_center_pos[0], self.node_center_pos[1])
        self.text_rect = self.text.get_rect(
            center=(area_center_pos[0], area_center_pos[1] - side_height * 0.1))  # Rect Textu

    def get_node_id(self):
        return self.node_id

    def set_node_id(self, node_id):
        self.node_id = node_id
        return self

    def get_is_usable(self):
        return self.is_usable

    def set_is_usable(self, is_usable):
        self.is_usable = is_usable
        return self

    def get_neighbours(self):
        return self.neighbours

    """Nastaví všechny sousedy pro tento uzel
    """
    def set_neighbours(self, neighbours):
        self.neighbours = neighbours
        return self

    def get_node_x_pos(self):
        return self.node_x_pos

    def set_node_x_pos(self, node_x_pos):
        self.node_x_pos = node_x_pos
        return self

    def get_node_y_pos(self):
        return self.node_y_pos

    def set_node_y_pos(self, node_y_pos):
        self.node_y_pos = node_y_pos
        return self

    def get_node_rect(self):
        return self.node_rect

    def set_node_rect(self, node_rect):
        self.node_rect = node_rect
        return self

    def get_text(self):
        return self.text

    def get_text_rect(self):
        return self.text_rect

    def set_text_rect(self, text_rect):
        self.text_rect = text_rect
        return self

    def get_node_center_pos(self):
        return self.node_center_pos

    def set_node_center_pos(self, node_center_pos):
        self.node_center_pos = node_center_pos
        return self

    def draw(self, color):
        if color == TRANSPARENT:
            transparent_surface = pygame.Surface((100, 100), pygame.SRCALPHA)
            transparent_surface.fill(TRANSPARENT)  # Nastavení průhledného pozadí
            pygame.draw.rect(transparent_surface, (255, 255, 255), transparent_surface.get_rect(), border_radius=10)
            SCREEN.blit(self.get_text(), self.get_text_rect())
            pygame.draw.rect(SCREEN, BLACK, [self.get_node_x_pos(), self.get_node_y_pos(), side_width, side_height], 3)
        else:
            pygame.draw.rect(SCREEN, color, self.get_node_rect())
            SCREEN.blit(self.get_text(), self.get_text_rect())
            pygame.draw.rect(SCREEN, BLACK, [self.get_node_x_pos(), self.get_node_y_pos(), side_width, side_height], 3)

    def convert_rect_to_polygon(self):
        top_left_node_point = [self.get_node_rect().topleft[0], self.get_node_rect().topleft[1]]
        top_left_area_point = Graph.convert_node_point_to_area_point(top_left_node_point[0], top_left_node_point[1])
        top_right_node_point = [self.get_node_rect().topright[0], self.get_node_rect().topright[1]]
        top_right_area_point = Graph.convert_node_point_to_area_point(top_right_node_point[0], top_right_node_point[1])
        bottom_right_node_point = [self.get_node_rect().bottomright[0], self.get_node_rect().bottomright[1]]
        bottom_right_area_point = Graph.convert_node_point_to_area_point(bottom_right_node_point[0],
                                                                         bottom_right_node_point[1])
        bottom_left_node_point = [self.get_node_rect().bottomleft[0], self.get_node_rect().bottomleft[1]]
        bottom_left_area_point = Graph.convert_node_point_to_area_point(bottom_left_node_point[0],
                                                                        bottom_left_node_point[1])

        return [top_left_area_point, top_right_area_point, bottom_right_area_point, bottom_left_area_point]

    def draw_area(self, color):
        polygon = self.convert_rect_to_polygon()

        if color != TRANSPARENT:
            pygame.draw.polygon(SCREEN, color, polygon)
        SCREEN.blit(self.get_text(), self.get_text_rect())
        pygame.draw.polygon(SCREEN, BLACK, polygon, 2)

    def is_clicked(self, position):
        if position[0] in range(self.get_node_x_pos(), self.get_node_x_pos() + side_width) and position[1] in range(
                self.get_node_y_pos(), self.get_node_y_pos() + side_height):
            return True

class Graph:
    def __init__(self, disusable_nodes):
        self.disusable_nodes = disusable_nodes          # pole uzlů (jejich node_id), které nepoužívat
        self.nodes = self.create_nodes()                # pole všech uzlů (přesněji pole řádků)
        self.set_disusable_nodes(disusable_nodes)       # nastavíme nepoužívané uzly
        self.neighbours = {}                            # každému uzlu zapíšeme se kterými uzly sousedí
        self.set_neighbours()
        self.heuristic_distances = []

    def get_disusable_nodes(self):
        return self.disusable_nodes

    def set_disusable_nodes(self, disusable_nodes):
        self.disusable_nodes = disusable_nodes
        self.set_disusable_nodes2()
        return self

    # Pole uzlů v grafu
    def get_nodes(self):
        return self.nodes

    def set_nodes(self, nodes):
        self.nodes = nodes
        return self

    def print_nodes(self):
        for i in range(COUNT_OF_ROWS):
            for j in range(COUNT_OF_COLS):
                if self.get_nodes()[i][j].get_is_usable():
                    print(self.get_nodes()[i][j].get_node_id(), end=" ")
                else:
                    print("--", end=" ")
            print("\n")

    def get_neighbours(self):
        return self.neighbours

    def get_neighbours_of(self, node_id):
        neighbours = self.get_neighbours()
        return neighbours[node_id]

    """Nastaví uzlu node všechny jeho sousedy
    """
    def set_neighbours_for(self, node):
        row, col = self.get_node_indexes(node.get_node_id())
        node_neighbours = []
        node_id = node.get_node_id()

        if node.get_is_usable():
            # Uzel nahoře
            if self.prev_row(node_id):
                if self.nodes[row - 1][col].get_is_usable():
                    node_neighbours.append(self.nodes[row - 1][col].get_node_id())
            # Uzel napravo
            if self.next_column(node_id):
                if self.nodes[row][col + 1].get_is_usable():
                    node_neighbours.append(self.nodes[row][col + 1].get_node_id())
            # Uzel nahoře, napravo
            if self.prev_row(node_id) and self.next_column(node_id):
                if self.nodes[row - 1][col + 1].get_is_usable():
                    if self.nodes[row - 1][col].get_is_usable() and self.nodes[row][col + 1].get_is_usable():
                        node_neighbours.append(self.nodes[row - 1][col + 1].get_node_id())
            # Uzel dole
            if self.next_row(node_id):
                if self.nodes[row + 1][col].get_is_usable():
                    node_neighbours.append(self.nodes[row + 1][col].get_node_id())
            # Uzel dole, napravo
            if self.next_row(node_id) and self.next_column(node_id):
                if self.nodes[row + 1][col + 1].get_is_usable():
                    if self.nodes[row][col + 1].get_is_usable() and self.nodes[row + 1][col].get_is_usable():
                        node_neighbours.append(self.nodes[row + 1][col + 1].get_node_id())
            # Uzel nalevo
            if self.prev_column(node_id):
                if self.nodes[row][col - 1].get_is_usable():
                    node_neighbours.append(self.nodes[row][col - 1].get_node_id())
            # Uzel dole, nalevo
            if self.next_row(node_id) and self.prev_column(node_id):
                if self.nodes[row + 1][col - 1].get_is_usable():
                    if self.nodes[row][col - 1].get_is_usable() and self.nodes[row + 1][col].get_is_usable():
                        node_neighbours.append(self.nodes[row + 1][col - 1].get_node_id())
            # Uzel nahoře, nalevo
            if self.prev_row(node_id) and self.prev_column(node_id):
                if self.nodes[row - 1][col - 1].get_is_usable():
                    if self.nodes[row - 1][col].get_is_usable() and self.nodes[row][col - 1].get_is_usable():
                        node_neighbours.append(self.nodes[row - 1][col - 1].get_node_id())
            self.get_neighbours()[node_id] = node_neighbours

    """Nastaví sousedy všem uzlům, které sousedí s uzlem node 
    """
    def set_neighbours_of(self, node):
        node_row, node_col = self.get_node_indexes(node.get_node_id())
        #Nastavení sousedů pro ...
        # ...souseda nahoře:
        if node_row != 0:
            self.set_neighbours_for(self.get_nodes()[node_row - 1][node_col])
            # ... souseda nahoře napravo:
            if node_col != COUNT_OF_COLS - 1:
                self.set_neighbours_for(self.get_nodes()[node_row - 1][node_col + 1])
        #   Souseda napravo:
        if node_col != COUNT_OF_COLS - 1:
            self.set_neighbours_for(self.get_nodes()[node_row][node_col + 1])
            # Souseda dole napravo:
            if node_row != COUNT_OF_ROWS - 1:
                self.set_neighbours_for(self.get_nodes()[node_row + 1][node_col + 1])
        #   Souseda dole:
        if node_row != COUNT_OF_ROWS - 1:
            self.set_neighbours_for(self.get_nodes()[node_row + 1][node_col])
            # Souseda dole nalevo:
            if node_col != 0:
                self.set_neighbours_for(self.get_nodes()[node_row + 1][node_col - 1])
        #   Souseda nahoře nalevo:
        if node_col != 0:
            self.set_neighbours_for(self.get_nodes()[node_row][node_col - 1])
            if node_row != 0:
                self.set_neighbours_for(self.get_nodes()[node_row - 1][node_col - 1])

    def get_heuristic_distances(self):
        return self.heuristic_distances

    def h(self, n):
        heurist_dist = self.get_heuristic_distances()
        return heurist_dist[n]

    # Vrátí index x a y na kterých se daný uzel nachází
    def get_node_indexes(self, node_id):
        if letters[node_id[0]] is not None:
            x = letters[node_id[0]]
            if x > COUNT_OF_ROWS:
                return None
            else:
                x -= 1
        else:
            return None
        if letters[node_id[1]] is not None:
            y = letters[node_id[1]]
            if y > COUNT_OF_COLS:
                return None
            else:
                y -= 1
        else:
            return None

        return [x, y]

    def get_node_on_position(self, position):
        node_position = self.convert_area_point_to_node_point(position[0], position[1])
        for row in self.get_nodes():
            for col in row:
                if col.is_clicked(node_position):
                    return col
        return None

    """Vrátí pole řádků jednotlivých uzlů
    """

    def create_nodes(self):
        result = []
        for x in range(1, COUNT_OF_ROWS + 1):
            act_row = []
            for y in range(1, COUNT_OF_COLS + 1):
                node_id = self.change_num_to_letter(x) + self.change_num_to_letter(y)
                node_x = side_width * (y - 1) + LEFT_CORNER
                node_y = side_height * (x - 1) + TOP_FLOOR

                act_row.append(Node(node_id, True, node_x, node_y))
            result.append(act_row)
        return result

    # Nastavení nepouživatelných uzlů
    def set_disusable_nodes2(self):
        disusable_nodes = self.get_disusable_nodes()
        nodes = self.get_nodes()
        for node in disusable_nodes:
            indexes = self.get_node_indexes(node)
            nodes[indexes[0]][indexes[1]].set_is_usable(False)

    # Nastavení sousedů jednotlivých uzlů
    def set_neighbours(self):

        for x in range(COUNT_OF_ROWS):
            for y in range(COUNT_OF_COLS):
                act_node = self.get_nodes()[x][y]
                act_node_id = act_node.get_node_id()
                self.set_neighbours_for(act_node)

    """Nastavíme heuristickou vzdálenost každému bodu k cílovému bodu, tu vypočítáme pomocí pythagorovy věty o přeponě
    """

    def set_heuristic_distances(self, end):
        end_node_x, end_node_y = self.get_node_indexes(end)
        if not (end_node_x, end_node_y):
            print("Tento uzel neexistuje")
            return False
        end_node = self.nodes[end_node_x][end_node_y]
        if not end_node.get_is_usable():
            print("Tento uzel nelze použít")
            return False

        heuristic_distances = {}

        for row in range(COUNT_OF_ROWS):
            for col in range(COUNT_OF_COLS):
                act_node = self.get_nodes()[row][col]
                act_node_id = act_node.get_node_id()
                a = b = 0
                copy_row = row
                copy_col = col
                if act_node.get_is_usable():

                    # Výpočet strany a
                    while row != end_node_x:
                        if row < end_node_x:
                            row += 1
                        else:
                            row -= 1
                        a += 1

                    # Výpočet strany b
                    while col != end_node_y:
                        if col < end_node_y:
                            col += 1
                        else:
                            col -= 1
                        b += 1

                    # Výpočet přepony
                    c = round(math.sqrt(a ** 2 + b ** 2), 5)

                    heuristic_distances[act_node_id] = c

                    row = copy_row
                    col = copy_col
                else:
                    heuristic_distances[act_node_id] = -1

        self.heuristic_distances = heuristic_distances
        return True

    """ Vrátí pole uzlů (jejich node_id) po/přes které postava projde po cestě ze startu do cíle
    """

    def a_star_algorithm(self, start, end):
        if self.set_heuristic_distances(end):
            open_lst = set([start])
            closed_lst = set([])

            poo = {}
            poo[start] = 0

            par = {}
            par[start] = start

            while len(open_lst) > 0:
                n = None
                for v in open_lst:
                    if n == None or poo[v] + self.h(v) < poo[n] + self.h(n):
                        n = v

                if n == None:
                    return None

                if n == end:
                    reconst_path = []

                    while par[n] != n:
                        reconst_path.append(n)
                        n = par[n]

                    reconst_path.append(start)
                    reconst_path.reverse()
                    return reconst_path

                for m in self.get_neighbours_of(n):
                    if m not in open_lst and m not in closed_lst:
                        open_lst.add(m)
                        par[m] = n
                        poo[m] = poo[n] + 1
                    else:
                        if poo[m] > poo[n] + 1:
                            poo[m] = poo[n] + 1
                            par[m] = n

                            if m in closed_lst:
                                closed_lst.remove(m)
                                open_lst.add(m)
                open_lst.remove(n)
                closed_lst.add(n)
        else:
            return None

    """Tato funkce pro číslo num, vrátí jeho písmeno
        """
    @staticmethod
    def change_num_to_letter(num):
        if num < 1 or num > 32:
            return None
        else:
            if num <= 26:
                num += 96
            else:
                num += 38
            return chr(num)

    """Pro node_id (např. "ab") vrátí následující řádek, tedy 'b'
    """
    @staticmethod
    def next_row(act_node_id):
        if not act_node_id: return None
        char_x = act_node_id[0]
        x = letters[char_x]
        if x == COUNT_OF_ROWS:
            return None
        else:
            return prev_next_letter[char_x][1]

    """Pro node_id (např. "bb") vrátí předchozí řádek (-> a)
    """
    @staticmethod
    def prev_row(act_node_id):
        if not act_node_id: return None
        char_x = act_node_id[0]
        x = letters[char_x]
        if x == 1:
            return None
        else:
            return prev_next_letter[char_x][0]

    @staticmethod
    def next_column(act_node_id):
        if not act_node_id: return None
        char_y = act_node_id[1]
        y = letters[char_y]
        if y == COUNT_OF_COLS:
            return None
        else:
            return prev_next_letter[char_y][1]

    @staticmethod
    def prev_column(act_node_id):
        if not act_node_id: return None
        char_y = act_node_id[1]
        y = letters[char_y]
        if y == 1:
            return None
        else:
            return prev_next_letter[char_y][0]

    """Pro act_node_id (např. "ab"), vrátí id uzlu nacházejícím se ve stejném sloupci a předchozím řádku (-> "bb")
    """
    @staticmethod
    def next_row_id(act_node_id):
        if not act_node_id: return None
        char_x = act_node_id[0]
        x = letters[char_x]
        if x == COUNT_OF_ROWS:
            return None
        else:
            return prev_next_letter[char_x][1] + act_node_id[1]

    """Pro node_id (např. "ab") vrátí předchozí řádek
    """

    @staticmethod
    def prev_row_id(act_node_id):
        if not act_node_id: return None
        char_x = act_node_id[0]
        x = letters[char_x]
        if x == 1:
            return None
        else:
            return prev_next_letter[char_x][0] + act_node_id[1]

    @staticmethod
    def next_column_id(act_node_id):
        if not act_node_id: return None
        char_y = act_node_id[1]
        y = letters[char_y]
        if y == COUNT_OF_COLS:
            return None
        else:
            return act_node_id[0] + prev_next_letter[char_y][1]

    @staticmethod
    def prev_column_id(act_node_id):
        if not act_node_id: return None
        char_y = act_node_id[1]
        y = letters[char_y]
        if y == 1:
            return None
        else:
            return act_node_id[0] + prev_next_letter[char_y][0]

    @staticmethod
    def convert_screen_coordinates_to_floor(x, y):
        return [x - LEFT_CORNER, y - TOP_FLOOR]

    @staticmethod
    def convert_floor_coordinates_to_screen(x, y):
        return [x + LEFT_CORNER, y + TOP_FLOOR]

    @staticmethod
    def convert_node_point_to_area_point(x, y):
        floor_point = Graph.convert_screen_coordinates_to_floor(x, y)
        x = floor_point[0]
        y = floor_point[1]
        z = x - FLOOR_MEDIAN
        if x <= FLOOR_MEDIAN:
            dx = (z * y) / 290
        else:
            dx = (z * y) / 300
        return Graph.convert_floor_coordinates_to_screen(x + dx, y)

    @staticmethod
    def convert_area_point_to_node_point(x, y):
        screen_point = Graph.convert_screen_coordinates_to_floor(x, y)
        x = screen_point[0]
        y = screen_point[1]
        if x <= FLOOR_MEDIAN:
            return Graph.convert_floor_coordinates_to_screen(round(x * 290 / (290 + y) + FLOOR_MEDIAN * y / (290 + y)),
                                                             y)
        else:
            return Graph.convert_floor_coordinates_to_screen(round(x * 300 / (300 + y) + FLOOR_MEDIAN * y / (300 + y)),
                                                             y)

    """Tato funkce odstraní chyby A* algoritmu v důsledku nedokonalé heurestiky, kterými budeme procházet"""

    def dest_nodes_filter(self, dest_nodes):
        # Uzly, které odstraníme
        nodes_to_remove = []
        sub_nodes_to_remove = []
        for i in range(len(dest_nodes)-2):
            act_node = dest_nodes[i]

            if self.next_column(act_node):
                next_column_id = self.next_column_id(act_node)
                row, col = self.get_node_indexes(next_column_id)
                next_column_node = self.get_nodes()[row][col]
                # Obcházíme uzel napravo
                if next_column_node.get_is_usable():
                    prev_row_id = self.prev_row_id(act_node)
                    prev_row_next_col_id = self.next_column_id(prev_row_id)

                    next_row_id = self.next_row_id(act_node)
                    next_row_next_col_id = self.next_column_id(next_row_id)

                    #Obcházíme pravý uzel vrchem
                    if (prev_row_id and dest_nodes[i+1] == prev_row_id) or (prev_row_next_col_id and dest_nodes[i+1] == prev_row_next_col_id):
                        sub_nodes_to_remove = []
                        for j in range(i+1, len(dest_nodes)-1):
                            node = dest_nodes[j]
                            next_row_id = self.next_row_id(node)
                            next_column_id = self.next_column_id(node)
                            next_row_next_col_id = self.next_row_id(next_column_id)

                            # Pokračujeme
                            if next_row_id and next_column_id and dest_nodes[j+1] == next_column_id:
                                row, col = self.get_node_indexes(next_row_id)
                                next_row_node = self.get_nodes()[row][col]
                                if next_row_node.get_is_usable():
                                    sub_nodes_to_remove.append(node)
                                else:
                                    break
                            # Jsme u konce
                            elif dest_nodes[j+1] == next_row_id or dest_nodes[j+1] == next_row_next_col_id:
                                row, col = self.get_node_indexes(next_row_id)
                                next_row_node = self.get_nodes()[row][col]
                                if next_row_node.get_is_usable():
                                    sub_nodes_to_remove.append(node)
                                    nodes_to_remove += sub_nodes_to_remove
                                    break
                            # Nejedná se o chybu
                            else:
                                break
                    # Obcházíme pravý uzel spodem
                    if (next_row_id and dest_nodes[i+1] == next_row_id) or (next_row_next_col_id and dest_nodes[i+1] == next_row_next_col_id):
                        sub_nodes_to_remove = []
                        for j in range(i+1, len(dest_nodes)-1):
                            node = dest_nodes[j]
                            prev_row_id = self.prev_row_id(node)
                            next_column_id = self.next_column_id(node)
                            prev_row_next_col_id = self.prev_row_id(next_column_id)

                            # Pokračujeme
                            if prev_row_id and next_column_id and dest_nodes[j+1] == next_column_id:
                                row, col = self.get_node_indexes(prev_row_id)
                                prev_row_node = self.get_nodes()[row][col]
                                if prev_row_node.get_is_usable():
                                    sub_nodes_to_remove.append(node)
                                else:
                                    break
                            # Jsme u konce
                            elif dest_nodes[j+1] == prev_row_id or dest_nodes[j+1] == prev_row_next_col_id:
                                row, col = self.get_node_indexes(prev_row_id)
                                prev_row_node = self.get_nodes()[row][col]
                                if prev_row_node.get_is_usable():
                                    sub_nodes_to_remove.append(node)
                                    nodes_to_remove += sub_nodes_to_remove
                                    break
                            #Nejedná se o chybu
                            else:
                                break

            if self.prev_column(act_node):
                prev_column_id = self.prev_column_id(act_node)
                row, col = self.get_node_indexes(prev_column_id)
                prev_column_node = self.get_nodes()[row][col]

                if prev_column_node.get_is_usable():
                    prev_row_id = self.prev_row_id(act_node)
                    prev_row_prev_col_id = self.prev_column_id(prev_row_id)

                    next_row_id = self.next_row_id(act_node)
                    next_row_prev_col_id = self.prev_column_id(next_row_id)

                    if (prev_row_id and dest_nodes[i + 1] == prev_row_id) or (
                            prev_row_prev_col_id and dest_nodes[i + 1] == prev_row_prev_col_id):
                        sub_nodes_to_remove = []
                        for j in range(i + 1, len(dest_nodes)-1):
                            node = dest_nodes[j]
                            next_row_id = self.next_row_id(node)
                            prev_column_id = self.prev_column_id(node)
                            next_row_prev_col_id = self.next_row_id(prev_column_id)

                            # Pokračujeme
                            if next_row_id and prev_column_id and dest_nodes[j + 1] == prev_column_id:
                                row, col = self.get_node_indexes(next_row_id)
                                next_row_node = self.get_nodes()[row][col]
                                if next_row_node.get_is_usable():
                                    sub_nodes_to_remove.append(node)
                                else:
                                    break
                            # Jsme u konce
                            elif dest_nodes[j + 1] == next_row_id or dest_nodes[j + 1] == next_row_prev_col_id:
                                row, col = self.get_node_indexes(next_row_id)
                                next_row_node = self.get_nodes()[row][col]
                                if next_row_node.get_is_usable():
                                    sub_nodes_to_remove.append(node)
                                    nodes_to_remove += sub_nodes_to_remove
                                    break
                            # Nejedná se o chybu
                            else:
                                break
                    elif (next_row_id and dest_nodes[i + 1] == next_row_id) or (
                        next_row_prev_col_id and dest_nodes[i + 1] == next_row_prev_col_id):
                        sub_nodes_to_remove = []
                        for j in range(i + 1, len(dest_nodes)-1):
                            node = dest_nodes[j]
                            prev_row_id = self.prev_row_id(node)
                            prev_column_id = self.prev_column_id(node)
                            prev_row_prev_col_id = self.prev_row_id(prev_column_id)

                            # Pokračujeme
                            if prev_row_id and prev_column_id and dest_nodes[j + 1] == prev_column_id:
                                row, col = self.get_node_indexes(prev_row_id)
                                prev_row_node = self.get_nodes()[row][col]
                                if prev_row_node.get_is_usable():
                                    sub_nodes_to_remove.append(node)
                                else:
                                    break
                            # Jsme u konce
                            elif dest_nodes[j + 1] == prev_row_id or dest_nodes[j + 1] == prev_row_prev_col_id:
                                row, col = self.get_node_indexes(prev_row_id)
                                prev_row_node = self.get_nodes()[row][col]
                                if prev_row_node.get_is_usable():
                                    sub_nodes_to_remove.append(node)
                                    nodes_to_remove += sub_nodes_to_remove
                                    break
                            # Nejedná se o chybu
                            else:
                                break

            if self.next_row(act_node):
                next_row_id = self.next_row_id(act_node)
                row, col = self.get_node_indexes(next_row_id)
                next_row_node = self.get_nodes()[row][col]

                if next_row_node.get_is_usable():
                    prev_col_id = self.prev_column_id(act_node)
                    next_row_prev_col_id = self.next_row_id(prev_col_id)

                    next_col_id = self.next_column_id(act_node)
                    next_row_next_col_id = self.next_row_id(next_col_id)

                    if (prev_col_id and dest_nodes[i+1] == prev_col_id) or (next_row_prev_col_id and dest_nodes[i+1] == next_row_prev_col_id):

                        sub_nodes_to_remove = []
                        for j in range(i+1, len(dest_nodes)-1):
                            node = dest_nodes[j]

                            next_row_id = self.next_row_id(node)
                            next_column_id = self.next_column_id(node)
                            next_row_next_col_id = self.next_row_id(next_column_id)

                            #Pokračujeme
                            if next_row_id and next_column_id and dest_nodes[j+1] == next_row_id:
                                row, col = self.get_node_indexes(next_column_id)
                                next_column_node = self.get_nodes()[row][col]
                                if next_column_node.get_is_usable():
                                    sub_nodes_to_remove.append(node)
                                else:
                                    break
                            #Jsme u konce
                            elif dest_nodes[j+1] == next_column_id or dest_nodes[j+1] == next_row_next_col_id:
                                row, col = self.get_node_indexes(next_column_id)
                                next_column_node = self.get_nodes()[row][col]
                                if next_column_node.get_is_usable():
                                    sub_nodes_to_remove.append(node)
                                    nodes_to_remove += sub_nodes_to_remove
                                    break
                            #Nejedná se o chybu
                            else:
                                break
                    if (next_col_id and dest_nodes[i+1] == next_col_id) or (next_row_next_col_id and dest_nodes[i+1] == next_row_next_col_id):
                        sub_nodes_to_remove = []
                        for j in range(i+1, len(dest_nodes)-1):
                            node = dest_nodes[j]
                            prev_column_id = self.prev_column_id(node)
                            next_row_id = self.next_row_id(node)
                            next_row_prev_col_id = self.prev_column_id(next_row_id)

                            #Pokračujeme
                            if prev_column_id and next_row_id and dest_nodes[j+1] == next_row_id:
                                row, col = self.get_node_indexes(prev_column_id)
                                prev_column_node = self.get_nodes()[row][col]
                                if prev_column_node.get_is_usable():
                                    sub_nodes_to_remove.append(node)
                                else:
                                    break
                            #Jsme u konce
                            elif dest_nodes[j+1] == prev_column_id or dest_nodes[j+1] == next_row_prev_col_id:
                                row, col = self.get_node_indexes(prev_column_id)
                                prev_column_node = self.get_nodes()[row][col]
                                if prev_column_node.get_is_usable():
                                    sub_nodes_to_remove.append(node)
                                    nodes_to_remove += sub_nodes_to_remove
                                    break
                            #Nejedná se o chybu
                            else:
                                break

            if self.prev_row(act_node):
                prev_row_id = self.prev_row_id(act_node)
                row, col = self.get_node_indexes(prev_row_id)
                prev_row_node = self.get_nodes()[row][col]

                if prev_row_node.get_is_usable():
                    prev_col_id = self.prev_column_id(act_node)
                    prev_row_prev_col_id = self.prev_row_id(prev_col_id)

                    next_col_id = self.next_column_id(act_node)
                    prev_row_next_col_id = self.prev_row_id(next_col_id)

                    if (prev_col_id and dest_nodes[i + 1] == prev_col_id) or (
                            prev_row_prev_col_id and dest_nodes[i + 1] == prev_row_prev_col_id):
                        sub_nodes_to_remove = []
                        for j in range(i + 1, len(dest_nodes)-1):
                            node = dest_nodes[j]
                            next_col_id = self.next_column_id(node)
                            prev_row_id = self.prev_row_id(node)
                            prev_row_next_col_id = self.next_column_id(prev_row_id)

                            # Pokračujeme
                            if next_col_id and prev_row_id and dest_nodes[j + 1] == prev_row_id:
                                row, col = self.get_node_indexes(next_col_id)
                                next_row_node = self.get_nodes()[row][col]
                                if next_row_node.get_is_usable():
                                    sub_nodes_to_remove.append(node)
                                else:
                                    break
                            # Jsme u konce
                            elif dest_nodes[j + 1] == next_col_id or dest_nodes[j + 1] == prev_row_next_col_id:
                                row, col = self.get_node_indexes(next_col_id)
                                next_row_node = self.get_nodes()[row][col]
                                if next_row_node.get_is_usable():
                                    sub_nodes_to_remove.append(node)
                                    nodes_to_remove += sub_nodes_to_remove
                                    break
                            # Nejedná se o chybu
                            else:
                                break

                    elif (next_col_id and dest_nodes[i + 1] == next_col_id) or (
                        prev_row_next_col_id and dest_nodes[i + 1] == prev_row_next_col_id):
                        sub_nodes_to_remove = []
                        for j in range(i + 1, len(dest_nodes)-1):
                            node = dest_nodes[j]
                            prev_column_id = self.prev_column_id(node)
                            prev_row_id = self.prev_row_id(node)
                            prev_row_prev_col_id = self.prev_row_id(prev_column_id)

                            # Pokračujeme
                            if prev_column_id and prev_row_id and dest_nodes[j + 1] == prev_row_id:
                                row, col = self.get_node_indexes(prev_column_id)
                                prev_column_node = self.get_nodes()[row][col]
                                if prev_column_node.get_is_usable():
                                    sub_nodes_to_remove.append(node)
                                else:
                                    break
                            # Jsme u konce
                            elif dest_nodes[j + 1] == next_column_id or dest_nodes[j + 1] == prev_row_prev_col_id:
                                row, col = self.get_node_indexes(prev_column_id)
                                prev_column_node = self.get_nodes()[row][col]
                                if prev_column_node.get_is_usable():
                                    sub_nodes_to_remove.append(node)
                                    nodes_to_remove += sub_nodes_to_remove
                                    break
                            # Nejedná se o chybu
                            else:
                                break

        for node in nodes_to_remove:
            dest_nodes.remove(node)

        dest_nodes.pop(0)
        dest_nodes.pop(len(dest_nodes) - 1)

        return dest_nodes