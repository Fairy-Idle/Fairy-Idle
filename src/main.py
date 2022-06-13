import pygame
from chapter import Chapter
from entity import Entity
from text import Text


class App:
    def __init__(self) -> None:
        pygame.init()

        # region Variables
        pygame.display.set_caption("Fairy Idle")
        self.screen: pygame.Surface = pygame.display.set_mode((1280, 720))
        self.clock: pygame.time.Clock = pygame.time.Clock()

        self.character_pos = (40, 200)
        self.dialogue_pos = (40, 640)
        self.chapter: Chapter

        self.dialogue_index = -1
        self.rendered_characters: dict = dict()
        self.rendered_dialogue: list = list()
        self.current_dialogue: Text
        self.current_character: Entity

        self.fonts: dict = dict()
        self.fonts[("Times New Roman", 28)] = pygame.font.SysFont("Times New Roman", 28)
        self.load_chapter("00 - Tutorial")
        # endregion

        while True:
            for event in pygame.event.get():
                match event.type:
                    case pygame.QUIT:
                        App.quit()
                    case pygame.KEYDOWN:
                        self.keydown_callback(event)
                    case pygame.KEYUP:
                        self.keyup_callback(event)
                    case pygame.MOUSEBUTTONDOWN:
                        self.mousebuttondown_callback(event)

            self.draw()

            pygame.display.flip()
            self.clock.tick(60)

    def draw(self) -> None:
        self.screen.fill((0, 0, 0))
        self.current_character.draw(self.screen)
        self.current_dialogue.draw(self.screen)

    def load_chapter(self, chapter_name) -> None:
        self.chapter = Chapter(chapter_name)
        for character in self.chapter.characters:
            if character not in self.rendered_characters:
                self.rendered_characters[character] = Entity(self.character_pos, self.chapter.characters[character]["Appearance"])
        for line in self.chapter.dialogue:
            rendered_line = Text(self.dialogue_pos, self.fonts[("Times New Roman", 28)], line, (255, 255, 0))
            self.rendered_dialogue.append(rendered_line)
        self.update_dialogue()

    def update_dialogue(self) -> None:
        self.dialogue_index += 1
        self.dialogue_index %= len(self.rendered_dialogue)
        self.current_dialogue = self.rendered_dialogue[self.dialogue_index]
        self.current_dialogue.visible = True
        self.current_character = self.rendered_characters[self.current_dialogue.text.split(": ")[0]]

    def keydown_callback(self, event) -> None:
        match event.key:
            case pygame.K_ESCAPE:
                App.quit()
            case pygame.K_e:
                self.current_dialogue.visible = False

    def keyup_callback(self, event) -> None:
        match event.key:
            case pygame.K_e:
                self.current_dialogue.visible = True

    def mousebuttondown_callback(self, event) -> None:
        self.update_dialogue()

    @staticmethod
    def quit() -> None:
        pygame.quit()
        quit()


if __name__ == "__main__":
    App()
