
class GameStats():
## Monitorowanie danych satystycznych w grze "alien invasion"
    def __init__(self, ai_settings):
        ##inicjalizacja danych statystycznych
        self.ai_settings = ai_settings
        self.reset_stats()
        self.game_active = False
        ##najlepszy wynik nigdy nie powinien zostac wyzerowany
        self.high_score = 0
    def reset_stats(self):
        ##inicjalizacja danych statystycznych które mogą zmienia się w trakcie gry
        self.ship_left = self.ai_settings.ship_limit
        self.score = 0
        self.level = 1