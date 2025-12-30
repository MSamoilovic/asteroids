import random

import pygame.draw

from asteroids.graphics.circleshape import CircleShape
from asteroids.utils.constants import LINE_WIDTH, ASTEROID_MIN_RADIUS, SCORE_LARGE_ASTEROID, SCORE_MEDIUM_ASTEROID, SCORE_SMALL_ASTEROID
from asteroids.utils.logger import log_event


class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)

    def draw(self, screen):
        pygame.draw.circle(screen, "white", self.position, self.radius, LINE_WIDTH)

    def update(self, dt):
        self.position += self.velocity * dt

    def split(self, game_state=None):
        self.kill()

        if game_state:
            if self.radius >= ASTEROID_MIN_RADIUS * 3:
                game_state.add_score(SCORE_LARGE_ASTEROID)
            elif self.radius >= ASTEROID_MIN_RADIUS * 2:
                game_state.add_score(SCORE_MEDIUM_ASTEROID)
            else:
                game_state.add_score(SCORE_SMALL_ASTEROID)

        if self.radius < ASTEROID_MIN_RADIUS:
            return
        else:
            log_event("asteroid_split")
            angle = random.uniform(20, 50)
            velocity1 = self.velocity.rotate(angle)
            velocity2 = self.velocity.rotate(-angle)
            new_radius = self.radius - ASTEROID_MIN_RADIUS
            asteroid1 = Asteroid(self.position.x, self.position.y, new_radius)
            asteroid2 = Asteroid(self.position.x, self.position.y, new_radius)
            asteroid1.velocity = velocity1 * 1.2
            asteroid2.velocity = velocity2 * 1.2
