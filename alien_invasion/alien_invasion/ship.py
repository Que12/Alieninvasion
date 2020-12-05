import pygame
from pygame.sprite import Sprite
class  Ship(Sprite):
    #inicjalizowanie statku kosmicznego i jego położenia początkowego
    def __init__(self, ai_settings,screen):  #odniesienie do egzemplarza, ustawien oraz ekranu
        super(Ship, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings
    # Wczytanie obrazu statku kosmicznego i pobranie jego prostokąta.
        self.image = pygame.image.load('images/ship.bmp') # wczytanie obrazu statku 
        self.rect = self.image.get_rect() # uzyskujemy dostęp do atrybutu rect powierzchni 
        self.screen_rect = screen.get_rect() # wymiary ekranu umieszczamy w screen_rect
        # Każdy nowy statek kosmiczny pojawia się na dole ekranu.
        self.rect.centerx = self.screen_rect.centerx # wysrodkowanie statku na ekranie
        self.rect.bottom = self.screen_rect.bottom #umieszczenie statku na dole ekranu
        # punkt środowy statku jest przechowywany w postaci liczy zmiennoprzecinkowej
        self.center = float(self.rect.centerx)
        ## opcje wskazujące na poruszanie się staktu 
        self.moving_right = False
        self.moving_left = False

    def update(self):
        # uaktualnienie wartości punktu środkowego statku a nie jego prostokąta
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.ai_settings.ship_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.center -= self.ai_settings.ship_speed_factor
        ## udaktualnienie obiektu rect na podstawie wartości self.factor
        self.rect.centerx = self.center       
    def blitme(self):
        """Wyświetlenie statku kosmicznego w jego aktualnym położeniu."""
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        ##umieszczanie statu na srodku przu dolnej krawdzi ekranu
        self.center = self.screen_rect.centerx
## Jednym z powodów dużej efektywności Pygame jest możliwość traktowania elementu jako prostokąta (rect),

