from entity import Entity
from pygame.font import Font
from pygame.surface import Surface
from pygame.draw import line


class Text(Entity):  # todo is this class necessary? might be needless abstraction and can be substituted with a function or two...
    def __init__(self, pos: tuple, font: Font, text: str, color: tuple, image: str = None, width: int = 0, height: int = 0, border: bool = True, justify: str = "left") -> None:
        super().__init__(pos, image, width, height)
        self.pos: tuple = pos
        self.font: Font = font
        self.text: str = text
        self.color: tuple = color
        self.border: bool = border
        self.justify: str = justify
        self.render: Surface = self.font.render(text, True, color)
        self.visible: bool = True

    def render_text(self, text):
        self.render = self.font.render(text, True, self.color)

    def draw(self, screen: Surface) -> None:
        if not self.visible:
            return
        super().draw(screen)
        pos = list(self.pos)  # todo resource intensive?
        width = self.width if self.width > 0 else self.render.get_width() + 10
        height = self.height if self.height > 0 else self.render.get_height() * 1.25
        if self.border:
            x_pos = (self.pos[0], self.pos[0] + width)
            y_pos = (self.pos[1], self.pos[1] + height)
            vertices = ((x_pos[0], y_pos[0]), (x_pos[0], y_pos[1]), (x_pos[1], y_pos[1]), (x_pos[1], y_pos[0]))
            for i in range(-1, len(vertices) - 1):
                line(screen, self.color, vertices[i], vertices[i + 1])
        if self.justify == "left":
            pos[0] += 5
            pos[1] += 5
        elif self.justify == "center":
            pos[0] += (width - self.render.get_width()) / 2
            pos[1] += 5
        screen.blit(self.render, pos)
