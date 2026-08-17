import sys
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
    Shot.containers = (shots, updatable, drawable)
    asteroid_field = AsteroidField()

    shots = pygame.sprite.Group()
    

    # Create the player in the center of the screen; pygame will auto-add it.
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, PLAYER_RADIUS)

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

        # Draw the background and all visible sprites each frame.
        screen.fill((6, 30, 41))
        for sprite in drawable:
            # These sprites implement draw(screen) instead of using an image/rect.
            sprite.draw(screen)

        pygame.display.flip()


if __name__ == "__main__":
    main()
