import pygame
import sys

from model import *
from Profile import Profile

"""
Tato třída obsahuje pole profilů, které jsou vytvořeny, načte je z disku,
umožňuje vytvořit nebo smazat profil. O úpravu (např. změna jména,
nebo postavy se stará třída Profile)"""
class Profiles():
    def __init__(self):
        self.list_of_profiles = [Profile("default", "default", "WAITER")]   # Pole profilů, které se načtou z disku
        self.actual_profile = Profile("default", "default", "WAITER")       # Aktuálně vybraný profil, který hráč zvolí a pro který bude spuštěná hra

    """
    Gettery/Settery"""

    def get_list_of_profiles(self):
        return self.list_of_profiles

    def set_list_of_profiles(self, list_of_profiles):
        self.list_of_profiles = list_of_profiles
        return self

    def get_actual_profile(self):
        return self.actual_profile

    def set_actual_profile(self, actual_profile):
        self.actual_profile = actual_profile
        return self

    """
    Načte profily z disku (název json souboru ve složce profiles = profile_id)"""
    def load_profiles(self):
        actual_profile = Profile("default", "default", "WAITER")
        self.set_list_of_profiles([actual_profile])
        self.set_actual_profile(actual_profile)

    """
    """
    def create_profile(self, new_profile):
        pass

    """
    """
    def delete_profile(self, profile_id):
        pass

