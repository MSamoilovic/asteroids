import pygame
import sys

from asteroids.entities import Asteroid, Player, Shot
from asteroids.game import AsteroidField, GameState
from asteroids.utils.constants import SCREEN_WIDTH, SCREEN_HEIGHT
from asteroids.utils.logger import log_state, log_event


def main():
    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    dt = 0

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    game_state = GameState()

    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    Shot.containers = (shots, updatable, drawable)

    AsteroidField.containers = updatable

    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    asteroid_field = AsteroidField()

    

    while True:
        log_state()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        updatable.update(dt)

        # Collision detection sa player-om (samo ako nije invincible)
        if not player.invincible:
            for asteroid in asteroids:
                if asteroid.collides_with(player):
                    log_event("player_hit")
                    game_state.lives -= 1
                    
                    if game_state.lives <= 0:
                        game_state.game_over = True
                        print("Game Over! Final Score:", game_state.score)
                        sys.exit()
                    else:
                        player.respawn(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

        # Collision detection između shot-ova i asteroida
        for asteroid in asteroids:
            for shot in shots:
                if asteroid.collides_with(shot):
                    log_event("asteroid_shot")
                    asteroid.split(game_state)
                    shot.kill()

        # Render deo
        screen.fill("black")
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {game_state.score}", True, "white")
        screen.blit(score_text, (10, 10))
        
        lives_text = font.render(f"Lives: {game_state.lives}", True, "white")
        screen.blit(lives_text, (10, 50))

        for thing in drawable:
            thing.draw(screen)

        pygame.display.flip()
        dt = clock.tick(60) / 1000

if __name__ == "__main__":
    main()
