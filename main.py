import sys
from pathlib import Path

import pygame
from asteroid import Asteroid
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from logger import log_state, log_event
from player import Player, PLAYER_RADIUS
from asteroidfield import AsteroidField
from shot import Shot


def main():
    # Show basic startup info so the game session is easier to diagnose.
    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")

    # Initialize pygame and create the main window and timing object.
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    # Create sprite groups first, then assign each class's containers so new
    # instances are automatically added to the correct groups.
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable)
    asteroid_field = AsteroidField()
    Shot.containers = (shots, updatable, drawable)
    

    # Create the player in the center of the screen; pygame will auto-add it.
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, PLAYER_RADIUS)

    # 1. Load the texture and use .convert() to optimize rendering speed
    image_path = Path(__file__).resolve().parent / "images" / "sky.jpeg"
    bg_texture = pygame.image.load(str(image_path)).convert()

    # Create a font object for rendering text on the screen
    font = pygame.font.Font(None, 36)

# 2. Scale the texture to the exact size of your screen
    bg_texture = pygame.transform.scale(bg_texture, (SCREEN_WIDTH, SCREEN_HEIGHT))

    # Initialize a counter for the number of asteroids destroyed
    asteroids_destroyed = 0

    while True:
        # Limit the loop to 60 FPS and convert the elapsed time to seconds.
        dt: float = clock.tick(60) / 1000.0

        # Log the game state each frame for debugging and tracking.
        log_state()

        # Handle window events like closing the game.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        # Update every sprite that implements an update(dt) method.
        updatable.update(dt)

        # Check for collisions between the player and any asteroid.
        for asteroid in asteroids:
            if player.collides_with(asteroid):
                log_event("player_hit")
                print("Game over!")
                sys.exit()

        # Check for collisions between shots and asteroids.
        for asteroid in asteroids:
            for shot in shots:
                if asteroid.collides_with(shot):
                    log_event("asteroid_shot")
                    asteroids_destroyed += 1
                    asteroid.split()
                    shot.kill()

        # Draw the background and all visible sprites each frame.
        screen.blit(bg_texture, (0, 0))
        for sprite in drawable:
            # These sprites implement draw(screen) instead of using an image/rect.
            sprite.draw(screen)

        # Render the score after the background so it remains visible.
        score_text = font.render(
            f"Asteroids Destroyed: {asteroids_destroyed}",
            True,
            "white",
        )
        screen.blit(score_text, (20, 20))

        pygame.display.flip()


if __name__ == "__main__":
    main()
