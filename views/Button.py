import pygame
from model import *

class Button():
    def __init__(self, image, x_pos, y_pos, text_input):
        super().__init__()
        self.image = image
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.rect = self.image.get_rect(center = (self.x_pos, self.y_pos))
        self.text_input = text_input
        self.text = header_font2.render(self.text_input, True, BLACK)
        self.text_rect = self.text.get_rect(center = (self.x_pos, self.y_pos - BUTTON_HEIGHT * 0.1))
        self.mask = pygame.mask.from_surface(self.image)
        
    def get_image(self):
        return self.image
    
    def set_image(self, image):
        self.image = image
        return self
    
    def get_x_pos(self):
        return self.x_pos
    
    def get_y_pos(self):
        return self.y_pos
    
    def get_rect(self):
        return self.rect
    
    def set_rect(self, rect):
        self.rect = rect
        return self
    
    def get_text(self):
        return self.text
    
    def get_text_rect(self):
        return self.text_rect
    
    def set_text_rect(self, text_rect):
        self.text_rect = text_rect
        return self
    
    def get_mask(self):
        return self.mask
    
#Vykreslení tlačítka        
    def draw_button(self):
        SCREEN.blit(self.get_image(), self.get_rect())
        if self.get_text() != None:
            SCREEN.blit(self.get_text(), self.get_text_rect())

#Zkontruluje, zda uživatel klikl na tlačítko
    def isButtonClicked(self, position):
        if position[0] in range(self.get_rect().left, self.get_rect().right) and position[1] in range(self.get_rect().top, self.get_rect().bottom):
            return True
        else:
            return False
        
    def button_hover(self, position, image):
        pos_in_mask = position[0] - self.get_rect().x, position[1] - self.get_rect().y
        touching = self.get_rect().collidepoint(*position) and self.get_mask().get_at(pos_in_mask)
        
        if touching:
            self.set_image(image)
            self.draw_button()
        else:
            self.set_image(YELLOW_BUTTON)
            self.draw_button()