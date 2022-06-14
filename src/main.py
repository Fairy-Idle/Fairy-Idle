import pygame
from chapter import Chapter
from entity import Entity
from text import Text
from player import Player


class App:
    def __init__(self) -> None:
        pygame.init()

        # region Variables
        pygame.display.set_caption("Fairy Idle")
        self.screen: pygame.Surface = pygame.display.set_mode((1280, 720))
        self.clock: pygame.time.Clock = pygame.time.Clock()

        self.fonts: dict = dict()
        self.fonts[("Times New Roman", 28)] = pygame.font.SysFont("Times New Roman", 28)

        self.chapter: Chapter
        self.event_index: int = 0
        self.dialogue_pos: tuple = (40, 640)
        self.chapter_events: list = list()
        self.rendered_characters: dict = dict()
        self.rendered_dialogue: list = list()
        self.current_dialogue: Text

        self.player = Player("Sacred")
        # endregion

        self.load_chapter("00 - Tutorial")

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
        for character in self.rendered_characters.values():
            character.draw(self.screen)
        self.current_dialogue.draw(self.screen)

    def load_chapter(self, chapter_name) -> None:
        self.chapter = Chapter(chapter_name)
        self.render_characters()
        self.render_dialogue()
        self.progress_chapter()

    def render_characters(self):
        self.rendered_characters.clear()
        for character in self.chapter.characters:
            if character not in self.rendered_characters:
                character_appearance = self.chapter.characters[character]["Appearance"]
                self.rendered_characters[character] = Entity((0, 0), character_appearance, width=512, height=512)
                self.rendered_characters[character].visible = False

    def render_dialogue(self):
        self.chapter_events.clear()
        self.rendered_dialogue.clear()
        for line in self.chapter.dialogue:
            words = line.split()
            match words[0]:
                case "Enter":
                    character, x, y = words[1], words[2][1:-1], words[3][:-1]
                    self.rendered_dialogue.append(len(self.chapter_events))
                    self.chapter_events.append((self.enter_event, character, x, y))
                case "Replace":
                    old_character, new_character = words[1], words[3]
                    self.rendered_dialogue.append(len(self.chapter_events))
                    self.rendered_characters[new_character].pos = self.rendered_characters[words[1]].pos
                    self.rendered_characters[new_character].visible = False
                    self.chapter_events.append((self.replace_event, old_character, new_character))
                case "Exit":
                    character = words[1]
                    self.rendered_dialogue.append(len(self.chapter_events))
                    self.chapter_events.append((self.exit_event, character))
                case _:
                    dialogue_font = self.fonts[("Times New Roman", 28)]
                    rendered_line = Text(self.dialogue_pos, dialogue_font, line, (255, 255, 0), width=1200, height=40)
                    self.rendered_dialogue.append(rendered_line)

    def progress_chapter(self) -> None:
        while isinstance(self.rendered_dialogue[self.event_index], int):
            command, *args = self.chapter_events[self.rendered_dialogue[self.event_index]]
            command(*args)
            self.event_index += 1
            self.event_index %= len(self.rendered_dialogue)
        self.current_dialogue = self.rendered_dialogue[self.event_index]
        self.format_dialogue()
        self.current_dialogue.visible = True
        self.event_index += 1
        self.event_index %= len(self.rendered_dialogue)

    def format_dialogue(self):
        if "{" in self.current_dialogue.text:
            text = self.current_dialogue.text
            start = text.find("{")
            end = text.find("}")
            text = f"{text[:start]}{eval(text[start + 1:end])}{text[end + 1:]}"
            self.current_dialogue.render_text(text)

    # region Dialogue Event Methods
    def enter_event(self, character, x, y):
        self.rendered_characters[character].pos = (int(x), int(y))
        self.rendered_characters[character].visible = True

    def replace_event(self, old_character, new_character):
        self.rendered_characters[new_character].pos = self.rendered_characters[old_character].pos
        self.rendered_characters[new_character].visible = True
        self.rendered_characters[old_character].visible = False

    def exit_event(self, character):
        self.rendered_characters[character].visible = False
    # endregion

    # region Callback Methods
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
        self.progress_chapter()
    # endregion

    @staticmethod
    def quit() -> None:
        pygame.quit()
        quit()


if __name__ == "__main__":
    App()
