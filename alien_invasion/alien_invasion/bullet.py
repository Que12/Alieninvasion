import pygame 
from pygame.sprite import Sprite
import math
class Bullet(Sprite):
    ## klasa przeznaczona do zarządzania pociskami wystrzeliwanymi przez statek

    def __init__(self, ai_settings, screen, ship):
        ## utworzenie obiektu pocisku w aktualnym położeniu statku
        super(Bullet, self).__init__() # super konieczne do poprawnego uzycia sprite
        self.screen = screen
        ## utworzenie prostokąta pocisku w punkcie (0,0) 
        ## a następnie zdefiniowanie dla niego odpowiedniego położenia 
        self.rect = pygame.Rect(0, 0, ai_settings.bullet_width,ai_settings.bullet_height) #tworzymy atrybut rect pocisku 
        self.rect.centerx = ship.rect.centerx ## przypisujemy położenie rect pocisku takie jak polozenie statku
        self.rect.top = ship.rect.top
        #Położenie pocisku zdefiniowane za pomocą wartości zmiennoprzecinkowej
        self.y = float(self.rect.y)

        self.color = ai_settings.bullet_color
        self.speed_factor = ai_settings.bullet_speed_factor # kontrola nad predkoscia statku 
    
    def update(self): ## zarządza położeniem pocisku
        #Poruszanie pociskiem na ekranie
    # uaktualnienie położenia pocisku
        self.y -= self.speed_factor
    # uaktualnienie położenia prostokąta pocisku
        self.rect.y = self.y

    def draw_bullet(self):
        ## wyswietlanie pocisku na ekranie
        pygame.draw.rect(self.screen, self.color,self.rect)
    
   