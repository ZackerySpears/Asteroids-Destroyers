import random
from pathlib import Path

import pygame
from circleshape import CircleShape
from constants import *
from logger import log_event

class Asteroid(CircleShape):
    def __init__(self, x: float, y: float, radius: float) ->None:
        super().__init__(x, y, radius)
        image_path = Path(__file__).resolve().parent / "images" / "asteroid_image.png"
        self.texture = pygame.image.load(str(image_path)).convert_alpha()
        
    def draw(self, screen: pygame.Surface) -> None:
        size = int(self.radius * 2)
        scaled_texture = pygame.transform.scale(self.texture, (size, size))
        position = scaled_texture.get_rect(center=self.position)
        screen.blit(scaled_texture, position)

    def update(self, dt:float) -> None:
        self.position += self.velocity * dt

    def split(self) -> None:
        self.kill()
        if self.radius <= ASTEROID_MIN_RADIUS:
            return

        log_event("asteroid_split")
        angle = random.uniform(20, 50)
        first_velocity = self.velocity.rotate(angle)
        second_velocity = self.velocity.rotate(-angle)
        new_radius = self.radius - ASTEROID_MIN_RADIUS

        first_asteroid = Asteroid(self.position.x, self.position.y, new_radius)
        second_asteroid = Asteroid(self.position.x, self.position.y, new_radius)
        first_asteroid.velocity = first_velocity * 1.2
        second_asteroid.velocity = second_velocity * 1.2



    