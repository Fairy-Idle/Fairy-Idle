from entity import Entity
from pygame.font import Font
from pygame.surface import Surface


class Text(Entity):
    def __init__(self, pos: tuple, font: Font, text: str, color: tuple, image: str = None) -> None:
        super().__init__(pos, image)
        self.pos = pos
        self.font: Font = font
        self.text: str = text
        self.color: tuple = color
        self.render: Surface = self.font.render(text, True, self.color)
        self.visible: bool = True

    def draw(self, screen: Surface) -> None:
        if not self.visible:
            return
        super().draw(screen)
        screen.blit(self.render, self.pos)
