import pygame
from constants import PLAYER_RADIUS, PLAYER_SHOOT_COOLDOWN, PLAYER_SHOT_SPEED, SCREEN_WIDTH, SCREEN_HEIGHT, PLAYER_TURN_SPEED, PLAYER_SPEED, PLAYER_SHOOT_COOLDOWN, LINE_WIDTH
from circleshape import CircleShape
from shot import Shot
from pathlib import Path


class Player(CircleShape):
    def __init__(self, x: float, y: float, radius: float = PLAYER_RADIUS) -> None:
        super().__init__(x, y, radius)
        self.rotation = 0
        self.cooldown = 0
        image_path = Path(__file__).resolve().parent / "images" / "rocket_ship.png"
        self.texture = pygame.image.load(str(image_path)).convert_alpha()

    def triangle(self) -> list[pygame.Vector2]:
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def draw(self, screen: pygame.Surface) -> None:
        size = int(self.radius * 2)
        texture = pygame.transform.smoothscale(
            self.texture,
            (size, size * 2),
        )
        rotated_texture = pygame.transform.rotate(texture, 180 - self.rotation)
        position = rotated_texture.get_rect(center=self.position)
        screen.blit(rotated_texture, position)

    def rotate(self, dt: float) -> None:
        self.rotation += PLAYER_TURN_SPEED * dt

    def update(self, dt: float) -> None:
        # Read the keyboard state once per frame so movement and shooting
        # respond to the player's current input without checking the OS again.
        keys = pygame.key.get_pressed()

        # Rotate left or right based on A/D input.
        if keys[pygame.K_a]:
            self.rotate(-dt)

        if keys[pygame.K_d]:
            self.rotate(+dt)

        # Move forward or backward relative to the ship's current facing.
        if keys[pygame.K_w]:
            self.move(dt)

        if keys[pygame.K_s]:
            self.move(-dt)

        # Fire a shot when space is held down.
        if keys[pygame.K_SPACE]:
            if self.cooldown <= 0:
                self.cooldown = PLAYER_SHOOT_COOLDOWN
                self.shoot(dt)
            else:
                self.cooldown -= dt

    def move(self, dt: float) -> None:
        # The ship's forward direction is a vector pointing down the screen,
        # then rotated to match the ship's current angle.
        unit_vector = pygame.Vector2(0, 1)
        rotated_vector = unit_vector.rotate(self.rotation)
        rotated_with_speed_vector = rotated_vector * PLAYER_SPEED * dt
        self.position += rotated_with_speed_vector

    def shoot(self, dt: float) -> None:
        # Spawn a projectile just in front of the ship and send it forward
        # at a constant speed.
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        shot_velocity = forward * PLAYER_SHOT_SPEED
        shot = Shot(
            self.position.x + forward.x * self.radius,
            self.position.y + forward.y * self.radius,
        )
        shot.velocity = shot_velocity
    