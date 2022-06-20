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
            self.focus = pygame.transform.scale(self.image, (int(width * 1.1), int(height * 1.1)))
        else:
            self.image = None
            self.focus = None
        self.visible: bool = True
        self.focused: bool = False

    def draw(self, screen: Surface) -> None:
        if not self.visible:
            return
        if self.focused:
            screen.blit(self.focus, (self.pos[0] - self.width * 0.05, self.pos[1] - self.height * 0.05))
        elif self.image is not None:
            screen.blit(self.image, self.pos)
