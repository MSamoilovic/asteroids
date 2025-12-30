class GameState:
    def __init__(self):
        self.score = 0
        self.lives = 3
        self.game_over = False
    
    def add_score(self, points):
        self.score += points
    
    def reset(self):
        self.score = 0
        self.lives = 3
        self.game_over = False