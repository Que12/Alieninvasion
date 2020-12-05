
import pygame
from pygame.sprite import Group
from settings import Settings
from ship import Ship
import game_functions as gf
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard

def run_game():
    # Inicjalizacja gry i utworzenie obiektu ekranu.
    pygame.init() # inicjalizuje ustawienia tła 
    ai_settings = Settings() # utworzenie obiektu ustawień
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height)) # podane w pikselach
    pygame.display.set_caption("Inwazja obcych") # nazwa okna gry
    #utworzenie przycisku gra
    play_button = Button(ai_settings, screen, "Gra")
    ##utworzenie egzemplarza przeznaczonego do przechowywania danych 
    #statystycznych dotyczących gry
    stats = GameStats(ai_settings)
    score = Scoreboard(ai_settings,screen,stats)
    ship = Ship(ai_settings, screen)
    bullets = Group()  #Utworzenie grupy przeznaczonej do przechowywania pocisków
    aliens = Group() # utworzenie grupy obcych
    gf.create_fleet(ai_settings,screen,ship, aliens)
    # Rozpoczęcie pętli głównej gry.
    while True: # kątroluje gre 
        # Oczekiwanie na naciśnięcie klawisza lub przycisku myszy.
        gf.check_events(ai_settings, screen,stats,score, play_button, ship,aliens,  bullets)
        if stats.game_active:
            ship.update() #by moetoda update była wykonywana w każdej iteracji petli
            gf.update_bullets(ai_settings, screen,stats, score,  ship, aliens, bullets)
            gf.update_aliens(ai_settings,stats, screen, ship,score,  aliens, bullets)
        
        gf.update_screen(ai_settings,screen,stats, score, ship,aliens, bullets, play_button)
        
run_game()
