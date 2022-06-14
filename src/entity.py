from pygame import Surface
import pygame


class Entity:
    def __init__(self, pos: tuple, image: str = None, width=0, height=0) -> None:
        self.pos = pos
        self.width = width
        self.height = height
        if image is not None:
            self.image = pygame.image.load(image)
            if width > 0 and height > 0:
                self.image = pygame.transform.scale(self.image, (width, height))
        else:
            self.image = None
        self.visible: bool = True

    def draw(self, screen: Surface) -> None:
        if not self.visible:
            return
        if self.image is not None:
            screen.blit(self.image, self.pos)
