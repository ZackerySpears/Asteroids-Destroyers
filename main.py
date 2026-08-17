import pygame
from asteroid import Asteroid
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from logger import log_state
from player import Player, PLAYER_RADIUS
from asteroidfield import AsteroidField


def main():
    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")

    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    # create groups first for player, then set the class containers so sprites auto-add
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    Player.containers = (updatable, drawable)

    # create groups first for asteroids, then set the class containers so sprites auto-add
    asteroids = pygame.sprite.Group()
    Asteroid.containers = (asteroids, updatable, drawable)

    AsteroidField.containers = (updatable)
    asteroid_field = AsteroidField()

    # now create the player (it will be added to the groups in CircleShape.__init__)
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, PLAYER_RADIUS)

    while True:
        # frame timing
        dt: float = clock.tick(60) / 1000.0

        log_state()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        # update all updatable sprites
        updatable.update(dt)

        # render
        screen.fill(("red"))
        for sprite in drawable:
            # our sprites implement `draw(screen)` (not `image/rect`), so call it
            sprite.draw(screen)

        pygame.display.flip()


if __name__ == "__main__":
    main()
