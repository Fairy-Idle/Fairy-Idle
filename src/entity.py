from pygame import Surface
import pygame


class Entity:
    def __init__(self, pos: tuple, image: str = None, width: int = 0, height: int = 0, transition: tuple = None, timer: float = 0.0) -> None:
        self.pos = pos
        self.width = width
        self.height = height
        if image is not None:
            self.image = pygame.image.load(image)
            if width > 0 and height > 0:
                self.focus = pygame.transform.scale(self.image, (int(width * 1.1), int(height * 1.1)))
                self.image = pygame.transform.scale(self.image, (width, height))
            self.image = self.image.convert_alpha()
            self.focus = self.focus.convert_alpha()
        else:
            self.image = Surface((width, height))
            self.focus = None
        self.visible: bool = True
        self.focused: bool = False
        self.transitioning: bool = False
        self.transition: tuple = transition
        self.timer: float = timer
        self.orig_timer: float = timer
        self.frames: int = 0

    def draw(self, screen: Surface) -> None:
        if not self.visible:
            return
        if self.focused:
            screen.blit(self.focus, (self.pos[0] - self.width * 0.05, self.pos[1] - self.height * 0.05))
        elif self.image is not None:
            screen.blit(self.image, self.pos)
