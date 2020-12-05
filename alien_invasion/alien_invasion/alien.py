import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    # klasa przedstawiająca pojedynczego obcego w flocie
    def __init__(self, ai_settings, screen):
        ## inicjalizacja obcego i zdefiniowanie jego położenia
        super(Alien, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

    ## wczyywanie obcego i zdefiniowanie jego atrybutu rect
        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()

    ## umieszczenie nowego obcego w pobliżu lewego górnego rogu ekranu
        self.rect.x = self.rect.width ## pozostawia miejsce wokół obcego równe jego szerokości
        self.rect.y = self.rect.height

    ## przechowywanie dokladnego położenia obcego
        self.x = float(self.rect.x)

    def blitme(self):
        ## wyswietlanie obcego w jego aktualnym położeniu
        self.screen.blit(self.image,self.rect)
     
    def check_edges(self):
        ## zwraca wartośc true jeśli obcy znajduje się przy krawędzi ekranu 
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True

    def update(self):
        ## przesuniecie obcego w prawo lub w lewo
        self.x += (self.ai_settings.alien_speed_factor * self.ai_settings.fleet_direction)
        self.rect.x = self.x