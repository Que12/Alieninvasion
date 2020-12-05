class Settings():
    def __init__(self):
        #parametry obrazu 
        self.screen_width = 950 
        self.screen_height = 600
        self.bg_color = (230, 230, 230) # definiuje kolor tła

        self.ship_limit = 3
        ##ustawienia dotyczące pocisków
        self.bullet_width = 2
        self.bullet_height = 15
        self.bullet_color = (0, 0, 255)
        self.bullets_allowed = 3

        self.fleet_drop_speed = 10

        #łatwa zmiana szybkości gry
        self.speedup_scale = 1.1
        self.initialize_dynamic_settings()
        #łatwa zmiana puntkow przyznawanych za zestrzelenie obcego
        self.score_scale = 1.5


    def initialize_dynamic_settings(self):
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 3
        self.alien_speed_factor = 1
        
        self.fleet_direction = 1
        #punktacja 
        self.alien_points = 50
    def increase_speed(self):
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)
        