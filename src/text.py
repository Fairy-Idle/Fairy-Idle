from entity import Entity
from pygame.font import Font
from pygame.surface import Surface
from pygame.draw import line


class Text(Entity):
    def __init__(self, pos: tuple, font: Font, text: str, color: tuple, image: str = None, width: int = 0, height: int = 0) -> None:
        super().__init__(pos, image, width, height)
        self.pos = pos
        self.font: Font = font
        self.text: str = text
        self.color: tuple = color
        self.render: Surface = self.font.render(text, True, color)
        self.visible: bool = True

    def render_text(self, text):
        self.render = self.font.render(text, True, self.color)

    def draw(self, screen: Surface) -> None:
        if not self.visible:
            return
        super().draw(screen)
        if self.width > 0 and self.height > 0:
            x_pos = (self.pos[0] - 10, self.pos[0] + self.width + 10)
            y_pos = (self.pos[1] - 10, self.pos[1] + self.height + 10)
            vertices = ((x_pos[0], y_pos[0]), (x_pos[0], y_pos[1]), (x_pos[1], y_pos[1]), (x_pos[1], y_pos[0]))
            for i in range(-1, len(vertices) - 1):
                line(screen, self.color, vertices[i], vertices[i + 1])
        screen.blit(self.render, self.pos)
