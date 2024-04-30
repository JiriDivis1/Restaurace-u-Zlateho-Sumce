from model import *
from Game import *

class Profile():
    def __init__(self, id, name, character_gender):
        self.id = id
        self.name = name                            # Jméno hráče
        self.character_gender = character_gender    # Waiter, pokud hraji za číšníka, Waitress, pokud hraji za číšnici
        self.money = 0                              # Částka peněz, které hráč na tomto profilu vydělal
        self.buy_stuff = None
        self.game = None

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name
        return self

    def get_character_gender(self):
        return self.character_gender
    
    def set_character_gender(self, character_gender):
        self.character_gender = character_gender
        return self

    def get_money(self):
        return self.money

    def set_money(self, money):
        self.money = money
        return self

    def get_buy_stuff(self):
        return self.buy_stuff

    def set_buy_stuff(self, buy_stuff):
        self.buy_stuff = buy_stuff
        return self

    def get_game(self):
        return self.game

    """
    Metoda, pro načtení dat z json souboru"""
    def load_profile_data_from_file(self):
        pass

    """
    metoda pro změnu dat (name, character_gender, money, buy_stuff). ULOŽENÍ ZMĚNY DO JSON FILE"""
    def update_profile_data(self):
        pass

    """
    Metoda, která spustí hru, poté, co si hráč zvolí level"""
    def start_game(self):
        if self.game is None:
            self.game = Game(self.get_id(), self.get_character_gender(), "t01", self.get_money(), self.get_buy_stuff())
        self.game.start_game()
