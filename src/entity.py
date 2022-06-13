from pygame import Surface
import pygame


class Entity:
    def __init__(self, pos: tuple, image: str = None) -> None:
        self.pos = pos
        if image is not None:
            image = pygame.image.load(image)
            self.image = pygame.transform.scale(image, (512, 512))
        else:
            self.image = None
        self.visible: bool = True

    def draw(self, screen: Surface) -> None:
        if not self.visible:
            return
        if self.image is not None:
            screen.blit(self.image, self.pos)
