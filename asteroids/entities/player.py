import pygame
from pygame import Color

from asteroids.graphics.circleshape import CircleShape
from asteroids.entities.shot import Shot
from asteroids.utils.constants import (
    PLAYER_RADIUS,
    LINE_WIDTH,
    PLAYER_TURN_SPEED,
    PLAYER_SPEED,
    SHOT_RADIUS,
    PLAYER_SHOT_SPEED,
    PLAYER_SHOOT_COOLDOWN_SECONDS,
    PLAYER_RESPAWN_TIME,
)


class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.cooldown = 0
        self.invincible = False
        self.invincible_timer = 0.0

    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def draw(self, screen):
        # Ako je invincible, treperi (ne crtaj svaki drugi frame)
        if self.invincible and int(self.invincible_timer * 10) % 2 == 0:
            return
        
        color = "White"
        points = self.triangle()
        pygame.draw.polygon(screen, Color(color), points, LINE_WIDTH)

    def rotate(self, dt):
        self.rotation += dt * PLAYER_TURN_SPEED

    def update(self, dt):
        keys = pygame.key.get_pressed()
        self.cooldown -= dt
        
        # Update invincibility timer
        if self.invincible:
            self.invincible_timer -= dt
            if self.invincible_timer <= 0:
                self.invincible = False

        if keys[pygame.K_a]:
            self.rotate(-dt)
        if keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_w]:
            self.move(dt)
        if keys[pygame.K_s]:
            self.move(-dt)
        if keys[pygame.K_SPACE]:
            self.shoot()
    
    def respawn(self, x, y):
        """Respawnuje igrača na novoj poziciji"""
        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.rotation = 0
        self.invincible = True
        self.invincible_timer = PLAYER_RESPAWN_TIME

    def move(self, dt):
        unit_vector = pygame.Vector2(0, 1)
        rotated_vector = unit_vector.rotate(self.rotation)
        rotated_with_speed_vector = rotated_vector * PLAYER_SPEED * dt
        self.position += rotated_with_speed_vector

    def shoot(self):
        if self.cooldown > 0:
            return
        shot = Shot(self.position.x, self.position.y, SHOT_RADIUS)
        shot.velocity = pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOT_SPEED
        self.cooldown = PLAYER_SHOOT_COOLDOWN_SECONDS

