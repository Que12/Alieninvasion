import sys # skorzystamy gdy wystąpi konieczność zakończenia gry na żądanie gracza
from time import sleep
import pygame

from bullet import Bullet
from alien import Alien 



def check_keydown_events(event,ai_settings, screen, ship, bullets):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE: # wystrzelenie pocisku po naciśnieciu spacji 
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
         sys.exit()

def fire_bullet(ai_settings, screen, ship, bullets):
    ## wystrzeliwanie pocisku jesli nie przekroczono limistu
        #utworzenie nowego pocisku i dodanie go do grupy pocisków
    if len(bullets) <= ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)

def check_keyup_events(event,ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False

def check_events(ai_settings,screen,stats, score, play_button, ship,aliens,  bullets):
    ## reakcja na zdarzenia generowane przez klawiature i mysz 
    for event in pygame.event.get(): # Pętla zdarzeń 
        if event.type == pygame.quit:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x,mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats,score,play_button,ship, aliens, bullets, mouse_x, mouse_y)
        elif event.type == pygame.KEYDOWN: # sprawdza czy został naciśnięty przycisk 
            check_keydown_events(event, ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP: # sprawdza czy został zwolniony przycisk
            check_keyup_events(event, ship)

def check_play_button(ai_settings, screen, stats,score, play_button,ship, aliens,bullets,  mouse_x, mouse_y):
    ##rozpoczecie nowej gry po kliknieciu przycisk Gra przez użytkowniak
    button_clicked = play_button.rect.collidepoint(mouse_x,mouse_y)
    if button_clicked and not stats.game_active:
        ai_settings.initialize_dynamic_settings()
        pygame.mouse.set_visible(False)
        stats.reset_stats()
        stats.game_active = True
        # Wyzerowanie obrazów tablicy wyników.
        score.prep_score()
        score.prep_high_score()
        score.prep_level()
        score.prep_ships()
    #usuniecie zawartości list aliens i bullets
        aliens.empty()
        bullets.empty()
        
        #utworzenie nowej floty i wysrodkowanie statku
        create_fleet(ai_settings,screen,ship,aliens)
        ship.center_ship()

def update_screen(ai_settings, screen, stats,score,  ship,aliens,  bullets, play_button):
    # odświeżanie ekranu w każdej iteracji petli
    screen.fill(ai_settings.bg_color)
    # Ponowne wyświetlenie wszystkich pociksów pod warstwami statku kosmicznego i obcych
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    score.show_score()
    ship.blitme() # wyświetlanie statku na ekranie 
    aliens.draw(screen)
    if not stats.game_active:
        play_button.draw_buttom()
    # wyswietlanie osatnio zmodyfikowanego ekranu 
    pygame.display.flip()
 
def update_bullets(ai_settings,screen,stats, score, ship, aliens,bullets):
     ## uaktualnienie położenia pocisków 
    bullets.update()  
    # usuniecie pociskow ktore sa poza ekranem 
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    check_bullet_alien_collision(ai_settings, screen, stats, score, ship, aliens, bullets)

def check_bullet_alien_collision(ai_settings, screen,stats,  score,  ship, aliens, bullets):
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True )
    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points
            score.prep_score()
        check_high_score(stats, score)
    if len(aliens) == 0:
        bullets.empty()
        ai_settings.increase_speed()
        # Inkrementacja numeru poziomu.
        stats.level += 1
        score.prep_level()
        create_fleet(ai_settings, screen, ship, aliens)
   

def get_number_aliens_x(ai_settings, alien_width):
    # ustalenie liczby obcych którzy zmieszą się w rzędzie
    avaliable_space_x = ai_settings.screen_width - 2* alien_width
    number_aliens_x = int(avaliable_space_x/(2*alien_width))
    return number_aliens_x

def get_nuber_rows(ai_settings, ship_height, alien_height):
    ##ustalenie ile rzędów obcych zmieści się na ekranie
    avaliable_space_y = (ai_settings.screen_height - (3*alien_height) - ship_height)
    number_rows = int((avaliable_space_y)/(2*alien_height))
    return number_rows

def create_alien(ai_settings, screen,aliens,alien_number, row_number):
    alien = Alien(ai_settings,screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2*alien_width*alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2*alien.rect.height * row_number
    aliens.add(alien)

def create_fleet(ai_settings, screen,ship,  aliens):
    ## utworzenie pełnej floty obcych
    #utworzenie obcego  ustalenie liczby obcych którzy zmieszą się w rzędzie
    # Odległość między obcymi jest róna szerokości obcego
    alien = Alien(ai_settings,screen)
    number_aliens_x = get_number_aliens_x(ai_settings,alien.rect.width)
    number_rows = get_nuber_rows(ai_settings,ship.rect.height,alien.rect.height)

    #utworzenie pierwszego rzędu obcyh
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings,screen,aliens,alien_number, row_number)

def check_fleed_edges(ai_settings, aliens):
    ##odpowiednie reakcje gdy obcy dotrze do krawędzie ekranu
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings,aliens)
            break

def change_fleet_direction(ai_settings, aliens):
    ##przesuniecie calej floty w dół i kierunku w ktorym się porusza
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed 
    ai_settings.fleet_direction *= -1

def ship_hit(ai_settings, stats, screen,ship,score, aliens,bullets):
    #Reakcja na uderzenie obcego w statek
    if stats.ship_left > 0:
        stats.ship_left -= 1
        score.prep_ships()
        #usuniecie zawartości aliens i bullets 
        aliens.empty()
        bullets.empty()
        #utworzenie nowej floty i wysrodkowanie statku
        create_fleet(ai_settings,screen,ship,aliens)
        ship.center_ship()

        #Pauza
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)
def check_aliens_bottom(ai_settings,stats,screen,ship,score, aliens,bullets):
    ## sprawdzenie czy którykolwiek obcy dotarł do dolnej krawedzi ekranu
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(ai_settings, stats,screen,ship,score, aliens,bullets)
            break
        

def update_aliens(ai_settings, stats, screen, ship,score,  aliens, bullets):
    ##sprawdzenie czy flota znajduje się przy krawędzie ekranu 
    # a następnie uaktualnienie polozenia wszystkich obcych w flocie 
    check_fleed_edges(ai_settings, aliens)
    aliens.update()
   
    #wykrywanie kolizji miedzy obcym i statkiem
    if pygame.sprite.spritecollideany(ship,aliens):
        ship_hit(ai_settings,stats,screen,ship,score, aliens, bullets)
    ## wyszukiwanie obych docierajacych do dolnej krawedzi ekranu
    check_aliens_bottom(ai_settings,stats,screen,ship,score,aliens,bullets)

def check_high_score(stats, score):
    #sprawdzamy czy mamy nowy najleoszy wynik osiagniey dotad w grze 
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        score.prep_high_score()

